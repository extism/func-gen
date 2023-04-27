# func-gen


## Build

```bash
poetry install
```

## Run

```bash
# Need to set the OpenAI API key
export OPENAI_API_KEY="sk-<paste-key-here>"

# Create a func
poetry run func-gen count_vowels -d "Write a function that counts the number of vowels in an input string"

# Use a func
echo "hello world" | poetry run func-gen count_vowels
# 3
```

