## Generate and distribute keys
```
ssh-keygen
ssh-copy-id root@centos
ssh root@centos
```

# Create and start Python virtualenv
```
python3.5 -m venv .venv
source .venv/bin/activate
```
# Download Python libs and list
```
cd admhyp
pip3 install -r requirements.txt
pip3 list
```

The user must have a private and public keys in ~/.ssh/id_rsa ~/.ssh/id_rsa.pub
