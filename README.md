# Python AI Learning Workshop

This repository is a comprehensive learning project for exploring Artificial Intelligence, Large Language Models (LLMs), Agents, Workflows, and related AI technologies using Python.

## 📚 About This Project

This project serves as a practical workspace where various AI and machine learning exercises are implemented and tested. The main goal is to progressively add learning exercises and examples that cover different aspects of modern AI development.

## 🎓 Learning Resources

The exercises and examples in this project are primarily sourced from:

- **Microsoft Learn**: Official Microsoft learning platform providing tutorials and documentation on AI, Azure AI Services, and related technologies
- **Microsoft Reactor**: Educational content from Microsoft Reactor YouTube videos and live sessions covering AI development, best practices, and hands-on demonstrations

## 🗂️ Project Structure

The repository is organized into the following main sections:

### `microsoft_learn_agent_framework/`

Contains exercises and implementations focused on agent-based architectures and workflows:

- **Basic Agents**: Fundamental agent implementations
- **Workflow Agents**: Different workflow patterns (basic, concurrent, conditional, requests-based)
- **Function Agents**: Agents with function calling capabilities
- **Middleware Agents**: Agents with middleware integration
- **Memory Agents**: Agents with conversation memory
- **Multi-turn Agents**: Agents handling multi-turn conversations
- **Persistence Agents**: Agents with state persistence
- **MCP Agents**: Model Context Protocol implementations
- **Images Agents**: Agents working with image generation/processing
- **Third-party Chat Agents**: Integration with external chat services

### `reactor_ai_python/`

Exercises from Microsoft Reactor sessions covering:

- **Basic Agents**: Foundational agent patterns
- **Tool Agents**: Agents using external tools
- **Supervisor Agents**: Multi-agent orchestration patterns
- **Workflow Agents**: Complex workflow implementations
- **Intent Classification**: Natural language understanding
- **Date Extraction**: Information extraction examples
- **Language Supervisors**: Multi-language handling
- **LLM Conversations**: Direct LLM interactions

### `speech_to_text/`

Implementations of speech recognition and audio processing using Azure AI Services.

### `resources/`

Supporting files and resources used across different exercises.

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Virtual environment (recommended)
- Azure account (for Azure AI Services examples)
- API keys for various AI services (OpenAI, Azure OpenAI, etc.)

### Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd python-ai
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows PowerShell
```

3. Install dependencies:

```bash
pip install -r requirements.txt
# or
pip install -e .
```

### Configuration

Set up your environment variables with the necessary API keys and endpoints:

```bash
# .env file example
AZURE_OPENAI_ENDPOINT=<your-endpoint>
AZURE_OPENAI_API_KEY=<your-key>
OPENAI_API_KEY=<your-key>
```

## 📖 Usage

Each directory contains standalone examples that can be run independently. Navigate to the specific exercise you want to explore and run the corresponding Python file.

Example:

```bash
python microsoft_learn_agent_framework/basic_agent.py
```

## 🎯 Learning Path

This project is designed for continuous learning and experimentation. As you progress:

1. Start with basic agent implementations
2. Explore different workflow patterns
3. Experiment with function calling and tool usage
4. Implement memory and persistence mechanisms
5. Build complex multi-agent systems
6. Integrate with various AI services and APIs

## 🤝 Contributing

This is a personal learning project, but suggestions and improvements are welcome. Feel free to open issues or submit pull requests.

## 📝 License

This project is for educational purposes. Please refer to the individual source materials (Microsoft Learn, Microsoft Reactor) for their respective licenses.

## 🔗 Additional Resources

- [Microsoft Learn - AI Learning Paths](https://learn.microsoft.com/training/browse/?products=ai-services)
- [Microsoft Reactor YouTube Channel](https://www.youtube.com/@MicrosoftReactor)
- [Azure AI Services Documentation](https://learn.microsoft.com/azure/ai-services/)

---

**Note**: This is an active learning repository. Content is continuously updated as new exercises and examples are added.
