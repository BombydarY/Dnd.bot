import asyncio
import base64
import requests
import telebot
from openai import OpenAI
import handlers.client
from decorators import neur_bum
from settings import GPT_TOKEN

client = OpenAI(api_key=GPT_TOKEN)


@neur_bum
async def get_answer_gpt(quastion: str, promt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": promt},
            {"role": "user", "content": quastion}
        ]
    )

    return response.choices[0].message.content

@neur_bum
async def pic_make(promt: str):
    response = client.images.generate(
      model="dall-e-3",
      prompt=promt,
      size="1024x1024",
      quality="standard",
      n=1,
    )

    return response.data[0].url

@neur_bum
async def picture_detect(pic_way: str, promt: str):
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    # Path to your image
    image_path = pic_way

    # Getting the base64 string
    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {client.api_key}"
    }

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": promt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 301
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    return response.json()["choices"][0]["message"]["content"]


@neur_bum
def pic(link: str, text: str):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": text},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": link,
                        },
                    },
                ],
            }
        ],
        max_tokens=300,
    )

    return response.choices[0].message.content
