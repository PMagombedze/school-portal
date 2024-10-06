from flask import Blueprint, render_template

dash = Blueprint('dash', __name__)

@dash.route('/dashboard')
def dashboard():
    return render_template('dash.html')
