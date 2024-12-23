# SwitchAI  

SwitchAI is a lightweight and flexible library that provides a standardized interface for interacting with various AI APIs like OpenAI, Anthropic, Mistral, and more. With SwitchAI, you can easily switch between AI providers or use multiple APIs simultaneously, all with a simple and consistent interface.  

## Installation  

Install with pip:  
```bash  
pip install switchai  
```

## Getting Started  

To use SwitchAI, you will need API keys for the AI providers you intend to interact with. You can set these keys either as environment variables or pass them as configuration to the `SwitchAI` client.  

If you choose to use environment variables, ensure you follow the naming conventions for each provider as outlined in the [documentation](https://switchai.readthedocs.io/en/latest/api_keys.html).

### Example Usage  

#### Chat  

```python
from switchai import SwitchAI

# Initialize the client with the desired AI model
client = SwitchAI(provider="openai", model_name="gpt-4o")

# Send a message and receive a response
response = client.chat(
    messages=[
        {"role": "user", "content": "Hello, how are you?"}
    ]
)

# Print the response
print(response)
```

#### Text Embedding  

```python
from switchai import SwitchAI

# Initialize the client with the chosen embedding model
client = SwitchAI(provider="google", model_name="models/text-embedding-004")

# Generate embeddings for a list of text inputs
response = client.embed(
    input=[
        "I am feeling great today!",
        "I am feeling sad today."
    ]
)

# Print the response
print(response)
```

#### Speech to text  

```python
from switchai import SwitchAI

# Initialize the client with the desired speech-to-text model
client = SwitchAI(provider="deepgram", model_name="nova-2")

# Transcribe an audio file
response = client.transcribe(
    audio_path="path/to/audio/file.wav"
)

# Print the response
print(response)
```

## Documentation  

For full documentation, visit [SwitchAI Documentation](https://switchai.readthedocs.io/).  

## Contributing  

Contributions are always welcome! If you'd like to help enhance SwitchAI, feel free to make a contribution.
