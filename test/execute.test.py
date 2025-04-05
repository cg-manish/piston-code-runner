import json
import requests

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
        "question_id":123,
        "user_id":12,
        "test_cases": [{"input":[[2,7,11,15],9], 
                        "expected_output": [0,1]},
        {"input":[ [3,2,4],6], "expected_output":[1,2]},
        {"input": [[3,3],6], "expected_output": [0,1]}
        ],
        "function_name":"twoSum",
        "language":{"name":"java", "version":"15.0.2"},
         'user_submitted_code': java_code
        }
        try:
            result= requests.post("https://code-runner.macgain.net/execute", json=payload, 
                                headers={"Content-Type": "application/json"})
            print(result.json())
            if result.json():
                with open("./result.json" , "w") as aaa:
                    aaa.writelines(result.json()["data"])
        except Exception as e:
             print(e)

test_execute()