import requests
import json
import sys
import argparse


user_key = sys.argv[1]

parser = argparse.ArgumentParser(description = "Description for my parser")
parser.add_argument('user_key')
argument = parser.parse_args()

def getPermissions():
    payload = '''
    {
      customerAdministration {
        permissions {
          items {
            feature
            category
            id
            product
          }
        }
      }
    }   
  '''
    endpoint = "https://api.newrelic.com/graphql"
    headers = {'Content-Type': 'application/json', 'API-Key': f'{user_key}'}
    response = requests.post(endpoint, headers=headers, json={'query': payload})
    if response.status_code == 200:
        dict_response = json.loads(response.content)
        return dict_response
    else:
        # raise an error with a HTTP response code
        raise Exception(f'Nerdgraph request failed with a {response.status_code}.')


    
if __name__ == '__main__':
    pretty_permissions = json.dumps(getPermissions(), indent=4)
    print(pretty_permissions)
