from flask import Flask, render_template
import os
from .forms import LoginForm

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret string')
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/basic')
def basic():
    form = LoginForm()
    return render_template('basic.html', form=form)


@app.route('/html')
def html():
    return render_template('Pure.html')


if __name__ == "__main__":
    app.run()
