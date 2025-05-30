import json
from ntpath import join
import os
import random
from models.models import Language


def wrap_code_runner(language: Language, user_code: str, function_name: str, args: list) -> str:
    print(f"Language is: {language.name}")
    
    lang= language.name.lower()

    if lang == "python":
        return wrap_python_code_runner(user_code, function_name, args)
    elif lang == "csharp.net":
        return wrap_csharp_code_runner(user_code, function_name, args)
    elif lang =="java":
        return wrap_java_code_runner(user_code, function_name, args)
    elif lang=="c++":
        return wrap_cpp_runner(user_code, function_name, args)
    elif lang=="javascript":
        return wrap_js_runner(user_code, function_name, args)
    else:
        return None

def convert_to_javascript_literal(value):
    """
    Recursively converts Python object to a valid JavaScript literal string.
    Supports: int, str, bool, list (arrays), and nested lists.
    """
    if isinstance(value, str):
        return f'"{value}"'
    elif isinstance(value, bool):
        return "true" if value else "false"
    elif isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, list):
        return "[" + ", ".join(convert_to_javascript_literal(item) for item in value) + "]"
    else:
        raise TypeError(f"Unsupported type: {type(value)}")

def wrap_js_runner(user_code:str, function_name:str, args:list)->str:
        js_args = ", ".join(convert_to_javascript_literal(arg) for arg in args)
        template_code="""
const sol = new Solution();
console.log(sol.<<FUNCTION_NAME>>(<<ARGS>>));
"""
        template_code= template_code.replace("<<FUNCTION_NAME>>",function_name)
        template_code= template_code.replace("<<ARGS>>", js_args)

        final_code= f"{user_code} \n\n {template_code}"
        
        return final_code

def wrap_cpp_runner(user_code:str, function_name:str, args:list)->str:
    cplusplus_args = ", ".join(convert_to_cplusplus_literal(arg) for arg in args)

    headers_code="""
    #include <iostream>
    #include <vector>
    using namespace std;
"""
    template_code = """
    int main() {
        Solution solution;
        vector<int> result = solution.<<FUNCTION_NAME>>(<<ARGS>>);
        for (int num : result) {
            cout << num << " ";
        }
        return 0;
    }
    """
    template_code= template_code.replace("<<FUNCTION_NAME>>", function_name)
    template_code= template_code.replace("<<ARGS>>", cplusplus_args)

    final_code= f" {headers_code}\n{user_code}\n\n{template_code} \n\n"
    return final_code



def convert_to_cplusplus_literal(value):
    """
    Recursively converts Python object to C++ literal string.
    Supports: int, str, bool, list (arrays), and nested lists.
    """
    if isinstance(value, str):
        return f'"{value}"'
    elif isinstance(value, bool):
        return "true" if value else "false"
    elif isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, list):
        # Handle lists of lists (for multi-dimensional arrays)
        if all(isinstance(x, list) for x in value):
            inner = ",".join("{" + convert_to_cplusplus_literal(x) + "}" for x in value)
            return f"{{{inner}}}"
        # Handle char arrays
        elif all(isinstance(x, str) and len(x) == 1 for x in value):
            return f"{{" + ",".join(f"'{x}'" for x in value) + "}}"
        else:
            return "{" + ",".join(convert_to_cplusplus_literal(x) for x in value) + "}"
    else:
        raise TypeError(f"Unsupported type: {type(value)}")

# Python wrapper
def wrap_python_code_runner(user_code: str, function_name: str, args: list) -> str:
    args_str = json.dumps(args)[1:-1]
    return f"""
from typing import List
{user_code}

if __name__ == "__main__":
    sol = Solution()
    result = sol.{function_name}({args_str})
    print(result)
"""

