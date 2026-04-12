import os
import json
from src.code_review_with_llm.output_objects.Error import Error
from src.code_review_with_llm.output_objects.FeedbackOutput import FeedbackOutput
from pydantic import BaseModel
from pathlib import Path

class LLM:
    def __init__(self, model, prompt_config_path=None):
        if prompt_config_path is None:
            prompt_dir = os.path.dirname(os.path.abspath(__file__))
            prompt_config_path = os.path.join(prompt_dir, "..", "..", "prompts.json")

        self.model = model
        self.prompt_config_path = prompt_config_path
        self.available_error_types = "OVERFLOW_ERROR, ROUND_OFF_ERROR, INFINITE_LOOP_ERROR," \
                "MODIFY_PARAMETER_VARIABLE_ERROR, OFF_BY_ONE_ERROR, ARITHMETIC_ERROR," \
                "BOUNDS_ERROR, UNINITIALIZED_ARRAY_ERROR, SQUELCH_EXCEPTION_ERROR," \
                "MAGIC_NUMBER_ERROR, DANGLING_ELSE_ERROR, OTHERS"
        
        # get the prompts from the json file
        try:
            with open(prompt_config_path, "r", encoding="utf-8") as file:
                prompts = json.load(file)

                self.system_prompt_error = prompts['system_prompt_error']
                print(f"System prompt error fetched: {self.system_prompt_error}")

                self.system_prompt_suggestion = prompts['system_prompt_suggestion']
                print(f"System prompt suggestion fetched: {self.system_prompt_suggestion}")

                self.get_error_prompt = prompts['get_error_prompt']
                print(f"Get error prompt fetched: {self.get_error_prompt}")

                self.suggestion_prompt = prompts['suggestion_prompt']
                print(f"Suggestion prompt fetched: {self.suggestion_prompt}")

                print(f"\n'{prompt_config_path}' successfully loaded!")
                
        except FileNotFoundError:
            print(f"Error: The file '{prompt_config_path}' was not found.")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

    def execute(self, code: str) -> FeedbackOutput:
        print(f"Requesting feedback.....")

        error_response = self.request_error(code)
        errors = self.parse_error_response(error_response, code)
        
        print(f"Feedback successfully generated!")

        print(f"Requesting suggestions.....")

        errors = self.get_all_fix_suggestions(errors)

        print(f"Suggestions successfully generated!")

        feedback_output = FeedbackOutput(errors)

        return feedback_output
    
    def request_error(self, code: str) -> str:
        raise NotImplementedError("Subclasses must implement request_error")

    def parse_error_response(self, error_response: str, code: str) -> list[Error]:
        """
        parse the json-like string into a json object.
        Then create Error objects containing all the information
        """   
        if error_response == "NONE":
            return []
        
        error_response = json.loads(error_response)
        
        parsed_errors = error_response['errors'] # end result or parsing the error response from LLM: a list of error information in consistent format

        # Create a list of Error objects. Assign error type, severity level, and error description generated from llm
        errors = []

        for idx, error_info in enumerate(parsed_errors):
            error_type = error_info['error_type']
            error_severity_level = error_info['severity']
            error_description = error_info['description']

            error = Error(error_type, error_severity_level, error_description, code)
            errors.append(error)

        return errors
    
    def request_suggestion(self, error: Error) -> Error:
        raise NotImplementedError("Subclasses must implement request_suggestion")

    def get_all_fix_suggestions(self, errors: list[Error]) -> list[Error]:
        """
        iterates through every Error and ask the LLM fix suggestions for each of them.
        Returns a list of Error objects.
        """
        for idx, error in enumerate(errors):
            errors[idx] = self.request_suggestion(error)

        return errors

    # json schema (format) for a list of get error LLM outputs 
    class ErrorListFormat(BaseModel):
        # json schema (format) for get error LLM output 
        class ErrorGetterFormat(BaseModel):
                error_type: str
                severity: str
                description: str
        errors: list[ErrorGetterFormat]

    # json schema (format) for a list of get suggestion LLM output 
    class SuggestionListFormat(BaseModel):
        # json schema (format) for get suggestion LLM output
        class SuggestionGetterFormat(BaseModel):
                suggestion: str
        suggestions: list[SuggestionGetterFormat]
