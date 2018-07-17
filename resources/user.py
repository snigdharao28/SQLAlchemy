from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument('username',
		type=str,
		required=True,
		help="this field cannot be left blank."
	)
	parser.add_argument('password',
		type=str,
		required=True,
		help="this field cannot be left blank."
	)


	def post(self):
		data = UserRegister.parser.parse_args()

		if UserModel.find_by_username(data['username']):
			return {'message':'a user with that username already exists.'}, 400

		user = UserModel(**data)
		user.save_to_db()

		return {"message": "user created successfully."}, 201


class User(Resource):
	@classmethod
	def get(cls, user_id: int):
		user = UserModel.find_by_id(user_id)
		if not user:
			return {'message': 'User Not Found'}, 404
		return user.json(), 200

	@classmethod
	def delete(cls, user_id: int):
		user = UserModel.find_by_id(user_id)
		if not user:
			return {'message':'User Not Found'}, 404
		user.delete_from_db()
		return {'message':'User Deleted.'}, 200