import requests
import json


def get_packages(branch):
    api_url = "https://rdb.altlinux.org/api/"
    url = f"{api_url}export/branch_binary_packages/{branch}"
    
    response = requests.get(url)
    if response.status_code != 200:
        print("Use branches sisyphus, p10 or p9")
        exit(1)

    return json.loads(response.text)

def create_dict(data):
    dct = {}
    for pkg in data:
        dct.setdefault(pkg["arch"], {})
        dct[pkg["arch"]][pkg["name"]] = pkg
    return dct

def compare(branch1, branch2):
    data1 = get_packages(branch1)["packages"]
    data2 = get_packages(branch2)["packages"]

    pkg_dict1 = create_dict(data1)
    pkg_dict2 = create_dict(data2)

    archs = set(pkg_dict1.keys()).intersection(set(pkg_dict2.keys()))
    result = {}
    for arch in sorted(archs):
        data1_names = set(pkg_dict1[arch].keys())
        data2_names = set(pkg_dict2[arch].keys())
        data_names = data1_names.intersection(data2_names)
        
        only_in1 = [pkg_dict1[arch][pkg] for pkg in pkg_dict1[arch] 
                    if pkg not in data2_names]
        only_in2 = [pkg_dict2[arch][pkg] for pkg in pkg_dict2[arch] 
                    if pkg not in data1_names]
        
        result.setdefault(arch, {})
        result[arch][f"Packages_only_in_{branch1}"] = only_in1
        result[arch][f"Packages_only_in_{branch2}"] = only_in2

        ver_greater_in1 = []
        for pkg in data_names:
            if (pkg_dict1[arch][pkg]["version"] >
                    pkg_dict2[arch][pkg]["version"]):
                ver_greater_in1.append(pkg_dict1[arch][pkg])
        ver_greater_name = f"Package_versions_greater_in_{branch1}"
        result[arch][ver_greater_name] = ver_greater_in1

    wtfile(result, "result")

def wtfile(data, file):
    with open(file, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

    