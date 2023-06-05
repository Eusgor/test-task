# test-task

test-task compares binary packages between two branches from public REST API 'https://rdb.altlinux.org/api/' using '/export/branch_binary_packages/{branch}' method

## Installing

'git clone https://github.com/Eusgor/test-task.git'

## Running test-task

test-task requires the following software:
- python (python3)

To run test-task do:

- cd test-task
- python3 main.py [-h] branch1 branch2
arguments: 
- -h - for help (optional) 
- branch1 and branch2 - allowed branch names are: sisyphus, p9 or p10

## Result

test-task saves the result in the 'result' file in JSON format.

The result format:
```json
{
    arch: {
        "Packages_only_in_branch1": [
            package,
            package,
            ...
        ],
        "Packages_only_in_branch2": [
            package,
            package,
            ...
        ],
        "Package_versions_greater_in_branch1": [
            package,
            package,
            ...
        ]
    }
    ...
    ...
}
```

where
- arch - package architecture
- Packages_only_in_branch1 - all packages that are in branch1 but not in branch2
- Packages_only_in_branch2 - all packages that are in branch2 but not in branch1
- Package_versions_greater_in_branch1 - all packages whose version-release is larger in branch1 than in branch2
- package - package info in the format:
    {
      "name": "string",
      "epoch": 0,
      "version": "string",
      "release": "string",
      "arch": "string",
      "disttag": "string",
      "buildtime": 0,
      "source": "string"
    }
