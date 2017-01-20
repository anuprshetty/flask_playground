from flask import Flask, redirect, url_for
from flask_restx import Api, Resource


# app --> Web Server Gateway Interface (WSGI) application.
# The Web Server Gateway Interface is a simple calling convention for web servers to forward requests to web applications or frameworks written in the Python programming language.
api = Api()
app = Flask(__name__)
api.init_app(app)

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
