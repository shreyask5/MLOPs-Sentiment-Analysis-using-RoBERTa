import time

from fastapi import APIRouter, BackgroundTasks, HTTPException

from app.api.schemas.request import BatchSentimentRequest, SentimentRequest
from app.api.schemas.response import BatchSentimentResponse, SentimentResponse
from app.models.prediction import predict_sentiment
from app.monitoring.metrics import record_prediction_metrics

router = APIRouter()


@router.post(
    "/sentiment",
    response_model=SentimentResponse,
    summary="Analyze sentiment of a text",
    description="Analyze the sentiment of a single text input as positive, negative, or neutral.",
)
async def analyze_sentiment(
    request: SentimentRequest, background_tasks: BackgroundTasks
) -> SentimentResponse:
    """
    Analyze the sentiment of a single text.

    Args:
        request: SentimentRequest containing the text to analyze
        background_tasks: FastAPI background tasks for async operations

    Returns:
        SentimentResponse with the analysis results
    """
    try:
        start_time = time.time()

        results = predict_sentiment(request.text)
        result = results[0]

        prediction_time = time.time() - start_time

        background_tasks.add_task(
            record_prediction_metrics,
            text_length=len(request.text),
            sentiment=result["sentiment"],
            confidence=result["confidence"],
            prediction_time=prediction_time,
        )

        return SentimentResponse(
            text=result["text"],
            sentiment=result["sentiment"],
            confidence=result["confidence"],
            probabilities=result["probabilities"],
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error analyzing sentiment: {str(e)}"
        )


@router.post(
    "/sentiment/batch",
    response_model=BatchSentimentResponse,
    summary="Analyze sentiment of multiple texts",
    description="Batch analyze the sentiment of multiple text inputs.",
)
async def analyze_sentiment_batch(
    request: BatchSentimentRequest, background_tasks: BackgroundTasks
) -> BatchSentimentResponse:
    """
    Analyze the sentiment of multiple texts.

    Args:
        request: BatchSentimentRequest containing the texts to analyze
        background_tasks: FastAPI background tasks for async operations

    Returns:
        BatchSentimentResponse with the analysis results
    """
    if not request.texts:
        raise HTTPException(status_code=400, detail="No texts provided for analysis")

    try:
        start_time = time.time()

        results = predict_sentiment(request.texts)

        prediction_time = time.time() - start_time

        for result in results:
            background_tasks.add_task(
                record_prediction_metrics,
                text_length=len(result["text"]),
                sentiment=result["sentiment"],
                confidence=result["confidence"],
                prediction_time=prediction_time,
            )

        response_items = [
            SentimentResponse(
                text=result["text"],
                sentiment=result["sentiment"],
                confidence=result["confidence"],
                probabilities=result["probabilities"],
            )
            for result in results
        ]

        return BatchSentimentResponse(results=response_items)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error analyzing sentiment batch: {str(e)}"
        )
