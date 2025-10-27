from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Load your OpenAI key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def home():
    return "Omnidim AI server running!"

# The main endpoint Omnidim will call
@app.route('/ask', methods=['POST'])
def ask_ai():
    try:
        data = request.get_json()
        prompt = data.get("prompt", "Hello")

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        return jsonify({
            "response": response.choices[0].message.content
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
