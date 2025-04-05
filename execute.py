import os
from typing import List
import requests
from models.models import Language, CodeExecutionResult
from utils.code_wrapper import *

PISTON_URL = "http://localhost:2000/api/v2/execute"

def validate_function_in_code(function_name: str, user_code: str, language: str):
    if language.name.lower() == "python":
        return function_name in user_code
    elif language.name.lower() == "csharp":
        return function_name in user_code
    return False


def execute_code(language: Language, function_name: str, code: str, test_cases: list)-> List[CodeExecutionResult]:
    # if not validate_function_in_code(function_name, code, language):
    #     return [{"error": f"Function '{function_name}' not found in submitted code."}]
    
    results=[]

    # print(code)

    for idx, case in enumerate(test_cases):
        args = case["input"]
        exec_code = wrap_code_runner(language, code, function_name, args)
        print(exec_code)    

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
            results.append(CodeExecutionResult(case=case, status=0, error= None, data= result_data))
        except Exception as e:
            print(e)
            results.append(CodeExecutionResult(case= case, status = 1, error=e, data= None))
    return results

souce_code_example='''
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        if len(nums)==2:
            return [0,1]
        else:
            return [3,45]
'''

test_payload={
        "question_id":123,
        "user_id":12,
        "test_cases": [{"input":[[2,7,11,15],9], "expected_output": [0,1]}],
        "function_name":"twoSum",
        "language":{"name":"python", "version":"3.12.0"},
        #  'user_submitted_code': source_code.encode('utf-8').decode('utf-8') 
        }


# res=execute_code(function_name="twoSum", 
#                             code= souce_code_example, 
#                             test_cases=test_payload["test_cases"],
#                             language=Language(name="python",version='3.12.0' )
#                             )
# print(res)


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