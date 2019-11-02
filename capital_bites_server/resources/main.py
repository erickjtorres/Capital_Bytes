from flask_restful import Resource
import gunicorn

class Main(Resource):
  def get(self):
    return {'Hello': 'Welcome to Capital One API!'}