def convert_to_csharp_literal(value):
    """
    Recursively converts Python object to C# literal string.
    Supports: int, str, bool, list (arrays), and nested lists.
    """
    if isinstance(value, str):
        return f'"{value}"'
    elif isinstance(value, bool):
        return "true" if value else "false"
    elif isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, list):
        # Handle lists of lists (for multi-dimensional arrays)
        if all(isinstance(x, list) for x in value):
            inner = ",".join("{" + convert_to_csharp_literal(x) + "}" for x in value)
            return f"new int[,]{{{inner}}}"
        # Handle char arrays
        elif all(isinstance(x, str) and len(x) == 1 for x in value):
            return f"new char[]{{" + ",".join(f"'{x}'" for x in value) + "}"
        else:
            return "new int[]{" + ",".join(convert_to_csharp_literal(x) for x in value) + "}"
    else:
        raise TypeError(f"Unsupported type: {type(value)}")
    
# C# Wrapper
def wrap_csharp_code_runner(user_code: str, function_name: str, args: list) -> str:
    csharp_args = ", ".join(convert_to_csharp_literal(arg) for arg in args)

    template_code="""
using System;
using System.Collections.Generic;

class Program {
    static void Main(string[] args) {
        var sol = new Solution();
        var result = sol.<<FUNCTION_NAME>>(<<ARGS>>);
        Console.WriteLine(string.Join(",", result));
    }
}
"""
    template_code= template_code.replace("<<ARGS>>", csharp_args)
    template_code= template_code.replace("<<FUNCTION_NAME>>", function_name)
    final_code=f"{template_code} \n\n{user_code}"
    return final_code

def _convert_to_java_literal(value):
    """
    Recursively converts Python object to Java literal string.
    Supports: int, str, list, nested lists, etc.
    """
    if isinstance(value, str):
        return f'"{value}"'
    elif isinstance(value, bool):
        return "true" if value else "false"
    elif isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, list):
        # Determine if it's a list of lists (for arrays)
        if all(isinstance(x, list) for x in value):
            inner = ",".join("{" + _convert_to_java_literal(x) + "}" for x in value)
            return "new int[][]{" + inner + "}"
        elif all(isinstance(x, str) and len(x) == 1 for x in value):
            return "new char[]{" + ",".join("'" + x + "'" for x in value) + "}"
        else:
            return "new int[]{" + ",".join(_convert_to_java_literal(x) for x in value) + "}"
    else:
        raise TypeError(f"Unsupported type: {type(value)}")

# Java Wrapper
def wrap_java_code_runner(user_code: str, function_name: str, args: list) -> str:
    java_args = ", ".join(_convert_to_java_literal(arg) for arg in args)

    template_code= """
public class Program {

    public static void main(String[] args){
        Solution solution = new Solution();
        var result=solution.<<FUNCTION_NAME>>(<<ARGS>>);
        System.out.println(java.util.Arrays.toString(result));
    }
}"""
    template_code= template_code.replace("<<ARGS>>", java_args)
    template_code= template_code.replace("<<FUNCTION_NAME>>", function_name)
    final_code=f"{template_code} \n\n{user_code}"

    return final_code


def convert_to_cplusplus_literal(value):
    """
    Recursively converts Python object to C++ literal string.
    Supports: int, str, bool, list (arrays), and nested lists.
    """
    if isinstance(value, str):
        return f'"{value}"'
    elif isinstance(value, bool):
        return "true" if value else "false"
    elif isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, list):
        # Handle lists of lists (for multi-dimensional arrays)
        if all(isinstance(x, list) for x in value):
            inner = ",".join("{" + convert_to_cplusplus_literal(x) + "}" for x in value)
            return f"{{{inner}}}"
        # Handle char arrays
        elif all(isinstance(x, str) and len(x) == 1 for x in value):
            return f"{{" + ",".join(f"'{x}'" for x in value) + "}}"
        else:
            return "{" + ",".join(convert_to_cplusplus_literal(x) for x in value) + "}"
    else:
        raise TypeError(f"Unsupported type: {type(value)}")




def parse_returned_from_stdout(stdout, output):
     data= input.split("\n")
     print(data[-2])

def get_random_sample_code():

    sample_files= os.listdir("./sample_user_codes")

    print(sample_files)

    file_name= sample_files[random.randint(0, len(sample_files)-1)]
    print(file_name)
    code_file=open("./sample_user_codes"+"/"+file_name, "r")
    print(code_file.read())

# get_random_sample_code()