from flask import Flask
from flask_restx import Api, Resource


# app --> Web Server Gateway Interface (WSGI) application.
# The Web Server Gateway Interface is a simple calling convention for web servers to forward requests to web applications or frameworks written in the Python programming language.
api = Api()
app = Flask(__name__)
api.init_app(app)

@api.route("/welcome/", methods=["GET"])
class Home(Resource):
    def get(self):
        return {"msg": "Welcome!"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
