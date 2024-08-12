import json

import pytest

from app.exceptions.quote_generator_exceptions import LlmOutputParsingException


def test_openai_client_can_generate_quote_and_caption(mock_openai_client):
    """
    GIVEN a mocked OpenAi client instance
    WHEN the quote and caption generation method is called
    THEN it should return a tuple with the generated quote and caption
    """
    # Call the method to generate the output
    quote, caption = mock_openai_client.generate_quote_and_caption("test_prompt")

    # Check that the output is as expected
    assert quote == "mock_quote"
    assert caption == "mock_caption"


def test_openai_client_can_parse_output(mock_openai_client):
    """
    GIVEN a mocked OpenAi client instance
    WHEN a valid output is parsed
    THEN it should return a tuple containing the quote and caption
    """
    # Initialize the valid output
    output = json.dumps(
        {
            "quote": "mock_quote",
            "caption": "mock_caption"
        }
    )

    # Parse the valid output
    quote, caption = mock_openai_client.parse_output(output)

    # Check that the parsed output is as expected
    assert quote == "mock_quote"
    assert caption == "mock_caption"


def test_openai_client_throws_exception_on_invalid_output(mock_openai_client):
    """
    GIVEN a mocked OpenAi client instance
    WHEN an invalid output is parsed
    THEN it should raise an exception
    """
    # Initialize the invalid output
    output = json.dumps({"invalid_key": "invalid_value"})

    # Check that the parsing of the invalid output raises an exception
    with pytest.raises(LlmOutputParsingException):
        mock_openai_client.parse_output(output)
