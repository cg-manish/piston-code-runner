import requests
import json
from models.models import Language, CodeExecutionResult
from utils.code_wrapper import *

PISTON_URL = "http://localhost:2000/api/v2/execute"

def validate_function_in_code(function_name: str, user_code: str, language: str):
    if language.name.lower() == "python":
        return f"def {function_name}" in user_code or f"self.{function_name}" in user_code
    elif language.name.lower() == "csharp":
        return function_name in user_code
    return False


def execute(language: Language, function_name: str, code: str, test_cases: list):
    if not validate_function_in_code(function_name, code, language):
        return [{"error": f"Function '{function_name}' not found in submitted code."}]
    
    results=[]

    for idx, case in enumerate(test_cases):
        args = case["input"]
        exec_code = wrap_code_runner(language, code, function_name, args)
        payload = {
            "language": language.name.lower(),
            "version": language.version,
            "files": [
                {"name": "main", "content": exec_code}
                ],
            "stdin": "",
            "compile_timeout": 10000,
            "run_timeout": 3000,
            "compile_cpu_time": 10000,
            "run_cpu_time": 3000,
            "compile_memory_limit": -1,
            "run_memory_limit": -1
        }
        try:
            response = requests.post(PISTON_URL, json=payload)

            response.raise_for_status()
            result_data = response.json()
            run_info=   print(result_data.get("run",{}))
            print(result_data)
            results.append(CodeExecutionResult(case=case, status=0, error= None, data= result_data))

        except Exception as e:
            print("Exception occurred")
            results.append(CodeExecutionResult(case= case, status = 1, error=e, data= None))
    return results


def entrypoint():

    test_cases = [
        {"input":[[2,7,11,15],9], "expected_output": [1,2,3,4,5]},
        {"input":[ [3,2,4],6], "expected_output": [12,9,8,5,4,5,3]},
        {"input": [[3,3],6], "expected_output": [12,9,8,5,4,15,10]},
    ]

    execution_results = execute( Language("python", "3.12.0"),"rotate" , user_code, test_cases)
    
    if execution_results:
        single=  execution_results[0]
        stdout= single["run"]["stdout"] if  single["run"]["stderr"] == '' else ""

        if stdout:
            parse_returned_from_stdout()

    print(len(execution_results))


if __name__ == "__main__":
    entrypoint()





""" Data expected by code executor: 
1. problem id
2. function name
3. Test cases and each test case's expected output
4. user_submitted_code

Optional:
- max run duration
- max memory
- max cpu
"""