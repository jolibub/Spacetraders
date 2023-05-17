import authorization_utils as au

def createAuthHeader(user: str) -> str:
    secrets = au.read_secrets()
    return 'Bearer ' + secrets[user]
