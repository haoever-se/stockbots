"""Entry point of slack application"""
import os
import json
import logging
import requests
from flask import Blueprint, request
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
from app.db import db, Symbol, symbols_schema

slack_blueprint = Blueprint('slack', __name__)
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@slack_blueprint.route('/slack/add', methods=['POST'])
def slack_add():
    """Add symbol to database"""
    symbol = request.form['text']
    test = Symbol.query.filter_by(symbol=symbol).first()
    if test:
        return 'That symbol already exists.', 409

    symbol = Symbol(symbol=symbol)
    db.session.add(symbol)
    db.session.commit()
    return 'symbol added successfully!', 201


@slack_blueprint.route('/slack/getDb', methods=['POST'])
def slack_get_db():
    """Get all symbol in database"""
    symbol_list = Symbol.query.all()
    result = symbols_schema.dump(symbol_list)
    return result


@slack_blueprint.route('/slack/getAll', methods=['POST'])
def slack_get_all():
    """Get all symbol in database then send message to Slack"""
    symbol_list = Symbol.query.all()
    try:
        for data in symbol_list:
            do_slack_check(data.symbol)
        return "Message posted to Slack"
    # pylint: disable=W0718
    except Exception as e:
        logger.error(str(e), exc_info=True)
        return "Something went wrong!", 500


@slack_blueprint.route('/slack/check', methods=['POST'])
def slack_check():
    """Endpoint to check stock price from a Slack command."""
    try:
        do_slack_check(request.form.get('text'))
        return "Message posted to Slack"
    # pylint: disable=W0718
    except Exception as e:
        logger.error(str(e), exc_info=True)
        return "Something went wrong!", 500


def do_slack_check(symbol):
    """Process the /slack/check command."""
    api_key = os.environ.get('API_KEY')
    token = os.environ.get('TOKEN')
    channel_id = os.environ.get('CHANNEL')

    url = (f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="
           f"{symbol}&apikey={api_key}")

    logger.debug("Stock Symbol: %s", symbol)
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    resp = response.text
    logger.debug("Response: %s", resp)

    res = json.loads(resp)
    last_date = res["Meta Data"]["3. Last Refreshed"]
    target = res["Time Series (Daily)"][last_date]
    message_blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*{last_date} {symbol}*: :blob-party:\n"
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
        response = WebClient(token=token).chat_postMessage(
            channel=channel_id,
            blocks=message_blocks
        )
    except SlackApiError as e:
        error_message = f"Error posting message to Slack: {e.response['error']}"
        logger.error("Slack API error: %s", error_message)
