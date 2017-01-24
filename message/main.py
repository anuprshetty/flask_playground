from flask import Flask, redirect, url_for, request, jsonify
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from flask_swagger_ui import get_swaggerui_blueprint


# app --> Web Server Gateway Interface (WSGI) application.
# The Web Server Gateway Interface is a simple calling convention for web servers to forward requests to web applications or frameworks written in the Python programming language.
api = Api()
app = Flask(__name__)
api.init_app(app)

basedir = os.path.abspath(os.path.dirname(__file__))

SWAGGER_URL = "/swagger/"
API_URL = "/static/swagger.json"
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={"app_name": "Flask-Playground"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Database
app.config["SQLALCHEMY_DATABASE_URI"] = r"sqlite:///" + os.path.join(
    basedir, "db.sqlite"
)
print(app.config["SQLALCHEMY_DATABASE_URI"])
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize SQL ORM (Object Relational Mapper)
sql_orm = SQLAlchemy(app)

# Initialize Marshmallow
marshmallow = Marshmallow(app)


# Product class/model
class Product(sql_orm.Model):
    id = sql_orm.Column(sql_orm.Integer, primary_key=True)
    name = sql_orm.Column(sql_orm.String(100), unique=True)
    description = sql_orm.Column(sql_orm.String(200))
    price = sql_orm.Column(sql_orm.Float)
    quantity = sql_orm.Column(sql_orm.Integer)

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


# Product Schema
class ProductSchema(marshmallow.Schema):
    class Meta:
        fields = ("id", "name", "description", "price", "quantity")


# Initialize schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# Create the database
sql_orm.create_all()

# route() decorator in Flask is used to bind URL to a function.
@app.route("/hello/<username>/<int:age>/")
def hello_world(username, age):
    return "Hello {}! Your age is {}".format(username, age)


# /flask != /flask/
@app.route("/flask")
def flask_app():
    return "Flask app"


# /python = /python/
@app.route("/python/")
def python_app():
    return "Python app"


@app.route("/app/<name>/")
def my_app(name):
    if name == "python":
        return redirect(url_for("python_app"))
    elif name == "flask":
        return redirect(url_for("flask_app"))
    else:
        return "Invalid app"


@api.route("/welcome/", methods=["GET"])
class Home(Resource):
    def get(self):
        return {"msg": "Welcome!"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
