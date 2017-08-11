import base64, zlib

from cryptography.hazmat.backends.openssl import decode_asn1


def new_method1(self):
    print("I am a new method1, I can access to attributs: {0} and to class attributs: {1}".format(self.value, Object.chaine))

def new_method2(self, val1, val2):
    print("I am a new method2, I this is my value: {0}, {1}".format(val1, val2))


class Object:
    chaine = "My chain"
    def __init__(self, val):
        self.value =val

class Object2 (Object):
    def __init__(self, val):
        super().__init__(val)

    def exec(self, cmd, kwargs=None):
        if kwargs:
            print (kwargs)
            getattr(self, cmd)(**kwargs)
        else:
            getattr(self, cmd)()


    def display(self):
        print ("I am a method, I can access to attributs: {0} and to class attributs: {1}".format(self.value, Object.chaine))

def encode_file(filename):
    with open("code1.py", "rb") as f:
        encoded = base64.b64encode(zlib.compress(f.read()))
        return encoded

def decode_and_execute_file(encoded):
    code = zlib.decompress(base64.b64decode(encoded))
    return exec(code)

def add_method_2_class(cl, method_name, method):
    setattr(cl, method_name, method)


if __name__ == '__main__':
    obj = Object2(5)
    obj.display()

    # add a method to a class
    add_method_2_class(Object, "action1", new_method1)
    add_method_2_class(Object, "action2", new_method2)
    obj.action1()

    # execute selector method
    obj.exec("action1")
    obj.exec("action2", kwargs={'val1':54, 'val2':55})

    # execute a new python code
    prog = "print (\"Hello I am a meta program\")"
    exec (prog)

    # serialize and unserialize python code
    encoded = encode_file("code1.py")
    decode_and_execute_file(encoded)
