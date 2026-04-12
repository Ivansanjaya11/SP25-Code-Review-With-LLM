from google import genai
from src.code_review_with_llm.model.LLM import LLM
import os
from dotenv import load_dotenv
import json
from src.code_review_with_llm.output_objects.Error import Error

class GeminiLLM(LLM):
    def __init__(self):
        super().__init__(model = 'gemini-2.5-flash-lite')
        load_dotenv()
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

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

        get_error_response = self.client.models.generate_content(
            model=self.model,
            config=genai.types.GenerateContentConfig(
                system_instruction=self.system_prompt_error,
                response_mime_type="application/json",
                response_schema=self.ErrorListFormat,
            ),
            contents=formatted_prompt,
        )

        error_response = get_error_response.text
        return error_response

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

        suggestion_response = self.client.models.generate_content(
            model=self.model,
            config=genai.types.GenerateContentConfig(
                system_instruction=self.system_prompt_suggestion,
                response_mime_type="application/json",
                response_schema=self.SuggestionListFormat,
            ),
            contents=formatted_prompt,
        )

        suggestion_response = suggestion_response.text  
        suggestion_response_parsed = json.loads(suggestion_response)['suggestions'][0]['suggestion']
        error.set_fix_suggestion(suggestion_response_parsed)

        return error
