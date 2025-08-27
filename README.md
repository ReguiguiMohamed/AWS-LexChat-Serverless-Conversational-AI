# AWS-LexChat-Serverless-Conversational-AI

A serverless chatbot built with AWS Lex, Lambda, and CloudFormation, designed to engage users with cultural, historical, and travel insights. Hosted on GitHub, this project showcases conversational AI and cloud skills.

## Project Structure

```
AWS-LexChat-Serverless-Conversational-AI/
├── .gitignore
├── LICENSE
├── README.md
├── docs/
├── scripts/
├── src/
│   └── lambda_function.py
├── templates/
│   └── template.yaml
└── tests/
    └── test_lambda_function.py
```

## Getting Started

### Prerequisites

*   AWS Account
*   AWS CLI configured
*   Python 3.9
*   AWS SAM CLI

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-username/AWS-LexChat-Serverless-Conversational-AI.git
    ```
2.  Navigate to the project directory:
    ```bash
    cd AWS-LexChat-Serverless-Conversational-AI
    ```
3.  Install dependencies (if any):
    ```bash
    # (e.g., pip install -r requirements.txt)
    ```

## Deployment

Deploy the application using AWS SAM:

```bash
sam build
sam deploy --guided
```

## Usage

Once deployed, you can interact with the chatbot through the AWS Lex console or by integrating it with your applications. The current Lambda handler responds to common greetings with a short cultural or historical fact and otherwise encourages users to ask about world history.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
