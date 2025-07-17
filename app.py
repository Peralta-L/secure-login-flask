"""Main python File where it will
 assign the proper routes and pages"""
import socket
import re
from passlib.hash import sha256_crypt
from datetime import datetime
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
u = None
host = socket.gethostname()
local_ip = socket.gethostbyname(host)
d = datetime.now()
current_date = d.strftime("%m/%d/%Y")
current_time = d.strftime("%H:%M:%S")


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Route to log in html this function will read the file
    and make sure the file with hash info matches the user inputs"""
    global u
    if request.method == "POST":
        users = []
        file = open("info.txt", 'r')
        lines = file.readlines()
        file.close()
        for line in lines:
            username, passcode, _ = line.strip().split()
            users.append({'user': username, 'password': passcode})
        u = request.form['name']
        code = request.form['passcode']
        for user in users:
            info1 = user['user']
            info2 = user['password']
            user_check = sha256_crypt.verify(u, info1)
            pass_check = sha256_crypt.verify(code, info2)
            if user_check and pass_check:
                return render_template('lab6.html', user_name=u)
            else:
                pass
        with open('failed_login.txt', 'a') as f:
            f.writelines(f"{current_date}, {current_time}, {local_ip}\n")
        return render_template('login.html', wrong=False)
    else:
        return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Route to register html this function will create
    a new user, password, authentication and save them in a file"""
    if request.method == "POST":
        p = request.form['passcode']
        n = request.form['name']
        c = request.form['second']
        if complexity(p) and commonly(c):
            hash_user = sha256_crypt.hash(n)
            hash_pass = sha256_crypt.hash(p)
            if not checks(n):
                with open("info.txt", 'a') as f:
                    f.write(f"{hash_user} {hash_pass} {c}\n")
                    return redirect('/login')
            else:
                return render_template('register.html', notification=False,
                                       rules=complexity(p))
        else:
            return render_template('register.html', rules=complexity(p), passcode=commonly(c))
    else:
        return render_template('register.html', notification=True, rules=True)


@app.route('/change', methods=['GET', 'POST'])
def change():
    """Route to change html this function will change the password"""
    if request.method == "POST":
        new = request.form['new']
        old = request.form['password']
        if complexity(new):
            hash_old = sha256_crypt.hash(old)
            hash_new = sha256_crypt.hash(new)
            if replace(old, hash_new):
                return redirect('/login')
            else:
                return render_template('change.html', match=False, )
        else:
            return render_template('change.html', notification=False, )
    else:
        return render_template('change.html')


@app.route('/passcode', methods=['GET', 'POST'])
def pass_c():
    """Route to passcode html, this template will make sure
     that the authentication by the user is correct"""
    if request.method == "POST":
        global u
        info = []
        with open("info.txt", 'r') as f:
            lines = f.readlines()
        for line in lines:
            username, passcode, _ = line.strip().split()
            info.append({'user': username, 'password': passcode, 'pin': _})
        for i in info:
            info1 = i['user']
            info3 = i['pin']
            user_check = sha256_crypt.verify(u, info1)
            pass_code = request.form['passcode']
            if user_check and pass_code == info3:
                return redirect('/change')
            else:
                return render_template('passcode.html', warning=False)
    else:
        return render_template('passcode.html')


def complexity(p):
    """Sets up the standards for the passwords"""
    rules = True
    if not re.search(r'[A-Z]', p):
        rules = False
    if not re.search(r'[a-z]', p):
        rules = False
    if not re.search(r'\d', p):
        rules = False
    if not re.search(r'[@!"§$%&/()=?*+|><]', p):
        rules = False
    return rules


def checks(n):
    """Checks if the User is valid"""
    match = False
    with open("info.txt", 'r') as f:
        repeats = f.readlines()
        for r in repeats:
            user, passcode, _ = r.strip().split()
            match = sha256_crypt.verify(n, user)
            if match:
                return match
    return match


def commonly(c):
    """checks if any authentication is weak"""
    compromised = True
    with open("CommonPassword.txt", 'r') as f:
        commons = f.readlines()
    for common in commons:
        passcode = common.strip().split()
        word = passcode[0]
        if word == c:
            compromised = False
        else:
            pass
    return compromised


def replace(old, hash_new):
    """This function will change the old password to the new one"""
    match = False
    with (open("info.txt", 'r+') as f):
        repeats = f.readlines()
        for r in repeats:
            new, hash_old, _ = r.strip().split()
            match = sha256_crypt.verify(old, hash_old)
            if match:
                chang = r.replace(hash_old, hash_new)
                f.seek(0)
                f.write(chang)
                f.truncate()
                return match
            else:
                match = False
                pass
    return match


@app.route('/')
def menu():
    """1st Template for the page"""
    return render_template('question.html')


@app.route('/password', methods=['GET', 'POST'])
def password():
    """route 1"""
    b = None
    if request.method == "POST":
        if request.form['button'] == 'YES':
            return redirect('/login')
            pass
        elif request.form['button'] == 'NO':
            return redirect('/register')
            pass
    return render_template('question.html', b=b)


@app.route('/Time')
def time():
    """route 2, gets time"""
    return render_template('time.html', Time=current_time)


@app.route('/Date')
def date():
    """route 3 gets date"""
    return render_template('date.html', Date=current_date)


if __name__ == '__main__':
    app.run()
