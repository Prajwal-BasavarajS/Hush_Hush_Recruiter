import os
import json
import requests
import re
import time
import smtplib
import ssl
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from mysql.connector import pooling

# Load environment variables from the .env file
load_dotenv()

# Initialize the Flask application
app = Flask(__name__)
CORS(app)

# --- Database Connection Pool ---
try:
    db_pool = pooling.MySQLConnectionPool(
        pool_name="doodle_pool",
        pool_size=5,
        host=os.getenv('MYSQL_HOST'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DATABASE')
    )
    print("Database connection pool created successfully.")
except Exception as e:
    print(f"Error creating database connection pool: {e}")
    db_pool = None

# --- AI Evaluation Function ---
# UPDATED: This function now uses your more detailed and stricter prompt.
def evaluate_code_with_ai(submissions):
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("Gemini API key is missing.")
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
    prompt = f"""
        You are an expert code reviewer for a programming competition.

        *CRITICAL SCORING RULE:*
        If a submission does not make a genuine attempt to solve the specific problem described in the question title, it MUST receive a score of 0. Code that is completely irrelevant to the problem (e.g., printing a random string for a palindrome question) must be scored as 0. Partial credit should only be given to genuine, on-topic attempts.

        Analyze the following code submissions based on these six criteria:

        1. Correctness:
        - Does the code produce the expected output for all valid inputs?
        - Does it handle edge cases (empty input, invalid values, max limits)?

        2. Code Quality & Readability:
        - Is the code clean and readable (good naming, indentation, spacing)?
        - Does it follow standard style guides (e.g., PEP 8 for Python)?

        3. Efficiency & Performance:
        - What is the time and space complexity (Big O notation)?
        - Could the solution scale to large datasets?

        4. Robustness & Error Handling:
        - Does the code validate inputs and fail gracefully with unexpected data?
        
        5. Maintainability:
        - Is the code modular and broken into reusable functions/classes?

        6. Innovation / Problem-Solving Approach:
        - Is the solution clear and elegant, or a temporary workaround?

        Provide a score out of 100 for each submission and an overall average score.
        You MUST respond with only a valid JSON object, with no extra text or markdown.

        The submissions are:
        {json.dumps(submissions, indent=2)}

        Your JSON response must follow this exact structure, with a feedback key for each of the 6 criteria:
        {{
          "overallScore": <integer>,
          "evaluations": [
            {{
              "questionTitle": "<title>",
              "score": <integer>,
              "feedback": {{
                "correctness": "<brief analysis>",
                "quality": "<brief analysis>",
                "efficiency": "<brief analysis>",
                "robustness": "<brief analysis>",
                "maintainability": "<brief analysis>",
                "innovation": "<brief analysis>"
              }}
            }}
          ]
        }}
    """
    response = requests.post(api_url, json={"contents": [{"parts": [{"text": prompt}]}]})
    response.raise_for_status()
    json_text = response.json()['candidates'][0]['content']['parts'][0]['text']
    match = re.search(r'```json\s*([\s\S]*?)\s*```|([\s\S]*)', json_text)
    if match:
        cleaned_json_text = match.group(1) if match.group(1) else match.group(2)
        return json.loads(cleaned_json_text.strip())
    raise ValueError("Could not find a valid JSON object in the AI response.")

# --- API Endpoint for Candidate Submissions ---
@app.route("/submit", methods=["POST"])
def handle_submission():
    if not db_pool: return jsonify({"error": "Database is not configured correctly."}), 500
    data = request.get_json()
    if not all([data.get('candidateName'), data.get('candidateEmail'), data.get('submissions')]):
        return jsonify({"error": "Missing required data."}), 400
    connection = None
    try:
        evaluation_result = evaluate_code_with_ai(data.get('submissions'))
        connection = db_pool.get_connection()
        cursor = connection.cursor()
        sql = "INSERT INTO exam_results (candidate_name, candidate_email, score) VALUES (%s, %s, %s);"
        cursor.execute(sql, (data.get('candidateName'), data.get('candidateEmail'), evaluation_result.get('overallScore')))
        connection.commit()
        return jsonify({"message": "Submission successful!", "score": evaluation_result.get('overallScore')}), 200
    except Exception as e:
        return jsonify({"error": f"An internal server error occurred: {e}"}), 500
    finally:
        if connection and connection.is_connected(): connection.close()

# ===================================================================
# --- RECRUITING MANAGER PLATFORM CODE ---
# ===================================================================
MANAGER_USERNAME = "manager"
MANAGER_PASSWORD = "password123"

# FINAL WORKING VERSION: Uses SMTP_SSL on port 465.
def send_decision_email(recipient_email, candidate_name, decision):
    sender_email, password = os.getenv("SENDER_EMAIL"), os.getenv("SENDER_PASSWORD")
    if not all([sender_email, password]):
        print("Email credentials are not set in .env file."); return False
    
    subject = f"Update on Your Doodle Corp. Coding Challenge"
    if decision.lower() == 'accepted':
        subject = f"Congratulations on Your Doodle Corp. Coding Challenge!"
        body = f"Dear {candidate_name},\n\nWe are thrilled to inform you that you have successfully passed the coding assessment. A recruiter will be in touch with you shortly regarding the next steps.\n\nBest regards,\nThe Doodle Corp. Hiring Team"
    else:
        body = f"Dear {candidate_name},\n\nThank you for your interest in Doodle Corp. and for taking the time to complete our coding assessment. After careful review, we have decided not to move forward with your application at this time.\n\nWe wish you the best of luck in your job search.\n\nSincerely,\nThe Doodle Corp. Hiring Team"
    
    message = f"Subject: {subject}\n\n{body}"
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(os.getenv("SMTP_SERVER"), int(os.getenv("SMTP_PORT")), context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, recipient_email, message.encode('utf-8'))
        print(f"Email sent successfully to {recipient_email}"); return True
    except Exception as e:
        print(f"Error sending email: {e}"); return False

@app.route("/manager/login", methods=["POST"])
def manager_login():
    data = request.get_json()
    if data.get('username') == MANAGER_USERNAME and data.get('password') == MANAGER_PASSWORD:
        return jsonify({"message": "Login successful!"}), 200
    return jsonify({"error": "Invalid credentials."}), 401

@app.route("/manager/candidates", methods=["GET"])
def get_candidates():
    connection = db_pool.get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT id, candidate_name, candidate_email, score FROM exam_results ORDER BY id DESC")
    candidates = cursor.fetchall()
    cursor.close(); connection.close()
    return jsonify(candidates), 200

@app.route("/manager/decide", methods=["POST"])
def decide_candidate():
    data = request.get_json()
    if not all([data.get('decision'), data.get('name'), data.get('email')]):
        return jsonify({"error": "Missing required data."}), 400
    email_sent = send_decision_email(data.get('email'), data.get('name'), data.get('decision'))
    if email_sent:
        return jsonify({"message": f"Email sent for decision: {data.get('decision')}"}), 200
    return jsonify({"error": "Failed to send email."}), 500

if __name__ == "__main__":
    app.run(debug=True, port=3000)