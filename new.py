import requests
import json

PISTON_URL = "http://localhost:2000/api/v2/execute"

class Language:
    def __init__(self, name:str, version:str):
        self.version = version
        self.name=name

def validate_function_in_code(function_name: str, user_code: str, language: str):
    if language.name.lower() == "python":
        return f"def {function_name}" in user_code or f"self.{function_name}" in user_code
    elif language.name.lower() == "csharp":
        return function_name in user_code  # Basic check for now
    return False



def execute(language: Language, function_name: str, code: str, test_cases: list):
    if not validate_function_in_code(function_name, code, language):
        return [{"error": f"Function '{function_name}' not found in submitted code."}]

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
            print(run_info)
            return run_info
        except Exception as e:
            print("Exception occurred")
            return e



def wrap_code_runner(language: str, user_code: str, function_name: str, args: list) -> str:
    if language.name.lower() == "python":
        return wrap_python_code_runner(user_code, function_name, args)
    elif language.name.lower() == "csharp":
        return wrap_csharp_code_runner(user_code, function_name, args)
    else:
        return None


def wrap_python_code_runner(user_code: str, function_name: str, args: list) -> str:
    args_str = json.dumps(args)[1:-1]
    return f"""{user_code}

if __name__ == "__main__":
    sol = Solution()
    result = sol.{function_name}({args_str})
    print(result)
"""


def wrap_csharp_code_runner(user_code: str, function_name: str, args: list) -> str:
    args_formatted = ", ".join(map(str, args))
    return f"""
using System;
using System.Collections.Generic;

{user_code}

class Program {{
    static void Main(string[] args) {{
        var sol = new Solution();
        var result = sol.{function_name}(new List<int>{{ {args_formatted} }}, 3);
        Console.WriteLine(string.Join(",", result));
    }}
}}
"""





# Example usage
if __name__ == "__main__":
    user_python_code = """
class Solution(object):
    def rotate(self, nums, k):
        print("k xa khabar")
        test=[1,2,3,4,5]
        print(f"jai shri ram: {test}")
        return [1,2,4,5]
"""

    test_cases = [
        {"input":[ [1,2,4,5,8,9,12],2], "expected_output": [1,2,3,4,5]},
        # {"input": [3,5,4,5,8,9,12], "expected_output": [12,9,8,5,4,5,3]},
        # {"input": [10,15,4,5,8,9,12], "expected_output": [12,9,8,5,4,15,10]},
    ]

    results = execute( Language("python", "3.12.0"),"rotate" , user_python_code, test_cases)


    # for r in results:
    #     print(json.dumps(r, indent=2))



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