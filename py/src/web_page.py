from flask import Flask

app = Flask(__name__)

# Landing page
@app.route("/")
def landing():
    return "Hello world!"

if __name__ == "__main__":
    app.run()


