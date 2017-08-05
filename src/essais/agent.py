import socket

params = ('127.0.0.1', 8808)

BUFFER_SIZE=1024
def get_result(value):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(params)
        print('\tData sended   >{} '.format(value))
        s.send("{}\n".format(value).encode())
        result = s.recv(BUFFER_SIZE)
        print('\tData received >{}'.format(result.decode("utf-8")))
        return result.decode()

if __name__== '__main__':
    get_result("I am an agent")
    get_result("action1:parametrer1")