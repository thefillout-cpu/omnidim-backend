from flask import Flask, request, jsonify
import openai
import requests
import os

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")
SERP_API_KEY = os.getenv("SERP_API_KEY")

@app.route("/omnidim", methods=["POST"])
def omnidim_webhook():
    data = request.json
    user_text = data.get("text", "")

    serp_result = ""
    if "search:" in user_text.lower():
        query = user_text.split("search:")[1]
        serp_url = f"https://serpapi.com/search.json?q={query}&api_key={SERP_API_KEY}"
        serp_data = requests.get(serp_url).json()
        if serp_data.get("organic_results"):
            serp_result = serp_data["organic_results"][0]["snippet"]

    completion = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful voice assistant."},
            {"role": "user", "content": f"{user_text}\n\n{serp_result}"}
        ]
    )

    reply = completion["choices"][0]["message"]["content"]
    return jsonify({"reply": reply})

@app.route("/")
def home():
    return "Omnidim AI server running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
