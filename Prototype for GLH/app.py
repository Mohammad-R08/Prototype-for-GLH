"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

import sqlite3
from flask import Flask, flash, render_template, request, url_for, redirect
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'B7jmSpix_aDo6dcGDswL-g'
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, forename, surname, account_type, address, email, password):
        self.id = str(id)
        self.forename = forename
        self.surname = surname
        self.account_type = account_type
        self.address = address
        self.email = email
        self.password = password


@login_manager.user_loader
def load_user(id):
    conn = sqlite3.connect('accounts.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM accounts where id = (?)', [id])
    lu = cur.fetchone()
    if lu is None:
        return None
    else:
        return User(int(lu[0]), lu[1], lu[2], lu[3], lu[4], lu[5], lu[6])






# conn = sqlite3.connect('accounts.db')
# cur = conn.cursor()

# cur.execute('create table accounts (id integer not null primary key autoincrement, forename text not null, surname text not null, account_type integer not null, address text, email text not null, password text not null)')

# conn.commit()
# cur.close()



# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app




@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')



@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        
        app.logger.warning('asdasdasddsadsasaddsasd')
        forename =   request.form.get('forename').capitalize()
        surname = request.form.get('surname').capitalize()
        account_type = request.form.get('account_type')
        email = request.form.get('email')
        hashed_pass = bcrypt.generate_password_hash(request.form.get('password'))
        conn = sqlite3.connect('accounts.db')
        cur = conn.cursor()
        cur.execute('INSERT INTO Accounts (forename,surname,account_type,email,password) VALUES(?,?,?,?,?)', (forename, surname, account_type, email, hashed_pass))
        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for('home'))

    return render_template('register.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        conn = sqlite3.connect('accounts.db')
        cur = conn.cursor()
        email = request.form.get('email')
        password = request.form.get('password')
        cur.execute('SELECT * FROM accounts where email = (?)', [email])
        user = list(cur.fetchone())
        user_obj = load_user(user[0])
        if email == user_obj.email and bcrypt.check_password_hash(user_obj.password, password):
            login_user(user_obj, remember = request.form.get('remember'))

        return redirect(url_for('user_dashboard'))

    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/forgotpassword')
def forgot_password():
    return render_template('forgotpassword.html')

@app.route('/resetpassword')
def reset_password():
    return render_template('resetpassword.html')



@app.route('/userdashboard')
@login_required
def user_dashboard():
    return render_template('userdashboard.html')

@app.route('/producerdashboard')
def producer_dashboard():
    return render_template('producerdashboard.html')

@app.route('/addproduct')
def reset_pass():
    return render_template('addproduct.html')



@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/order')
def order():
    return render_template('order.html')





if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
