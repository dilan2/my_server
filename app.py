from my_server import Server

import sys
sys.path.append('.')


server = Server()
import controllers
print(Server.routes)

if __name__ == '__main__':
    server.serve_forever()
