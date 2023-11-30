"""database"""
import logging
import os
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import Column, Integer, String

basedir = os.path.abspath(os.path.dirname(__file__))

# Initialize the database
db = SQLAlchemy()
ma = Marshmallow()


def setup_database(app):
    """setup Database"""
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'stocks.db')
    db.init_app(app)
    ma.init_app(app)


class Symbol(db.Model):  # pylint: disable=R0903
    """Database models"""
    __tablename__ = 'symbol'
    id = Column(Integer, primary_key=True)
    symbol = Column(String, unique=True)


class SymbolSchema(ma.Schema):
    """Schema definition"""
    class Meta:  # pylint: disable=R0903
        """Fields"""
        fields = ('id', 'symbol')


# Instantiate schemas
symbol_schema = SymbolSchema()
symbols_schema = SymbolSchema(many=True)
