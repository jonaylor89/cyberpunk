
import random
import requests

host = random.choice((requests.get('https://api.audius.co')).json()['data'])