import dotenv
import openai
# from openai import AssistantEventHandler
dotenv.load_dotenv()

"""
Flow:
    Create Assistant --> assistant_id is generated
    Create Thread --> thread_id is generated
    Add Message To The Thread --> we need thread_id to attach the message to it
    Create Run --> run_id is generated
         - check if run is completed or in-progress or cancelled or aborted
         
    Assistant has 3 types of tool:
        1) retriever
        2) interpreter
        3) function
    
    To use 'retriever', you must upload your file into openai and get the 'file_id'. You can use this 'file_id' can be used to create vector store.
"""
#
################################################################################################################################################
#### Step-1 --> Assistant creation
#
# assistant = openai.beta.assistants.create(
#     model='gpt-4o',
#     temperature=0.7,
#     instructions="You're an AI assistant who has access to tools to complete the task."
#                  "You should apply ReAct and Tree-of-thoughts approach to complete the given task.",
#     tools=[{"type": "code_interpreter"}]
# )
## --------------------------------------------------------------------------------------------------------------------------------------------------
##
## tools=[{"type": "code_interpreter"}]
## tools=[{"type": "file_search"}]
## tools= [{"type": "function", "function": {"name": "sum", "parameters": [{"name": "a", "type": "number"}, {"name": "b", "type": "number"}]   }}]
##
## -------------------------------------------------------------------------------------------------------------------------------------------------
##
## tool_resources = {  # Optional
##     "code_interpreter": {
##         "file_ids": ["file_1234567890"]
##     }
## }
##
## tool_resources={
##     "file_search": {
##         "vector_store_ids": ["vs_1234567890"], # Optional
##        "vector_stores": {                     # Optional
##             "file_ids": ["file_1234567890"],
##             "metadata": {
##                 "key": "value"
##         }
##     }
## }
## --------------------------------------------------------------------------------------------------------------------------------------------------
#
# print(assistant.id) # asst_8Lkj24Ki8bBKUXfeTMSxUILt
#
################################################################################################################################################
##### Step-2 --> Thread created
#
# thread = openai.beta.threads.create()
# print(thread.id) # thread_W7c1wITiWNp7yTtMLDom5AW6
#
################################################################################################################################################
#### Step-3 --> file (Optional) [Only required for retrieval]
#
# with open(os.path.abspath("./record-java.txt"), 'rb') as f:
#     file = openai.files.create(file=f, purpose="assistants")
#     print(file.id) # file-lAj9R9xvE0DIjHI5YmGWkaDr
#
################################################################################################################################################
#### Step-4 --> vector store (Optional)
#
# vector_store = openai.beta.vector_stores.create(file_ids=['file-lAj9R9xvE0DIjHI5YmGWkaDr'])
# print(vector_store.id) # vs_WlHgooZgpA1wVme1mIemXgaE
#
################################################################################################################################################
#### Step-5 --> create and attach message to the thread
#
# messages = openai.beta.threads.messages.create(
#     thread_id="thread_W7c1wITiWNp7yTtMLDom5AW6",
#     role="user",
#     attachments=[{
#         "file_id": "file-lAj9R9xvE0DIjHI5YmGWkaDr",
#         "tools": [
#             {
#                 "type": "file_search"  # "code_interpreter"
#             }
#         ]
#     }],
#     content=[
#         {
#             "type": "text",
#             "text": "What is Canonical Constructors in Java?"
#         }
#     ]
# )
# # print(messages)
# print(messages.id) # msg_qL6f8xUaRooXuAiGBiV6y1JG
#
# # """
# #  content=[{
# #     "type": "image_file",
# #     "image_file": "base64 encoded image file"
# # },
# #         {
# #     "type": "image_url",
# #     "image_url": "https://example.com/image.jpg"
# # }]
# # """
# #
################################################################################################################################################
#### Step-6 --> run the assistant using stream
#
# class EventHandler(AssistantEventHandler):
#     @override
#     def on_text_created(self, text) -> None:
#         print(f"\nassistant > ", end="", flush=True)
# 
#     @override
#     def on_text_delta(self, delta, snapshot):
#         print(delta.value, end="", flush=True)
# 
#     def on_tool_call_created(self, tool_call):
#         print(f"\nassistant > {tool_call.type}\n", flush=True)
# 
#     def on_tool_call_delta(self, delta, snapshot):
#         if delta.type == 'code_interpreter':
#             if delta.code_interpreter.input:
#                 print(delta.code_interpreter.input, end="", flush=True)
#             if delta.code_interpreter.outputs:
#                 print(f"\n\noutput >", flush=True)
#                 for output in delta.code_interpreter.outputs:
#                     if output.type == "logs":
#                         print(f"\n{output.logs}", flush=True)
# 
# 
# with openai.beta.threads.runs.stream(
#         thread_id="thread_W7c1wITiWNp7yTtMLDom5AW6",
#         assistant_id="asst_8Lkj24Ki8bBKUXfeTMSxUILt",
#         instructions="Please answer the question is simpler english with an example.",
#         event_handler=EventHandler(),
# ) as stream:
#     stream.until_done()
#
################################################################################################################################################
# OUTPUT :-
#
# assistant > Canonical constructors in Java are special types of constructors used with record classes.
# A record class is a special kind of class in Java introduced in Java 14 (as a preview feature) and formally introduced in Java 16.
# They are intended to be a simpler way to create data-carrying classes.
#
# A canonical constructor in a record is automatically created and corresponds to the list of components (fields) in the record.
# This constructor initializes the fields of the record directly.
#
# ### Example:
#
# Imagine you have a record class called `Person` with two fields: `name` and `age`.
#
# ```java
# public record Person(String name, int age) {
# }
# ```
#
# This record class automatically provides a canonical constructor like this:
#
# ```java
# public Person(String name, int age) {
#     this.name = name;
#     this.age = age;
# }
# ```
#
# Here’s how you can create an instance of `Person` using the canonical constructor:
#
# ```java
# Person person = new Person("Alice", 30);
# System.out.println(person.name());  // Output: Alice
# System.out.println(person.age());   // Output: 30
# ```
#
# In summary, canonical constructors in records help to reduce boilerplate code by automatically providing a constructor that initializes all the fields.
#
################################################################################################################################################
#### Step-6 --> Alternative way to run the assistant using create_and_poll
#
run = openai.beta.threads.runs.create_and_poll(
    thread_id="thread_W7c1wITiWNp7yTtMLDom5AW6",
    assistant_id="asst_8Lkj24Ki8bBKUXfeTMSxUILt",
    instructions="Please answer the question is simpler english with an example."
)

