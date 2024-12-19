import os
import tempfile
from typing import Any, Union
from unittest.mock import Mock, patch

import pytest
from pydantic import BaseModel

from tecton_gen_ai.utils._cache import CacheProtocol, get_cache
from tecton_gen_ai.tecton_utils.structured_outputs import (
    T_OutputType,
    batch_generate,
    batch_generate_dicts,
)


def generate_dict(
    model: Union[str, dict[str, Any]],
    text: str,
    schema: Union[type[T_OutputType], dict[str, Any]],
) -> dict[str, Any]:
    return batch_generate_dicts(model, [text], schema)[0]


def generate(
    model: Union[str, dict[str, Any]], text: str, schema: type[T_OutputType]
) -> T_OutputType:
    return batch_generate(model, [text], schema)[0]


class SampleModel(BaseModel):
    field1: str
    field2: int


@pytest.fixture(autouse=True)
def reset_cache():
    with tempfile.TemporaryDirectory() as temp_dir:
        _old_cache_dir = os.environ.get("XDG_CACHE_HOME")
        os.environ["XDG_CACHE_HOME"] = str(temp_dir)
        try:
            yield
        finally:
            if _old_cache_dir is not None:
                os.environ["XDG_CACHE_HOME"] = _old_cache_dir


def test_generate():
    result = generate("openai/gpt-4o-mini", "field1: value, field2: 42", SampleModel)
    assert result.field1 == "value"
    assert result.field2 == 42


def test_generate_dict():
    result = generate_dict(
        "openai/gpt-4o-mini", "field1: value, field2: 42", SampleModel
    )
    expected = {"field1": "value", "field2": 42}
    assert result == expected


def test_batch_generate():
    results = batch_generate(
        "openai/gpt-4o-mini",
        ["field1: value1, field2: 42", "field1: value2, field2: 43"],
        SampleModel,
    )
    expected = [
        SampleModel(field1="value1", field2=42),
        SampleModel(field1="value2", field2=43),
    ]
    assert len(results) == len(expected)
    for result, expected in zip(results, expected):
        assert result.field1 == expected.field1
        assert result.field2 == expected.field2


def test_batch_generate_dicts():
    results = batch_generate_dicts(
        "openai/gpt-4o-mini",
        ["field1: value1, field2: 42", "field1: value2, field2: 43"],
        SampleModel,
    )
    expected = [{"field1": "value1", "field2": 42}, {"field1": "value2", "field2": 43}]
    assert len(results) == len(expected)
    for result, expected in zip(results, expected):
        assert result == expected


def test_batch_generate_dicts_invalid_model():
    with pytest.raises(ValueError, match="Model .* not supported"):
        batch_generate_dicts("invalid-model", ["text1", "text2"], SampleModel)


@pytest.mark.parametrize(
    "func,schema",
    [(batch_generate, SampleModel), (batch_generate_dicts, SampleModel)],
)
def test_cache_behavior(func, schema):
    texts = ["field1: value1, field2: 42", "field1: value2, field2: 43"]

    cache = get_cache("tecton-gen-ai", "structured_outputs")
    mock_cache = Mock(spec=CacheProtocol, wraps=cache)

    with patch(
        "tecton_gen_ai.utils._cache.get_cache",
        return_value=mock_cache,
    ):
        # Call the function to test
        func("openai/gpt-4o-mini", texts, schema)

        # Ensure cache was checked and set
        assert mock_cache.aget.call_count == 2  # Cache checked twice
        assert mock_cache.aset.call_count == 2  # Cache set twice

        # Call the function again
        func("openai/gpt-4o-mini", texts, schema)

        # Ensure cache was checked again but not set (meaning we returned from cache)
        assert mock_cache.aget.call_count == 4  # Cache checked twice more
        assert mock_cache.aset.call_count == 2  # Cache set should not increase
