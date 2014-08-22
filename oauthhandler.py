from rauth import OAuth1Service
import json

NFL_GAME_KEY = 331
 
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
 
params = {'format':'json'}
 
#r = session.get('users;use_login=1/games', params=params, verify=True)
#game_key = fantasy['content_content']['users']['0']['user'][1]['games']['0']['game'][0]['game_key']
#leagues = session.get('users;use_login=1/games;game_keys={}/leagues'.format(NFL_GAME_KEY), params=params, verify=True)

teams = session.get('users;use_login=1/games;game_keys={}/teams'.format(NFL_GAME_KEY), params=params, verify=True)
 
team_json = json.loads(teams.content)
team_key = team_json['fantasy_content']['users']['0']['user'][1]['games']['0']['game'][1]['teams']['0']['team'][0][0]['team_key']

team = session.get('team/{}/roster/players'.format(team_key), params=params, verify=True)
print team.content
