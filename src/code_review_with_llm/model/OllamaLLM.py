from src.code_review_with_llm.model.LLM import LLM
import json
import ollama
from src.code_review_with_llm.output_objects.Error import Error

class OllamaLLM(LLM):
    def __init__(self, model="llama3:latest", host="http://localhost:11434"):
        super().__init__(model=model)
        self.client = ollama.Client(host=host)

    def request_repo_analysis(self, changes):
        formatted_prompt = self.get_repo_analysis_prompt.format(
            changes = changes
        )

        print(formatted_prompt[:1000])

        print(self.system_prompt_repo)

        print(f"Requesting repo analysis.....")

        get_repo_analysis_response = self.client.chat(
            model = self.model,
            messages=[
                {"role": "system", "content": self.system_prompt_repo},
                {"role": "user", "content": formatted_prompt}
            ],
            format=self.RepoAnalysisFormat.model_json_schema()
        )

        print("response received!")

        repo_analysis_response = get_repo_analysis_response["message"]["content"]

        repo_analysis_json = json.loads(repo_analysis_response)

        print(repo_analysis_json)

        print(f"response parsed!")

        repo_analysis = repo_analysis_json["analysis"]

        print(f"Repo analysis generated \n {repo_analysis}")

        return repo_analysis

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