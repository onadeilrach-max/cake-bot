import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# --- CONFIGURATION ---
# Siguraduha nga ang environment variable sa Render kay "OPENAI_API_KEY"
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ.get("OPENAI_API_KEY")
)

# Knowledge Base para sa Sweet Moments Cake Shop
KNOWLEDGE_BASE = """
You are a helpful customer service assistant for 'Sweet Moments Cake Shop'.
Use this information to answer customers:
- Menu: 
    * Chocolate Cake: Small (P400), Medium (P600), Large (P800)
    * Ube Cake: Small (P450), Medium (P650), Large (P850)
    * Red Velvet: Small (P500), Medium (P700), Large (P900)
- Delivery: Free within 3km, P50 otherwise.
- Rules: Orders must be placed 2 days in advance.
- Contact: 0912-345-6789.
- Language: Respond in a friendly manner. You can speak English or Bisaya/Cebuano.
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
        # API Call to Groq
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": KNOWLEDGE_BASE},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7
        )
        bot_response = response.choices[0].message.content
        return jsonify({"response": bot_response})

    except Exception as e:
        print(f"Error: {e}") # Kini mugawas sa Render logs para makita nato ang problema
        return jsonify({"response": "Sorry, naay gamay nga problema sa system. Palihug tawag sa 0912-345-6789."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
