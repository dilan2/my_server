import os
import json


class Response:
    def __init__(self, version, directory, client_connection):
        self.directory = directory
        self.client_connection = client_connection
        self.status_code = 404
        self.version = version
        self.message = 'Not found'

    def send_file(self, path, context):
        if os.path.exists(os.path.join(self.directory, path)):
            self.status_code = 200
            self.message = "OK"
            with open(os.path.join(self.directory, path)) as answerfile:
                answer_body = "".join(answerfile.readlines())
                answer_body = \
                    answer_body.format(data=context)
        hh = "Content-type: text/html"
        answer_headers = "{version} \
        {status_code} \
            {message}\n{headerss}\n\n".format(
                version=self.version,
                status_code=self.status_code,
                message=self.message,
                headerss=hh)
        answer = answer_headers + answer_body
        self.client_connection.send(answer.encode())

    def send_data(self, data):
        hh = "Content-type: text/html"
        answer_headers = "{version} \
        {status_code} \
            {message}\n{headerss}\n\n".format(
                version=self.version,
                status_code=200,
                message='OK',
                headerss=hh)
        answer = answer_headers.encode() + data.encode()
        self.client_connection.send(answer)

    def __repr__(self):
        return 'Status: ' + str(self.status_code)

    def send_json(self, data):
        hh = "Content-type: text/html"
        answer_headers = "{version} \
        {status_code} \
            {message}\n{headerss}\n\n".format(
                version=self.version,
                status_code=200,
                message='OK',
                headerss=hh)
        answer = answer_headers.encode() + json.dumps(data).encode()
        self.client_connection.send(answer)
