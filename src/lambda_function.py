import json

def lambda_handler(event, context):
    """
    Main Lambda handler function.
    """
    # TODO: Implement your chatbot logic here
    
    response = {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
                "contentType": "PlainText",
                "content": "Hello from your Lex Chatbot!"
            }
        }
    }
    
    return response
