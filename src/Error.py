class Error:
    '''
    Error object holds the error type, severity level, and description of the
    error in one object. Used to send to the LLM to get fix suggestions.
    '''
    def __init__(self, error_type: str, error_severity_level: str, error_description: str):
        self.error_type = error_type
        self.error_severity_level = error_severity_level
        self.error_description = error_description
        self.fix_suggestion: str | None = None

    def get_error_type(self) -> str:
        return self.error_type
    
    def get_error_severity_level(self) -> str:
        return self.error_severity_level
    
    def get_error_description(self) -> str:
        return self.error_description
    
    def set_fix_suggestion(self, fix_suggestion: str) -> None:
        self.fix_suggestion = fix_suggestion
