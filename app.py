from flask import Flask, render_template, redirect

app = Flask(__name__)


@app.route("/")
def homepage():
    return render_template("index.html")

@app.route("/season")
def season():
    return render_template("season.html")