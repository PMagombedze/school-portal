from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import JWTManager, get_jwt_identity, create_access_token, jwt_required
from models import *


jwt = JWTManager()
api = Api()

"""
login using email and password
"""
class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        parser.add_argument('role', type=str, help='Role is required')
        args = parser.parse_args()

        if not args['email'] or not args['password'] or not args['role']:
            return {'message': 'Email, password, and role are required'}, 400

        user = User.query.filter_by(email=args['email']).first()
        if user and user.check_password(args['password']):
            access_token = create_access_token(identity=args['email'])
            return {'message': 'success', 'access_token': access_token,
                    'role': args['role'], 'id': user.id}, 200
        elif not user:
            new_user = User(email=args['email'], role=args['role'])
            new_user.set_password(args['password'])
            db.session.add(new_user)
            db.session.commit()
            access_token = create_access_token(identity=args['email'])
            return {'message': 'success', 'access_token': access_token, 'role': args['role'], 'id': user.id}, 201
        else:
            return {'message': 'Invalid credentials'}, 401

"""Teacher submit marks for subjects
"""
class SubmitMarks(Resource):
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('student_id', type=int, required=True)
        parser.add_argument('subject_id', type=int, required=True)
        parser.add_argument('score', type=int, required=True)
        args = parser.parse_args()
        user_id = get_jwt_identity()
        user = User.query.filter_by(email=user_id).first()
        if user.role == 'teacher':
            mark = Mark(student_id=args['student_id'], subject_id=args['subject_id'], teacher_id=user.id, score=args['score'])
            db.session.add(mark)
            db.session.commit()
            return {'message': 'success'}, 201
        else:
            return {'message': 'Unauthorized'}, 401


api.add_resource(SubmitMarks, '/api/marks')
api.add_resource(Login, '/api/auth')