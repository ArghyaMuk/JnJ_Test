from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
import os
from flask import Flask, redirect, url_for, session, jsonify

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
oauth = OAuth(app)


oauth.register(
    name = 'google',
    client_id = os.getenv('Google_Client_ID'),
    client_secret = os.getenv('Google_Client_Secret'),
    server_metadata_url = 'https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs = {'scope':"openid email profile"}   
)
# print("Google Client ID:", os.getenv('Google_Client_ID'))
# print("Google Client Secret:", os.getenv('Google_Client_Secret'))

@app.route('/login')
def login():
    redirect_uri = url_for('auth', _external=True)
  #  print("Client ID:", os.getenv("Google_Client_ID"))
    print("Redirect URI:", url_for('auth', _external=True))
    return oauth.google.authorize_redirect(redirect_uri)
  

@app.route('/auth')
def auth():
    token = oauth.google.authorize_access_token()
    return jsonify(token['userinfo'])






if __name__ == '__main__':
    app.run(debug=True)

