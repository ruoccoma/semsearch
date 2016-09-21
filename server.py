#https://impythonist.wordpress.com/2015/07/12/build-an-api-under-30-lines-of-code-with-python-and-flask/

from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from json import dumps
import json
import requests
from flask import Response
import Search
import pandas

app = Flask(__name__)
api = Api(app)
s = Search.Search();

class GetSimilarItem_byId(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str)
        parser.add_argument('query', type=str)
        args = parser.parse_args()
        id = args['id']
        query = args['query']
        print(args)
        res = s.get_nns_by_id(id,10)
        df = pandas.DataFrame(index = res[0], data = res[1])
        print(df)
        from flask import Response
        resp = Response(response=df.reset_index().to_json(orient='values'), status=200, mimetype="application/json");
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp        

api.add_resource(GetSimilarItem_byId, '/semsearch/get', endpoint = 'get')

if __name__ == '__main__':
    #app.run()
    app.run(host='0.0.0.0')

