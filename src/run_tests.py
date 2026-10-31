
import subprocess
import sys


def main():
    print("\nRUNNING AUTOMATED DATA QUALITY TESTS")

    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-v"],
        check=False
    )

    if result.returncode == 0:
        print("\nALL AUTOMATED TESTS PASSED!")
        return 0

    print("\nAUTOMATED TESTS FAILED. STOPPING PIPELINE.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
