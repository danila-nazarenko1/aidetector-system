from llm_client import LLMClient
from llm_output_parser import parse_files
from ai_detector import detect_from_code


def run_pipeline(task: str, student_code: str) -> dict:

    report = {}


    client = LLMClient(task)

    openrouter = client.get_openrouter_responses()
    gemini = client.get_gemini_responses()

    all_generated = {
        **openrouter,
        **gemini
    }

    reference_code = {}

    for model, raw in all_generated.items():
        parsed = parse_files(raw)

        reference_code[model] = [
            {
                "filename": f["filename"],
                "code": f["code"]
            }
            for f in parsed
        ]


    detection = detect_from_code(student_code)


    report["task"] = task

    report["student_analysis"] = detection

    report["reference_generation"] = reference_code

    return report
