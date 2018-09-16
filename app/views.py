from main import app
from models import *
from flask import render_template, request, flash, session, redirect, url_for

import docker


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/registerForm', methods=['POST'])
def registerForm():
    user = User(request.form['username'], request.form['email'], request.form['password'])
    db.session.add(user)    # add user to database
    db.session.commit()     # update database
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/loginForm', methods=['GET', 'POST'])
def loginForm():
    error = ''
    try:
        if request.method == 'POST':
            attempted_username = request.form['username']
            attempted_password = request.form['password']
            # if attempted_username == 'test2' and attempted_password == 'test2':

            username = User.query.filter_by(username=attempted_username).first()
            password = User.query.filter_by(password=attempted_password).first()

            if username and password:
                session['logged_in'] = True
                session['current_username'] = attempted_username
                return redirect(url_for('profile', username=session['current_username']))
                #return render_template('profile.html', username=attempted_username)
                #return render_template('logged_in.html', error=error, username=attempted_username)
            else:
                error = 'Invalid username and password.'
                flash(error)
        else:
            error = 'Invalid request'
            return render_template('login.html', error=error)

        return render_template('login.html', error=error)

    except Exception as e:
        flash(e)
        return render_template('login.html', e=error)


@app.route('/logout')
def logout():
    session['logged_in'] = False
    return index()


@app.route('/profile/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first()
    return render_template('profile.html', username=user)


@app.route('/createContainer', methods=['GET', 'POST'])
def create_container():
    error = ''
    try:
        if request.method == 'POST':
            container_name = request.form['cont_name']
            try:
                client = docker.from_env()
                client.containers.run("alpine", ["echo", "hello", "world"])
                return render_template('profile.html', username=session['current_username'], error=error)
            except ContainerError as e:
                flash(e)
                return render_template('profile.html', username=session['current_username'], error=error)
            except ImageNotFound as e:
                flash(e)
                return render_template('profile.html', username=session['current_username'], error=error)
            except APIError as e:
                flash(e)
                return render_template('profile.html', username=session['current_username'], error=error)
            except Exception as e:
                flash(e)
                return render_template('profile.html', username=session['current_username'], error=error)
            except builtins.TypeError as e:
                flash(e)
                return render_template('profile.html', username=session['current_username'], error=error)
        else:
            error = 'Invalid request'
            return render_template('profile.html', username=session['current_username'], error=error)


    except Exception as e:
        flash(e)
        #return redirect(request.url)
        return render_template('profile.html', username=session['current_username'], error=error)


@app.route('/console', methods=['GET'])
def open_console():
    return render_template('terminal.html')


@app.route('/start-xterm')
def start_xterm_server():
    try:
        from terminal import run
        run()
    except ImportError:
        raise ImportError('Import module failed.')
