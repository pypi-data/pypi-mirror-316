import requests
import json

def teams_webhook(webhook_url:str, title:str, message:str):
    """
    Send a formatted message to a Microsoft Teams channel using a webhook URL.
    
    :param webhook_url: The webhook URL for the Teams channel
    :param title: The title of the message
    :param message: The body of the message
    """
    headers = {
        'Content-Type': 'application/json'
    }
    
    payload = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "type": "AdaptiveCard",
                    "body": [
                        {
                            "type": "TextBlock",
                            "size": "Medium",
                            "weight": "Bolder",
                            "text": title
                        },
                        {
                            "type": "TextBlock",
                            "text": message,
                            "wrap": True
                        }
                    ],
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "version": "1.0"                }
            }
        ]
    }
    
    try:
        response = requests.post(webhook_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while sending the message: {e}")



def ntfy(server: str, message: str):
    """
    Send a notification message to an ntfy.sh server.

    This function sends a POST request to the specified ntfy.sh server
    with the provided message.

    Args:
        server (str): The name of the ntfy.sh server/topic to send the message to.
        message (str): The message to be sent.

    Raises:
        ValueError: If server or message is empty.
        requests.RequestException: If there's an error with the HTTP request.
    """
    if not server or not message:
        raise ValueError("Both server and message must be non-empty strings.")

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    
    try:
        response = requests.post(f'https://ntfy.sh/{server}', headers=headers, data=message)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
    except requests.RequestException as e:
        print(f"Error sending notification: {e}")