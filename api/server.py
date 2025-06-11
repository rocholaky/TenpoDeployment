import logging
import sys
from contextlib import asynccontextmanager

import torch
from fastapi import Body, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pythonjsonlogger import jsonlogger

from api.api_payload import PredictionBody

## Set up logging
logger = logging.getLogger("APILogger")
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stdout)
formatter = jsonlogger.JsonFormatter(
    "%(asctime)s %(levelname)s %(name)s %(message)s",
    rename_fields={"levelname": "severity"},
)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Loading Double it model")
    try:
        ts = torch.jit.load("api/models/doubleit_model.zip")
    except ValueError as e:
        logger.error(f"Error loading model: {e}")
        raise RuntimeError("Failed to load the model. Please check the model file.")
    app.state.model = ts
    yield {"message": "API is starting up"}


app = FastAPI(lifespan=lifespan)
origins = ["*"]  # Allow requests from any origin


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/predict")
async def predict(request: Request, body: PredictionBody = Body(...)):
    """
    Endpoint to handle prediction requests.
    """
    logger.info("Received prediction request")
    # Convert inputs to a tensor
    inputs_tensor = torch.tensor(body.inputs)

    # Perform inference
    try:
        result = app.state.model(inputs_tensor)
        response_data = {
            "result": result.tolist()
        }  # Convert tensor to list for JSON serialization
        logger.info("Prediction successful")
        return JSONResponse(content=response_data)
    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        return JSONResponse(status_code=500, content={"error": "Prediction failed"})
