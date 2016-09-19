#https://impythonist.wordpress.com/2015/07/12/build-an-api-under-30-lines-of-code-with-python-and-flask/

from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from json import dumps
import json
import requests
from flask import Response



app = Flask(__name__)
api = Api(app)


class GetSimilarItem_byId(Resource):
    def get(self):
        print("hete")
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str)
        parser.add_argument('query', type=str)
        args = parser.parse_args()
        id = args['id']
        query = args['query']
        print(args)
        
        from flask import Response
        #resp = Response(response=dfSuggest[1:int(count)].reset_index().to_json(orient='records'), status=200, mimetype="application/json")
        
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp        

api.add_resource(GetSimilarItem_byId, '/semsearch/get', endpoint = 'get')

if __name__ == '__main__':
    app.run()

