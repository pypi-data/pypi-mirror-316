import asyncio
from typing import Any, Callable, TypeVar, Union

from pydantic import BaseModel
from tecton import Attribute
from tecton.types import Field as TectonField
from ..utils import _cache, _coroutine
from ..utils.config_wrapper import from_json_config, to_json_config
from ..utils.hashing import to_uuid

_DEFAULT_LOCAL_CONCURRENCY = 5
T_OutputType = TypeVar("T_OutputType", bound=BaseModel)


def batch_generate_dicts(
    model: Union[str, dict[str, Any]],
    texts: list[str],
    schema: Union[type[T_OutputType], dict[str, Any]],
    concurrency: int = _DEFAULT_LOCAL_CONCURRENCY,
) -> list[dict[str, Any]]:
    """
    Generate structured outputs for a list of texts

    Args:

        model: The model to use for generation
        texts: The list of texts to generate structured outputs for
        schema: The schema of the structured outputs
        concurrency: The number of concurrent requests to make, defaults to 5

    Returns:

        list[dict[str, Any]]: The structured outputs (python dicts)

    Examples:

        ```python
        from tecton_gen_ai.utils.structured_outputs import batch_generate_dicts
        from pydantic import BaseModel, Field

        model = "openai/gpt-4o"
        texts = ["I am 4", "She is 5"]

        class Age(BaseModel):
            age: int = Field(description="The age")

        outputs = batch_generate_dicts(model, texts, Age)
        ```
    """
    processor = BatchProcessor.make(model=model, schema=schema)
    return processor.process_texts(texts, concurrency=concurrency)


def batch_generate(
    model: Union[str, dict[str, Any]],
    texts: list[str],
    schema: type[T_OutputType],
    concurrency: int = _DEFAULT_LOCAL_CONCURRENCY,
) -> list[T_OutputType]:
    """
    Generate structured outputs for a list of texts

    Args:

        model: The model to use for generation
        texts: The list of texts to generate structured outputs for
        schema: The pydantic schema of the structured outputs
        concurrency: The number of concurrent requests to make, defaults to 5

    Returns:

        list[T_OutputType]: The structured outputs

    Examples:

        ```python
        from tecton_gen_ai.utils.structured_outputs import batch_generate

        model = "openai/gpt-4o"
        texts = ["I am 4", "She is 5"]

        class Age(BaseModel):
            age: int = Field(description="The age")

        outputs = batch_generate(model, texts, Age)
        ```
    """
    return [
        schema.model_validate(x)
        for x in batch_generate_dicts(
            model=model, texts=texts, schema=schema, concurrency=concurrency
        )
    ]


class BatchProcessor:
    _PROCESSORS: list[
        tuple[Callable[[dict[str, Any]], bool], type["BatchProcessor"]]
    ] = []

    @staticmethod
    def register(fn: Callable[[dict[str, Any]], bool]):
        def _register(cls):
            BatchProcessor._PROCESSORS.append((fn, cls))
            return cls

        return _register

    @staticmethod
    def make(
        model: Union[str, dict[str, Any]],
        schema: Union[type[T_OutputType], dict[str, Any]],
    ) -> "BatchProcessor":
        if isinstance(model, str):
            model = {"model": model}
        _cls = BatchProcessor._get_cls(model)
        return _cls(model, schema)

    @staticmethod
    def from_json_str(json_str: str) -> "BatchProcessor":
        data = from_json_config(json_str)
        return BatchProcessor.make(data["model"], data["schema"])

    @staticmethod
    def _get_cls(model: dict[str, Any]) -> type["BatchProcessor"]:
        _load_dependencies()
        for fn, cls in BatchProcessor._PROCESSORS:
            if fn(model):
                return cls
        raise ValueError(f"Model {model} not supported")

    def __init__(
        self, model: dict[str, Any], schema: Union[type[T_OutputType], dict[str, Any]]
    ):
        self.serializable_schema = (
            schema if isinstance(schema, dict) else self.schema_to_json_dict(schema)
        )
        self.model = model

    def get_tecton_fields(
        self, as_attributes: bool = False
    ) -> list[Union[TectonField, Attribute]]:
        raise NotImplementedError

    def to_json_str(self) -> str:
        return to_json_config({"model": self.model, "schema": self.serializable_schema})

    def schema_to_json_dict(self, schema: type[T_OutputType]) -> dict[str, Any]:
        raise NotImplementedError

    async def aprocess_text(self, text: str) -> dict[str, Any]:
        raise NotImplementedError

    def process_texts(
        self, texts: list[str], concurrency: int = _DEFAULT_LOCAL_CONCURRENCY
    ) -> list[dict[str, Any]]:
        # NOTE: default size limit of 1GB (https://grantjenks.com/docs/diskcache/api.html#constants)
        cache = _cache.get_cache("tecton-gen-ai", "structured_outputs")

        async def fn(sem, text: str) -> T_OutputType:
            async with sem:
                key = to_uuid((text, self.serializable_schema))
                if (cached := await cache.aget(key)) is not None:
                    # Deserialize from JSON based on the return type
                    return cached

                result = await self.aprocess_text(text)
                await cache.aset(key, result)
                return result

        async def _gather():
            sem = asyncio.Semaphore(concurrency)
            _jobs = [fn(sem, text) for text in texts]
            return await asyncio.gather(*_jobs)

        return _coroutine.run(_gather())


def _load_dependencies():
    try:
        from tecton_gen_ai.integrations import instructor  # noqa
    except ImportError:
        pass
