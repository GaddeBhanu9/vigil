"""
Unit tests for utility functions.
"""

import pytest

from src.utils import calculate_trust_score, classify_trust_score


def test_calculate_trust_score_perfect():
    """Test perfect data (all scores = 1.0)."""
    score = calculate_trust_score(completeness=1.0, accuracy=1.0, freshness=1.0, anomaly_score=1.0)
    assert score == 1.0


def test_calculate_trust_score_mixed():
    """Test mixed scores (50%, 80%, 60%, 90%)."""
    score = calculate_trust_score(completeness=0.5, accuracy=0.8, freshness=0.6, anomaly_score=0.9)
    # Expected: 0.5*0.3 + 0.8*0.4 + 0.6*0.2 + 0.9*0.1
    # = 0.15 + 0.32 + 0.12 + 0.09 = 0.68
    assert score == 0.68


def test_calculate_trust_score_zero():
    """Test all zeros."""
    score = calculate_trust_score(0.0, 0.0, 0.0, 0.0)
    assert score == 0.0


def test_calculate_trust_score_invalid_input():
    """Test that invalid input raises ValueError."""
    with pytest.raises(ValueError, match="All scores must be between 0 and 1"):
        calculate_trust_score(1.5, 0.8, 0.6, 0.9)


def test_calculate_trust_score_negative():
    """Test that negative input raises ValueError."""
    with pytest.raises(ValueError, match="All scores must be between 0 and 1"):
        calculate_trust_score(-0.1, 0.8, 0.6, 0.9)


def test_classify_trust_score_excellent():
    """Test classification for excellent score."""
    assert classify_trust_score(0.96) == "Excellent"
    assert classify_trust_score(0.99) == "Excellent"


def test_classify_trust_score_good():
    """Test classification for good score."""
    assert classify_trust_score(0.85) == "Good"
    assert classify_trust_score(0.80) == "Good"


def test_classify_trust_score_fair():
    """Test classification for fair score."""
    assert classify_trust_score(0.70) == "Fair"
    assert classify_trust_score(0.60) == "Fair"


def test_classify_trust_score_poor():
    """Test classification for poor score."""
    assert classify_trust_score(0.50) == "Poor"
    assert classify_trust_score(0.10) == "Poor"
