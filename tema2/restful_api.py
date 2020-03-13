from pymongo import MongoClient
from bson.json_util import dumps, loads
from bson.objectid import ObjectId
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
import re

# https://docs.python.org/3/library/http.server.html
# https://api.mongodb.com/python/current/api/pymongo/results.html
# https://stackoverflow.com/questions/18444395/basehttprequesthandler-with-custom-instance
# https://thekondor.blogspot.com/2013/05/pass-arguments-to-basehttprequesthandler.html
config = os.path.join(os.path.dirname(__file__), 'mongo_config.json')
username, password = None, None
with open(config) as f:
    data = json.load(f)
    username = data['username']
    password = data['password']


cluster = MongoClient("mongodb+srv://{}:{}@ccrestfulapi-aalew.mongodb.net/test?retryWrites=true&w=majority".format(username, password))

db = cluster['cloudcomputing']
collection = db['cars']

HOST = '127.0.0.1'
PORT = 5000


class HttpRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if re.fullmatch('/cars/?', self.path):
            self.get_cars_collection()
        elif re.fullmatch('/cars/\w+/?', self.path):
            id = self.path.split('/')[2]
            self.get_car_by_id(id)

    def get_cars_collection(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/json')
        self.end_headers()

        query_cursor = collection.find()
        
        self.wfile.write(dumps(query_cursor).encode())

    def get_car_by_id(self, car_id):
        try:
            query = collection.find_one({'_id': ObjectId(car_id)})
            if len(query) == 0:
                raise Exception('Invalid CarId')

            self.send_response(200)
            self.send_header('Content-Type', 'text/json')
            message = dumps(query).encode()
        except Exception:
            self.send_response(404)
            self.send_header('Content-Type', 'text/plain')
            message = 'Error 404: CarId {} not found or invalid'.format(car_id).encode()
        finally:
            self.end_headers()
            self.wfile.write(message)


    # Reintorci ID-ul noii resurse
    def do_POST(self):
        if re.fullmatch('/cars/?', self.path):
            self.post_cars_collection()
        elif re.fullmatch('/cars/\w+/?', self.path):
            id = self.path.split('/')[2]
            self.post_car_by_id(id)

    def post_cars_collection(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data_dict = loads(post_data.decode())

            result = collection.insert_one(data_dict)

            self.send_response(201)
            self.send_header('Content-Type', 'text/plain')
            self.send_header('Location', '{}:{}/cars/{}'.format(HOST, PORT, result.inserted_id))
        except Exception:
            self.send_response(500)
        finally:
            self.end_headers()


    def post_car_by_id(self, car_id):
        self.send_response(501)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        
        message = 'Error 501: Not Implemented!'
        self.wfile.write(message.encode())

    # Reintorci resursa modificata
    def do_PUT(self):
        if re.fullmatch('/cars/?', self.path):
            self.put_cars_collection()
        elif re.fullmatch('/cars/\w+/?', self.path):
            id = self.path.split('/')[2]
            self.put_car_by_id(id)

    def put_cars_collection(self):
        self.send_response(405)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        
        message = 'Error 405: Method not allowed!'
        self.wfile.write(message.encode())

    def put_car_by_id(self, car_id):
        try:
            content_length = int(self.headers['Content-Length'])
            put_data = self.rfile.read(content_length)
            data_dict = loads(put_data.decode())

            myquery = collection.find_one({'_id': ObjectId(car_id)})
            if myquery:
                newvalues = { "$set": data_dict }
            else:
                raise Exception('CarId not found or invalid')

            res = collection.update_one(myquery, newvalues)

            # print(res.matched_count)
            if res.matched_count == 1:
                self.send_response(200)
                self.send_header('Content-Type', 'text/json')
                myquery = collection.find_one({'_id': ObjectId(car_id)})
                message = dumps(myquery)
            else:
                raise Exception("Update failed")

        except Exception:
            self.send_response(404)
            self.send_header('Content-Type', 'text/plain')
            message = 'Error 404: CarId not found or invalid'
        finally:
            self.end_headers()
            self.wfile.write(message.encode())
            

    def do_DELETE(self):
        if re.fullmatch('/cars/?', self.path):
            self.delete_cars_collection()
        elif re.fullmatch('/cars/\w+/?', self.path):
            id = self.path.split('/')[2]
            self.delete_car_by_id(id)

    def delete_cars_collection(self):
        self.send_response(405)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        
        message = 'Error 405: Method not allowed!'
        self.wfile.write(message.encode())

    def delete_car_by_id(self, car_id):
        try:
            query = collection.delete_one({'_id': ObjectId(car_id)})
            if query.deleted_count == 0:
                raise Exception("Entry with CarId {} not found".format(car_id))
            
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            message = 'Entry with CarId {} was successfully deleted'.format(car_id)
        except Exception:
            self.send_response(404)
            message = 'Error 404: CarId not found or invalid'
        finally:
            self.end_headers()
            self.wfile.write(message.encode())


if __name__ == '__main__':
    try:
        server_address = (HOST, PORT)
        server = HTTPServer(server_address, HttpRequestHandler)
        server.serve_forever()
    except:
        print('Server connection closed')
