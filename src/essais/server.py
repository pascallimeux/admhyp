import socketserver

params = ('127.0.0.1', 8808)


class MyTCPHandler(socketserver.StreamRequestHandler):
    def handle(self):
        raw_data=self.rfile.readline().strip().decode().split(":")
        if len(raw_data) == 1:
            command = ""
        else:
            command , params = raw_data[0], ":"".join(raw_data[1]:)"
            getattr(self, command)(*params)
        agent_address = self.client_address[0]
        print("Data from {0} > {1}".format(agent_address, self.raw_data.decode("utf-8")))
        data_response = "Hello agent {}".format(agent_address)
        print("Data sended   > {}".format(data_response))
        self.wfile.write(data_response.encode()+b".\n")

    def action1 (param1):
        print ("action1 params: {}".format(param1))

    def action2 (param1):
        print ("action1 params: {}".format(param1))

if __name__== '__main__':
    server = socketserver.TCPServer(params, MyTCPHandler)
    server.serve_forever()