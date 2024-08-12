class LlmOutputGenerationException(Exception):
    """
    Exception raised when the LLM model fails to generate an output.
    """
    def __init__(self,
        llm_model: str,
        message: str = "Failed to generate output with the LLM model."
        ):
        super().__init__(message)
        self.llm_model = llm_model


class LlmOutputParsingException(Exception):
    """
    Exception raised when the LLM model output cannot be parsed properly.
    """
    def __init__(self,
        llm_model: str,
        message: str = "Failed to parse the output from the LLM model."
        ):
        super().__init__(message)
        self.llm_model = llm_model
