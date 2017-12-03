import sys
sys.path.append('..')
from app import server


@server.register('/')
def index(request, response):
    print('index function called')
    print(request)
    print(response)
    response.send_file('index.html', 'hello')
