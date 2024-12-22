# Lucius Assistant

[![PyPI version](https://badge.fury.io/py/luciusassistant.svg)](https://badge.fury.io/py/luciusassistant)

**Lucius Assistant** is an agentic AI assistant built on top of the Llama language model, designed to provide intelligent assistance through a robust function calling system. It offers seamless integration of chat capabilities with file operations and memory management.

## Features

- **Intelligent Model Selection**: Automatically selects the most suitable Llama model (3.1, 3.2, or others) with preference for 8b parameter versions
- **File Operations**: 
  - Directory listing with safety checks
  - File reading and writing with path validation
  - File and folder copying with automatic directory creation
- **Memory System**:
  - Store and retrieve text memories with UUID-based identification
  - Contextual memory search with relevance scoring
  - Memory management (add, remove, search)
- **Event-Driven Architecture**:
  - Real-time streaming text processing
  - Separate handling of chat and function calls
  - Automated response generation
- **Safety Features**:
  - Path validation to prevent directory traversal
  - Relative path enforcement
  - Graceful error handling
  - Automatic parent directory creation

## Installation

```bash
pip install luciusassistant
```

## Requirements

- Python 3.7+
- ollama
- chatollama # This is also my python module, I have documentationfor it here https://pypi.org/project/chatollama/

## Usage

### Basic Usage

```python
from luciusassistant import LuciusAssistant, get_builtin_function_calls

# Initialize Lucius with built-in functions
lucius = LuciusAssistant()
lucius.set_function_calls(get_builtin_function_calls()) # Contains a built-in function to list the current directory and read files

# Chat with Lucius
response = lucius.chat("Hello, can you take a look at the current project?")
```

### File Operations

```python
from luciusassistant import LuciusAssistant, get_builtin_function_calls

# Initialize with built-in functions
lucius = LuciusAssistant()
lucius.set_function_calls(get_builtin_function_calls())

# List directory contents
lucius.chat("List the contents of the current directory")

# Read a file
lucius.chat("Read the contents of config.json")

# Write to a file
lucius.chat("Create a new file named example.txt with 'Hello World' content")
```

### Memory System

```python
from luciusassistant import LuciusAssistant, get_builtin_function_calls

# Initialize with built-in functions
lucius = LuciusAssistant()
lucius.set_function_calls(get_builtin_function_calls()) # Contains a built-in function to store and retrieve memories

# Store a memory
lucius.chat("Remember this phone number for support: 1-800-SUPPORT")

# Long conversation later...

# Search memories
lucius.chat("Find any stored support contact information")

# Lucius finds the support phone number memory

# Remove a memory
lucius.chat("Remove that memory")
```

### Creating Custom Functions

You can extend Lucius's capabilities by creating custom functions:

```python
from luciusassistant import LuciusAssistant, FunctionCall, get_builtin_function_calls

# Create a custom function
class WeatherFunctionCall(FunctionCall):
    def __init__(self):
        super().__init__(
            name="get_weather",
            parameters={
                "city": "Name of the city",
                "country": "Country code (e.g., US, UK)"
            },
            description="Get the current weather for a specified city"
        )

    def invoke(self, city: str, country: str = "US"):
        try:
            # Implement your weather API call here
            return f"Weather information for {city}, {country}"
        except Exception as e:
            return f"Failed to get weather: {str(e)}"

# Initialize Lucius with both built-in and custom functions
lucius = LuciusAssistant()
function_calls = get_builtin_function_calls()
function_calls.append(WeatherFunctionCall())
lucius.set_function_calls(function_calls) # Very impotant you call this function at the start because this will clear the conversation history

# Use the custom function
lucius.chat("What's the weather like in San Francisco?")
```

## Architecture

Lucius Assistant is built with a modular architecture:

1. **Core Engine**: Based on chatollama, utilizing Llama models for text generation
2. **Function Call System**: XML-like format for structured function invocation
3. **Event System**: Handles streaming, function results, and response generation
4. **Memory Management**: In-memory storage with UUID-based retrieval
5. **Safety Layer**: Input validation and path safety checks

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built on top of the Llama language model
- Uses chatollama for core functionality