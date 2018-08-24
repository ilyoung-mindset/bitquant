from flask import Flask

api_gateway = Flask(__name__)

@api_gateway.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    api_gateway.run()
    print("api gateway startup...")
