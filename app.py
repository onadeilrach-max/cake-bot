from flask import Flask, render_template, request, jsonify
import openai  # Pwede ni ilisan og Groq o uban pang LLM library

app = Flask(__name__)

# SETTINGS: Ibutang imong API Key diri
client = openai.OpenAI(api_key="IMONG_API_KEY_DIRI")

# KINI ANG KNOWLEDGE BASE (Ang fake data sa Cake Shop)
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
    
    # KINI ANG SYSTEM PROMPT (Ang nag-control sa AI)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo", # o bisan unsa nga model nga imong gamit
        messages=[
            {"role": "system", "content": f"You are a friendly assistant for Sweet Moments Cake Shop. Use this information: {CAKE_SHOP_INFO}. Answer politely. If the answer is not in the info, ask them to call 0912-345-6789."},
            {"role": "user", "content": user_message}
        ]
    )
    
    bot_reply = response.choices[0].message.content
    return jsonify({"reply": bot_reply})

if __name__ == '__main__':
    app.run(debug=True)
