import os
import argparse
import re
import hashlib
import pathlib
import sys
from extism import Context
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    HumanMessage,
    SystemMessage
)

MARKDOWN_RE = re.compile("\\`\\`\\`javascript([^\\`]*)\\`\\`\\`")
HOME_DIR = pathlib.Path.home() / ".func-gen"


def generate_code(description):
    chat = ChatOpenAI(temperature=0, client=None)

    messages = [
        SystemMessage(content="Your goal is to write a Javascript function."),
        SystemMessage(content="You must export the function as the default export, using the CommonJS module syntax"),
        SystemMessage(content="You must not include any comments, explanations, or markdown. The response should be JavaScript only."),
        HumanMessage(content=description),
    ]

    response = chat(messages)
    code = response.content
    match = MARKDOWN_RE.match(code)
    if match and match.group(1):
        code = match.group(1)
    return code


def execute_code(code, input):
    wasm_file_path = pathlib.Path(__file__).parent / "eval.wasm"
    wasm = wasm_file_path.read_bytes()
    hash = hashlib.sha256(wasm).hexdigest()
    config = {"wasm": [{"data": wasm, "hash": hash}], "memory": {"max": 5}}

    with Context() as context:
        plugin = context.plugin(config, wasi=True)
        plugin.call("register_function", code)
        return plugin.call("invoke", input)

def init_argparse():
    parser = argparse.ArgumentParser(
        usage="%(prog)s [FUNC_NAME] [OPTIONS]",
        description="Create and execute text processing functions by English descriptions"
    )
    parser.add_argument('func_name', type=str, nargs='?')
    parser.add_argument('-d', '--description', type=str, nargs='?')
    parser.add_argument('-l', '--list', action=argparse.BooleanOptionalAction)
    return parser

def main():
    parser = init_argparse()
    args = parser.parse_args()

    if not os.path.exists(HOME_DIR):
        os.makedirs(HOME_DIR)

    if args.list:
        import glob
        for f in glob.glob(str(HOME_DIR / "*.js")):
            print(os.path.basename(f)[:-3])
        exit(0)

    if not args.func_name:
        print("Function name is a required argument")
        exit(1)

    if args.description:
        code = generate_code(args.description)
        with open(HOME_DIR / f"{args.func_name}.js", 'w') as file:
            file.write(code)
        print(code)
        exit(0)

    # if f"{args.func_name}.js" not in functions:
    #     print(f"Could not find function {args.func_name}")
    #     exit(1)

    target = HOME_DIR / f"{args.func_name}.js"

    if not os.path.exists(target):
        print(f"Could not find function {args.func_name} in {HOME_DIR}")
        print("To define it use the -d parameter with an English description. Example:")
        print(f"  func-gen {args.func_name} -d 'Write a function that counts the number of vowels in a string'")
        exit(1)

    with open(target, 'r') as file:
        result = execute_code(file.read(), sys.stdin.read())
        print(result.decode('utf-8'))


