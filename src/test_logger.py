"""
Quick test to see structured logging in action.
"""

from src.utils import calculate_trust_score, classify_trust_score


def main():
    print("\n" + "=" * 60)
    print("Testing Project VIGIL with Structured Logging")
    print("=" * 60 + "\n")

    # Test 1: Normal calculation
    score = calculate_trust_score(0.8, 0.9, 0.7, 1.0)
    category = classify_trust_score(score)

    print(f"\n📊 Result: Score = {score}, Category = {category}")

    # Test 2: Edge case (invalid input - this will raise an error)
    print("\n" + "=" * 60)
    print("Testing invalid input (this will trigger an error log)...")
    print("=" * 60 + "\n")

    try:
        calculate_trust_score(1.5, 0.8, 0.6, 0.9)
    except ValueError as e:
        print(f"\n✅ Error caught as expected: {e}")


if __name__ == "__main__":
    main()
