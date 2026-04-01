from _datetime import datetime
from Error import Error

class FeedbackOutput:
    '''
    FeedbackOutput contains the list of Error objects and 
    the timestamp (the time when the feedback is generated for the user)
    '''
    def __init__(self, errors: list[Error], timestamp: datetime = datetime.now().replace(microsecond=0)):
        self.errors = errors
        self.timestamp = timestamp

    def get_all_errors(self) -> list[Error]:
        return self.errors
    
    def get_timestamp(self) -> datetime:
        return self.timestamp

    def add_error(self, error: Error):
        self.errors.append(error)
    
    def __str__(self):
        string = f"Timestamp: {self.timestamp}\n"

        for error in self.errors:
            string += ("-"*25 + "\n")
            string += ("Error type: " + error.get_error_type() + "\n")
            string += ("Severity: " + error.get_error_severity_level() + "\n")
            string += ("Description: " + error.get_error_description() + "\n")
            string += ("Suggestion: " + error.get_fix_suggestion())
            string += ("\n")

        return string