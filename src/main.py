import os
import re
import src.constants as c
import sys

def main():
    if len(sys.argv) < 2:
        sys.exit("missing path argument")

    root_path = sys.argv[1]

    if not os.path.exists(root_path):
        sys.exit("path does not exist: " + root_path)

    regex = re.compile(r'[0-9]{4}-[0-9]{2}-[0-9]{2}')
    prefix_length = len(root_path) if root_path.endswith("/") else len(root_path) + 1

    def handle(path):
        match = regex.match(path[prefix_length:].replace("/", "-"))
        if match:
            print(f"{path} {match.group()}")
        else:
            print(f"{c.color.ERROR}Error!{c.color.CLEAR} {path}")

    for root, dirs, files in os.walk(root_path):
        for file in files:
            handle(os.path.join(root, file))
