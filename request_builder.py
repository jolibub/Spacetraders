import requests as req
import authorization as auth


def build_request(type: str, endpoint: str, payload: dict = {}):
  baseURL = 'https://api.spacetraders.io/v2'

  headers = { 
    'Authorization': auth.createAuthHeader('jolibub') 
    } 

  return req.request(type, baseURL + endpoint, headers=headers, data=payload)

