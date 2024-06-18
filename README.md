# Pseudonymization using presidio

A package for text anonymization and deanonymization (pseudonymization) using Presidio.

## Recognizers

- All built-in presidion recognizers
- Sort code recognizer (any 6 digit number seperated by spaces or dashes, OR malformed sequence of 6 numbers which are preceded by the words "sort code" )

## Project structure
The project follows a structured layout to organize the code, configurations, and documentation effectively. Below is an overview of the project structure:
```
presidio/
├── anonymizer/
│   ├── __init__.py
│   └── anonymizer.py
├── main.py
├── README.md
├── requirements.txt
├── setup.py
├── .env.example
├── .gitignore
└── tests/
    ├── __init__.py
    ├── test_anonymizer.py
    └── test_sortcode_recognizer.py
```

### Directory and File Descriptions

- `anonymizer/`: The main package directory containing the implementation of the anonymizer functionalities.
  - `__init__.py`: An initialization file for the package. It makes the directory a Python package and allows you to import the `setup_presidio` function.
  - `anonymizer.py`: Contains the implementation of the Presidio setup and custom anonymizer logic.

- `main.py`: The entry point of the FastAPI application. It sets up the API endpoints and integrates the Presidio anonymizer with the OpenAI API.

- `README.md`: The main documentation file for the project. It provides an overview, installation instructions, and usage examples.

- `requirements.txt`: Lists the dependencies required for the project. These can be installed using `pip`.

- `.env.example`: A template for the `.env` file, which contains environment variables. Developers should copy this file to `.env` and add their own values.

- `.gitignore`: Specifies files and directories that should be ignored by Git. This typically includes environment files like `.env`.

- `tests/`: Directory containing test cases for the project.
  - `__init__.py`: Initialization file for the tests directory.
  - `test_anonymizer.py`: Contains test cases for the anonymizer functionalities.


## Installation

Overview of installation steps:
- Clone the repo 
- Create conda environment
- Setup OpenAI API key to use LLM endpoint in main.py
- Build presidio anonymizer code as a pip package
- Install pip package locally
- Run the FastAPI application locally
- Voilà!

### Create conda environment and install requirements
```sh
conda create --name presidio python=3.12 pip=24.0
conda activate presidio
pip install -r requirements.txt
```

### Install the spacy model used in the presidio package
Run this in terminal in the project directory:
```sh
python -m spacy download en_core_web_lg
```

### Copy the .env.example file to .env and setup OpenAI API key:

Copy example .env file to actual .env:
```sh
cp .env.example .env
```

In .env add the OpenAI API key
```
OPENAI_API_KEY=your_openai_api_key_here
```

### Package the presidio code

To build the pip package with the anonymizer code we use the setup.py script, run this command in the project working directory.
```sh
python setup.py sdist bdist_wheel
```



Once the package is built, we need to install it locally using pip so we can use it in the FastAPI application.

Uninstall first if already installed (no need to do this if installing package for first time)

```sh
pip uninstall rbs_pii_anonymizer  # Optional 
pip install .
```

### Run FastAPI app
Once package is built and installed locally, we can now run the FastAPI application locally and test out the endpoint.
Run the following command to run the application:

```sh
uvicorn main:app --reload
```
The application will be available at http://127.0.0.1:8000/

API Endpoints:
```
GET /: Serve the index page.
POST /api/process: Anonymize input text, send it to the OpenAI API, and deanonymize the response.
```
    
Example Request:

```sh
curl -X POST "http://127.0.0.1:8000/api/process" -H "Content-Type: application/json" -d '{"text": "Your input text here."}'
```

Example response:
```json
{
  "text": "Processed and deanonymized response text."
}
```
