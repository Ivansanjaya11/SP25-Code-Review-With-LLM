import ollama
import json
from src.code_review_with_llm.output_objects.Error import Error
from src.code_review_with_llm.output_objects.FeedbackOutput import FeedbackOutput
from pydantic import BaseModel
from pathlib import Path

class LLM:
    def __init__(self, model, prompt_config_path=Path("../../prompts.json"), host="http://localhost:11434"):
        self.model = model
        self.prompt_config_path = prompt_config_path
        self.host = host
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

        self.client = ollama.Client(host=self.host)

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
        """
        use LLM to check if there are any errors in the code.
        Will return a json-like string.
        """
        code = code.replace("{", "{{").replace("}", "}}")
        formatted_prompt = self.get_error_prompt.format(
            code = code, # the code in string format containing the changes in a specific pull request mined from the repo
            available_error_types = self.available_error_types
        )

        get_error_response = self.client.chat(
            model = self.model,
            messages = [
                {"role": "system", "content": self.system_prompt_error},
                {"role": "user", "content": formatted_prompt}
            ],
            format = self.ErrorListFormat.model_json_schema()
        )

        error_response = get_error_response["message"]["content"]
        return error_response

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
        """
        use LLM to give suggestions to all the errors.
        Will return an Error object.
        """
        error_type = error.get_error_type()
        severity = error.get_error_severity_level()
        error_description = error.get_error_description()
        code = error.get_code()
        code = code.replace("{", "{{").replace("}", "}}")

        formatted_prompt = self.suggestion_prompt.format(
            error_type = error_type,
            severity = severity,
            error_description = error_description,
            code = code
        )

        suggestion_response = self.client.chat(
            model = self.model,
            messages = [
                {"role": "system", "content": self.system_prompt_suggestion},
                {"role": "user", "content": formatted_prompt}
            ],
            format = self.SuggestionListFormat.model_json_schema()
        )

        suggestion_response = suggestion_response["message"]["content"]

        suggestion_response_parsed = json.loads(suggestion_response)['suggestions'][0]['suggestion']

        error.set_fix_suggestion(suggestion_response_parsed)

        return error

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
