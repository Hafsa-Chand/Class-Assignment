import os
from dotenv import load_dotenv
import google.generativeai as genai

# === Environment Setup ===
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)

# AI model setup
bot_model = genai.GenerativeModel("gemini-1.5-flash")

# === Inventory Data Store ===
inventory_data = []

# === Inventory Operations ===
def add_item(prod_id: int, prod_name: str, prod_qty: int, prod_action: str):
    entry = {
        "product_id": prod_id,
        "name": prod_name,
        "qty": prod_qty,
        "action": prod_action
    }
    inventory_data.append(entry)
    return f"✅ Item added: {prod_name} | ID: {prod_id}, Qty: {prod_qty}, Action: {prod_action}"

def remove_item(prod_id: int):
    for idx, entry in enumerate(inventory_data):
        if entry["product_id"] == prod_id:
            inventory_data.pop(idx)
            return f"🗑️ Product with ID {prod_id} removed."
    return f"❌ No record exists with ID {prod_id}."

def update_item(prod_id: int, prod_name: str, prod_qty: int, prod_action: str):
    for idx, entry in enumerate(inventory_data):
        if entry["product_id"] == prod_id:
            inventory_data[idx] = {
                "product_id": prod_id,
                "name": prod_name,
                "qty": prod_qty,
                "action": prod_action
            }
            return f"🔄 Product {prod_id} updated → {prod_name}, Qty: {prod_qty}, Action: {prod_action}"
    return f"❌ No product found with ID {prod_id}."

# === Chat Handler ===
print("🤖 Inventory Assistant Ready (type 'exit' anytime to stop)")

while True:
    user_input = input("You: ").lower().strip()
    if user_input == "exit":
        break

    if "add" in user_input:
        pid = int(input("Enter Product ID: "))
        pname = input("Enter Product Name: ")
        qty = int(input("Enter Quantity: "))
        result = add_item(pid, pname, qty, "add")

    elif "update" in user_input:
        pid = int(input("Enter Product ID: "))
        pname = input("Enter New Name: ")
        qty = int(input("Enter New Quantity: "))
        result = update_item(pid, pname, qty, "update")

    elif "remove" in user_input:
        pid = int(input("Enter Product ID to remove: "))
        result = remove_item(pid)

    else:
        result = "🤔 I couldn’t figure out what to do. Try add/update/remove."

    print("Bot:", result)
