from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import JWTManager, create_access_token
from models import *


jwt = JWTManager()
api = Api()


"""login using email and password
"""
class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        parser.add_argument('role', type=str, required=True)
        args = parser.parse_args()

        if not args['email'] or not args['password'] or not args['role']:
            return {'message': 'Email, password, and role are required'}, 400

        user = User.query.filter_by(email=args['email'], role=args['role']).first()
        if user and user.check_password(args['password']):
            access_token = create_access_token(identity=args['email'])
            return {'message': 'success', 'access_token': access_token,
                    'role': args['role'], 'id': user.id, 'email': user.email}, 200
        elif not user:
            new_user = User(email=args['email'], role=args['role'])
            new_user.set_password(args['password'])
            db.session.add(new_user)
            db.session.commit()
            access_token = create_access_token(identity=args['email'])
            return {'message': 'success', 'access_token': access_token, 'role': args['role'], 'id': new_user.id, 'email': user.email}, 201
        else:
            return {'message': 'Invalid credentials'}, 401
        

"""Teacher submit marks for subjects
"""
class SubmitMarks(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('student_id', type=int, required=True)
        parser.add_argument('subject_id', type=int, required=False)
        parser.add_argument('score', type=int, required=False)
        parser.add_argument('teacher_id', type=int, required=True)
        args = parser.parse_args()
        if not args['student_id'] or not args['teacher_id']:
            return {'message': 'Student ID and teacher ID are required'}, 400
        mark = Mark(student_id=args['student_id'], subject_id=args['subject_id'], score=args['score'], teacher_id=args['teacher_id'])
        db.session.add(mark)
        db.session.commit()
        return {'message': 'Marks submitted successfully'}, 201


"""Students
"""
class Students(Resource):
    def get(self):
        students = User.query.filter_by(role='student').all()
        return {'students': [{'email': student.email, 'id': student.id} for student in students]}, 200


class GetMarks(Resource):
    def get(self):
        students = User.query.filter_by(role='student').all()
        result = []
        for student in students:
            marks = Mark.query.filter_by(student_id=student.id).all()
            student_marks = {
                'student_id': student.id,
                'email': student.email,
                'marks': [{'subject_id': mark.subject_id, 'score': mark.score} for mark in marks]
            }
            result.append(student_marks)
        return {'students': result}, 200

api.add_resource(GetMarks, '/api/marks/all')
api.add_resource(Students, '/api/students')
api.add_resource(SubmitMarks, '/api/marks')
api.add_resource(Login, '/api/auth')