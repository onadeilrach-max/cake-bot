from flask import Flask, render_template, request, jsonify
import openai
import os

app = Flask(__name__)

# KINI ANG CONFIGURATION PARA SA GROQ
# Ang API key kuhaon gikan sa Render Environment Variables (OPENAI_API_KEY)
client = openai.OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# KNOWLEDGE BASE
CAKE_SHOP_INFO = """
Shop Name: Sweet Moments Cake Shop
Menu:
- Chocolate Cake: Small (P400), Medium (P600), Large (P800)
- Ube Cake: Small (P450), Medium (P650), Large (P850)
- Red Velvet: Small (P500), Medium (P700), Large (P900)
Delivery: Free within 3km, P50 outside.
Order Rule: Must order 2 days in advance.
Contact: 0912-345-6789.
"""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192", # Kini ang standard fast model sa Groq
            messages=[
                {"role": "system", "content": f"You are a friendly assistant for Sweet Moments Cake Shop. Use this information: {CAKE_SHOP_INFO}. Answer politely. If the answer is not in the info, ask them to call 0912-345-6789."},
                {"role": "user", "content": user_message}
            ]
        )
        bot_reply = response.choices[0].message.content
    except Exception as e:
        bot_reply = "Sorry, naay gamay nga problema sa system. Palihug tawag sa 0912-345-6789."

    return jsonify({"reply": bot_reply})

if __name__ == '__main__':
    app.run(debug=True)
