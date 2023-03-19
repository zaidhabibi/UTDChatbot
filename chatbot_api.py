from flask import Flask, request
from flask_restful import Resource, Api
from chatbot import Chatbot
from flask_cors import CORS


app = Flask(__name__)
api = Api(app)
# allow Cross-Origin information sharing
CORS(app)

class chatbot_api(Resource):
    
    def __init__(self):
        self.chatbot = Chatbot("utd_web_data.csv", "text-embedding-ada-002")
    
    def get(self):
        return {'message': 'Please send POST request to this endpoint.'}
    
    def post(self):
        user_input = request.json['user_input']
        response = self.chatbot.search_routine(user_input)
        return {'message': response}
    
api.add_resource(chatbot_api, '/chatbot')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port = 5000, debug = False)



