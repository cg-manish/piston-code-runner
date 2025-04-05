from flask import Flask, request, jsonify
import json
import requests
from execute import execute_code
from models.models import Language
app = Flask(__name__)

@app.route('/health-check', methods=["GET"])
def health_check():
    return jsonify({"status": "success", "status_code": 200, "result": "Pong"})

@app.route('/execute', methods=['POST'])
def execute():

    data = request.get_json()

    question_id = data.get("question_id")
    user_id = data.get("user_id")
    user_submitted_code = data.get("user_submitted_code")
    test_cases = data.get("test_cases")
    function_name = data.get("function_name")
    language = data.get("language") 
    
    if not all([question_id, user_id, user_submitted_code, test_cases, function_name, language]):
        return jsonify({"status": "error", "message": "Missing required fields"}), 400
    
    return execute_code(function_name=function_name, 
                        code= user_submitted_code, 
                        test_cases=test_cases,
                         language=Language(name=language["name"],version=language["version"] )
                         )


if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0")