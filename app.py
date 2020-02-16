# from flask import Flask, render_template
# from flask import url_for
#
#
# app = Flask(__name__)
#
# name = 'Grey Li'
# movies = [
# {'title': 'My Neighbor Totoro', 'year': '1988'},
# {'title': 'Dead Poets Society', 'year': '1989'},
# {'title': 'A Perfect World', 'year': '1993'},
# {'title': 'Leon', 'year': '1994'},
# {'title': 'Mahjong', 'year': '1996'},
# {'title': 'Swallowtail Butterfly', 'year': '1996'},
# {'title': 'King of Comedy', 'year': '1999'},
# {'title': 'Devils on the Doorstep', 'year': '1999'},
# {'title': 'WALL-E', 'year': '2008'},
# {'title': 'The Pork of Music', 'year': '2012'},
# ]
#
#
# # @app.route('/index')
# # @app.route('/')
# # def hello():
# #     return 'welcome to my flask'
# # 视图函数的名称是可以随意的
#
#
# @app.route('/')
# def index():
#     return render_template('index.html', name=name, movies=movies)
#
# # 可以把参数传入到视图函数中
# @app.route('/user/<name>')
# def user_page(name):
#     return 'User:%s' % name
#
# @app.route('/test')
# def test_url_for():
# # 下面是一些调用示例（请在命令行窗口查看输出的 URL）：
#     print(url_for('index')) # 输出：/
# # 注意下面两个调用是如何生成包含 URL 变量的 URL 的
#     print(url_for('user_page', name='greyli')) # 输出：/user/greyli
#     print(url_for('user_page', name='peter')) # 输出：/user/peter
#     print(url_for('test_url_for')) # 输出：/test
# # 下面这个调用传入了多余的关键字参数，它们会被作为查询字符串附加到 URL后面。
#     print(url_for('test_url_for', num=2)) # 输出：/test?num=2
#     return 'Test page'


# -*- coding: utf-8 -*-
import os
from flask import Flask, request, url_for, send_from_directory
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.getcwd()
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


html = '''
    <!DOCTYPE html>
    <title>Upload File</title>
    <h1>图片上传</h1>
    <form method=post enctype=multipart/form-data>
         <input type=file name=file>
         <input type=submit value=上传>
    </form>
    '''


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_url = url_for('uploaded_file', filename=filename)
            return html + '<br><img src=' + file_url + '>'
    return html


if __name__ == '__main__':
    app.run()