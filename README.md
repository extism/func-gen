# func-gen

func-gen can be used to generate unix text processing utilities from English text.
It uses [langchain](https://python.langchain.com/en/latest/index.html) to create javascript functions
to process text, and it uses [Extism](https://extism.org/) and the [JavaScript PDK](https://extism.org/docs/write-a-plugin/js-pdk)
to safely execute the code in a Wasm sandbox.

> **Warning**: This only works for very small, simple functions. We have yet to learn about all the tools and techniques to build a reliable code generation model. We'd love some help making the model better and incorporating things like teaching the model documentation for people's Extism plug-in systems.

## Demo Video

[https://www.loom.com/share/d956147a1a7d449391ec0778ebe12918](https://www.loom.com/share/d956147a1a7d449391ec0778ebe12918)

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

