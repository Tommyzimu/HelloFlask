import click
import os
from flask import Flask, json, make_response, jsonify, redirect, url_for, request, session, abort, render_template, \
    Markup, flash
from urllib.parse import urlparse, urljoin
from jinja2.utils import generate_lorem_ipsum

# 从flask包里面导入Flask类  并实例化这个类 app
app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY', 'secret string')
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/hi')
@app.route('/hello')
def hello():
    name = request.args.get('name')
    if name is None:
        name = request.cookies.get('name', 'Human')
        response = '<h1>Hello, %s!</h1>' % name
    if 'logged_in' in session:
        response += '[Authenticated]'
    else:
        response += '[Not Authenticated]'
    return response


@app.route('/greet', defaults={'name': 'Programmer'})
# @app.route('/greet')
@app.route('/greet/<name>')
def greet(name):
    return '<h1>Hello,%s!</h1>' % name


# @app.cli.command()
# def hello():
#     """Just say hello"""
#     click.echo('Hello, Human!')


@app.route('/goback/<int:year>')
def go_back(year):
    return '<p>Welcome to %d year!</p>' % (2019 - year), 200


# 查询参数 手动加入包含当前页面的url 这个参数一般命名为  next
@app.route('/foo')
def foo():
    # data = {
    #     'name': 'Tommy',
    #     'gender': 'male'
    # }
    # response = make_response(json.dumps(data))
    # response.mimetype = 'application/json'
    # return response
    # return jsonify(name='Tommy Li', gender='male')
    return '<h1>Foo page</h1><a href="%s">Do something and redirect</a>' % url_for('do_something',
                                                                                   next=request.full_path)


# ,next=request.full_path


@app.route('/bar')
def bar():
    return '<h1>Bar page</h1><a href="%s">Do something and redirect</a>' % url_for('do_something',
                                                                                   next=request.full_path)


# 返回上一个页面 使用request.referrer
@app.route('/do-something')
def do_something1():
    # return redirect(request.referrer or url_for('hello'))  # method 1
    return redirect(request.args.get('next', url_for('hello')))  # method 2


def redirect_back(default='hello', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))


@app.route('/do_something_and_redirect')
def do_something():
    # do something
    return redirect_back()


@app.route('/hil')
def hi():
    return redirect(url_for('say_hello'))


@app.route('/set/<name>')
def set_cookie(name):
    response = make_response(redirect(url_for('hello')))
    response.set_cookie('name', name)
    return response


@app.route('/login')
def login():
    session['logged_in'] = True
    return redirect(url_for('hello'))


@app.route('/admin')
def admin():
    if 'logged_in' not in session:
        abort(403)
    return "Welcome to admin page!"


@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')
    return redirect(url_for('hello'))


# 验证url的安全
def is_safe_url(target):
    ref_url = urlparse(request.host_url)  # 获取程序内的主机URL
    test_url = urlparse(urljoin(request.host_url, target))  # 使用urljoin（）函数将目标URL转换为绝对URL
    # 然后使用urlparse函数解析两个URL 最后对目标url的模式和主机地址进行验证 确保只有属于程序内部的url才会被返回
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


@app.route('/post')
def show_post():
    post_body = generate_lorem_ipsum(n=2)  # 生成两段随机文本
    return '''
<h1>A very long post</h1>
<div class="body">%s</div>
<button id="load">Load More</button>
<script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
<script type="text/javascript">
$(function(){
    $('#load').click(function(){
        $.ajax({
            url:'/more',                 // 目标url
            type:'get',                  // 请求方法
            success:function(data){      // 返回2XX响应后触发的回调函数  data 发送到服务器的数据
                $('.body').append(data); // 将返回的响应插入到页面中
            }
        
        })
    })
})  
</script> ''' % post_body


user = {
    'username': 'Tommy Li',
    'bio': 'A boy who loves movies and music.'
}
movies = [
    {'name': 'My Neighbor Totoro', 'year': '1998'},
    {'name': 'Three Colors trilogy', 'year': '1993'},
    {'name': 'Black Swan', 'year': '1995'},
    {'name': 'Love is beautiful', 'year': '2010'},
    {'name': 'Three Bears', 'year': '2013'},
    {'name': 'Snow Queen', 'year': '2019'},
]


@app.route('/more')
def load_post():
    return generate_lorem_ipsum(n=1)


@app.route('/watchlist')
def watchlist():
    return render_template('watchlist.html', user=user, movies=movies)


@app.route('/watchlist2')
def watchlist_with_static():
    return render_template('watchlist_with_static.html', user=user, movies=movies)


# register template context handler
@app.context_processor
def inject_info():
    foo = 'I am foo.'
    return dict(foo=foo)  # equal to: return {'foo': foo}


# register template global function
@app.template_global()
def bar():
    return 'I am bar.'


# register template filter
@app.template_filter()
def musical(s):
    return s + Markup(' &#9835;')


# register template test
@app.template_test()
def baz(n):
    if n == 'baz':
        return True
    return False


# message flashing
@app.route('/flash')
def just_flash():
    flash('I am flash, who is looking for me?')
    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500


if __name__ == '__main__':
    app.run()
