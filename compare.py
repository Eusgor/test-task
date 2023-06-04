import requests
import json


def get_packages(branch):
    url = f"https://rdb.altlinux.org/api/export/branch_binary_packages/{branch}?arch=x86_64"
    response = requests.get(url)
    response.raise_for_status()
    return json.loads(response.text)

def compare(branch1, branch2):
    data1 = get_packages(branch1)["packages"]
    data2 = get_packages(branch2)["packages"]

    wtfile(data1)

#for testing
def wtfile(data):
    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

    