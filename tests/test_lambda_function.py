"""Unit tests for the Lambda handler."""

import unittest

from src import lambda_function


class TestLambdaFunction(unittest.TestCase):
    """Tests for :func:`lambda_function.lambda_handler`."""

    def _base_event(self, transcript: str) -> dict:
        return {
            "currentIntent": {
                "name": "LexChatbotIntent",
                "slots": {},
                "confirmationStatus": "None",
            },
            "bot": {
                "name": "LexChatbot",
                "alias": "$LATEST",
                "version": "$LATEST",
            },
            "userId": "test_user",
            "inputTranscript": transcript,
            "invocationSource": "FulfillmentCodeHook",
            "outputDialogMode": "Text",
            "messageVersion": "1.0",
            "sessionAttributes": {},
        }

    def test_greeting_response(self) -> None:
        event = self._base_event("Hello")
        response = lambda_function.lambda_handler(event, {})

        self.assertEqual(response["dialogAction"]["type"], "Close")
        self.assertEqual(response["dialogAction"]["fulfillmentState"], "Fulfilled")
        self.assertIn("Olympic Games", response["dialogAction"]["message"]["content"])

    def test_generic_response(self) -> None:
        event = self._base_event("Tell me a fact")
        response = lambda_function.lambda_handler(event, {})

        self.assertEqual(response["dialogAction"]["type"], "Close")
        self.assertEqual(response["dialogAction"]["fulfillmentState"], "Fulfilled")
        self.assertTrue(
            response["dialogAction"]["message"]["content"].startswith(
                "Thanks for your message"
            )
        )


if __name__ == "__main__":
    unittest.main()

