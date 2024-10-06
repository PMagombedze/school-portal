from flask import Blueprint, render_template

dash = Blueprint('dash', __name__)

@dash.route('/teacher/dashboard/<string:id>')
def dashboard(id):
    return render_template('dash.html')


@dash.route('/student/dashboard/<string:id>')
def student(id):
    return render_template('student.html')