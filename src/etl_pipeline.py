
import subprocess
import sys
from pathlib import Path

from logger_config import get_logger


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = Path(__file__).resolve().parent

logger = get_logger("ETL_PIPELINE")

ETL_STAGES = [
    ("Generate Raw Data", "generate_sample_data.py"),
    ("Inspect Data Quality", "inspect_data.py"),
    ("Transform Data", "transform_data.py"),
    ("Run Automated Tests", "run_tests.py"),
    ("Load Data into PostgreSQL", "load_data.py"),
]


def run_stage(stage_name, script_name):
    """Execute an ETL stage and record its output."""

    script_path = SRC_DIR / script_name

    print("\n" + "=" * 60, flush=True)
    print(f"STARTING: {stage_name}", flush=True)
    print("=" * 60, flush=True)

    logger.info("Starting stage: %s", stage_name)

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True
    )

    if result.stdout:
        print(result.stdout, end="", flush=True)
        for line in result.stdout.splitlines():
            logger.info("[%s] %s", stage_name, line)

    if result.stderr:
        print(result.stderr, end="", file=sys.stderr, flush=True)
        for line in result.stderr.splitlines():
            logger.error("[%s] %s", stage_name, line)

    if result.returncode == 0:
        logger.info("Completed stage: %s", stage_name)
        print(f"\nCOMPLETED: {stage_name}", flush=True)
        return "SUCCESS"

    if result.returncode == 2 and script_name == "load_data.py":
        logger.warning("Database loading safely skipped.")
        print(
            "\nSKIPPED SAFELY: Database already contains records.",
            flush=True
        )
        return "SKIPPED"

    logger.error("Stage failed: %s", stage_name)
    raise RuntimeError(f"ETL failed during stage: {stage_name}")


def main():
    logger.info("E-Commerce ETL pipeline started.")
    print("\nE-COMMERCE ETL PIPELINE STARTED", flush=True)

    results = {}

    try:
        for stage_name, script_name in ETL_STAGES:
            results[stage_name] = run_stage(stage_name, script_name)

        print("\n" + "=" * 60)
        print("ETL PIPELINE EXECUTION SUMMARY")
        print("=" * 60)

        for stage_name, status in results.items():
            print(f"{stage_name}: {status}")

        if "SKIPPED" in results.values():
            print("\nETL PIPELINE COMPLETED WITH LOAD SKIPPED.")
            logger.warning("Pipeline completed with database loading skipped.")
        else:
            print("\nETL PIPELINE COMPLETED SUCCESSFULLY!")
            logger.info("Pipeline completed successfully.")

    except Exception:
        logger.exception("ETL pipeline failed.")
        print("\nETL PIPELINE FAILED!")
        sys.exit(1)


if __name__ == "__main__":
    main()
