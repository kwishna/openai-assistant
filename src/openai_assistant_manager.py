import json
import os
from typing import BinaryIO, Literal, Iterable, List

import dotenv
from openai import OpenAI
from openai.types.beta import AssistantToolParam
from openai.types.beta.thread_create_params import Message
from openai.types.beta.threads import MessageContentPartParam
from openai.types.shared_params import FunctionParameters

dotenv.load_dotenv()

ASSISTANT_INSTRUCTION = "You're an AI assistant who has access to tools to complete the task. You should apply ReAct and Tree-of-thoughts approach to complete the given task."


class AssistantManager:
    def __init__(self, model_name: str = 'gpt-4o', temperature: float = 0.7):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

        self.model_name = model_name
        self.temperature = temperature
        self.tools: List[AssistantToolParam] = []
        self.tools_resources = None
        self.tools_resources = None
        self.thread_id = None
        self.assistant_id = None
        self.run_id = None
        self.file_ids_for_code_interpreter = []
        self.file_ids_for_search = []
        self.vector_store_ids = []

    def add_code_interpreter_to_assistant(self):
        if "code_interpreter" not in self.tools:
            self.tools.append({"type": "code_interpreter"})

    def add_file_search_to_assistant(self):
        if "file_search" not in self.tools:
            self.tools.append({"type": "file_search"})

    def add_function_to_assistant(
            self,
            function_name: str,
            function_description: str,
            parameters: FunctionParameters
    ):
        self.tools.append({
            "type": "function",
            "function": {
                "name": function_name,
                "description": function_description,
                "parameters": parameters
            }
        })

    @staticmethod
    def _read_file(file_path: str):
        _file: BinaryIO = None

        try:
            with open(file_path, 'rb') as f:
                _file = f

        except FileNotFoundError:
            print(f"File not found: {file_path}")

        return _file

    def create_file_in_openai(self, file_path: str):
        _file = self._read_file(file_path)
        _upload_file_response = None

        if _file is not None:
            _upload_file_response = self.client.files.create(file=_file, purpose="assistants")
        else:
            print("File not uploaded to openai: ", file_path)

        return _upload_file_response

    def __create_file_in_openai_for_code_interpreter(self, file_path: str) -> None:
        upload_file_response = self.create_file_in_openai(file_path)

        if upload_file_response is not None:
            self.file_ids_for_code_interpreter.append(upload_file_response.id)
        else:
            print("File creation failed for code interpreter: ", file_path)

    def __create_file_in_openai_for_search(self, file_path: str) -> None:
        upload_file_response = self.create_file_in_openai(file_path)

        if upload_file_response is not None:
            self.file_ids_for_search.append(upload_file_response.id)
        else:
            print("File creation failed for search: ", file_path)

    def __create_vector_store_in_openai(self, file_path: str):
        self.__create_file_in_openai_for_search(file_path)

        vector_store = self.client.beta.vector_stores.create(file_ids=self.file_ids_for_search)
        self.vector_store_ids.append(vector_store.id)

    def add_file_for_code_interpreter(self, file_path: str):
        self.__create_file_in_openai_for_code_interpreter(file_path)
        self.tools_resources = {
            "code_interpreter": {
                "file_ids": self.file_ids_for_code_interpreter
            }
        }

    def add_file_for_data_search(self, file_path: str):
        self.__create_vector_store_in_openai(file_path)
        self.tools_resources = {
            "vector_store_ids": self.vector_store_ids
        }

    def create_thread(self):
        thread = self.client.beta.threads.create()
        self.thread_id = thread.id

    def create_thread_with_message(self, messages: Iterable[Message]):
        thread = self.client.beta.threads.create(messages=messages)
        self.thread_id = thread.id

    def add_text_to_message_in_thread(self,
                                      role: Literal["user", "assistant"],
                                      msg: str):
        self.client.beta.threads.messages.create(
            role=role,
            content=[{"type": "text", "text": msg}],
            thread_id=self.thread_id
        )

    def add_image_url_to_message_in_thread(self,
                                           role: Literal["user", "assistant"],
                                           url: str):
        self.client.beta.threads.messages.create(
            role=role,
            content=[{"type": "image_url", "image_url": {"url": url}}],
            thread_id=self.thread_id
        )

    def add_image_data_to_message_in_thread(self,
                                            role: Literal["user", "assistant"],
                                            image_file_path: str):

        _upload_file_response = self.create_file_in_openai(file_path=image_file_path)

        if _upload_file_response is not None:
            self.client.beta.threads.messages.create(
                role=role,
                content=[{"type": "image_file", "image_file": {"file_id": _upload_file_response.id}}],
                thread_id=self.thread_id
            )
        else:
            print("File creation failed for image: ", image_file_path)

    def add_message_in_thread_with_attachment_for_file_search(
            self,
            file_path: str,
            role: Literal["user", "assistant"],
            content: Iterable[MessageContentPartParam]
    ):

        upload_file_response = self.create_file_in_openai(file_path)

        if upload_file_response is not None:
            self.client.beta.threads.messages.create(
                role=role,
                content=content,
                thread_id=self.thread_id,
                attachments=[{
                    "file_id": upload_file_response.id,
                    "tools": [
                        {
                            "type": "file_search"
                        }
                    ]
                }],
            )
        else:
            print("File creation failed for data search: ", file_path)

    def add_message_in_thread_with_attachment_for_code_interpreter(
            self,
            file_path: str,
            role: Literal["user", "assistant"],
            content: Iterable[MessageContentPartParam]
    ):

        upload_file_response = self.create_file_in_openai(file_path)

        if upload_file_response is not None:
            self.client.beta.threads.messages.create(
                role=role,
                content=content,
                thread_id=self.thread_id,
                attachments=[{
                    "file_id": upload_file_response.id,
                    "tools": [
                        {
                            "type": "code_interpreter"
                        }
                    ]
                }],
            )
        else:
            print("File creation failed for code interpreter: ", file_path)
