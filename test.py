import json
import pandas as pd

if __name__ == '__main__':
    with open('data/credentials.json', 'r') as f:
        data = json.load(f)
    url = data['url']
    key = data['key']
    username = data['username']
    password = data['password']
    print(url, key, username, password)

    try:
        student_list = pd.read_csv("data/studentlist2.csv")
    except Exception as e:
        print("Failed to load Student List CSV. Please check Settings.", e)

    print(student_list)

