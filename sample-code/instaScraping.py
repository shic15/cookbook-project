import requests
from openai import OpenAI
from dotenv import load_dotenv
import os
import time


load_dotenv()

actor_task_id = 'holographic_fahrenheit~instacookbook'

# URL for running the actor task synchronously and getting dataset items
url = f'https://api.apify.com/v2/actor-tasks/{actor_task_id}/run-sync-get-dataset-items'

apify_api_token = os.getenv("APIFY_API_KEY")

def getPostCaption(postUrl):
  input_data = {
      'username': [postUrl]
  }

  # Headers with the API token
  headers = {
      'Content-Type': 'application/json',
      'Authorization': f'Bearer {apify_api_token}'
  }

  response = requests.post(url, json=input_data, headers=headers)

  if response.status_code == 201:
      run_data = response.json()
      run_id = run_data[0]['id']  # Access the first item in the list
      print(f"Actor task run started successfully. Run ID: {run_id}")
      # print('Caption: ', run_data[0]['caption'])
  return run_data

captionRetrieved = getPostCaption('https://www.instagram.com/reel/CzTo-s1p4Uk/?hl=enhttps://www.instagram.com/reel/CzTo-s1p4Uk/?hl=en')

gpt_api_token = os.getenv("GPT_API_KEY")

client = OpenAI(api_key=gpt_api_token)

completion = client.chat.completions.create(
  model="gpt-3.5-turbo-1106",
  messages=[
    {"role": "system", "content": "You are a recipe master that converts a given recipe in any format to a json including array of ingredients, instructions and notes."},
    {"role": "user", "content": captionRetrieved[0]['caption']}
  ])
print(completion.choices[0].message.content)