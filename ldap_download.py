""" ARCHFLAGS="-arch x86_64" python -m pip install python-ldap """
import ldap.asyncsearch
import json
import csv
import pandas as pd


def ldap_studenlist_download(username: str, password: str, filename: str):
    ldap_connection = ldap.initialize('ldap://dc-01.tgm.ac.at:389', bytes_mode=False)  # TODO add to settings
    ldap_connection.simple_bind_s(username, password)

    ldap_search = ldap.asyncsearch.List(ldap_connection)
    column_names = ['mail', 'sn', 'givenName', 'name', 'department']
    ldap_search.startSearch('OU=HIT,OU=Schueler,OU=People,OU=tgm,DC=tgm,DC=ac,DC=at', ldap.SCOPE_SUBTREE, '(mail=*)',
                            column_names)

    try:
        partial = ldap_search.processResults()
    except ldap.SIZELIMIT_EXCEEDED:
        print('Warning: Server-side size limit exceeded.\n')
    else:
        if partial:
            print('Warning: Only partial results received.\n')

    # print(len(ldap_search.allResults), "Results")

    dataframe_list = []
    for r in ldap_search.allResults:
        dataframe_list.append([r[1][1][x][0].decode('UTF-8') for x in column_names])

    df = pd.DataFrame(dataframe_list, columns=column_names)
    df.to_csv(filename, index=False, quoting=csv.QUOTE_NONNUMERIC)


if __name__ == '__main__':
    with open("data/credentials.json", "r") as f:
        data = json.load(f)
    username = data['username'] + "@tgm.ac.at"
    password = data['password']

    ldap_studenlist_download(username, password)
