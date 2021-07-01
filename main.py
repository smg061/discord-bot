import discord
import requests
import random
import http.client
import urllib.parse
import json
import os
from dotenv import load_dotenv
from database import connect_to_db
from discord.ext import commands

load_dotenv()

# setting up the connection
client = commands.Bot(command_prefix='$')
db_client = connect_to_db()
collection = db_client.DiscordBotDb.User


async def request_quote(message):
    r = requests.post(
        "https://api.deepai.org/api/text-generator",
        data={
            'text': message
        },
        headers={'api-key': os.getenv('OPENAI_API_KEY')}
    )
    return r.json()


async def request_magic_ball(question):
    conn = http.client.HTTPSConnection("8ball.delegator.com")
    conn.request('GET', '/magic/JSON/' + question)
    response = conn.getresponse()
    return json.loads(response.read())


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.command(brief="Generate text using the OPENAI Natural Language Processing model API")
async def generate(context, *args):
    prompt = " ".join(args)
    quote = await request_quote(prompt)
    try:
        await context.send(quote['output'])
    except KeyError:
        await context.send(quote)


@client.command(brief="Return what you just said right back")
async def echo(context, *args):
    prompt = " ".join(args)
    await context.send(f'You wrote: "{prompt}"')


@client.command(brief="Ask a question to the magic 8-ball")
async def magic_ball(context, *args):
    question = " ".join(args)
    print(urllib.parse.quote(question))
    magic_ball_response = await request_magic_ball(urllib.parse.quote(question))
    print(magic_ball_response)
    try:
        await context.send(magic_ball_response['magic']['answer'])
    except:
        await context.send("Something went wrong with your request")

@client.command(brief="agony, pure pain")

async def agony(context):
    length = random.randint(5,120)
    scream = ''.join(random.choice(['a', 'A']) for i in range(length))
    await context.send(scream)


@client.event
async def on_message(message):
    if message.content.startswith("$save"):
        collection.insert_one({"user": str(message.author), "message": message.content})
        await message.channel.send("I saved your message")
    elif message.content.startswith("$hello"):
        await message.channel.send(f'Hello, {message.author.name}!')
        print(message)
    await client.process_commands(message)



client.run(os.getenv('TOKEN'))
