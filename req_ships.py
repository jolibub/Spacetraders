import request_builder as rq

def get():
    res = rq.build_request("GET", "/my/ships", payload={})
    return res.text

def get_one(shipSymbol: str):
    res = rq.build_request("GET", f"/my/ships/{shipSymbol}", payload={})
    return res.text