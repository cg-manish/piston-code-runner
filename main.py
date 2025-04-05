import requests
import json

PISTON_URL = "http://localhost:3000/api/v2/execute"

class Language:
    def __init__(self, name:str, version:str):
        self.version = version
        self.name=name

def execute(language: Language, code: str, test_cases: list):
    """
    Execute user-submitted code against test cases using Piston executor.

    :param language: Programming language (e.g., "python", "csharp")
    :param code: Code submitted by the user
    :param test_cases: List of dictionaries with `input` and `expected_output`
    :return: List of test results
    """
    results = []

    for idx, case in enumerate(test_cases):
        user_input = case["input"]
        expected_output = case["expected_output"]

        # Wrap Python code with execution block
        if language.lower() == "python":
            exec_code = code + f"""
if __name__ == "__main__":
    sol = Solution()
    result = sol.rotate({user_input})
    print(result)
"""
        elif language.lower() == "csharp":
            exec_code = wrap_csharp_runner(code, user_input)
        else:
            return [{"error": f"Unsupported language: {language}"}]

        print(exec_code)
        
        # Send to piston API
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

            if 'run' in result_data:
                stdout = result_data['run'].get('stdout', '').strip()
                stderr = result_data['run'].get('stderr', '').strip()

                if stderr:
                    results.append({
                        "test_case": idx + 1,
                        "status": "error",
                        "error": stderr
                    })
                else:
                    try:
                        output = json.loads(stdout) if stdout.startswith("[") else eval(stdout)
                    except:
                        output = stdout
                    passed = output == expected_output
                    results.append({
                        "test_case": idx + 1,
                        "status": "passed" if passed else "failed",
                        "expected": expected_output,
                        "actual": output,
                    })
            else:
                results.append({
                    "test_case": idx + 1,
                    "status": "error",
                    "error": "Unexpected Piston response"
                })

        except Exception as e:
            results.append({
                "test_case": idx + 1,
                "status": "error",
                "error": str(e)
            })

    return results


def wrap_csharp_runner(user_code: str, input_list: list):
    """
    Wraps user C# code inside a Program.cs-style runner for testing.
    """
    input_str = ", ".join(map(str, input_list))
    return f"""
using System;
using System.Collections.Generic;

{user_code}

class Program {{
    static void Main(string[] args) {{
        var sol = new Solution();
        var nums = new List<int>{{ {input_str} }};
        var result = sol.Rotate(nums, 3); // You can set k=3 or extract it from args
        Console.WriteLine(string.Join(",", result));
    }}
}}
"""

# Example usage
if __name__ == "__main__":
    user_python_code = """
class Solution(object):
    def rotate(self, nums, k):
        return [1,2,4,5]
"""

    test_cases = [
        {"input": [1,2,4,5,8,9,12], "expected_output": [12,9,8,5,4,2]},
        # {"input": [3,5,4,5,8,9,12], "expected_output": [12,9,8,5,4,5,3]},
        # {"input": [10,15,4,5,8,9,12], "expected_output": [12,9,8,5,4,15,10]},
    ]

    results = execute( Language("python", "3.12.0"), user_python_code, test_cases)

    for r in results:
        print(json.dumps(r, indent=2))
