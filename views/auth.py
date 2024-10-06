from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)

@auth.route('/')
def authboard():
    return render_template('auth/auth.html')
