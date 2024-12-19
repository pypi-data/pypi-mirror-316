from typing import Any, Union

import instructor
from tecton import Attribute
from tecton.types import Field as TectonField

from tecton_gen_ai.tecton_utils import _schema_utils
from tecton_gen_ai.tecton_utils.structured_outputs import BatchProcessor, T_OutputType


@BatchProcessor.register(lambda model: model["model"].startswith("openai/"))
class InstructorOpenAIProcessor(BatchProcessor):
    def __init__(
        self, model: dict[str, Any], schema: Union[type[T_OutputType], dict[str, Any]]
    ):
        import openai

        super().__init__(model=model, schema=schema)
        self.aclient = instructor.from_openai(openai.AsyncOpenAI())
        self.provider, self.provider_model = model["model"].split("/", 1)
        model_cp = model.copy()
        model_cp.pop("model")
        self.kwargs = model_cp

    async def aprocess_text(self, text: str) -> dict[str, Any]:
        response = await self.aclient.chat.completions.create(
            model=self.provider_model,
            messages=[
                {"role": "user", "content": text},
            ],
            response_model=None,
            **self.serializable_schema["instructor_kwargs"],
        )
        return self._parse_tools(response)

    def schema_to_json_dict(self, schema: type[T_OutputType]) -> dict[str, Any]:
        schema_dict = schema.model_json_schema()
        _, kwargs = instructor.process_response.handle_response_model(schema)
        return dict(json_schema=schema_dict, instructor_kwargs=kwargs)

    def get_tecton_fields(
        self, as_attributes: bool = False
    ) -> list[Union[TectonField, Attribute]]:
        fields = list(
            _schema_utils.get_tecton_fields_from_json_schema(
                self.serializable_schema["json_schema"]
            )
        )
        if as_attributes:
            return [Attribute(name=field.name, dtype=field.dtype) for field in fields]
        return fields

    def _parse_tools(self, completion: Any) -> dict[str, Any]:
        serializable_schema = self.serializable_schema
        message = completion.choices[0].message

        if hasattr(message, "refusal") and message.refusal is not None:
            raise ValueError(f"Unable to generate a response due to {message.refusal}")
        if len(message.tool_calls or []) != 1:
            raise ValueError(
                "Tecton does not support multiple tool calls, use list[Model] instead"
            )

        tool_call = message.tool_calls[0]
        if tool_call.function.name != serializable_schema["json_schema"]["title"]:
            raise ValueError("Tool name does not match")

        return _schema_utils.load_to_rich_dict(
            tool_call.function.arguments, serializable_schema["json_schema"]
        )
