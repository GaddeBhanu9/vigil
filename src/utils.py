"""
Utility functions for Project VIGIL.
"""


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
    # Validate inputs
    for value in [completeness, accuracy, freshness, anomaly_score]:
        if not (0 <= value <= 1):
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

    return round(score, 4)


def classify_trust_score(score):
    """
    Classify the Data Trust Score into a human-readable category.

    Args:
        score (float): Data Trust Score (0-1)

    Returns:
        str: Category label
    """
    if score >= 0.95:
        return "Excellent"
    elif score >= 0.80:
        return "Good"
    elif score >= 0.60:
        return "Fair"
    else:
        return "Poor"
