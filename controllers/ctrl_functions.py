import sys
sys.path.append('..')
from app import server


# @server.register('/')
# def index(request, response):
#     print('index function called')
#     print(request)
#     print(response)
#     response.send_file('index.html', 'hello')



@server.register('/')
class IndexController:
    def __init__(self):
        print('IndexControllerInit')

    def get(self, request, response):
        print('IndexController get func')
        print('RRRREEEEQQQQ: ')
        print(request)
        response.send_file('index.html', 'hello')

    def __repr__(self):
        return 'FROM INSEX CTRL'
