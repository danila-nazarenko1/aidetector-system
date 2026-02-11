import argparse
import json

from pipeline import run_pipeline


def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def main():

    parser = argparse.ArgumentParser(
        description="AI Detection + Reference Code Generator"
    )

    parser.add_argument(
        "--task",
        required=True,
        help="Path to task description file"
    )

    parser.add_argument(
        "--code",
        required=True,
        help="Path to student code file"
    )

    parser.add_argument(
        "--out",
        default="report.json",
        help="Output report file"
    )

    args = parser.parse_args()

    task_text = read_file(args.task)
    student_code = read_file(args.code)

    print("\n=== Running Analysis Pipeline ===\n")

    report = run_pipeline(task_text, student_code)

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"\nReport saved to {args.out}\n")


if __name__ == "__main__":
    main()
