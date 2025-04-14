import json
from typing import List
import requests



PISTON_URL = "http://localhost:2000/api/v2/execute"


def test_execute():
        
        source_code="""
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        if len(nums)==2:
            return [0,1]
        else:
            return [3,45]

""" 
        java_code="""
class Solution {
    public int[] twoSum(int[] nums, int target) {
        int[] result= {5,6};
        return result;
        
    }
}
"""

        payload={
"language":"java", "version":"15.0.2",
"files":[
    {"name":"main", "content": generate_java_code([[2,7,11,15],9])}
]
        }
        try:
            result= requests.post(PISTON_URL, json=payload, 
                                headers={"Content-Type": "application/json"})
            print(result.json())
            if result.json():
                with open("./result.json" , "w") as aaa:
                    aaa.writelines(result.json()["data"])
        except Exception as e:
             print(e)




def convert_to_java_literal(value):
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
            inner = ",".join("{" + convert_to_java_literal(x) + "}" for x in value)
            return "new int[][]{" + inner + "}"
        elif all(isinstance(x, str) and len(x) == 1 for x in value):
            return "new char[]{" + ",".join("'" + x + "'" for x in value) + "}"
        else:
            return "new int[]{" + ",".join(convert_to_java_literal(x) for x in value) + "}"
    else:
        raise TypeError(f"Unsupported type: {type(value)}")


def generate_java_code(test_case: List):

    # for example: for two_sum: [ [2,3,5,9,11,7], 9]
    # input array = [2,3,5,9,11,7], target = 9

    java_code="""
    class Solution {
        public int[] twoSum(int[] nums, int target) {
            int[] result= {5,6};
            return result;
        }
    }
    """


    template_code="""
public class Main{
    public static void main(String[] args){
        Solution solution = new Solution();
        solution.twoSum(<<ARGS>>);
        System.out.println(java.util.Arrays.toString(result));
    }
}


"""
    java_args = ", ".join(convert_to_java_literal(arg) for arg in test_case)

    template_code= template_code.replace("<<ARGS>>", java_args)
    final_code= f"{java_code}\n\n {template_code}"

    print(final_code)

# generate_java_code([[1,3,56,6,7], 5])

test_execute()