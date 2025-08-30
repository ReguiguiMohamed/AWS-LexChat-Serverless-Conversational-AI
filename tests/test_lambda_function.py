"""Unit tests for the banking chatbot Lambda handler."""

from __future__ import annotations

import unittest
from unittest.mock import patch

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))
import lambda_function


def lex_v2_event(
    intent_name: str,
    *,
    slots: dict | None = None,
    user_id: str = "user123",
    confirmation_state: str | None = None,
    session_attributes: dict | None = None,
) -> dict:
    """Construct a minimal Lex V2 event for testing."""

    return {
        "interpretations": [{"intent": {"name": intent_name, "slots": slots or {}}}],
        "sessionState": {
            "intent": {
                "name": intent_name,
                "slots": slots or {},
                "confirmationState": confirmation_state,
            },
            "sessionAttributes": session_attributes or {},
        },
        "userId": user_id,
    }


class TestLambdaFunction(unittest.TestCase):
    """Tests for :func:`lambda_function.lambda_handler`."""

    def test_greeting_intent_returns_user_name(self) -> None:
        event = lex_v2_event("GreetingIntent")
        response = lambda_function.lambda_handler(event, None)

        self.assertEqual(
            response["sessionState"]["intent"]["state"], "Fulfilled"
        )
        self.assertIn(
            "John", response["messages"][0]["content"]
        )

    def test_banking_inquiry_balance_known_account(self) -> None:
        slots = {
            "AccountType": {"value": {"interpretedValue": "checking"}},
            "BankingOperation": {"value": {"interpretedValue": "balance"}},
        }
        event = lex_v2_event("BankingInquiryIntent", slots=slots)
        response = lambda_function.lambda_handler(event, None)

        self.assertIn("$1500.75", response["messages"][0]["content"])

    def test_transfer_money_intent_confirmed(self) -> None:
        slots = {
            "fromAccountType": {"value": {"interpretedValue": "checking"}},
            "toAccountType": {"value": {"interpretedValue": "savings"}},
            "transferAmount": {"value": {"interpretedValue": "100"}},
        }
        event = lex_v2_event(
            "TransferMoneyIntent", slots=slots, confirmation_state="Confirmed"
        )
        response = lambda_function.lambda_handler(event, None)

        self.assertIn("Successfully transferred", response["messages"][0]["content"])

    def test_fallback_intent(self) -> None:
        event = lex_v2_event("FallbackIntent")
        response = lambda_function.lambda_handler(event, None)

        self.assertIn(
            "didn't understand", response["messages"][0]["content"]
        )

    def test_authentication_failure(self) -> None:
        event = lex_v2_event("GreetingIntent", user_id="unknown")
        response = lambda_function.lambda_handler(event, None)

        self.assertEqual(
            response["sessionState"]["intent"]["state"], "Failed"
        )

    def test_banking_inquiry_unknown_account(self) -> None:
        slots = {
            "AccountType": {"value": {"interpretedValue": "unknown"}},
            "BankingOperation": {"value": {"interpretedValue": "balance"}},
        }
        event = lex_v2_event("BankingInquiryIntent", slots=slots)
        response = lambda_function.lambda_handler(event, None)

        self.assertIn("You do not have a unknown account.", response["messages"][0]["content"])

    def test_transfer_money_insufficient_funds(self) -> None:
        slots = {
            "fromAccountType": {"value": {"interpretedValue": "checking"}},
            "toAccountType": {"value": {"interpretedValue": "savings"}},
            "transferAmount": {"value": {"interpretedValue": "2000"}},
        }
        event = lex_v2_event(
            "TransferMoneyIntent", slots=slots, confirmation_state="Confirmed"
        )
        response = lambda_function.lambda_handler(event, None)

        self.assertIn("Insufficient funds", response["messages"][0]["content"])

    def test_transfer_money_denied(self) -> None:
        slots = {
            "fromAccountType": {"value": {"interpretedValue": "checking"}},
            "toAccountType": {"value": {"interpretedValue": "savings"}},
            "transferAmount": {"value": {"interpretedValue": "100"}},
        }
        event = lex_v2_event(
            "TransferMoneyIntent", slots=slots, confirmation_state="Denied"
        )
        response = lambda_function.lambda_handler(event, None)

        self.assertIn("cancelled the transaction", response["messages"][0]["content"])


if __name__ == "__main__":  # pragma: no cover
    unittest.main()

