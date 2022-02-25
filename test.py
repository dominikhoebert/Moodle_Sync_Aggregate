import json
import requests

if __name__ == '__main__':
    with open('data/credentials.json', 'r') as f:
        data = json.load(f)
    url = data['url']
    key = data['key']
    username = data['username']
    password = data['password']
    print(url, key, username, password)
    obj = {"username": username, "password": password, "service": "tgm_hoedmoodlesync"}

    response = requests.post(url + "/login/token.php", data=obj)
    response = response.json()
    token = response['token']
    private_token = response['privatetoken']
    print(token, private_token)
