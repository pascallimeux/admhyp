

def get_external_ipaddress():
    import urllib.request
    extipaddr = urllib.request.urlopen('http://ident.me').read().decode('utf8')
    return extipaddr

def get_local_ipaddress():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('google.com', 0))
    ipaddr=s.getsockname()[0]
    return (ipaddr)