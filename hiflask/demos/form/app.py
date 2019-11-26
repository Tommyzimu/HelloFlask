from flask import Flask, render_template, request, flash, redirect, url_for
import os

from .forms import LoginForm

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret string')
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/basic', methods=['GET', 'POST'])
def basic():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        flash('Welcome home, %s' % username)
        return redirect(url_for('index'))
    return render_template('basic.html', form=form)


@app.route('/html', methods=['GET', 'POST'])
def html():
    form = LoginForm()
    if request.method == 'POST':
        username = request.form.get('username')
        flash('Welcome home, %s' % username)
        return redirect(url_for('index'))
    return render_template('Pure.html')


if __name__ == "__main__":
    app.run()
