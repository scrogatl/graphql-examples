import requests
import json
import sys

user_key = sys.argv[1]
account_id = sys.argv[2]
env = sys.argv[3]


allowed_names = ['Frontend']

def get(account):
    payload = '''
    {
        actor {
            entitySearch(
                queryBuilder: {
                    domain: BROWSER, 
                    type: APPLICATION, 
                    tags: {key: "accountId", value: "'''+str(account)+'''"}
                }
            ) {
                results {
                    entities {
                        name
                        guid
                    }
                }
            }
        }
    }
    '''
    endpoint = "https://api.newrelic.com/graphql"
    headers = {'Content-Type': 'application/json', 'API-Key': f'{user_key}'}
    response = requests.post(endpoint, headers=headers, json={'query': payload})

    # list of tuples (name, guid)
    allowlist_name_guid_tuple = []

    if response.status_code == 200:
        dict_response = json.loads(response.content)
        print(dict_response)
    else:
        # raise an error with a HTTP response code
        raise Exception(f'Nerdgraph request failed with a {response.status_code}.')
    for i in dict_response['data']['actor']['entitySearch']['results']['entities']:
        allowlist_name_guid_tuple.append((i['name'], i['guid']))
    return allowlist_name_guid_tuple

def delete(guid):
    payload = '''
    mutation {
        agentApplicationDelete(
            guid: "'''+guid+'''"
        ) {
            success
        }
    }
    '''
    endpoint = "https://api.newrelic.com/graphql"
    headers = {'Content-Type': 'application/json', 'API-Key': f'{user_key}'}
    response = requests.post(endpoint, headers=headers, json={'query': payload})

    if response.status_code == 200:
        dict_response = json.loads(response.content)
        print(dict_response)
    else:
        print(response.content)
        # raise an error with a HTTP response code
        raise Exception(f'Nerdgraph request failed with a {response.status_code}.')

    
if __name__ == '__main__':
    print(f"Listing non-reporting APMs for {account_id}")

    name_guid_tuples = []
    name_guid_tuples = get(account_id)
   
    print("Cleaning up browser entities")
    for tuple in name_guid_tuples:
        name = tuple[0]
        guid = tuple[1]
        if name not in allowed_names:
            print(f"Debug - deleting {name}")
            #delete(guid)
