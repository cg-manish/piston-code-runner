from flask import Flask, request, jsonify
import json
import requests
from execute import execute_code
from models.models import Language
import base64
from flask_cors import CORS

app = Flask(__name__)

CORS(app, origins=["http://localhost:3000", "https://wecanhack.com", "https://127.0.0.1:3000"])

@app.route('/health-check', methods=["GET"])
def health_check():
    return jsonify({"status": "success", "status_code": 200, "result": "Pong"})

@app.route('/execute', methods=['POST'])
def execute():

    try:
        data = request.get_json()

        question_id = data.get("question_id")
        user_id = data.get("user_id")
        user_submitted_code = data.get("user_submitted_code")
        test_cases = data.get("test_cases")
        function_name = data.get("function_name")
        language = data.get("language") 
        
        if not all([question_id, user_id, user_submitted_code, test_cases, function_name, language]):
            return jsonify({"status": "error", "message": "Missing required fields"}), 400
        
        results=execute_code(function_name=function_name, 
                            code= user_submitted_code, 
                            test_cases=test_cases,
                            language=Language(name=language["name"],version=language["version"] )
                            )
        print(results)
        results_dict = [r.to_dict() for r in results]

        json_data = json.dumps(results_dict, indent=1)

        return jsonify({"data":json_data, "status_code":200})
    except Exception as e:
        # print(str(e))
        return {"error":str(e)}



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8000)