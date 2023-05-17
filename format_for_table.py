import json
import req_ships as rs

def get_ships():
    output = []
    #Headlines
    output.append(("Name", "Location", "Status", "Role"))
    res = json.loads(rs.get())
    for ship in res["data"]:
        
        shipSymbol = ship["symbol"]
        shipLocation = ship["nav"]["waypointSymbol"]
        shipStatus = ship["nav"]["status"]
        shipRole = ship["registration"]["role"]

        shipinfo = (shipSymbol, shipLocation, shipStatus, shipRole)
        output.append(shipinfo)
    return output

get_ships()