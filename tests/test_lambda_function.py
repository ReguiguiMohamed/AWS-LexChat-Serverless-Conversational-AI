import json
import unittest
from src import lambda_function

class TestLambdaFunction(unittest.TestCase):

    def test_lambda_handler(self):
        # Create a sample event
        event = {
            "currentIntent": {
                "name": "LexChatbotIntent",
                "slots": {},
                "confirmationStatus": "None"
            },
            "bot": {
                "name": "LexChatbot",
                "alias": "$LATEST",
                "version": "$LATEST"
            },
            "userId": "test_user",
            "inputTranscript": "Hello",
            "invocationSource": "FulfillmentCodeHook",
            "outputDialogMode": "Text",
            "messageVersion": "1.0",
            "sessionAttributes": {}
        }
        
        # Call the lambda handler
        context = {}
        response = lambda_function.lambda_handler(event, context)
        
        # Check the response
        self.assertEqual(response['dialogAction']['type'], 'Close')
        self.assertEqual(response['dialogAction']['fulfillmentState'], 'Fulfilled')
        self.assertEqual(response['dialogAction']['message']['content'], 'Hello from your Lex Chatbot!')

if __name__ == '__main__':
    unittest.main()
