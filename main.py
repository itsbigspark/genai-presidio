from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from anonymizer.anonymizer import setup_presidio
from presidio_anonymizer import OperatorConfig
import openai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Allow all CORS (adjust as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# # Mount static files
# app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Presidio components
analyzer, anonymizer_engine, deanonymizer_engine, _ = setup_presidio()

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
if openai.api_key is None:
    raise ValueError("OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable.")


class ProcessRequest(BaseModel):
    text: str


class ProcessResponse(BaseModel):
    text: str


@app.get("/", response_class=HTMLResponse)
async def get():
    with open("templates/index.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)


@app.post("/api/process", response_model=ProcessResponse)
async def process_text(request: ProcessRequest):
    try:
        # Initialize entity mapping for this request
        entity_mapping = {}

        # Step 1: Anonymize the text using our anonymizer package
        analyzer_results = analyzer.analyze(text=request.text, language="en")
        anonymized_result = anonymizer_engine.anonymize(
            request.text,
            analyzer_results,
            {
                "DEFAULT": OperatorConfig("entity_counter", {"entity_mapping": entity_mapping})
            }
        )
        anonymized_text = anonymized_result.text  # Get the anonymized input text
        entity_mapping = anonymized_result.items  # Get the updated entity mapping specific to current request

        # # Step 2: Send anonymized text to OpenAI API
        # # TODO: prompt engineering to explain to model to preserve anonymized text in response (be consistent)
        # response = openai.Completion.create(
        #     engine="text-davinci-003",  # Choose the appropriate engine
        #     prompt=anonymized_text,
        #     max_tokens=150  # Adjust max tokens based on your needs
        # )
        # anonymized_llm_response = response.choices[0].text.strip()

        anonymized_llm_response = anonymized_text

        # Step 3: Deanonymize the LLM response
        deanonymized_text = deanonymizer_engine.deanonymize(
            anonymized_llm_response,
            [],
            {
                "DEFAULT": OperatorConfig("entity_counter_deanonymizer", {"entity_mapping": entity_mapping})
            }
        )

        # Return the deanonymized response
        return ProcessResponse(text=deanonymized_text.text)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# To run the FastAPI app, use the command below:
# uvicorn main:app --reload
