import json
from typing import List
import requests



PISTON_URL = "http://localhost:2000/api/v2/execute"
CODE_RUNNER_LOCAL_URL="http://localhost:7000/execute"

java_code="""
class Solution {
    public int[] twoSum(int[] nums, int target) {
        int[] result= {5,6};
        return result;
        
    }
}
"""

java_code="""
class Solution {
    public int[] twoSum(int[] nums, int target) {
        int[] result= {5,6};
        return result;
        
    }
}
"""

csarp_code="""
public class Solution {
    public int[] TwoSum(int[] nums, int target) {
        for (int i = 0; i < nums.Length; i++) {
            for (int j = i + 1; j < nums.Length; j++) {
                if (nums[i] + nums[j] == target) {
                    return new int[]{i, j}; 
                }
            }
        }
        return new int[0]; 
    }
}
"""

def test_execute():
        

        payload={
"language":"java", "version":"15.0.2",
"files":[
    {"name":"main", "content": generate_java_code([[2,7,11,15],9])}
]
        }

        print(payload)

        try:
            result= requests.post(PISTON_URL, json=payload, 
                                headers={"Content-Type": "application/json"})
            print(result.json())
            if result.json():
                with open("./result.json" , "w") as aaa:
                    aaa.writelines(result.json()["data"])
        except Exception as e:
             print(e)




def test_run_local():
        
        payload={
        "question_id":123,
        "user_id":12,
        "test_cases": [
        {"input":[[2,7,11,15],9], "expected_output": [0,1]}
        ],
        "function_name":"TwoSum",
        "language":{"name":"csharp.net", "version":"5.0.201"},
         "user_submitted_code": csarp_code
        }

        try:
            result= requests.post(CODE_RUNNER_LOCAL_URL, json=payload, 
                                headers={"Content-Type": "application/json"})
            print(result.json())
            # if result.json():
            #     with open("./result.json" , "w") as aaa:
            #         aaa.writelines(result.json()["data"])
        except Exception as e:
             print(e)

test_run_local()
# test_execute()