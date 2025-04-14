import os
from typing import List
import requests
from models.models import  Language, CodeExecutionResult
from utils.code_wrapper import *

PISTON_URL = "http://localhost:2000/api/v2/execute"

def validate_function_in_code(function_name: str, user_code: str, language: str):
    if language.name.lower() == "python":
        return function_name in user_code
    elif language.name.lower() == "csharp":
        return function_name in user_code
    elif language.name.lower()=="java":
        return function_name in user_code
    return False


def execute_code(language: Language, function_name: str, code: str, test_cases: list)-> List[CodeExecutionResult]:
    if not validate_function_in_code(function_name, code, language):
        return [{"error": f"Function '{function_name}' not found in submitted code."}]
    
    results=[]

    # print(code)

    for idx, case in enumerate(test_cases):
        args = case["input"]
        exec_code = wrap_code_runner(language, code, function_name, args)
        
        print("Code to execute:\n")
        print(exec_code)    

        payload = {
            "language": language.name.lower(),
            "version": language.version,
            "files": [
                {"name": "main", "content": exec_code}
                ],
        }

        print(payload)
        try:
            response = requests.post(PISTON_URL, json=payload)

            response.raise_for_status()
            response_json=response.json()
            # result_data = json.loads(response_json)
            print(response_json.get("run",{}))

            results.append(CodeExecutionResult(case=case,  status=0, error= None, data= response_json))

        except Exception as e:
            print("Code execution error")
            print(e)
            results.append(CodeExecutionResult(case= case, status = 1, error=e, data= None))
    return results

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