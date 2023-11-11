# an object of WSGI application
from flask import *  # Flask, redirect, url_for

app = Flask(__name__)  # Flask constructor


# A decorator used to tell the application
# which URL is associated function
@app.route('/')
def hello():
    return render_template("first.html")


@app.route('/admin')
def hello_admin():
    return 'Hello Admin!'


@app.route('/guest/<guest>')
def hello_guest(guest):
    return 'Hello %s as Guest!' % guest


# albo tak zamiast route:  app.add_url_rule('/', 'hello', hello_world)


@app.route('/user/<name>')
def hello_user(name):
    if name == 'admin':
        return redirect(url_for('hello_admin'))
    else:
        return redirect(url_for('hello_guest', guest=name))


@app.route('/login', methods=['POST'])
def login():
    user = request.form['name']
    return redirect(url_for('hello_user', name=user))


@app.route('/marks')
def student():
    return render_template("student.html")


@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form
        return render_template("result.html", result=result)


if __name__ == '__main__':
    app.run(debug=True)
