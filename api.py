from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import JWTManager, get_jwt_identity, create_access_token, jwt_required
from models import *

api = Api()
jwt = JWTManager()

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
        user = User.query.filter_by(email=args['email']).first()
        if user and user.check_password(args['password']):
            access_token = create_access_token(identity=args['email'])
            return {'message': 'login successful', 'access_token': access_token, 'role': args['role']}, 200
        elif not user:
            new_user = User(email=args['email'], role=args['role'])
            new_user.set_password(args['password'])
            db.session.add(new_user)
            db.session.commit()
            access_token = create_access_token(identity=args['email'])
            return {'message': 'signup successful', 'access_token': access_token, 'role': args['role']}, 201
        else:
            return {'message': 'Invalid credentials'}, 401


api.add_resource(Login, '/api/auth')