from flask_restful import Resource, reqparse 
from resources.helper.post_twilio import subscribe_to_twilio

#https://[heroku_url]/favorites?companyName=apple&phoneNumber=%2b13124785453

parser = reqparse.RequestParser()
parser.add_argument('companyName', type=str)
parser.add_argument('phoneNumber', type=str)


class Favorites(Resource):
  def get(self):
    args = parser.parse_args()
    company_name = args['companyName']
    phone_number = args['phoneNumber']
    subscribe_to_twilio(phone_number, company_name)
    return {'success': 'Text has been sent! Thank you very much!'}