import os
from flask import Flask
from flask_restful import reqparse, Api, Resource
import snscrape.modules.twitter as sntwitter
import requests
import pickle

url = "https://github.com/yousefhassan1999/depressionGuardPythonServer/releases/download/modelFile/pipeline.pkl"
filename = 'pipeline.pkl'

if not (os.path.isfile(filename)):
    print("Downloading...")
    r = requests.get(url, allow_redirects=True)
    open(filename, 'wb').write(r.content)

with open(filename, 'rb') as f:
    pipeline = pickle.load(f)

app = Flask(__name__)
api = Api(app)

parser1 = reqparse.RequestParser()
parser1.add_argument('Post',type=str,help="Post is required",required=True)

parser2 = reqparse.RequestParser()
parser2.add_argument('Username',type=str,help="Username is required",required=True)
parser2.add_argument('From',type=str,help="From is required",required=True)
parser2.add_argument('To',type=str,help="To is required",required=True)

class ModelPrediction(Resource):
    def get(self):
        args = parser1.parse_args()
        PostToPredict = args['Post']
        return pipeline(PostToPredict)
    
    
class GetUserTwittes(Resource):
    def get(self):
        args2 = parser2.parse_args()
        Username = args2['Username']
        From = args2['From']
        To = args2['To']
        tweets = []
        for tweet in sntwitter.TwitterSearchScraper(f'(from:{Username}) until:{To} since:{From}').get_items():
            tweets.append([tweet.id,tweet.rawContent])
            if len(tweets) > 5:
                break;
        return tweets
    
    
 
api.add_resource(ModelPrediction, '/predict')
api.add_resource(GetUserTwittes, '/GetUserTwittes')

if __name__ == '__main__':
    app.run(debug=True)