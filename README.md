# func-gen

func-gen can be used to generate unix text processing utilities from English text.
It uses [langchain](https://python.langchain.com/en/latest/index.html) to create javascript functions
to process text, and it uses [Extism](https://extism.org/) and the [JavaScript PDK](https://extism.org/docs/write-a-plugin/js-pdk)
to safely execute the code in a Wasm sandbox.

## Install

> **Note**: First you need to [install Extism](https://extism.org/docs/install) on your machine if you have not:

```bash
pip install --upgrade extism-func-gen
```

## Run

```bash
# Need to set the OpenAI API key
export OPENAI_API_KEY="sk-<paste-key-here>"

# Create a func
func-gen count_vowels -d "Write a function that counts the number of vowels in an input string"

# Use a func
echo "hello world" | func-gen count_vowels
# 3


# List the funcs
func-gen --list
```

