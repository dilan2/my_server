import errno
import os
import signal
import socket
import configparser
import time

SERVER_ADDRESS = (HOST, PORT) = '', 9999
REQUEST_QUEUE_SIZE = 1024


class Server:

    def __init__(self):
        self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listen_socket.bind(SERVER_ADDRESS)
        self.listen_socket.listen(REQUEST_QUEUE_SIZE)
        print('Serving HTTP on port {port} ...'.format(port=PORT))

        self.config = configparser.ConfigParser()
        self.config.read(os.path.join(".", "conf", "localhost.conf"))

        signal.signal(signal.SIGCHLD, self.grim_reaper)

    def serve_forever(self):

        while True:
            try:
                client_connection, client_address = self.listen_socket.accept()
                client_connection.setblocking(0)
            except IOError as e:
                code, msg = e.args
                # restart 'accept' if it was interrupted
                if code == errno.EINTR:
                    continue
                else:
                    raise

            pid = os.fork()
            if pid == 0:  # child
                self.listen_socket.close()  # close child copy
                self.handle_request(client_connection)
                client_connection.close()
                os._exit(0)
            else:  # parent
                client_connection.close()  # close parent copy and loop over

    def __get_data(self, client_connection):
        timeout = 2
        total_data = []
        data = ''
        begin = time.time()

        while True:
            if total_data and time.time() - begin > timeout:
                break

            elif time.time() - begin > timeout*2:
                break

            try:
                data = client_connection.recv(1024).decode()
                if data:
                    total_data.append(data)
                    begin = time.time()
                else:
                    time.sleep(0.1)
            except Exception:
                pass
                # print("socket error: " + str(e))

        return ''.join(total_data)

    def handle_request(self, client_connection):
        # request = client_connection.recv(1024)
        request = self.__get_data(client_connection)
        print(request)
        data_list = request.split("\r\n")
        headers, msg_body = self.__get_headers_and_body(data_list)
        print("HEADERS: ")
        print(headers)
        print('MESSAGE')
        print(msg_body)
        host = headers["Host"]
        no_port_host = host.split(':')[0]
        self.directory = self.config.get(no_port_host, "Directory")
        answer = getattr(self, '_handle_{}'.format(
            headers["method"].lower()))(headers, msg_body)
        print("ANSWER")
        print(answer)
        client_connection.send(answer.encode())

    def __get_headers_and_body(self, data_list):
        print('DATA_LIST:')
        print(data_list)
        headers = {}
        msg_body = ""
        headers["method"], headers["uri"], headers["version"] = \
            data_list[0].split()
        for header in data_list[1:]:
            if header != "":
                if ": " in header:
                    header_name, header_value = header.split(": ")
                    headers[header_name] = header_value
                else:
                    msg_body += header + "\r\n"
        return headers, msg_body

    def _handle_get(self, headers, msg_body):
        print('HANDLING GET...')
        status_code = 404
        message = "Not Found"
        answer_body = ""
        if "?" in headers["uri"]:
            uri_file, uri_params = headers["uri"].split("?")
        else:
            uri_file, uri_params = headers["uri"], ''
        if uri_file in ["/", "/index", "/index.html"]:
            if os.path.exists(os.path.join(self.directory, "index.html")):
                status_code = 200
                message = "OK"
                with open(os.path.join(self.directory,
                                       "index.html")) as indexfile:
                    answer_body = "".join(indexfile.readlines())
                    answer_body = \
                        answer_body.format(data=uri_params.replace("&", "\n"))
        else:
            path = os.path.join(*uri_file.split("/")[1:])
            if os.path.exists(os.path.join(self.directory, path)):
                status_code = 200
                message = "OK"
                with open(os.path.join(self.directory, path)) as answerfile:
                    answer_body = "".join(answerfile.readlines())
                    answer_body = \
                        answer_body.format(data=uri_params.replace("&", "\n"))
        hh = "Content-type: text/html"
        answer_headers = "{version} \
        {status_code} \
            {message}\n{headerss}\n\n".format(
                version=headers["version"],
                status_code=status_code,
                message=message,
                headerss=hh)
        answer = answer_headers + answer_body
        return answer

    def _handle_post(self, headers, msg_body):
        status_code = 404
        message = "Not Found"
        answer_body = ""
        uri_file, uri_params = headers["uri"], msg_body
        if uri_file in ["/", "/index", "/index.html"]:
            if os.path.exists(os.path.join(self.directory, "index.html")):
                status_code = 200
                message = "OK"
                with open(os.path.join(self.directory,
                                       "index.html")) as indexfile:
                    answer_body = "".join(indexfile.readlines())
                    answer_body = \
                        answer_body.format(data=uri_params.replace("&", "\n"))
        else:
            path = os.path.join(*uri_file.split("/")[1:])
            if os.path.exists(os.path.join(self.directory, path)):
                status_code = 200
                message = "OK"
                with open(os.path.join(self.directory, path)) as answerfile:
                    answer_body = "".join(answerfile.readlines())
                    answer_body = \
                        answer_body.format(data=uri_params.replace("&", "\n"))
        hh = "Content-type: text/html"
        answer_headers = "{version} \
            {status_code}\
            {message}\n{headerss}\n\n".format(
            version=headers["version"],
            status_code=status_code,
            message=message,
            headerss=hh)
        answer = answer_headers + answer_body
        return answer

    def grim_reaper(self, signum, frame):
        while True:
            try:
                pid, status = os.waitpid(
                    -1,          # Wait for any child process
                    os.WNOHANG  # Do not block and return EWOULDBLOCK error
                )
            except OSError:
                return

            if pid == 0:  # no more zombies
                return


if __name__ == '__main__':
    Server().serve_forever()
