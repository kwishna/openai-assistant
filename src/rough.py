import base64
import os, openai
import dotenv

dotenv.load_dotenv()

# with open(os.path.abspath("./record-java.txt"), 'rb') as f:
#     print(f.read().decode('utf-8'))
#     print("-------------")


file = openai.files.content(file_id="file-WlFH4TVlPC08qH8oxadzh4Oc")
print(file.content)
# file.bytes
with open(os.path.abspath("./output.png"), 'wb') as f:
    f.write(file.content)
