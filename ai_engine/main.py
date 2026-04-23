"""AI Engine main entry point for testing the resume analyzer."""
from model.predictor import analyze_resume


def main() -> None:
    """Run a test analysis on a sample resume."""
    with open("resumes/resume1.txt", "r", encoding="utf-8") as f:
        text = f.read()

    result = analyze_resume(text)
    print(result)


if __name__ == "__main__":
    main()

