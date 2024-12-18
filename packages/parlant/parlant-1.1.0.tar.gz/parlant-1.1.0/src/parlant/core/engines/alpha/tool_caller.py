# Copyright 2024 Emcie Co Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
from dataclasses import dataclass, asdict
from itertools import chain
import json
import traceback
from typing import Any, Mapping, NewType, Optional, Sequence

from parlant.core.customers import Customer
from parlant.core.tools import Tool, ToolContext
from parlant.core.agents import Agent
from parlant.core.common import JSONSerializable, generate_id, DefaultBaseModel
from parlant.core.context_variables import ContextVariable, ContextVariableValue
from parlant.core.nlp.generation import GenerationInfo, SchematicGenerator
from parlant.core.services.tools.service_registry import ServiceRegistry
from parlant.core.sessions import Event, ToolResult
from parlant.core.glossary import Term
from parlant.core.engines.alpha.guideline_proposition import GuidelineProposition
from parlant.core.engines.alpha.prompt_builder import PromptBuilder, BuiltInSection
from parlant.core.engines.alpha.utils import emitted_tool_events_to_dicts
from parlant.core.emissions import EmittedEvent
from parlant.core.logging import Logger
from parlant.core.tools import ToolId, ToolService

ToolCallId = NewType("ToolCallId", str)
ToolResultId = NewType("ToolResultId", str)


class ToolCallEvaluation(DefaultBaseModel):
    name: str
    rationale: str
    applicability_score: int
    arguments: Optional[Mapping[str, Any]] = dict()
    same_call_is_already_staged: bool
    should_run: bool


class ToolCallInferenceSchema(DefaultBaseModel):
    last_customer_message: Optional[str] = None
    most_recent_customer_inquiry_or_need: Optional[str] = None
    most_recent_customer_inquiry_or_need_was_already_resolved: Optional[bool] = False
    tool_call_evaluations: list[ToolCallEvaluation]


@dataclass(frozen=True)
class ToolCall:
    id: ToolCallId
    tool_id: ToolId
    arguments: Mapping[str, JSONSerializable]


@dataclass(frozen=True)
class ToolCallResult:
    id: ToolResultId
    tool_call: ToolCall
    result: ToolResult


