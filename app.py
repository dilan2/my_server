from http_base.my_server import Server

import sys
sys.path.append('.')


server = Server()
import controllers

if __name__ == '__main__':
    server.serve_forever()
