from flask import Flask, request
import json
from datetime import datetime

app = Flask(__name__)

DATA_FILE = "bal.json"
MIN_USD = 0.2

# ================= LOAD BALANCE =================
def load_bal():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

# ================= SAVE BALANCE =================
def save_bal(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ================= WEBHOOK =================
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    print("\n==== NEW PAYMENT ====")
    print(data)

    try:
        # Only confirm completed payments
        if data.get("payment_status") == "finished":

            user_id = str(data.get("order_id"))
            amount = float(data.get("price_amount", 0))

            print(f"User: {user_id}")
            print(f"Amount: ${amount}")

            # Minimum check
            if amount < MIN_USD:
                print("❌ Below minimum deposit, ignored")
                return "ignored"

            # Load current balances
            balances = load_bal()

            # Add balance
            balances[user_id] = balances.get(user_id, 0) + amount

            # Save
            save_bal(balances)

            print(f"✅ Balance added: ${amount} to user {user_id}")

    except Exception as e:
        print("❌ ERROR:", e)

    return "ok"

# ================= START SERVER =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
