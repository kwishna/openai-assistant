import os.path
import dotenv
import openai

dotenv.load_dotenv()

def save_file_from_message(messages):
    file = openai.files.content(file_id=messages.data[0].content[0].image_file.file_id)
    with open(os.path.abspath("./output.png"), 'wb') as f:
        f.write(file.content)

file = openai.files.create(file=open(os.path.abspath("./store-sales.xlsx"), 'rb'), purpose="assistants")

assistant = openai.beta.assistants.create(
    model='gpt-4o',
    temperature=0.7,
    instructions="You're an AI assistant who has access to tools to complete the task."
                 "You should apply ReAct and Tree-of-thoughts approach to complete the given task.",
    tools=[{"type": "code_interpreter"}],
    tool_resources={
        "code_interpreter": {
            "file_ids": [file.id]
        }
    }
)

thread = openai.beta.threads.create(
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "You're given an .CSV file. Please draw some insights from the data similar to the given image."
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://www.vector-eps.com/wp-content/gallery/charts-and-pies-vectors/3d-charts-and-pies-vector2.jpg"
                    }
                }
            ]
        }
    ],
)

run = openai.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions="Please answer the question is simpler english with an example."
)

if run.status == 'completed':
    messages = openai.beta.threads.messages.list(
        thread_id=thread.id
    )
    print(messages)
    print(messages.data[0].content)

    save_file_from_message(messages)
else:
    print(run.status)


## messages = openai.beta.threads.messages.list(thread_id="thread_eiZsjUMq3u1iVFHTe5Ev1LAR")
## print(messages.data[0].content[0].image_file.file_id)

