import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = Path(__file__).resolve().parent

ETL_STAGES = [
    ("Generate Raw Data", "generate_sample_data.py"),
    ("Inspect Data Quality", "inspect_data.py"),
    ("Transform Data", "transform_data.py"),
    ("Load Data into PostgreSQL", "load_data.py"),
]


def run_stage(stage_name, script_name):
    """Execute one ETL stage and return its status."""

    script_path = SRC_DIR / script_name

    print("\n" + "=" * 60, flush=True)
    print(f"STARTING: {stage_name}", flush=True)
    print("=" * 60, flush=True)

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=PROJECT_ROOT
    )

    if result.returncode == 0:
        print(f"\nCOMPLETED: {stage_name}", flush=True)
        return "SUCCESS"

    # Exit code 2 means database loading was safely skipped.
    if result.returncode == 2 and script_name == "load_data.py":
        print(
            "\nSKIPPED SAFELY: Database already contains records.",
            flush=True
        )
        return "SKIPPED"

    raise RuntimeError(
        f"ETL failed during stage: {stage_name}"
    )


def main():
    print("\nE-COMMERCE ETL PIPELINE STARTED", flush=True)

    results = {}

    try:
        for stage_name, script_name in ETL_STAGES:
            status = run_stage(stage_name, script_name)
            results[stage_name] = status

        print("\n" + "=" * 60)
        print("ETL PIPELINE EXECUTION SUMMARY")
        print("=" * 60)

        for stage_name, status in results.items():
            print(f"{stage_name}: {status}")

        if "SKIPPED" in results.values():
            print("\nETL PIPELINE COMPLETED WITH LOAD SKIPPED.")
            print("Existing database records were preserved.")
        else:
            print("\nETL PIPELINE COMPLETED SUCCESSFULLY!")

    except Exception as error:
        print("\nETL PIPELINE FAILED!")
        print(f"Error: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()