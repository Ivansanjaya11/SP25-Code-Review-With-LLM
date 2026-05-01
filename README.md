# Introduction
Our system aims to automate the tedious process of code review in large codebases using an LLM. As a project's codebase grows, so does 
the time, effort, and resources required to ensure the code works well and meets standards. The purpose of this tool is to ease the load 
on the code reviewers so they can shift their focus to other tasks. 

# Features
### Analyze Pull Request
This feature will receieve as input a github repository url and a pull request number. It will then collect the final version of each commit 
file in the pull request and send them to an llm prompting for code review. After the analysis is complete it will print the analysis on the 
screen and save it to a json file. The system also allows saving analysis result into a pdf file.

### Saved Feedback
This feature gives the ability to search for previously ran analysis by using a date range.

### Analyze Repo
This feature takes as input a github repository url. The repository will be mined and each commit will be analyzed one by one to give an analysis 
of the entire repository over time.

# Libraries
| Library | Description |
|---------|-------------|
| ollama | Local LLM client |
| google-genai | Gemini API client |
| pydriller | Mining git repositories |
| pygithub | GitHub API for pull request data |
| gitpython | Git operations |
| pydantic | JSON schema validation for LLM responses |
| reportlab | PDF report generation |
| customtkinter | Desktop GUI |
| hypothesis | Test case generation |
| black | Code formatting |
| ruff | Linting |
| python-dotenv | Loading API keys from .env file |
| pybuilder | Build automation |
| tqdm | Progress bars in terminal |
| pytest | Testing framework |
| pytest-cov | Code coverage reporting |

# Setup
### Clone the repo
```
git clone https://github.com/Ivansanjaya11/SP25-Code-Review-With-LLM/
```

### Create and activate the virtual environment
```
python -m venv venv
```

Windows:
```
.\venv\Scripts\Activate
```

Mac/Linux:
```
source venv/bin/activate
```

### Download the dependencies
```
pip install -r requirements.txt
```

### Set up the .env file
Add a .env file to the project root with these two lines
```
GITHUB_API_KEY='github api key goes here'
GEMINI_API_KEY='gemini api key goes here'
```

### Gemini API Setup
Create an API key at [Google AI Studio](https://aistudio.google.com). Note: The free tier is limited to 20 requests per day. For full 
functionality, especially the Analyze Repo feature, a paid tier is recommended ($10 minimum prepay).

### Ollama Setup (optional)
If using Ollama as the LLM provider, install Ollama from [ollama.com](https://ollama.com) and pull the model:
```
ollama pull llama3
```

# Project Structure
```
SP25-Code-Review-With-LLM/
├── src/
│   ├── code_review_with_llm/
│   │   ├── model/           # LLM, pipelines, miners, PDF/JSON generators
│   │   ├── output_objects/  # Error, Output, FeedbackOutput, etc.
│   │   ├── Controller.py
│   │   ├── Model.py
│   │   └── View.py
│   ├── prompts.json         # LLM prompts
│   └── main.py
├── tests/                   # pytest test files
├── results/                 # generated JSON output (auto-created)
├── generated_pdf/           # generated PDF reports (auto-created)
├── test_case_out/           # generated test cases (auto-created)
├── requirements.txt
├── build.py                 # PyBuilder config
├── .env                     # API keys (not committed)
└── README.md
```

# How to run
```
pyb
```

# Testing
To run test cases, use the command:
```
pyb test
```

# Contributors
Ivan Sanjaya  
George Candal