"""
SyncCursorPage[Message](data=[Message(id='msg_talna5cVVKA6lA1lFxm5VgIe', assistant_id='asst_NSFyRbcvbwunY0pdrbItOBKY', attachments=[], completed_at=None, content=[ImageFileContentBlock(image_file=ImageFile(file_id='file-WlFH4TVlPC08qH8oxadzh4Oc', detail=None), type='image_file'), TextContentBlock(text=Text(annotations=[], value='The pie chart shows the distribution of sales by product category. "Office Supplies" account for the largest share of sales, followed by "Technology" and "Furniture."\n\n### Summary\n- **Order Priorities**: Most orders have "Low" priority, with "Critical," "Medium," and "High" following.\n- **Sales by Product Category**: "Office Supplies" generate the highest sales, followed by "Technology" and "Furniture."\n\nThese visualizations help us understand the distribution of order priorities and the contribution of different product categories to total sales. If you have any specific questions or need further analysis, feel free to ask!'), type='text')], created_at=1716694541, incomplete_at=None, incomplete_details=None, metadata={}, object='thread.message', role='assistant', run_id='run_6XDKZANH1FbyQIg7p09Guhjd', status=None, thread_id='thread_eiZsjUMq3u1iVFHTe5Ev1LAR'), Message(id='msg_e2LG9Ft2c0k7LbMvHnKHfg8l', assistant_id='asst_NSFyRbcvbwunY0pdrbItOBKY', attachments=[], completed_at=None, content=[ImageFileContentBlock(image_file=ImageFile(file_id='file-36vnjoXFei4Jj8XWvY7K3EDw', detail=None), type='image_file'), TextContentBlock(text=Text(annotations=[], value='The pie chart shows the distribution of order priorities. "Low" priority orders constitute the largest segment, followed by "Critical" (not specified), "Medium," and "High" priority orders.\n\n#### 2. Sales by Product Category\nNext, let\'s visualize the total sales amount for each product category.'), type='text')], created_at=1716694530, incomplete_at=None, incomplete_details=None, metadata={}, object='thread.message', role='assistant', run_id='run_6XDKZANH1FbyQIg7p09Guhjd', status=None, thread_id='thread_eiZsjUMq3u1iVFHTe5Ev1LAR'), Message(id='msg_rMLZHe7xpMFWbL6hAnXOUPfI', assistant_id='asst_NSFyRbcvbwunY0pdrbItOBKY', attachments=[], completed_at=None, content=[TextContentBlock(text=Text(annotations=[], value='The dataset contains various columns related to orders, such as "Order Priority," "Unit Price," "Shipping Cost," "Customer Name," "Product Category," "Region," and more.\n\n### Let\'s draw some insights from this data:\n1. **Distribution of Order Priorities**: How many orders fall into each priority category?\n2. **Sales by Product Category**: What is the total sales amount for each product category?\n\nWe\'ll create visualizations similar to a pie chart for these insights.\n\n#### 1. Distribution of Order Priorities\nLet\'s start by visualizing the distribution of order priorities.'), type='text')], created_at=1716694519, incomplete_at=None, incomplete_details=None, metadata={}, object='thread.message', role='assistant', run_id='run_6XDKZANH1FbyQIg7p09Guhjd', status=None, thread_id='thread_eiZsjUMq3u1iVFHTe5Ev1LAR'), Message(id='msg_nA0mw2xqaHycXkGlwfZfpRIU', assistant_id='asst_NSFyRbcvbwunY0pdrbItOBKY', attachments=[], completed_at=None, content=[TextContentBlock(text=Text(annotations=[], value='The Excel file contains a sheet named "Orders". Let\'s load the data from this sheet and take a look at the first few rows to understand its structure.'), type='text')], created_at=1716694513, incomplete_at=None, incomplete_details=None, metadata={}, object='thread.message', role='assistant', run_id='run_6XDKZANH1FbyQIg7p09Guhjd', status=None, thread_id='thread_eiZsjUMq3u1iVFHTe5Ev1LAR'), Message(id='msg_TjKthOSY2JZy4yTsjY35I191', assistant_id='asst_NSFyRbcvbwunY0pdrbItOBKY', attachments=[], completed_at=None, content=[TextContentBlock(text=Text(annotations=[], value="The extracted contents include several files and directories typically found in a Microsoft Excel file (.xlsx). It seems that the uploaded file is actually an Excel file compressed in the .xlsx format.\n\nLet's identify and read the main data sheet from the Excel file to draw insights from it."), type='text')], created_at=1716694506, incomplete_at=None, incomplete_details=None, metadata={}, object='thread.message', role='assistant', run_id='run_6XDKZANH1FbyQIg7p09Guhjd', status=None, thread_id='thread_eiZsjUMq3u1iVFHTe5Ev1LAR'), Message(id='msg_lMctZL9klR9Ow9UjsIzyrggy', assistant_id='asst_NSFyRbcvbwunY0pdrbItOBKY', attachments=[], completed_at=None, content=[TextContentBlock(text=Text(annotations=[], value='It looks like the file might not be a standard CSV file but rather a compressed file, such as a ZIP file. This is suggested by the presence of the "PK" header, which indicates a ZIP format.\n\nLet\'s try to extract the contents of this file to check if there are any CSV files within it.'), type='text')], created_at=1716694499, incomplete_at=None, incomplete_details=None, metadata={}, object='thread.message', role='assistant', run_id='run_6XDKZANH1FbyQIg7p09Guhjd', status=None, thread_id='thread_eiZsjUMq3u1iVFHTe5Ev1LAR'), Message(id='msg_EcyRm8VbH1UvAd6F9Mow98QA', assistant_id='asst_NSFyRbcvbwunY0pdrbItOBKY', attachments=[], completed_at=None, content=[TextContentBlock(text=Text(annotations=[], value="It appears that the CSV file has some inconsistencies or irregularities in its structure. To better understand the issue, let's read the first few lines of the file directly to see how the data is formatted. This will help us identify any problems with the file."), type='text')], created_at=1716694492, incomplete_at=None, incomplete_details=None, metadata={}, object='thread.message', role='assistant', run_id='run_6XDKZANH1FbyQIg7p09Guhjd', status=None, thread_id='thread_eiZsjUMq3u1iVFHTe5Ev1LAR'), Message(id='msg_MYGMbScSi6TwmCOOw8PWbj41', assistant_id='asst_NSFyRbcvbwunY0pdrbItOBKY', attachments=[], completed_at=None, content=[TextContentBlock(text=Text(annotations=[], value="It seems like there is an issue with the encoding of the CSV file. Let's try reading the file again with a different encoding, such as `ISO-8859-1` (also known as Latin-1), which is commonly used for files with special characters."), type='text')], created_at=1716694484, incomplete_at=None, incomplete_details=None, metadata={}, object='thread.message', role='assistant', run_id='run_6XDKZANH1FbyQIg7p09Guhjd', status=None, thread_id='thread_eiZsjUMq3u1iVFHTe5Ev1LAR'), Message(id='msg_U6YNpALWFZpIvFjuBDvev2V4', assistant_id='asst_NSFyRbcvbwunY0pdrbItOBKY', attachments=[], completed_at=None, content=[TextContentBlock(text=Text(annotations=[], value="Alright, let's start by examining the CSV file to understand its structure and content. Once we have a good understanding of the data, we can create some visualizations similar to the pie chart in the image.\n\nLet's load the CSV file and take a look at the first few rows."), type='text')], created_at=1716694474, incomplete_at=None, incomplete_details=None, metadata={}, object='thread.message', role='assistant', run_id='run_6XDKZANH1FbyQIg7p09Guhjd', status=None, thread_id='thread_eiZsjUMq3u1iVFHTe5Ev1LAR'), Message(id='msg_AZzV6tCbfk4q96AgS3Csb7dG', assistant_id=None, attachments=[], completed_at=None, content=[TextContentBlock(text=Text(annotations=[], value="You're given an .CSV file. Please draw some insights from the data similar to the given image."), type='text'), ImageURLContentBlock(image_url=ImageURL(url='https://www.vector-eps.com/wp-content/gallery/charts-and-pies-vectors/3d-charts-and-pies-vector2.jpg', detail='auto'), type='image_url')], created_at=1716694471, incomplete_at=None, incomplete_details=None, metadata={}, object='thread.message', role='user', run_id=None, status=None, thread_id='thread_eiZsjUMq3u1iVFHTe5Ev1LAR')], object='list', first_id='msg_talna5cVVKA6lA1lFxm5VgIe', last_id='msg_AZzV6tCbfk4q96AgS3Csb7dG', has_more=False)

content=[ImageFileContentBlock(image_file=ImageFile(file_id='file-WlFH4TVlPC08qH8oxadzh4Oc', detail=None), type='image_file'),

The pie chart shows the distribution of sales by product category.
"Office Supplies" account for the largest share of sales, followed by "Technology" and "Furniture."
### Summary- 
**Order Priorities**: Most orders have "Low" priority, with "Critical," "Medium," and "High" following.
**Sales by Product Category**: "Office Supplies" generate the highest sales, followed by "Technology" and "Furniture."
These visualizations help us understand the distribution of order priorities and the contribution of different product categories to total sales.
If you have any specific questions or need further analysis, feel free to ask!'
"""