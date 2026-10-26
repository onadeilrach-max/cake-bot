import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

# Mga gusto nga models (unahon ang una, kung wala mo-adto sa sunod)
PREFERRED = [
    os.environ.get("GROQ_MODEL", ""),
    "llama-3.3-70b-versatile",
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
    "llama-3.1-8b-instant",
]

SYSTEM_PROMPT = (
    "Ikaw ang Cake Bot, usa ka mabination nga assistant sa cake shop. "
    "Tubaga ang mga pangutana bahin sa cakes, presyo, ug orders. "
    "Mubo ug klaro ang tubag. Bisaya ang default nga pinulongan."
)

_working_model = None

def get_candidates():
    """Preferred models nga naa gyud sa imong account, dayon ang uban."""
    try:
        available = [m.id for m in client.models.list().data]
    except Exception:
        return [m for m in PREFERRED if m]
    skip = ("whisper", "tts", "guard", "embed", "orpheus", "prompt-guard")
    chat_models = [m for m in available if not any(s in m.lower() for s in skip)]
    ordered = [m for m in PREFERRED if m in chat_models]
    ordered += [m for m in chat_models if m not in ordered]
    return ordered

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    global _working_model
    data = request.get_json(silent=True) or {}
    history = data.get("history", [])

    clean = []
    for m in history[-10:]:
        if m.get("role") in ("user", "assistant") and isinstance(m.get("content"), str):
            clean.append({"role": m["role"], "content": m["content"][:2000]})

    if not clean or clean[-1]["role"] != "user":
        return jsonify({"reply": "Palihog ibutang ang imong mensahe."}), 400

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + clean
    candidates = [_working_model] if _working_model else get_candidates()
    last_err = None

    for model in candidates[:6]:
        try:
            resp = client.chat.completions.create(model=model, messages=messages)
            _working_model = model
            return jsonify({"reply": resp.choices[0].message.content})
        except Exception as e:
            last_err = e
            msg = str(e)
            # Model problem ra ang i-skip; ang uban nga error i-show dayon
            if "model_not_found" in msg or "decommissioned" in msg or "404" in msg:
                _working_model = None
                continue
            return jsonify({"reply": f"Error: {e}"}), 500

    return jsonify({"reply": f"Walay model nga mogana. Last error: {last_err}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
