from hendlers import *

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = 'pcduino'

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)

@app.route('/')
def home():
    return render_template('scripts.html')

@app.route('/scripts')
def scripts():
    if current_user.is_authenticated:
        current_user.clear_scripts()
        db.session.commit()
        return render_template('scripts.html', root_path=os.getcwd())
    return flash_and_redirect('Not authorized')

@app.route('/add_script', methods=['GET', 'POST'])
def add_script():
    if current_user.is_authenticated:
        if request.method == 'POST':
            user = User.find_by_name(request.form['username'])
            if not request.form['scriptname']:
                flash('Script name can not be empty')
                return redirect(url_for('add_script'))
            else:
                Script(request.form['scriptname'], request.form['arguments'], user).save()
            return redirect(url_for('scripts'))
        else:
            users = User.query.all()
            return render_template('add_script.html', users=users)
    return flash_and_redirect('Not authorized')

@app.route('/scripts/<int:id>', methods=['POST'])
def run_script(id):
    script = Script.query.get(id)
    if current_user.id == script.user_id:
        script.arguments = request.form['arguments']
        if script.check_arguments():
            db.session.commit()
            current_user.run(script)
        else:
            flash('Incorrect arguments')
        return redirect(url_for('scripts'))
    return flash_and_redirect('Not authorized')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.find_by_name(request.form['username'])
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('scripts'))
        else:
            return flash_and_redirect('Username or password incorrect')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/files')
@login_required
def files():
    return split_folders_and_files('/')

@app.route('/files/<path:req_path>')
@login_required
def dir_listing(req_path):
    try:
        abs_path = '/' + req_path
        return handle_files(abs_path)
    except OSError:
        flash('Permission denied')
        return redirect(url_for('files'))

if __name__ == '__main__':
    app.run(debug=True)
