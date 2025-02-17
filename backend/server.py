import os
import json
from flask import Flask, jsonify, request
import openai

app = Flask(__name__)

# Set your OpenAI API key here or via an environment variable.
openai.api_key = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY")

@app.route('/gigs', methods=['GET'])
def get_gigs():
    # Reads gigs from gigs.json and returns them.
    with open('backend/gigs.json') as f:
        gigs = json.load(f)
    return jsonify(gigs)

@app.route('/fulfill_order', methods=['POST'])
def fulfill_order():
    # Receives an order and uses OpenAI to generate service output.
    data = request.get_json()
    gig_type = data.get("gig_type", "service")
    prompt_text = data.get("prompt", f"Generate a high-quality {gig_type} service output.")

    try:
        # Using GPT-4 (or GPT-3.5) via ChatCompletion API
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"You are an expert in providing {gig_type} services."},
                {"role": "user", "content": prompt_text}
            ],
            temperature=0.7,
            max_tokens=300
        )
        result = response.choices[0].message['content'].strip()
        return jsonify({"status": "success", "output": result})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
