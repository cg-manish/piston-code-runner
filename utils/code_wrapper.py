import json

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

def parse_returned_from_stdout(stdout, output):
     data= input.split("\n")
     print(data[-2])


input='k xa khabar\nouch : [1, 2, 3, 4, 5]\n[1, 2, 4, 5]\n'

parse_returned_from_stdout(input, input)