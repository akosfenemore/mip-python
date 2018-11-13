from collections import OrderedDict
import pandas as pd
from flask import Flask, jsonify, request, make_response
# from flask_restful import Resource, Api, reqparse
from flask_restplus import Api, reqparse, Resource, fields

from src.logexception.logframework import CustomLogger

mylog = CustomLogger().logger

data = pd.read_csv('/Users/akofenem/PycharmProjects/mip-python/data/flights.csv')

app = Flask(__name__)
api = Api(app)


parser = reqparse.RequestParser()
parser.add_argument('AIRLINE')


class GetHead(Resource):
    def get(self):
        mylog.info('Getting head of data')
        return make_response(data.head().to_csv())
        #return jsonify(data.head())


api.add_resource(GetHead, '/data_head')

# TODO: Have a GET method which takes the name of a column and returns the top 20 rows of that column


class GetTopTwenty(Resource):
    def get(self,colname):
        mylog.info('Getting the top 20 rows of ' + colname)
        # return data[colname].head(20).to_frame().to_html()
        return make_response(data[colname].head(20).to_frame().to_csv())


api.add_resource(GetTopTwenty, '/data/<string:colname>')

# # TODO: GET on route 'data_airlines' which takes an airline name (e.g. 'AA') and returns cols/rows for it


class GetAirline(Resource):
    def get(self,airline_name):
        mylog.info('Getting all the data for ' + airline_name)
        # return data[data['AIRLINE'].astype('str') == airline_name].to_html()
        return make_response(data[data['AIRLINE'].astype('str') == airline_name].to_csv())


api.add_resource(GetAirline, '/airline/<string:airline_name>')


# TODO: POST method to update the an airline code of choice to another code, as long as it's 2 chars


class PostCode(Resource):
    def post(self,airline_code):
        args = parser.parse_args()
        if len(args['AIRLINE']) == 2:
            mylog.info('Changing airline code for ' + airline_code + ' to ' + args['AIRLINE'])
            data['AIRLINE'][data['AIRLINE'] == airline_code] = args['AIRLINE']
            return make_response(data.head().to_csv())
        else:
            mylog.info('String entered was not the right length')
            return "Please replace with a two character name"


api.add_resource(PostCode, '/airlineswap/<string:airline_code>')

# TODO: Input-validate your inputs in the POST request




# TODO: Apply marshalling to your endpoints

#
# model = api.model('Model', {
#     'task': fields.String,
#     'uri': fields.Url('todo')
# })
#
#
# class TodoDao(object):
#     def __init__(self, todo_id, task):
#         self.todo_id = todo_id
#         self.task = task
#
#         # This field will not be sent in the response
#         self.status = 'active'
#
#
# @api.route('/todo')
# class Todo(Resource):
#     @api.marshal_with(model)
#     def get(self, **kwargs):
#         return TodoDao(todo_id='my_todo', task='Remember the milk')



# TODO: Convert the responses of the API into JSON format




# TODO: Implement the api to authorize the user with an API_KEY


# TODO: Create swagger documentation your api
#
# @api.route('/my-resource/<id>', endpoint='my-resource')
# @api.doc(params={'id': 'An ID'})
# class MyResource(Resource):
#     def get(self, id):
#         return {}
#
#     @api.doc(responses={403: 'Not Authorized'})
#     def post(self, id):
#         api.abort(403)


# TODO: Make the API production-ready (not just dev version) and serve with a WSGI server



app.run(port=5000)