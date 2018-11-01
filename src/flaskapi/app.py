import pandas as pd
from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
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
        return data.head().to_html()


api.add_resource(GetHead, '/data_head')

# TODO: Have a GET method which takes the name of a column and returns the top 20 rows of that column


class GetTopTwenty(Resource):
    def get(self,colname):
        mylog.info('Getting the top 20 rows of ' + colname)
        return data[colname].head(20).to_frame().to_html()


api.add_resource(GetTopTwenty, '/data/<string:colname>')

# # TODO: GET on route 'data_airlines' which takes an airline name (e.g. 'AA') and returns cols/rows for it


class GetAirline(Resource):
    def get(self,airline_name):
        mylog.info('Getting all the data for ' + airline_name)
        return data[data['AIRLINE'].astype('str') == airline_name].to_html()


api.add_resource(GetAirline, '/airline/<string:airline_name>')


# TODO: POST method to update the an airline code of choice to another code, as long as it's 2 chars


class PostCode(Resource):
    def post(self,airline_code):
        args = parser.parse_args()
        mylog.info('Changing airline code for ' + airline_code + ' to ' + args['AIRLINE'])
        data.loc['AIRLINE'] = args['AIRLINE']
        return data.head().to_html()


api.add_resource(PostCode, '/airlineswap/<string:airline_code>')

# TODO: Input-validate your inputs in the POST request


# TODO: Apply marshalling to your endpoints


# TODO: Convert the responses of the API into JSON format


# TODO: Implement the api to authorize the user with an API_KEY


# TODO: Create swagger documentation your api


# TODO: Make the API production-ready (not just dev version) and serve with a WSGI server

app.run(port=5000)