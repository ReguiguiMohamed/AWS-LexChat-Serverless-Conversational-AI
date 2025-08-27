"""Lambda handler for the AWS Lex chatbot."""

from __future__ import annotations

import json
import logging

# Mock database for user accounts
MOCK_ACCOUNTS = {
    "user123": {
        "userName": "John",
        "checking": {"balance": 1500.75},
        "savings": {"balance": 5000.00},
        "credit": {"balance": -500.00},
        "loan": {"balance": -10000.00},
    }
}

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_account_balance(user_id: str, account_type: str) -> float | None:
    """Retrieve the account balance from the mock database."""
    return MOCK_ACCOUNTS.get(user_id, {}).get(account_type, {}).get("balance")

def update_account_balance(user_id: str, account_type: str, amount: float) -> None:
    """Update the account balance in the mock database."""
    if user_id in MOCK_ACCOUNTS and account_type in MOCK_ACCOUNTS[user_id]:
        MOCK_ACCOUNTS[user_id][account_type]["balance"] += amount

def authenticate_user(event: dict) -> str | None:
    """Simulate user authentication."""
    user_id = event.get("userId")
    if user_id in MOCK_ACCOUNTS:
        return user_id
    return None

def lambda_handler(event: dict, context) -> dict:
    """Return a simple Lex Close dialog action.

    The handler inspects the incoming event's ``currentIntent`` and returns a
    response based on the intent.
    """

    logger.info(f"Received event: {json.dumps(event)}")

    intent_name = event.get("interpretations", [{}])[0].get("intent", {}).get("name")
    slots = event.get("sessionState", {}).get("intent", {}).get("slots", {})
    session_attributes = event.get("sessionState", {}).get("sessionAttributes", {})
    confirmation_state = event.get("sessionState", {}).get("intent", {}).get("confirmationState")

    user_id = authenticate_user(event)

    if not user_id:
        message_content = "Authentication failed. Please try again later."
        return {
            "sessionState": {
                "dialogAction": {"type": "Close"},
                "intent": {"name": intent_name, "state": "Failed"},
            },
            "messages": [{"contentType": "PlainText", "content": message_content}],
        }

    if intent_name == "GreetingIntent":
        user_name = MOCK_ACCOUNTS.get(user_id, {}).get("userName")
        if user_name:
            session_attributes["userName"] = user_name
            message_content = f"Hello, {user_name}! How can I help you with your banking needs today?"
        else:
            message_content = "Hello! How can I help you with your banking needs today?"
        
        response = {
            "sessionState": {
                "dialogAction": {"type": "Close"},
                "intent": {"name": intent_name, "state": "Fulfilled"},
                "sessionAttributes": session_attributes,
            },
            "messages": [{"contentType": "PlainText", "content": message_content}],
        }

    elif intent_name == "BankingInquiryIntent":
        account_type = slots.get("AccountType", {}).get("value", {}).get("interpretedValue")
        if not account_type:
            account_type = session_attributes.get("account_type")
        else:
            session_attributes["account_type"] = account_type

        banking_operation = slots.get("BankingOperation", {}).get("value", {}).get("interpretedValue")
        amount = slots.get("Amount", {}).get("value", {}).get("interpretedValue")

        if account_type and banking_operation:
            if banking_operation == "balance":
                balance = get_account_balance(user_id, account_type)
                if balance is not None:
                    message_content = f"Your {account_type} account balance is ${balance:.2f}."
                else:
                    message_content = f"You do not have a {account_type} account."
            else:
                message_content = f"You want to perform a {banking_operation} on your {account_type} account."
                if amount:
                    message_content += f" for the amount of ${amount}."

            response = {
                "sessionState": {
                    "dialogAction": {"type": "Close"},
                    "intent": {"name": intent_name, "state": "Fulfilled"},
                    "sessionAttributes": session_attributes,
                },
                "messages": [{"contentType": "PlainText", "content": message_content}],
            }
        else:
            response = {
                "sessionState": {
                    "dialogAction": {"type": "Delegate"},
                    "intent": {"name": intent_name, "slots": slots},
                    "sessionAttributes": session_attributes,
                }
            }

    elif intent_name == "TransferMoneyIntent":
        from_account_type = slots.get("fromAccountType", {}).get("value", {}).get("interpretedValue")
        to_account_type = slots.get("toAccountType", {}).get("value", {}).get("interpretedValue")
        transfer_amount = float(slots.get("transferAmount", {}).get("value", {}).get("interpretedValue"))

        if confirmation_state == "Confirmed":
            from_balance = get_account_balance(user_id, from_account_type)
            if from_balance is not None and from_balance >= transfer_amount:
                update_account_balance(user_id, from_account_type, -transfer_amount)
                update_account_balance(user_id, to_account_type, transfer_amount)
                message_content = f"Successfully transferred ${transfer_amount:.2f} from your {from_account_type} to your {to_account_type} account."
            else:
                message_content = "Insufficient funds to complete the transfer."
            
            response = {
                "sessionState": {
                    "dialogAction": {"type": "Close"},
                    "intent": {"name": intent_name, "state": "Fulfilled"},
                    "sessionAttributes": session_attributes,
                },
                "messages": [{"contentType": "PlainText", "content": message_content}],
            }

        elif confirmation_state == "Denied":
            message_content = "Okay, I have cancelled the transaction."
            response = {
                "sessionState": {
                    "dialogAction": {"type": "Close"},
                    "intent": {"name": intent_name, "state": "Fulfilled"},
                    "sessionAttributes": session_attributes,
                },
                "messages": [{"contentType": "PlainText", "content": message_content}],
            }
        else:
            response = {
                "sessionState": {
                    "dialogAction": {"type": "Delegate"},
                    "intent": {"name": intent_name, "slots": slots},
                    "sessionAttributes": session_attributes,
                }
            }

    elif intent_name == "FallbackIntent":
        message_content = "Sorry, I didn't understand that. Please try rephrasing your request."
        response = {
            "sessionState": {
                "dialogAction": {"type": "Close"},
                "intent": {"name": intent_name, "state": "Fulfilled"},
                "sessionAttributes": session_attributes,
            },
            "messages": [{"contentType": "PlainText", "content": message_content}],
        }
    else:
        message_content = "Thanks for your message! How can I assist you?"
        response = {
            "sessionState": {
                "dialogAction": {"type": "Close"},
                "intent": {"name": intent_name, "state": "Fulfilled"},
                "sessionAttributes": session_attributes,
            },
            "messages": [{"contentType": "PlainText", "content": message_content}],
        }

    logger.info(f"Returning response: {json.dumps(response)}")
    return response

