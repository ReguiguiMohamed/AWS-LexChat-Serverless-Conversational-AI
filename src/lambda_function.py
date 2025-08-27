"""Lambda handler for the AWS Lex chatbot."""

from __future__ import annotations

import json


def lambda_handler(event: dict, context) -> dict:
    """Return a simple Lex Close dialog action.

    The handler inspects the incoming event's ``inputTranscript`` and returns a
    cultural or historical fact when a greeting is detected. For any other
    input, a generic prompt encouraging the user to ask about history is
    returned.
    """

    transcript = event.get("inputTranscript", "").lower()

    if any(greeting in transcript for greeting in ("hello", "hi")):
        message_content = (
            "Hello! Did you know the first modern Olympic Games were held in 1896"
            " in Athens?"
        )
    else:
        message_content = "Thanks for your message! Ask me about world history."

    response = {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
                "contentType": "PlainText",
                "content": message_content,
            },
        }
    }

    return response

