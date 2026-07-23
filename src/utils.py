"""
Utility functions for Project VIGIL with structured logging.
"""

from src.logger import logger


def calculate_trust_score(completeness, accuracy, freshness, anomaly_score):
    """
    Calculate the Data Trust Score (DTS) using weighted aggregation.

    Args:
        completeness (float): 0-1 score for data completeness
        accuracy (float): 0-1 score for data accuracy
        freshness (float): 0-1 score for data freshness
        anomaly_score (float): 0-1 score for anomaly detection

    Returns:
        float: Weighted Data Trust Score (0-1)
    """
    logger.info(
        "Calculating Data Trust Score",
        extra={
            "extra_fields": {
                "completeness": completeness,
                "accuracy": accuracy,
                "freshness": freshness,
                "anomaly_score": anomaly_score,
            }
        },
    )

    # Validate inputs
    for value in [completeness, accuracy, freshness, anomaly_score]:
        if not (0 <= value <= 1):
            logger.error(
                "Invalid input: score must be between 0 and 1",
                extra={"extra_fields": {"invalid_value": value}},
            )
            raise ValueError("All scores must be between 0 and 1")

    # Weights
    weights = {
        "completeness": 0.30,
        "accuracy": 0.40,
        "freshness": 0.20,
        "anomaly_score": 0.10,
    }

    # Calculate weighted sum
    score = (
        completeness * weights["completeness"]
        + accuracy * weights["accuracy"]
        + freshness * weights["freshness"]
        + anomaly_score * weights["anomaly_score"]
    )

    score = round(score, 4)

    logger.info(
        "Data Trust Score calculated successfully",
        extra={"extra_fields": {"final_score": score}},
    )

    return score


def classify_trust_score(score):
    """
    Classify the Data Trust Score into a human-readable category.

    Args:
        score (float): Data Trust Score (0-1)

    Returns:
        str: Category label
    """
    logger.info(
        "Classifying Trust Score",
        extra={"extra_fields": {"score": score}},
    )

    if score >= 0.95:
        category = "Excellent"
    elif score >= 0.80:
        category = "Good"
    elif score >= 0.60:
        category = "Fair"
    else:
        category = "Poor"

    logger.info(
        "Classification complete",
        extra={"extra_fields": {"category": category}},
    )

    return category
