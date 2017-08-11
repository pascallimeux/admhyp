
def check_default_keyfiles():
    default_filename="id_rsa"
    path = os.path.expanduser('~') + "/.ssh/"
    pubkey_filename = path+default_filename+".pub"
    privkey_filename = path+default_filename
    if Path(pubkey_filename).exists() and Path(privkey_filename).exists():
        logger.debug ("Private and public keys already exist: {}".format(pubkey_filename))
        return
    if not os.path.exists(path):
        os.makedirs(path)
    logger.warning("Create new private and public keys!")

    key = RSA.generate(2048)
    with open(privkey_filename, "wb") as f:
        os.chmod(privkey_filename, 0o600)
        f.write(key.exportKey('PEM'))

    pubkey = key.publickey()
    with open(pubkey_filename, "wb") as f:
        f.write(pubkey.exportKey('OpenSSH'))
