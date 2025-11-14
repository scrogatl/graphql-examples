GraphQL Examples
================================================

## Requirements:

* python
* pip

----



`get_non_reporting_apms.py` - List APMs that have not reported in 24 hours. Add `-D` to actually delete the APM from New Relic.

`get_permissions.py` - Retreive all the account permissions. Output to .json file to use in creating a new role.

`create_role.py` - Will create a "Custom Role" using the .json file above. Add `-C` to actually create the role (otherwise it is a dry run).


To use: 
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---
Retrieve the permissions:
```
python get_permissions.py [NRAK-**************]  > all_perms.json
```
Edit the .json to reflect the desired permissions.

Verify it is correct:
```
python create_role.py [NRAK-**************]  all_perms.json 
```
Actually create the role:

```
python create_role.py [NRAK-**************]  all_perms.json -C
```
