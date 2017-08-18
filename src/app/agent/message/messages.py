import json

class Message ():
    def __init__(self, id, body, error):
        self.Id = id
        self.Body = body
        self.Error = error

    def To_str(self):
        return "Id={0}, Body={1}, Error={2}".format(self.Id, self.Body, self.Error)

    def To_json(self):
        return json.dumps(self)

def build_message(json_message):
    return json.loads(json_message.decode(encoding='UTF-8'))