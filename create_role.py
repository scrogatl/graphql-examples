import requests
import json
import sys
import argparse


if len(sys.argv) < 4:
    print("Usage: python create_role.py <user_key> <permission_file> <role_name> [-C]")
    sys.exit(1)

user_key = sys.argv[1]
permission_file = sys.argv[2]
role_name = sys.argv[3]

parser = argparse.ArgumentParser(description = "Description for my parser")
parser.add_argument('user_key')
parser.add_argument('permission_file')
parser.add_argument('role_name')
parser.add_argument("-C", "--create", required=False, action='store_true')
argument = parser.parse_args()


def getOrgId():
    payload = '''
    {
      actor {
        organization {
          id
        }
      }
    }
    '''
    endpoint = "https://api.newrelic.com/graphql"
    headers = {'Content-Type': 'application/json', 'API-Key': f'{user_key}'}
    response = requests.post(endpoint, headers=headers, json={'query': payload})
    if response.status_code == 200:
        dict_response = json.loads(response.content)
        return dict_response['data']['actor']['organization']['id']
    else:
        # raise an error with a HTTP response code
        raise Exception(f'Nerdgraph request failed with a {response.status_code}.')
    return None

def loadPermissions(filename):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except json.JSONDecodeError:
        print("Error: Could not decode JSON from 'data.json'. Check file format.")
    perm_ids = []
    for item in data['data']['customerAdministration']['permissions']['items']:
        perm_ids.append(int(item['id']))
        print(f"Permission ID: {item['id']}, Feature: {item['feature']}, Category: {item['category']}, Product: {item['product']}")
    return perm_ids

def createRole(role_name, org_id, permissions):
    payload = '''
    mutation {{ 
      customRoleCreate(
      container: {{
        id: "{org_id}"
        type: "ORANIZATION"
      }}
        name: "{role_name}"
          permissionIds: {permissions}
          scope: "account"
        ) {{
          id
        }}
      }}
      '''.format(org_id=org_id, role_name=role_name, permissions=json.dumps(permissions))
    print(payload)
    if argument.create == False:
      return
    
    print("Creating Role...")
        
  
    endpoint = "https://api.newrelic.com/graphql"
    headers = {'Content-Type': 'application/json', 'API-Key': f'{user_key}'}
    response = requests.post(endpoint, headers=headers, json={'query': payload})
    if response.status_code == 200:
        dict_response = json.loads(response.content)
        print(f"No Error {dict_response}")
    else:
        # raise an error with a HTTP response code
        raise Exception(f'Nerdgraph request failed with a {response.status_code}.')
    return None
    
if __name__ == '__main__':
    org_id = getOrgId()
    permissions = loadPermissions(permission_file)
    print(f"Organization ID: {org_id}")
    createRole(argument.role_name, org_id, permissions)