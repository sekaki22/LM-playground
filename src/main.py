import argparse

from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
import uvicorn

import torch
from transformers import pipeline

app = FastAPI()

MODELS = ['databricks/dolly-v2-3b', 'EleutherAI/pythia-2.8b', 't5-small']
CURRENT_MODEL = 'databricks/dolly-v2-3b'
# get_text = lambda res: res[0]["generated_text"]


def string_extractors():
    string_extractors = {model: lambda res: res[0]["generated_text"] for model in MODELS}
    string_extractors['t5-small'] = lambda res: res
    return string_extractors


class ModelRequest(BaseModel):
    model: str


def validate_user_input():
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Optional argument flag which defaults to False
    parser.add_argument("-p", "--port", action="store_const", default=8000)

    # Optional argument flag which defaults to False
    parser.add_argument("-h", "--host", action="store_const", default='http://127.0.0.1')

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))

    args = parser.parse_args()
    return args


generate_text = pipeline(model=CURRENT_MODEL,
                         torch_dtype=torch.bfloat16,
                         trust_remote_code=True,
                         device_map="auto")


@app.get("/predict")
async def prompt(prompt: str):
    global CURRENT_MODEL

    res = generate_text(prompt)

    get_text = string_extractors()[CURRENT_MODEL]
    
    response_text = get_text(res)
    print(response_text)

    return response_text


@app.get("/run_tests")
async def test():
    pass


@app.post("/model")
async def select_model(model: ModelRequest):
    # try:
    global generate_text
    global CURRENT_MODEL

    CURRENT_MODEL = model.model
    del generate_text
    torch.cuda.empty_cache()

    generate_text = pipeline(model=CURRENT_MODEL,
                             torch_dtype=torch.bfloat16,
                             trust_remote_code=True,
                             device_map="auto")
    # except RuntimeError as e:
    #     raise HTTPException(
    #         status_code=406,
    #         detail="Model not found",
    #         headers={"X-Error": "Pipeline could not load model"},
    #     )


# Place After All Other Routes
app.mount('', StaticFiles(directory="front/public/", html=True), name="static")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
