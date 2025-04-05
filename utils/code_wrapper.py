import json
from ntpath import join
import os
import random

def wrap_code_runner(language: str, user_code: str, function_name: str, args: list) -> str:
    if language.name.lower() == "python":
        return wrap_python_code_runner(user_code, function_name, args)
    elif language.name.lower() == "csharp":
        return wrap_csharp_code_runner(user_code, function_name, args)
    else:
        return None

# Python wrapper
def wrap_python_code_runner(user_code: str, function_name: str, args: list) -> str:
    args_str = json.dumps(args)[1:-1]
    return f"""{user_code}

if __name__ == "__main__":
    sol = Solution()
    result = sol.{function_name}({args_str})
    print(result)
"""

# C# Wrapper
def wrap_csharp_code_runner(user_code: str, function_name: str, args: list) -> str:
    args_formatted = ", ".join(map(str, args))
    return f"""
using System;
using System.Collections.Generic;

{user_code}

class Program {{
    static void Main(string[] args) {{
        var sol = new Solution();
        var result = sol.{function_name}(new List<int>{{ {args_formatted} }});
        Console.WriteLine(string.Join(",", result));
    }}
}}
"""

# Java Wrapper
def wrap_java_code_runner(user_code: str, function_name: str, args: list) -> str:
    args_formatted = ", ".join(map(str, args))
    return f"""
public class Solution {{
    {user_code}

    public static void main(String[] args) {{
        Solution sol = new Solution();
        int[] arr = new int[]{{ {args_formatted} }};
        var result = sol.{function_name}(arr);
        System.out.println(result);
    }}
}}
"""

# Ruby Wrapper
def wrap_ruby_code_runner(user_code: str, function_name: str, args: list) -> str:
    args_formatted = ", ".join(map(str, args))
    return f"""
{user_code}

if __FILE__ == $0
  sol = Solution.new
  result = sol.{function_name}([ {args_formatted} ])
  puts result
end
"""

# Swift Wrapper
def wrap_swift_code_runner(user_code: str, function_name: str, args: list) -> str:
    args_formatted = ", ".join(map(str, args))
    return f"""
{user_code}

let sol = Solution()
let result = sol.{function_name}([ {args_formatted} ])
print(result)
"""

# Go Wrapper
def wrap_go_code_runner(user_code: str, function_name: str, args: list) -> str:
    args_formatted = ", ".join(map(str, args))
    return f"""
package main

import "fmt"

{user_code}

func main() {{
    sol := Solution{{}}
    result := sol.{function_name}([]int{{ {args_formatted} }})
    fmt.Println(result)
}}
"""

# Scala Wrapper
def wrap_scala_code_runner(user_code: str, function_name: str, args: list) -> str:
    args_formatted = ", ".join(map(str, args))
    return f"""
object Solution {{
    {user_code}

    def main(args: Array[String]): Unit = {{
        val sol = new Solution()
        val result = sol.{function_name}(Array({args_formatted}))
        println(result.mkString(","))
    }}
}}
"""

# Kotlin Wrapper
def wrap_kotlin_code_runner(user_code: str, function_name: str, args: list) -> str:
    args_formatted = ", ".join(map(str, args))
    return f"""
fun main() {{
    val sol = Solution()
    val result = sol.{function_name}(arrayOf({args_formatted}))
    println(result.joinToString(","))
}}

{user_code}
"""

# # Rust Wrapper
# def wrap_rust_code_runner(user_code: str, function_name: str, args: list) -> str:
#     args_formatted = ", ".join(map(str, args))
#     return f"""
# {user_code}

# fn main() {{
#     let sol = Solution::new();
#     let result = sol.{function_name}(vec![{args_formatted}]);
#      # TODO: Fix this line below for rust
#      # println!("{:?}", result);
# }}
# """

# C++ Wrapper
def wrap_cpp_code_runner(user_code: str, function_name: str, args: list) -> str:
    args_formatted = ", ".join(map(str, args))
    return f"""
#include <iostream>
#include <vector>
using namespace std;

{user_code}

int main() {{
    Solution sol;
    vector<int> args = {{{args_formatted}}};
    auto result = sol.{function_name}(args);
    for (const auto& elem : result) {{
        cout << elem << " ";
    }}
    cout << endl;
}}
"""

# C Wrapper
def wrap_c_code_runner(user_code: str, function_name: str, args: list) -> str:
    args_formatted = ", ".join(map(str, args))
    return f"""
#include <stdio.h>
#include <stdlib.h>

{user_code}

int main() {{
    int args[] = {{ {args_formatted} }};
    {function_name}(args, sizeof(args)/sizeof(args[0]));
    return 0;
}}
"""

# Dotnet (C#) Wrapper
def wrap_dotnet_code_runner(user_code: str, function_name: str, args: list) -> str:
    args_formatted = ", ".join(map(str, args))
    return f"""
using System;
using System.Collections.Generic;

{user_code}

class Program {{
    static void Main(string[] args) {{
        var sol = new Solution();
        var result = sol.{function_name}(new List<int>{{ {args_formatted} }});
        Console.WriteLine(string.Join(",", result));
    }}
}}
"""

# JavaScript Wrapper
def wrap_javascript_code_runner(user_code: str, function_name: str, args: list) -> str:
    args_formatted = ", ".join(map(str, args))
    return f"""
{user_code}

const sol = new Solution();
const result = sol.{function_name}([{args_formatted}]);
console.log(result);
"""

# TypeScript Wrapper
def wrap_typescript_code_runner(user_code: str, function_name: str, args: list) -> str:
    args_formatted = ", ".join(map(str, args))
    return f"""
{user_code}

const sol = new Solution();
const result = sol.{function_name}([{args_formatted}]);
console.log(result);
"""

# Bash Wrapper
def wrap_bash_code_runner(user_code: str, function_name: str, args: list) -> str:
    args_str = " ".join(map(str, args))
    return f"""
#!/bin/bash
{user_code}
{function_name} {args_str}
"""


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

get_random_sample_code()