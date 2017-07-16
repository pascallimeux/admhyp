## Prerequisites:
- install python 3.6
sudo add-apt-repository ppa:jonathonf/python-3.6
sudo apt update && sudo apt install -y python3.6

- The user must have a private and public keys in ~/.ssh/id_rsa ~/.ssh/id_rsa.pub
- Download fabric (https://gerrit/hyperledger.org/r/fabric)
- Dowload fabric-ca (https://gerrit/hyperledger.org/r/fabric-ca)
- Build binaries (peer, orderer, fabric-ca-client fabric-ca-server)
- Build docker images (zookeeper, kafka)
- Build binaries tools (configtxgen)
- Customize config.yaml (certificate and admin informations for CA)
- Customize fabric-ca-client-config.yaml (certificate info for cliente "user", "admin", "peer", "orderer")
- Customize core.yaml (configuration for PEER)
- Customize orderer.yaml (configuration ORDERER)
- Customize configtx.yaml (configuration genesis block)
