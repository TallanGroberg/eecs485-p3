"""Login page for the photo sharing app."""
import flask
from flask import request,Response, redirect, session, make_response, jsonify
import insta485
from insta485.views.accounts.check_password import check_password
import base64
from functools import wraps


@insta485.app.route('/accounts/login/', methods=['GET', 'POST'])
def show_login():
    """Display /accounts/login."""
    print("hit login")
    if request.method == 'POST':
        print("going into post")
        return do_the_login(request)
    else:
        return show_the_login_form()


def do_the_login(request):
    """Handle the login process."""
    username = request.form.get('username')
    password = request.form.get('password')
    target = request.args.get('target')
    if check_credentials(username, password):
        return redirect(target or "/")
    else:
        return redirect("/accounts/login/")
    # Redirect to the desired page after successful login



def show_the_login_form():
    """Display /accounts/login form."""
    return flask.render_template("login.html")


@insta485.app.route('/accounts/logout/', methods=['GET', 'POST'])
def do_logout():
    """Logout the user."""
    # Remove the username from the session if it's there
    flask.session.clear()
    response = make_response("Logout successful!", 200)

    return redirect('/accounts/login/')


def require_authentication(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        """Check if the user is authenticated."""
    
        if 'username' not in session and 'password' not in session:
            print(args)
            return jsonify({'message': 'Authentication required'}), 403
        
        # print(session.headers.get('Authorization'))
        # if auth_type.lower() != 'basic':
        #     return jsonify({'message': 'Invalid authentication mechanism'}), 403
        
        # credentials = base64.b64decode(credentials).decode('utf-8')

        # username, password = credentials.split(':')


        # if not check_credentials(username, password):
        #     return jsonify({'message': 'Invalid credentials'}), 403
        return f( *args, **kwargs)
    return decorated


def check_credentials(username, password):
    """Check if a username/password combination is valid."""
    print("In check credentials.\n")
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    )
    user = cur.fetchone()
    if(password == user['password']):
        print("passwords match")

    if (user == None) or check_password(user['password'], password):
        print("Invalid username or password.")
        return False

    print("Assigning username and password to session.\n")
    flask.session['username'] = user['username']
    flask.session['password'] = password
    print("leaving check credentials\n")
    return True
