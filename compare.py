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

    data1_names = set(pkg["name"] for pkg in data1)
    data2_names = set(pkg["name"] for pkg in data2)
    data_names = data1_names.intersection(data2_names)

    only_in1 = [pkg for pkg in data1 if pkg["name"] not in data2_names]
    only_in2 = [pkg for pkg in data2 if pkg["name"] not in data1_names]


    wtfile(only_in1, "only_in1")
    wtfile(only_in2, "only_in2")

#for testing
def wtfile(data, file):
    with open(file, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

    