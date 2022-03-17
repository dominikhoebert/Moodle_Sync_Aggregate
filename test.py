import json
import pandas as pd
from openpyxl import Workbook, worksheet

if __name__ == '__main__':
    with open('data/credentials.json', 'r') as f:
        data = json.load(f)
    url = data['url']
    key = data['key']
    username = data['username']
    password = data['password']
    print(url, key, username, password)

    df1 = pd.DataFrame([['a', 'b'], ['x', 'y']], columns=['first', 'sec'])
    df2 = pd.DataFrame([['c', 'd'], ['z', 'z']], columns=['first', 'sec'])

    wb

