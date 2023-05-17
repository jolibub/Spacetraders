import request_builder as rq
import json
import time

#### Vars
ship = 'JOLIBUB-2'
farmedResource = 'ALUMINUM_ORE'

cargoNotFull = True

def orbit(shipSymbol: str):
    res = json.loads(rq.build_request("POST", f"/my/ships/{shipSymbol}/orbit", {}).text)
    print(res["data"]["nav"]["status"])

def extract(shipSymbol: str):
    res = json.loads(rq.build_request("POST", f"/my/ships/{shipSymbol}/extract", {}).text)
    print("extracted " + res["data"]["extraction"]["yield"]["symbol"])
    return float(res["data"]["cooldown"]["totalSeconds"])

def isCargoFull(shipSymbol: str):
    res = json.loads(rq.build_request("GET", f"/my/ships/{shipSymbol}/cargo", {}).text)
    return int(res["data"]["capacity"]) == int(res["data"]["units"])

def dock(shipSymbol: str):
    res = json.loads(rq.build_request("POST", f"/my/ships/{shipSymbol}/dock", {}).text)
    print(res["data"]["nav"]["status"])

def sellCargo(shipSymbol: str, cargo: list):
    for item in cargo:
        payload = {
            "symbol": item["symbol"],
            "units": item["units"]
        }
        res = json.loads(rq.build_request("POST", f"/my/ships/{shipSymbol}/sell", payload).text)
        print("sold " + res["data"]["transaction"]["tradeSymbol"])

def getCargo(shipSymbol: str):
    res = json.loads(rq.build_request("GET", f"/my/ships/{shipSymbol}/cargo", {}).text)
    return res["data"]["inventory"]

#starting in docked state at astroid location
while True:
  orbit(ship)
  while cargoNotFull:
    time.sleep(extract(ship))
    cargoNotFull = not isCargoFull(ship)
  dock(ship)
  cargo = getCargo(ship)
  sellList = []
  for item in cargo:
      if item["symbol"] == farmedResource: continue
      sellList.append(item)
  sellCargo(ship, sellList)
  cargoNotFull = not isCargoFull(ship)