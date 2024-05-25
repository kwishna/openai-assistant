import os
import dotenv
import openai

dotenv.load_dotenv()

FILE_IDS = []
MESSAGE_IDS = []

assistant = openai.beta.assistants.create(
    model='gpt-4o',
    temperature=0.7,
    instructions="You're an AI assistant who has access to tools to complete the task."
                 "You should apply ReAct and Tree-of-thoughts approach to complete the given task.",
    tools=[{"type": "code_interpreter"}]
)
ASSISTANT_ID = assistant.id

print("Assistant ID: ", ASSISTANT_ID)
##
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
################################################################################################################################################
##### Step-2 --> Thread created

thread = openai.beta.threads.create()
THREAD_ID = thread.id

print("Thread ID: ", THREAD_ID)
##
################################################################################################################################################
#### Step-3 --> file (Optional) [Only required for retrieval]
#
file = openai.files.create(file=open(os.path.abspath("./record-java.txt"), 'rb'), purpose="assistants")
FILE_IDS.append(file.id)

print("FILE IDS: ", FILE_IDS)
#
################################################################################################################################################
#### Step-5 --> create and attach message to the thread

ATTACHMENTS = []

for file_id in FILE_IDS:
    ATTACHMENTS.append(
        {
            "file_id": file_id,
            "tools": [
                {
                    "type": "file_search"
                }
            ]
        }
    )

print("ATTACHMENTS: ", ATTACHMENTS)

message = openai.beta.threads.messages.create(
    thread_id=THREAD_ID,
    role="user",
    attachments=ATTACHMENTS,
    content=[
        {
            "type": "text",
            "text": "What is Canonical Constructors in Java?"
        }
    ]
)
MESSAGE_IDS.append(message.id)

# #
# #  content=[{
# #     "type": "image_file",
# #     "image_file": "base64 encoded image file"
# # },
# # {
# #     "type": "image_url",
# #     "image_url": "https://example.com/image.jpg"
# # }]
# #

################################################################################################################################################
#### Step-6 --> Alternative way to run the assistant using create_and_poll
#
run = openai.beta.threads.runs.create_and_poll(
    thread_id=THREAD_ID,
    assistant_id=ASSISTANT_ID,
    instructions="Please answer the question is simpler english with an example."
)

if run.status == 'completed':
    messages = openai.beta.threads.messages.list(
        thread_id=THREAD_ID
    )
    print(messages.data[0].content[0].text.value)
else:
    print(run.status)

################################################################################################################################################
# Assistant ID:  asst_kdQB9BurTkU8iaq7XxxTrH4M
# Thread ID:  thread_pVhuWoXYNHXDYuFJXvQ6pHYF
# FILE IDS:  ['file-F0uY14yCqoJET60GRnJY5MOs']
# ATTACHMENTS:  [{'file_id': 'file-F0uY14yCqoJET60GRnJY5MOs', 'tools': [{'type': 'file_search'}]}]
# In Java, a canonical constructor is a constructor that initializes all the fields of a class. It's the most complete constructor you can define for a class because it sets values for all the instance variables. This is useful for creating fully initialized objects in one go.
#
# Here's a simple example to illustrate this:
#
# Imagine you have a class called `Person` with three fields: `name`, `age`, and `address`.
#
# ```java
# public class Person {
#     private String name;
#     private int age;
#     private String address;
#
#     // Canonical Constructor
#     public Person(String name, int age, String address) {
#         this.name = name;
#         this.age = age;
#         this.address = address;
#     }
# }
# ```
#
# In this example, the constructor `Person(String name, int age, String address)` is the canonical constructor because it takes all the necessary parameters to initialize a `Person` object completely.
#
# Here's how you might use this canonical constructor:
#
# ```java
# public class Main {
#     public static void main(String[] args) {
#         Person person = new Person("John Doe", 30, "123 Main St");
#         System.out.println(person.name);  // Output: John Doe
#         System.out.println(person.age);   // Output: 30
#         System.out.println(person.address); // Output: 123 Main St
#     }
# }
# ```
#
# In this way, you ensure that every `Person` object is created with all the required information right from the start.