if run.status == 'completed':
    messages = openai.beta.threads.messages.list(
        thread_id="thread_W7c1wITiWNp7yTtMLDom5AW6"
    )
    print(messages.data[0].content[0].text.value)
else:
    print(run.status)
#
##################################################################################################################################################
# OUTPUT :-
#
# Canonical constructors in Java are special types of constructors used with record classes.
# A record class is a special kind of class in Java introduced in Java 14 (as a preview feature) and formally introduced in Java 16.
# They are intended to be a simpler way to create data-carrying classes.
#
# A canonical constructor in a record is automatically created and corresponds to the list of components (fields) in the record.
# This constructor initializes the fields of the record directly.
#
# ### Example:
#
# Imagine you have a record class called `Person` with two fields: `name` and `age`.
#
# ```java
# public record Person(String name, int age) {
# }
# ```
#
# This record class automatically provides a canonical constructor like this:
#
# ```java
# public Person(String name, int age) {
#     this.name = name;
#     this.age = age;
# }
# ```
#
# Here’s how you can create an instance of `Person` using the canonical constructor:
#
# ```java
# Person person = new Person("Alice", 30);
# System.out.println(person.name());  // Output: Alice
# System.out.println(person.age());   // Output: 30
# ```
#
# In summary, canonical constructors in records help to reduce boilerplate code by automatically providing a constructor that initializes all the fields.
