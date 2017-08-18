go get github.com/eclipse/paho.mqtt.golang
go get golang.org/x/net/websocket
go get golang.org/x/net/proxy
go get github.com/op/go-logging

mosquitto_pub -t "orders/agent1" -m "{\"Id\":\"1\",\"Body\":\"stop\"}"