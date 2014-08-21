from rauth import OAuth1Service
 
try:
    read_input = raw_input
except NameError:
    read_input = input
 
yahoo = OAuth1Service(
    name='yahoo',
    consumer_key='consumer_key',
    consumer_secret='consumer_secret',
    request_token_url='https://api.login.yahoo.com/oauth/v2/get_request_token',
    access_token_url='https://api.login.yahoo.com/oauth/v2/get_token',
    authorize_url='https://api.login.yahoo.com/oauth/v2/request_auth',
    base_url='http://fantasysports.yahooapis.com/fantasy/v2/',
)
 
params = {'oauth_callback': 'oob'}
request_token, request_token_secret = yahoo.get_request_token(params={'oauth_callback': 'oob'})
 
authorize_url = yahoo.get_authorize_url(request_token)
 
print('Visit this URL in your browser: {url}'.format(url=authorize_url))
pin = read_input('Enter PIN from browser: ')
 
session = yahoo.get_auth_session(request_token,
                                   request_token_secret,
                                   method='POST',
                                   data={'oauth_verifier': pin})
 
params = {}
 
r = session.get('users;use_login=1/games', params=params, verify=True)
 
print(r.content)