class ToolCaller:
    def __init__(
        self,
        logger: Logger,
        service_registry: ServiceRegistry,
        schematic_generator: SchematicGenerator[ToolCallInferenceSchema],
    ) -> None:
        self._service_registry = service_registry
        self._logger = logger
        self._schematic_generator = schematic_generator

    async def infer_tool_calls(
        self,
        agents: Sequence[Agent],
        customer: Customer,
        context_variables: Sequence[tuple[ContextVariable, ContextVariableValue]],
        interaction_history: Sequence[Event],
        terms: Sequence[Term],
        ordinary_guideline_propositions: Sequence[GuidelineProposition],
        tool_enabled_guideline_propositions: Mapping[GuidelineProposition, Sequence[ToolId]],
        staged_events: Sequence[EmittedEvent],
    ) -> tuple[GenerationInfo, Sequence[ToolCall]]:
        async def _get_id_tool_pairs(tool_ids: Sequence[ToolId]) -> Sequence[tuple[ToolId, Tool]]:
            services: dict[str, ToolService] = {}
            tools = []
            for id in tool_ids:
                if id.service_name not in services:
                    services[id.service_name] = await self._service_registry.read_tool_service(
                        id.service_name
                    )
                tools.append((id, await services[id.service_name].read_tool(id.tool_name)))
            return tools

        inference_prompt = self._format_tool_call_inference_prompt(
            agents,
            customer,
            context_variables,
            interaction_history,
            terms,
            ordinary_guideline_propositions,
            {
                p: await _get_id_tool_pairs(tool_ids)
                for p, tool_ids in tool_enabled_guideline_propositions.items()
            },
            staged_events,
        )

        with self._logger.operation("Tool classification"):
            generation_info, inference_output = await self._run_inference(inference_prompt)

        return generation_info, [
            ToolCall(
                id=ToolCallId(generate_id()),
                tool_id=ToolId.from_string(tc.name),
                arguments=tc.arguments or {},
            )
            for tc in inference_output
            if tc.should_run and tc.applicability_score >= 6
        ]

    async def execute_tool_calls(
        self,
        context: ToolContext,
        tool_calls: Sequence[ToolCall],
    ) -> Sequence[ToolCallResult]:
        with self._logger.operation("Tool calls"):
            tool_results = await asyncio.gather(
                *(
                    self._run_tool(
                        context=context,
                        tool_call=tool_call,
                        tool_id=tool_call.tool_id,
                    )
                    for tool_call in tool_calls
                )
            )

            return tool_results

    def _format_tool_call_inference_prompt(
        self,
        agents: Sequence[Agent],
        customer: Customer,
        context_variables: Sequence[tuple[ContextVariable, ContextVariableValue]],
        interaction_event_list: Sequence[Event],
        terms: Sequence[Term],
        ordinary_guideline_propositions: Sequence[GuidelineProposition],
        tool_enabled_guideline_propositions: Mapping[
            GuidelineProposition, Sequence[tuple[ToolId, Tool]]
        ],
        staged_events: Sequence[EmittedEvent],
    ) -> str:
        assert len(agents) == 1

        id_tool_pairs = list(chain(*tool_enabled_guideline_propositions.values()))

        proposition_tool_ids = {
            p: [t_id for t_id, _ in pairs]
            for p, pairs in tool_enabled_guideline_propositions.items()
        }

        staged_calls = self._get_staged_calls(staged_events)

        builder = PromptBuilder()

        builder.add_section(
            """


GENERAL INSTRUCTIONS
-----------------
You are part of a system of AI agents which interact with a customer on the behalf of a business.
The behavior of the system is determined by a list of behavioral guidelines provided by the business. 
Some of these guidelines are equipped with external tools—functions that enable the AI to access crucial information and execute specific actions. 
Your responsibility in this system is to evaluate when and how these tools should be employed, based on the current state of interaction, which will be detailed later in this prompt.

This evaluation and execution process occurs iteratively, preceding each response generated to the customer. 
Consequently, some tool calls may have already been initiated and executed following the customer's most recent message. 
Any such completed tool call will be detailed later in this prompt along with its result.
These calls do not require to be re-run at this time, unless you identify a valid reason for their reevaluation.


"""
        )
        builder.add_agent_identity(agents[0])
        builder.add_section(
            f"""
-----------------
TASK DESCRIPTION
-----------------
Your task is to review the available tools and, based on your most recent interaction with the customer, decide whether to use each one. 
For each tool, assign a score from 1 to 10 to indicate its usefulness at this time, where a higher score indicates that the tool call should execute. 
For any tool with a score of 5 or higher, provide the arguments for activation, following the format in its description.

While doing so, take the following instructions into account:

1. You may suggest tools that don’t directly address the customer’s latest interaction but can advance the conversation to a more useful state based on function definitions.
2. Each tool may be called multiple times with different arguments.
3. Avoid calling a tool with the same arguments more than once, unless clearly justified by the interaction.
4. Ensure each tool call relies only on the immediate context and staged calls, without requiring other tools not yet invoked, to avoid dependencies.
5. Use the "should_run" argument to indicate whether a tool should be executed, meaning it has a high applicability score and either (a) has not been staged with the same arguments, or (b) was staged but needs to be re-executed.
6. If a tool needs to be applied multiple times (each with different arguments), you may include it in the output multiple times.


Produce a valid JSON object according to the following general format:
```json
{{
    "last_customer_message": "<REPEAT THE LAST USER MESSAGE IN THE INTERACTION>",
    "most_recent_customer_inquiry_or_need": "<customer's inquiry or need>",
    "most_recent_customer_inquiry_or_need_was_already_resolved": <BOOL>,
    "tool_call_evaluations": [
        {{
            "name": "<TOOL NAME>",
            "rationale": "<A FEW WORDS THAT EXPLAIN WHETHER AND HOW THE TOOL NEEDS TO BE CALLED>",
            "applicability_score": <INTEGER FROM 1 TO 10>,
            "arguments": <ARGUMENTS FOR THE TOOL. CAN BE DROPPED IF THE TOOL SHOULD NOT EXECUTE>,
            "same_call_is_already_staged": <BOOLEAN>,
            "should_run": <BOOL>,
        }},
        ...
    ]
}}
```

where each tool provided to you under appears at least once in "tool_call_evaluations", whether you decide to use it or not.
The exact format of your output will be provided to you at the end of this prompt.

The following examples show correct outputs for various hypothetical situations. 
Only the responses are provided, without the interaction history or tool descriptions, though these can be inferred from the responses.

EXAMPLES
-----------------
###
Example 1:

Context - the id of the customer is 12345, and check_balance(12345) is the only staged tool call
###
```json
{{
    "last_customer_message": "Do I have enough money in my account to get a taxi from New York to Newark?",
    "most_recent_customer_inquiry_or_need": "Checking customer's balance, comparing it to the price of a taxi from New York to Newark, and report the result to the customer",
    "most_recent_customer_inquiry_or_need_was_already_resolved": false,
    "tool_call_evaluations": [
        {{
            "name": "check_balance",
            "rationale": "We need the client's current balance to respond to their question",
            "applicability_score": 9,
            "arguments": {{
                "customer_id": "12345",
            }},
            "same_call_is_already_staged": true,
            "should_run": false,
        }},
        {{
            "name": "ping_supervisor",
            "rationale": "There is no reason to notify the supervisor of anything",
            "applicability_score": 1,
            "same_call_is_already_staged": false,
            "should_run": false,
        }},
        {{
            "name": "check_ride_price",
            "rationale": "We need to know the price of a ride from New York to Newark to respond to the customer",
            "applicability_score": 9,
            "arguments": {{
                "origin": "New York",
                "Destination": "Newark",
            }},
            "same_call_is_already_staged": false,
            "should_run": true,
        }},
        {{
            "name": "order_taxi",
            "rationale": "The client hasn't asked for a taxi to be ordered yet",
            "applicability_score": 2,
            "same_call_is_already_staged": false,
            "should_run": false,
        }},
    ]
}}
```
###
Example 2:
Context - there are two available tools, and no calls have been staged yet:
check_calories(<product_name>): returns the number of calories in a the product
check_stock(): returns all menu items that are currently in stock
###
```json
{{
    "last_customer_message": "Which pizza has more calories, the classic margherita or the deep dish?",
    "most_recent_customer_inquiry_or_need": "Checking the number of calories in two types of pizza and replying with which one has more",
    "most_recent_customer_inquiry_or_need_was_already_resolved": false,
    "tool_call_evaluations": [
        {{
            "name": "check_calories",
            "rationale": "We need to check how many calories are in the margherita pizza",
            "applicability_score": 9,
            "arguments": {{
                "product_name": "margherita",
            }},
            "same_call_is_already_staged": false,
            "should_run": true,
        }},
        {{
            "name": "check_calories",
            "rationale": "We need to check how many calories are in the deep dish pizza",
            "applicability_score": 9,
            "arguments": {{
                "product_name": "deep dish",
            }},
            "same_call_is_already_staged": false,
            "should_run": true,
        }},
        {{
            "name": "check_stock",
            "rationale": "Knowing which of the mentioned pizzas are in stock could improve the quality of the agent's next response, even if it's not directly called for",
            "applicability_score": 7,
            "arguments": {{
            }},
            "same_call_is_already_staged": false,
            "should_run": true,
        }},
    ]
}}
```
"""  # noqa
        )
        builder.add_context_variables(context_variables)
        builder.add_glossary(terms)
        builder.add_interaction_history(interaction_event_list)

        builder.add_section(
            self._get_guideline_propositions_section(
                ordinary_guideline_propositions,
                proposition_tool_ids,
            ),
            name=BuiltInSection.GUIDELINE_DESCRIPTIONS,
        )
        builder.add_tool_definitions(id_tool_pairs)
        if staged_calls:
            builder.add_section(
                f"""
STAGED TOOL CALLS
-----------------
The following is a list of tool calls staged after the interaction’s latest state. Use this information to avoid redundant calls and to guide your response.

Reminder: If a tool is already staged with the exact same arguments, set "same_call_is_already_staged" to true. 
You may still choose to re-run the tool call, but only if there is a specific reason for it to be executed multiple times.

The staged tool calls are:
{staged_calls}
###
"""
            )
        else:
            builder.add_section(
                """
STAGED TOOL CALLS
-----------------
There are no staged tool calls at this time.
###
"""
            )

        builder.add_section(
            f"""
OUTPUT FORMAT
-----------------
Given these tools, your output should adhere to the following format:
{self._get_output_format(id_tool_pairs)}

However, note that you may choose to duplicate certain entries in 'tool_call_evaluations' if you wish to call a certain tool multiple times with different arguments.
###
        """
        )

        return builder.build()

    def _get_output_format(self, id_tool_pairs: Sequence[tuple[ToolId, Tool]]) -> str:
        tool_call_evaluation_format = "\n".join(
            [
                f"""
        {{
            "name": "{tool_id.service_name}:{tool_id.tool_name}",
            "rationale": "<A FEW WORDS THAT EXPLAIN WHETHER AND HOW THE TOOL NEEDS TO BE CALLED>",
            "applicability_score": <INTEGER FROM 1 TO 10>,
            "arguments": <ARGUMENTS FOR THE TOOL. CAN BE OMITTED IF THE TOOL SHOULD NOT EXECUTE>,
            "same_call_is_already_staged": <BOOLEAN>,
            "should_run": <BOOL>,
        }},                                                
"""
                for tool_id, _ in id_tool_pairs
            ]
        )
        return f"""
```json
{{
    "last_customer_message": "<REPEAT THE LAST USER MESSAGE IN THE INTERACTION>",
    "most_recent_customer_inquiry_or_need": "<customer's inquiry or need>",
    "most_recent_customer_inquiry_or_need_was_already_resolved": <BOOL>,
    "tool_call_evaluations": [{tool_call_evaluation_format}]
}}
```
"""

    def _get_guideline_propositions_section(
        self,
        ordinary_guideline_propositions: Sequence[GuidelineProposition],
        proposition_tool_ids: Mapping[GuidelineProposition, Sequence[ToolId]],
    ) -> str:
        all_propositions = list(chain(ordinary_guideline_propositions, proposition_tool_ids))

        if all_propositions:
            guidelines = []

            for i, p in enumerate(all_propositions, start=1):
                guideline = (
                    f"{i}) When {p.guideline.content.condition}, then {p.guideline.content.action}"
                )

                if p in proposition_tool_ids:
                    service_tool_names = ", ".join(
                        [
                            f"{t_id.service_name}:{t_id.tool_name}"
                            for t_id in proposition_tool_ids[p]
                        ]
                    )
                    guideline += f"\n    [Associated Tools: {service_tool_names}]"

                guidelines.append(guideline)

            guideline_list = "\n".join(guidelines)
        return f"""
GUIDELINES
---------------------
The following guidelines have been identified as relevant to the current state of interaction with the customer. 
Some guidelines have tools associated with them, which you may decide to apply as needed. Use these guidelines to understand the context for each tool.

Guidelines: 
###
{guideline_list}
###
"""

    def _get_staged_calls(
        self,
        emitted_events: Sequence[EmittedEvent],
    ) -> Optional[str]:
        staged_calls = list(
            chain(*[e["data"] for e in emitted_tool_events_to_dicts(emitted_events)])
        )

        if not staged_calls:
            return None

        return json.dumps(
            [
                {
                    "tool_id": invocation["tool_id"],
                    "arguments": invocation["arguments"],
                    "result": invocation["result"],
                }
                for invocation in staged_calls
            ]
        )

    async def _run_inference(
        self,
        prompt: str,
    ) -> tuple[GenerationInfo, Sequence[ToolCallEvaluation]]:
        self._logger.debug(f"Tool call inference prompt: {prompt}")

        inference = await self._schematic_generator.generate(
            prompt=prompt,
            hints={"temperature": 0.0},
        )

        self._logger.debug(
            f"Tool call request results: {json.dumps([t.model_dump(mode='json') for t in inference.content.tool_call_evaluations], indent=2),}"
        )
        return inference.info, inference.content.tool_call_evaluations

    async def _run_tool(
        self,
        context: ToolContext,
        tool_call: ToolCall,
        tool_id: ToolId,
    ) -> ToolCallResult:
        try:
            self._logger.debug(
                f"Tool call executing: {tool_call.tool_id.to_string()}/{tool_call.id}"
            )
            service = await self._service_registry.read_tool_service(tool_id.service_name)
            result = await service.call_tool(
                tool_id.tool_name,
                context,
                tool_call.arguments,
            )
            self._logger.debug(
                f"Tool call returned: {tool_call.tool_id.to_string()}/{tool_call.id}: {json.dumps(asdict(result), indent=2)}"
            )

            return ToolCallResult(
                id=ToolResultId(generate_id()),
                tool_call=tool_call,
                result={
                    "data": result.data,
                    "metadata": result.metadata,
                    "control": result.control,
                },
            )
        except Exception as e:
            self._logger.error(
                f"Tool execution error (tool='{tool_call.tool_id.to_string()}', "
                "arguments={tool_call.arguments}): " + "\n".join(traceback.format_exception(e)),
            )

            return ToolCallResult(
                id=ToolResultId(generate_id()),
                tool_call=tool_call,
                result={
                    "data": "Tool call error",
                    "metadata": {"error_details": str(e)},
                    "control": {},
                },
            )
