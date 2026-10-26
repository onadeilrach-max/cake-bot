import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

MODEL = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")

SYSTEM_PROMPT = (
    "Ikaw ang Cake Bot, usa ka mabination nga assistant sa cake shop. "
    "Tubaga ang mga pangutana bahin sa cakes, presyo, ug orders. "
    "Mubo ug klaro ang tubag. Bisaya ang default nga pinulongan."
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    history = data.get("history", [])

    # Limpyohi ang history: role user/assistant lang, ug last 10 ra
    clean = []
    for m in history[-10:]:
        if m.get("role") in ("user", "assistant") and isinstance(m.get("content"), str):
            clean.append({"role": m["role"], "content": m["content"][:2000]})

    if not clean or clean[-1]["role"] != "user":
        return jsonify({"reply": "Palihog ibutang ang imong mensahe."}), 400

    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + clean,
        )
        return jsonify({"reply": resp.choices[0].message.content})
    except Exception as e:
        return jsonify({"reply": f"Error: {e}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
