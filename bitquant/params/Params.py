import json

class Params(object):
    def __init__(self):
        with open('config/config.json', 'r') as f:
            self.params = json.load(f)


params = Params().params

if __name__ == "__main__":
    print(params.params)
