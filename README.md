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
├── README.md
├── requirements.txt
├── setup.py
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

- `tests/`: Directory containing test cases for the project.
  - `__init__.py`: Initialization file for the tests directory.
  - `test_anonymizer.py`: Contains test cases for the anonymizer functionalities.
  - `test_sortcode_recognizer.py`: Contains test cases for the sort code recognizer.
  
- `fastapi_app/`: The main directory for the fastapi application
  - `__init__.py`: An initialization file for the package.
  - `main.py`: FastAPI application containing the endpoints to interact with the presidio package

- `notebooks/`: Directory containing Jupyter notebooks for dev work on presidio components.

- `setup.py`: Setup script that packages up the presidio anonymizer code as a pip package.

- `README.md`: The main documentation file for the project. It provides an overview, installation instructions, and usage examples.

- `environment.yaml`: Conda environment yaml file.

- `.gitignore`: Specifies files and directories that should be ignored by Git. This typically includes environment files like `.env`.


## Installation

### Create conda environment 
```sh
conda env create -f environment.yml
```

### Packaging the presidio code

To build the pip package with the anonymizer code we use the setup.py script, run this command in the project working directory.
```sh
python setup.py sdist bdist_wheel
```

Once the setup.py is complete it will create the dist folder which will contain the package to be uploaded to whatever package repository needed.


## Running the FastAPI application
Run the following command to run the application locally:

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
