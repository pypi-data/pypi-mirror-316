from typing import Any, Dict, Optional, Generator
from openai import NOT_GIVEN, OpenAI
from ...types import EnumLLMProvider, LLMProvider, ChatCompletionParams

class OpenAIGateway(LLMProvider):
    def __init__(self, api_key: str, **kwargs):
        super().__init__(EnumLLMProvider.OPENAI)
        self.client = OpenAI(api_key=api_key)

    def chat_completion(self, params: ChatCompletionParams) -> Dict[str, Any]:
        response = self.client.chat.completions.create(
            model=params.model,
            messages=[msg.__dict__ for msg in params.messages],
            temperature=params.temperature or NOT_GIVEN,
            max_completion_tokens=params.max_completion_tokens or NOT_GIVEN,
            top_p=params.top_p or NOT_GIVEN,
            tools=params.tools or NOT_GIVEN,
            tool_choice=params.tool_choice or NOT_GIVEN
        )

        completion = response.choices[0]
        if completion.finish_reason == 'tool_calls':
            response.llm_gateway_output = [{
                'type': 'tool_calls',
                'tool_name': completion.message.tool_calls[0].function.name,
                'arguments': completion.message.tool_calls[0].function.arguments
            }]
        else:
            response.llm_gateway_output = [{
                'type': 'text',
                'content': completion.message.content
            }]
        return response

    def chat_completion_stream(self, params: ChatCompletionParams) -> Generator[Dict[str, Any], None, None]:
        stream = self.client.chat.completions.create(
            model=params.model,
            messages=[msg.__dict__ for msg in params.messages],
            temperature=params.temperature or NOT_GIVEN,
            max_completion_tokens=params.max_completion_tokens or NOT_GIVEN,
            top_p=params.top_p or NOT_GIVEN,
            tools=params.tools or NOT_GIVEN,
            tool_choice=params.tool_choice or NOT_GIVEN,
            stream=True
        )

        for chunk in stream:
            completion = chunk.choices[0]
            if completion.finish_reason == 'tool_calls':
                chunk.llm_gateway_output = [{
                    'type': 'tool_calls',
                    'tool_name': completion.message.tool_calls[0].function.name,
                    'arguments': completion.message.tool_calls[0].function.arguments
                }]
            else:
                chunk.llm_gateway_output = [{
                    'type': 'text',
                    'content': completion.delta.content if completion.delta.content else ''
                }]
            yield chunk
