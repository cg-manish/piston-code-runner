from flask import Flask, request, jsonify
import json
import requests
from execute import execute_code
from models.models import Language
import base64

app = Flask(__name__)

@app.route('/health-check', methods=["GET"])
def health_check():
    return jsonify({"status": "success", "status_code": 200, "result": "Pong"})

@app.route('/execute', methods=['POST'])
def execute():

    try:
        data = request.get_json()
        user_submitted_code = data.get("user_submitted_code")
        test_cases = data.get("test_cases")
        function_name = data.get("function_name")
        language = data.get("language") 
        
        if not all([ user_submitted_code, test_cases, function_name, language]):
            return jsonify({"status": "error", "message": "Missing required fields", "sent_field":[]}), 400
        
        results=execute_code(function_name=function_name, 
                            code= user_submitted_code, 
                            test_cases=test_cases,
                            language=Language(name=language["name"],version=language["version"] )
                            )
        print(results)
        results_dict = [r.to_dict() for r in results]

        json_data = json.dumps(results_dict)
        return json.dumps({"data":results_dict, "status_code":200})
    except Exception as e:
        # print(str(e))
        return {"error":str(e)}



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=7000)