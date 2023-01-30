import discord
import os
from dcs_server_trigger import *
import functools
import typing
import asyncio


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

def to_thread(func: typing.Callable) -> typing.Coroutine:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        wrapped = functools.partial(func, *args, **kwargs)
        return await loop.run_in_executor(None, wrapper)
    return wrapper

@to_thread
def start_dcs():
    message = dcs_server_start()
    return message

@client.event
async def on_message(message):

    if message.content == "!dcs start":
        
        
        msg = await message.channel.send("Checking status....")
        #await msg.add_reaction("👋")
        #await msg.add_reaction("🙂")
        status, is_active = dcs_server_status()
        await message.channel.send(status)
        if is_active == False:
            await message.channel.send("Starting DCS Server.... This can take about 15 minutes.")
            start_msg = dcs_server_start()
            await message.channel.send(start_msg)
        elif is_active == True:
            await message.channel.send("Pew Pew time!")
        else:
            await message.channel.send("UwU something sussybaka is going on here. Pokey wokey your local Admin. Nyaaaaaa~~~")


    elif message.content == "!dcs stop":
        dcs_server_stop()
        msg = await message.channel.send("DCS Server deleting....")
    elif message.content == "!dcs status":
        await message.channel.send("Checking status....")
        status, is_active = dcs_server_status()
        await message.channel.send(status)



@client.event
async def on_reaction_add(reaction, user):
    if user != client.user:
        if reaction.emoji == "👋":
            await reaction.message.channel.send("You reacted with a wave.")
        elif reaction.emoji == "🙂":
            await reaction.message.channel.send("You reacted with a smile.")

nyaaim = os.getenv("NYAAIM_NINE")
client.run(token=nyaaim)