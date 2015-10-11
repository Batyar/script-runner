from flask import Flask, flash, redirect, url_for, request, get_flashed_messages, render_template, session
from flask.ext.login import LoginManager, current_user, login_user, logout_user, login_required
from flask.ext.bcrypt import check_password_hash
from models import *

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = 'pcduino'

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/scripts')
def scripts():
    if current_user.is_authenticated:
        current_user.clear_scripts()
        db.session.commit()
        return render_template('scripts.html')

@app.route('/add_script', methods=['GET', 'POST'])
def add_script():
    if current_user.is_authenticated:
        if request.method == 'POST':
            user = User.find_by_name(request.form['username'])
            Script(request.form['scriptname'], request.form['arguments'], user).save()
            return redirect(url_for('scripts'))
        else:
            users = User.query.all()
            return render_template('add_script.html', users=users)

@app.route('/scripts/<int:id>', methods=['POST'])
def run_script(id):
    script = Script.query.get(id)
    if current_user.id == script.user_id:
        current_user.run(script)
        return redirect(url_for('scripts'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.find_by_name(request.form['username'])
        try:
            check_password_hash(user.password, request.form['password'])
            login_user(user)
            return redirect(url_for('scripts'))
        except ValueError:
            flash('Username or password incorrect')
            return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
