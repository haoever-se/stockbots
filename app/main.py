"""Entry point of the server"""
from flask import Flask
from app.db import db, setup_database
from app.slack import slack_blueprint

app = Flask(__name__)
# Setup database
setup_database(app)
# Setup Flask Blueprints
app.register_blueprint(slack_blueprint)


# export FLASK_APP=app.main
# flask db_create
@app.cli.command('db_create')
def db_create():
    """Create database"""
    db.create_all()
    print('Database created!')


# flask db_drop
@app.cli.command('db_drop')
def db_drop():
    """Drop table"""
    db.drop_all()
    print('Database dropped!')


@app.route("/")
def hello_world():
    """Health check function"""
    return "Hello, World!"


if __name__ == '__main__':
    app.run(debug=True)
