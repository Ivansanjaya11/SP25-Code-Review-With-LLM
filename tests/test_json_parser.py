from datetime import datetime
from pathlib import Path
import pytest
import os
from src.code_review_with_llm.model.JSONParser import JSONParser
from src.code_review_with_llm.output_objects.Output import Output

@pytest.fixture
def json_parser():
    return JSONParser()

def test_filter_and_parse(tmp_path, json_parser):
    results_dir = tmp_path / "results" / "2024_7"
    results_dir.mkdir(parents=True)

    json_file = results_dir / "test.json"
    json_file.write_text("""
    {
        "pr_info": {
            "pr_id": 1,
            "pr_title": "Fix bug",
            "pr_description": "desc",
            "pr_changes": "changes",
            "pr_commit_id_list": ["abc"]
        },
        "repository_info": {
            "repo_name": "repo",
            "repo_url": "url",
            "repo_branches": ["main"],
            "repo_commit_id_list": ["abc"],
            "repo_changes": "changes"
        },
        "test_cases": [],
        "errors": [],
        "timestamp": "2024-07-15 10:30:00"
    }
    """)

    os.chdir(tmp_path)

    outputs = json_parser.filter_and_parse(7, 2024)

    assert len(outputs) == 1
    assert isinstance(outputs[0], Output)

