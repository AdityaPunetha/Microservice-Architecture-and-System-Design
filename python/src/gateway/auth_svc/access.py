import os, requests


def login(request):
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return None, ("Invalid credentials", 401)
    basic_auth = (auth.username, auth.password)
    response = requests.post(
        f"http://{os.environ['AUTH_SVC_ADDRESS']}/login", auth=basic_auth
    )
    if response.status_code == 200:
        return response.json()["token"], None
    return None, ("Invalid credentials", 401)
