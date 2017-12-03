class Request:
    def __init__(self, data):
        self.data = data
        print("Inside Request Class")
        self.data_list = self.data.split("\r\n")
        self.__headers, self.__body = self.__get_headers_and_body()

    def __get_headers_and_body(self):
        print('DATA_LIST:')
        print(self.data_list)
        headers = {}
        msg_body = ""
        headers["method"], headers["uri"], headers["version"] = \
            self.data_list[0].split()
        for header in self.data_list[1:]:
            if header != "":
                if ": " in header:
                    header_name, header_value = header.split(": ")
                    headers[header_name] = header_value
                else:
                    msg_body += header + "\r\n"
        return headers, msg_body

    @property
    def headers(self):
        return self.__headers

    @property
    def body(self):
        return self.__body

    def __repr__(self):
        return 'Headers: {headers}, Body: {body}'.format(headers = self.headers,
                                                         body = self.body)
