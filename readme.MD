# OpenAI GPT-4o Assistant

This project is a Python-based application that utilizes the powerful GPT-4o language model from OpenAI to provide an intelligent and versatile AI assistant. With its advanced natural language processing capabilities.
The GPT-4o model can engage in human-like conversations, answer questions, provide explanations, and assist with a wide range of tasks.

This project is mainly focused on using `Assistant` API.

Assistant has 3 types of tool:
   1) file_search
   2) code-interpreter
   3) function

OpenAI Assistant intelligently uses the tool that is best suited to answer the user's query to complete the task, and
provides the user with a response.

## Features

- **Conversational AI**: Engage in natural language conversations with the GPT-4o model, allowing you to ask questions, provide context, and receive intelligent responses.
- **Task Assistance**: Leverage the GPT-4o model's capabilities to assist with various tasks such as writing, coding, research, analysis, and problem-solving.
- **Knowledge Base**: The GPT-4o model has been trained on a vast corpus of data, enabling it to provide information and insights on a wide range of topics.
- **Customizable Prompts**: Easily customize the prompts and instructions provided to the GPT-4 model to tailor its responses to your specific needs.

## Getting Started

### Prerequisites

- Python 3.6 or higher
- OpenAI API key (obtain one from the [OpenAI website](https://openai.com/api/))

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/openai-gpt4-assistant.git
  
2. Navigate to the project directory:
   ```bash
   cd openai-gpt4-assistant

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt

### Usage
1. Set your OpenAI API key as an environment variable:
   ```bash
   export OPENAI_API_KEY=your_api_key_here

2. Run the application:
   ```bash
   python <file_name>.py
 
3. Start interacting with the GPT-4o model by typing your queries or instructions.

### Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

### License
This project is free for use by anyone.
