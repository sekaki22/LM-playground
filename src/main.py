from pydantic import BaseModel

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

import torch
from numba import cuda
from transformers import pipeline

app = FastAPI()

class ModelRequest(BaseModel):
    model: str
generate_text = pipeline(model="EleutherAI/pythia-2.8b", torch_dtype=torch.bfloat16, trust_remote_code=True, device_map="auto")


@app.get("/predict")
async def prompt(prompt: str):
    
    res = generate_text(prompt)
    response_text = res[0]["generated_text"]
    print(response_text)

    return response_text

@app.get("/run_tests")
async def test():
    
    pass

@app.post("/model")
async def prompt(model: ModelRequest):
    # try:
    global generate_text
    del generate_text
    torch.cuda.empty_cache()

    generate_text = pipeline(model=model.model, torch_dtype=torch.bfloat16, trust_remote_code=True, device_map="auto")
    # except RuntimeError as e:
    #     raise HTTPException(
    #         status_code=406,
    #         detail="Model not found",
    #         headers={"X-Error": "Pipeline could not load model"},
    #     )


# Place After All Other Routes
app.mount('', StaticFiles(directory="front/public/", html=True), name="static")



# if __name__ == "__main__":
#     pass
