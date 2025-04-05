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
        payload={
        "question_id":123,
        "user_id":12,
        "test_cases": [{"input":[[2,7,11,15],9], 
                        "expected_output": [0,1]},
        {"input":[ [3,2,4],6], "expected_output":[1,2]},
        {"input": [[3,3],6], "expected_output": [0,1]}
        ],
        "function_name":"twoSum",
        "language":{"name":"python", "version":"3.12.0"},
         'user_submitted_code': source_code
        }

        result= requests.post("https://code-runner.macgain.net/execute", json=payload, 
                              headers={"Content-Type": "application/json"})
        print(result.json()["data"])
        with open("./result.json" , "w") as aaa:
               aaa.writelines(result.json()["data"])

test_execute()