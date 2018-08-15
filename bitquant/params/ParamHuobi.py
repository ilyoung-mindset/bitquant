
class ParamHuobi(object):
    def __init__(self, params):
        self.params = {}
        
        self.params['http_proxy_host'] = None
        self.params['http_proxy_host'] = params['network']['http_proxy']['host']
        self.params['http_proxy_port'] = params['network']['http_proxy']['port']
        self.params['websocket'] = params['market']['huobi']['websocket']
      

class ParamHadax(object):
    def __init__(self, params):
        self.params = {}

        self.params['http_proxy_host'] = None
        self.params['http_proxy_host'] = params['network']['http_proxy']['host']
        self.params['http_proxy_port'] = params['network']['http_proxy']['port']
        self.params['websocket'] = params['market']['hadax']['websocket']
