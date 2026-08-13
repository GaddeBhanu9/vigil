
import os
from dotenv import load_dotenv

import great_expectations as gx
from great_expectations.expectations import (
    ExpectColumnValuesToNotBeNull,
    ExpectColumnValuesToBeBetween,
    ExpectColumnValuesToBeUnique,
    ExpectColumnValuesToMatchRegex,
)

load_dotenv()


def run_validation():
    
    print(" PROJECT VIGIL - GREAT EXPECTATIONS VALIDATION")
    print("=" * 60)

    context = gx.get_context(mode="ephemeral")

    connection_string = os.getenv("DATABASE_URL")
    if not connection_string:
        raise ValueError("DATABASE_URL not found in .env file")

    datasource = context.data_sources.add_postgres(
        name="neon_datasource",
        connection_string=connection_string,
    )

    asset = datasource.add_table_asset(
        name="customers_asset",
        table_name="customers",
    )

    print(" Fetching data from Neon...")
    batch_request = asset.build_batch_request()
    print(" Batch request created successfully")

    suite = context.suites.add(
        gx.ExpectationSuite(name="customer_quality_suite")
    )

    # Expectations
    suite.add_expectation(ExpectColumnValuesToBeUnique(column="CustomerID"))
    suite.add_expectation(ExpectColumnValuesToBeBetween(column="Age", min_value=18, max_value=100))
    suite.add_expectation(ExpectColumnValuesToNotBeNull(column="email"))
    suite.add_expectation(ExpectColumnValuesToMatchRegex(column="email", regex=r".*@.*"))
    suite.add_expectation(ExpectColumnValuesToBeBetween(column="purchase_amount", min_value=0, max_value=None))

    print(f" Created {len(suite.expectations)} validation rules")

    print("\n Running validation...")
    validator = context.get_validator(
        batch_request=batch_request,
        expectation_suite=suite
    )
    validation_result = validator.validate()

    stats = validation_result["statistics"]


    print(" VALIDATION RESULTS")
    print(f" Passed Expectations: {stats['successful_expectations']}")
    print(f" Failed Expectations: {stats['unsuccessful_expectations']}")
    print(f" Total Expectations: {stats['evaluated_expectations']}")
    print(f" Success Rate: {stats['success_percent']:.2f}%")

    print("\n Detailed Results:")
    for result in validation_result["results"]:
        config = result.get("expectation_config", {})
        #  FIX: Use 'type' (GX 1.0+) or fallback to 'expectation_type'
        expectation_name = config.get("type") or config.get("expectation_type") or "Unknown Expectation"
        status = " PASS" if result["success"] else " FAIL"
        print(f"   {status}: {expectation_name}")

    return validation_result


if __name__ == "__main__":
    run_validation()