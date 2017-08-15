go get github.com/eclipse/paho.mqtt.golang
go get golang.org/x/net/websocket
go get golang.org/x/net/proxy
go get github.com/op/go-logging



fix bug
ajouter dans le makefile l'installation de mosquitto et mosquitto client
faire un sequenseur pour les orders (generique)
transferer des fichiers avec mqtt cf voit c&c commands (modifier le format du message pour etre generiques nb args)
developper le getsystemstatus




depuis python installer l'agent
mettre à jour les deux vars depuis python avant la compilation


mosquitto_pub -t "orders/agent1" -m "{\"Id\":\"1\",\"Body\":\"stop\"}"