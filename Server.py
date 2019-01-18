# -*- coding: utf-8 -*-

# Imports
from flask import Flask
from flask_restful import Resource, Api, reqparse
from util.database_io import get_response



# Flask initialisieren
app = Flask(__name__)
api = Api(app)


class Users(Resource):
    def get(self, username):
        # Limit parameter mit dem RequestParser auslesen
        parser = reqparse.RequestParser()
        parser.add_argument('limit', type=int)
        args = parser.parse_args()
        limit = args['limit']

        response, is_available = get_response(username, limit)
        if is_available:
            return response
        else:
            return response, 202

# Ressourcen/URI's zuordnen
api.add_resource(Users, '/users/<string:username>')

if __name__ == '__main__':
    app.run(debug=True)