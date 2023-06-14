import requests
import json
import re


def get_packages(branch):
    api_url = "https://rdb.altlinux.org/api/"
    url = f"{api_url}export/branch_binary_packages/{branch}"
    
    response = requests.get(url)
    if response.status_code != 200:
        print("Use sisyphus, p10 or p9 branches")
        exit(1)

    return json.loads(response.text)

def create_dict(data):
    dct = {}
    for pkg in data:
        dct.setdefault(pkg["arch"], {})
        dct[pkg["arch"]][pkg["name"]] = pkg
    return dct

def ver_compare(ver1, rel1, ver2, rel2):

    vlist1 = [int(i) for i in re.split("\D+", ver1) if i != ""]
    vlist2 = [int(i) for i in re.split("\D+", ver2) if i != ""]

    if vlist1 > vlist2:
        return True
    elif vlist1 == vlist2:
    
        rlist1 = [int(i) for i in re.split("\D+", rel1) if i != ""]
        rlist2 = [int(i) for i in re.split("\D+", rel2) if i != ""]

        if rlist1 > rlist2:
            return True
        
    return False

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
            ret = ver_compare(pkg_dict1[arch][pkg]["version"], 
                              pkg_dict1[arch][pkg]["release"],
                              pkg_dict2[arch][pkg]["version"], 
                              pkg_dict2[arch][pkg]["release"])
            
            if ret:
                ver_greater_in1.append(pkg_dict1[arch][pkg])
            
        ver_greater_name = f"Package_versions_greater_in_{branch1}"
        result[arch][ver_greater_name] = ver_greater_in1

    wtfile(result, "result")
    print("Done!")

def wtfile(data, file):
    with open(file, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

    