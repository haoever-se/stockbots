"""main function of Stockbots"""
import os
from pathlib import Path
from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from alpha_vantage.timeseries import TimeSeries
from dotenv import load_dotenv


env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


#initial Flask and Slacl client
app = Flask(__name__)
slack_events_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'], "/slack/events", app)
slack_client = WebClient(token=os.environ['SLACK_TOKEN'])

#Alpha Vantage
ts = TimeSeries(key=os.environ['ALPHA_VANTAGE_KEY'])

#events adapter
@slack_events_adapter.on("message")
def handle_message(event_data):
    """function handle message"""
    message = event_data["event"]
    #ignore message from bot
    if message.get("subtype") == "bot_message":
        return

    #Parse
    text = message.get('text')
    if text and text.startswith('!stock '):
        # get stock's symbol
        _, symbol = text.split(' ', 1)
        # get price
        stock_price = get_stock_price(symbol)
        # send message to Slack
        channel_id = message["channel"]
        slack_client.chat_postMessage(channel=channel_id, text=stock_price)

def get_stock_price(symbol):
    """function for getting prize through API"""
    try:
        # get price function
        data, _ = ts.get_quote_endpoint(symbol)
        price = data['05. price']
        print(data)
        return f"The current price of {symbol} is: ${price}"
    except Exception as e:
        #return f"Not a existing symbol."
        return f"Error retrieving stock price: {str(e)}"

if __name__ == '__main__':
    app.run(port=3000)
