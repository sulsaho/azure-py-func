from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello World"


@app.route("/another-route")
def another_route():
    return "Hello World from another route"


# if __name__ == "__main__":
#     app.run()
