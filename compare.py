import requests
import json
import re


class Version:

    def __init__(self, ver, rel, epoch):
        self.version = re.findall("\d+|[A-Za-z]+", ver)
        self.release = re.findall("\d+|[A-Za-z]+", rel)
        self.epoch = epoch
    
    def __compare(self, version, other):
        slen = len(version)
        olen = len(other)

        lmax = max(slen, olen)
        lmin = min(slen, olen)

        for i in range(lmax):
            if i == lmin:
                if slen > olen:
                    return 1
                elif slen < olen:
                    return -1
                break

            v1 = version[i]
            v2 = other[i]

            if v1.isdigit():
                if v2.isdigit():
                    if int(v1) > int(v2):
                        return 1
                    elif int(v1) < int(v2):
                        return -1
                else:               
                    return 1
            elif v1.isalpha() and v2.isalpha():
                if v1 > v2:
                    return 1
                elif v1 < v2:
                    return -1
            else:
                return -1
            
        return 0

    def __gt__(self, other):

        if self.epoch > other.epoch:
            return True
        elif self.epoch < other.epoch:
            return False
        
        res = self.__compare(self.version, other.version)

        if res == 0:            
            res = self.__compare(self.release, other.release)

        if res == 1:
            return True
        
        return False


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

def ver_compare(ver1, rel1, epoch1, ver2, rel2, epoch2):

    version1 = Version(ver1, rel1, epoch1)       
    version2 = Version(ver2, rel2, epoch2)

    return version1 > version2

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
                              int(pkg_dict1[arch][pkg]["epoch"]),
                              pkg_dict2[arch][pkg]["version"], 
                              pkg_dict2[arch][pkg]["release"],
                              int(pkg_dict2[arch][pkg]["epoch"]))
            
            if ret:
                ver_greater_in1.append(pkg_dict1[arch][pkg])

        ver_greater_name = f"Package_versions_greater_in_{branch1}"
        result[arch][ver_greater_name] = ver_greater_in1

    wtfile(result, "result")
    print("Done!")

def wtfile(data, file):
    with open(file, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

    