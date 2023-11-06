"""Entry point of the server"""
import requests
from flask import Flask, request
import os
import logging
from slack_sdk import WebClient
import json

from slack_sdk.errors import SlackApiError

app = Flask(__name__)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route("/")
def hello_world():
    """Health check function"""
    return "Hello, World!"


@app.route('/slack/check', methods=['POST'])
def slack_check():
    try:
        return do_slack_check(request.form)
    except Exception as e:
        logger.error(str(e), exc_info=True)
        return "Something went wrong!", 500


def do_slack_check(form_data):
    API_KEY = os.environ.get('API_KEY')
    TOKEN = os.environ.get('TOKEN')
    CHANNEL = os.environ.get('CHANNEL')

    stock = form_data.get('text')
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock}&apikey={API_KEY}"

    logger.debug(f"[StockPriceQueryController] request :{form_data}")
    response = requests.get(url)
    response.raise_for_status()
    resp = response.text
    logger.debug(f"resp: {resp}")

    res = json.loads(resp)
    last_date = res["Meta Data"]["3. Last Refreshed"]
    target = res["Time Series (Daily)"][last_date]
    message_blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*{last_date} {stock}*:\n"
                        f"`Open price`: {target['1. open']}\n"
                        f"`Highest price`: {target['2. high']}\n"
                        f"`Lowest price`: {target['3. low']}\n"
                        f"`Close price`: {target['4. close']}\n"
                        f"`Volume`: {target['5. volume']}"
            }
        },
        {"type": "divider"}
    ]

    try:
        response = WebClient(token=TOKEN).chat_postMessage(
            channel=CHANNEL,
            blocks=message_blocks
        )
        logger.debug("Message posted to Slack")
        return "Message posted to Slack"
    except SlackApiError as e:
        error_message = f"Error posting message to Slack: {e.response['error']}"
        logger.error(error_message)
        return error_message


if __name__ == '__main__':
    app.run(debug=True)
