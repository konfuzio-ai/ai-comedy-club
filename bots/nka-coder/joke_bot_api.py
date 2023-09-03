from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from joke_bot import Bot

# creating the flask app
app = Flask(__name__)
api = Api(app)

# Resource to introduce the boot to the user
class Hello(Resource):
	def get(self):
		bot = Bot()
		return jsonify({"message": "Hello bro! \n I'm as AI comedian. ;-) \n My name is {}. I'm specialized on joke about: {}.".format(bot.name, bot.joke_categories),
		                "comedian": bot.name})

	def post(self):	
		data = request.get_json()	
		return jsonify({"data": data}), 201


# Resource to get bot name
class Name(Resource):
	def get(self):
		bot = Bot()
		return jsonify({"comedian": bot.name})

	def post(self):	
		data = request.get_json()	
		return jsonify({"data": data}), 201

# Resource to tell a joke
class tellJoke(Resource):
	def get(self,category="all"):
		bot = Bot()
		return jsonify({"message": bot.tell_joke(category.lower()), "comedian": bot.name})

	def post(self):	
		data = request.get_json()	
		return jsonify({"data": data}), 201

# Resource to rate a joke
class rateJoke(Resource):
	def get(self,joke):
		bot = Bot()
		return jsonify({"message": bot.rate_joke(joke), "comedian": bot.name})

	def post(self):	
		data = request.get_json()	
		return jsonify({"data": data}), 201

# Resource to feedback of a joke a joke
class collectJokeFeedback(Resource):
	def get(self,joke, rating):
		bot = Bot()
		bot.collect_feedback(joke, rating)
		return jsonify({"Message": "Thanks for the feedback. It helps me improve my skills."})

	def post(self):
		data = request.get_json()	
		return jsonify({"data": data}), 201


# adding the defined resources along with their corresponding urls
api.add_resource(Hello, '/')
api.add_resource(Name, '/comedian')
api.add_resource(tellJoke, '/tell-joke/<string:category>')
api.add_resource(rateJoke, '/rate-joke/<string:joke>')
api.add_resource(collectJokeFeedback, '/collect-feedback/<string:joke>/<int:rating>')


# driver function
if __name__ == '__main__':

	app.run(debug = True)
