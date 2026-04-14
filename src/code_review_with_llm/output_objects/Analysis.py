class Analysis:
    def __init__(self, commit_id: str, filename: str, changes: str, analysis: str = None):
        self.commit_id = commit_id
        self.filename = filename
        self.changes = changes
        self.analysis = analysis

    def get_commit_id(self):
        return self.commit_id

    def get_filename(self):
        return self.filename

    def get_changes(self):
        return self.changes

    def get_analysis(self):
        return self.analysis

    def set_analysis(self, analysis: str):
        self.analysis = analysis
