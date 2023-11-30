"""Entry point of the server"""
import logging
import os

from flask import Flask
from db import db, setup_database, Symbol, symbols_schema
from slack import slack_blueprint
from dotenv import load_dotenv
from threading import Thread, Event
import bot



# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)
# Setup database
setup_database(app)
# Setup Flask Blueprints
app.register_blueprint(slack_blueprint)
# Set the logging level to DEBUG
logging.basicConfig(level=logging.DEBUG)

# top_stock_companies = Symbol.query.all()

# export FLASK_APP=app.main
# flask db_create
@app.cli.command('db_create')
def db_create():
    """Create database"""
    db.create_all()
    logging.debug('Database created!')


# flask db_drop
@app.cli.command('db_drop')
def db_drop():
    """Drop table"""
    db.drop_all()
    logging.debug('Database dropped!')


@app.route("/")
def hello_world():
    """Health check function"""
    return "Hello, World!"


# Create an event to signal when variables are ready to be accessed
shared_data_ready = Event()
with app.app_context():

    shared_data_ready.data = app
    logging.error(f"app.context: {shared_data_ready.data}")

def run_discord_bot(event):
    # Pass the event to the Discord bot
    bot.start_bot(event)

if __name__ == '__main__':
    # Create a thread for running the Discord bot
    discord_thread = Thread(target=run_discord_bot, args=(shared_data_ready,))

    # Start the Discord bot thread
    discord_thread.start()

    # Start the Flask app
    app.run(debug=False)
