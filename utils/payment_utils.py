import os
from datetime import datetime

def generate_receipt(user_id, user_name, amount):
    receipt_content = f"""
    PG-Nest Payment Receipt
    -------------------------
    User ID: {user_id}
    User NAME: {user_name}
    Amount Paid: {amount} INR
    Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    -------------------------
    Thank you for staying with PG-Nest!
    """

    receipt_dir = "receipts"
    if not os.path.exists(receipt_dir):
        os.makedirs(receipt_dir)

    receipt_path = os.path.join(receipt_dir, f"receipt_user_{user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt")
    with open(receipt_path, "w") as file:
        file.write(receipt_content)

    return receipt_path
