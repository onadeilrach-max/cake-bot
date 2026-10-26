import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ.get("OPENAI_API_KEY")
)

KNOWLEDGE_BASE = """
You are a helpful assistant for 'Sweet Moments Cake Shop'.
- Menu: 
    * Chocolate Cake: S(P400), M(P600), L(P800)
    * Ube Cake: S(P450), M(P650), L(P850)
    * Red Velvet: S(P500), M(P700), L(P900)
- Delivery: Free within 3km, P50 otherwise.
- Rules: Orders must be placed 2 days in advance.
- Contact: 0912-345-6789.
Respond in a friendly manner. You can use English or Bisaya/Cebuano.
"""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"response": "Palihug pag-type og message."}), 400
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": KNOWLEDGE_BASE},
                {"role": "user", "content": user_message}
            ]
        )
        return jsonify({"response": response.choices[0].message.content})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"response": "Sorry, naay problema. Tawag sa 0912-345-6789."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
