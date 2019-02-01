from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from util.database_io import get_available_data



# Flask initialisieren
app = Flask(__name__)
cors = CORS(app, resources={r"/users/*": {"origins": "*"}}) 
api = Api(app)

'''
    Diese Klasse nimmt einen GET-Request entgegen, parsed parameter
    und führt die Datenabfrage durch. Wenn Daten verfügbar sind
    wird mit dem Status-Code 200 geantwortet, wenn nicht 202.
    So kann am Frontend unterschieden werden on es ein Lade-Symbol
    anzeigen soll oder nicht.
'''
class Users(Resource):
    def get(self, username):
        # Limit parameter mit dem RequestParser auslesen
        parser = reqparse.RequestParser()
        parser.add_argument('limit', type=int)
        args = parser.parse_args()
        limit = args['limit']

        response, is_available = get_available_data(username, limit)
        if is_available:
            return response
        else:
            return response, 202

# Ressourcen/URI's zuordnen
api.add_resource(Users, '/users/<string:username>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')