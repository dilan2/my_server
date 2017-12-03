import sys
sys.path.append('..')
from app import server


@server.register('/')
def index(request):
    print('index function called')


