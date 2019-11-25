from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello Flask'

@app.route('/html')
def html():
    return render_template('Pure.html')


if __name__ == "__main__":
    app.run()
