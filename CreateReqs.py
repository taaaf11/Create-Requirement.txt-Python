"""
Author: Muhammad Altaaf
Contact email: taafuuu@gmail.com
Description: Python 3 script for creating requirements.txt file
"""
import os
from sys import stdlib_module_names, argv as cmd
from importlib_metadata import packages_distributions, version


def get_lines_of_file(file) -> list:
    not_eof = True
    # read file
    lines = list()
    with open(file) as f:
        while not_eof:
            line = f.readline()
            if "#" in line:
                continue
            if not line:
                not_eof = False
            lines.append(line)
    return lines


def get_imports(file) -> list:
    imports = []
    # get imported 'things' from file
    for line in get_lines_of_file(file):
        splitted = line.split(" ")
        # simple import statement
        if "import" in splitted and "from" not in splitted:
            # import 'this'
            if splitted[1][-1] == '\n':
                imports.append(splitted[splitted.index("import") + 1][:-1])
            # if 'import that.this' exists
            if "." in splitted[1]:
                imports.append(splitted[1][:splitted[1].index(".")])
        # from that import this
        elif "from" and "import" in splitted:
            imports.append(splitted[splitted.index("from") + 1])
            for i in splitted:
                if "." in i:
                    if i.index(".") == 0:
                        imports.append(i[i.index(".")+1:])
                        continue
                    try:
                        imports.append(splitted[splitted.index("from") + 1][:i.index(".")])
                    except ValueError:
                        continue
    return sorted(set(imports))


def verify_imports(file) -> list:
    output = packages_distributions().items()
    imports_list = get_imports(file)
    requirements = []
    # iterating through the provided list of imports
    for _import in imports_list:
        # if import is present in current dir
        for i in os.walk("."):
                if _import in i:
                    continue
        # if import is present in standard library
        if _import in stdlib_module_names:
                continue
        # iterating through <the names used to import> and <the distribution names>
        for import_name, dist_name in output:
            # if name is present in the standard library
            if _import in import_name:
                requirements.append(dist_name[0] + "=" + version(dist_name[0]))
    return sorted(requirements)


def create_file():
    print("Creating file... ")
    with open("requirements.txt", "w") as f:
        # get file name from command line argument and pass it to get_imports function
        for _import in verify_imports(cmd[1]):
            # write to file
            f.write(_import + "\n")
    print("done!")
    input("\nHit Enter to exit! ")


if __name__ == "__main__":
    create_file()
