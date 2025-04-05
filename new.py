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
            results.append(CodeExecutionResult(case=case,user_code=code, status=0, error= None, data= result_data))

        except Exception as e:
            print("Exception occurred")
            results.append(CodeExecutionResult(case= case, status = 1, error=e, data= None))
    return results


if __name__ == "__main__":
    user_python_code = """
class Solution(object):
    def rotate(self, nums, k):
        print("k xa khabar")
        test=[1,2,3,4,5]
        print(f"ouch : {test}")
        return [1,2,4,5]
"""

    test_cases = [
        {"input":[ [1,2,4,5,8,9,12],2], "expected_output": [1,2,3,4,5]},
        {"input":[ [3,5,4,5,8,9,12],2], "expected_output": [12,9,8,5,4,5,3]},
        {"input": [[10,15,4,5,8,9,12],5], "expected_output": [12,9,8,5,4,15,10]},
    ]

    results = execute( Language("python", "3.12.0"),"rotate" , user_python_code, test_cases)
    print(len(results))


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