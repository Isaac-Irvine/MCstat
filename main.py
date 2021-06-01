from os import getenv
import os
import discord
from discord.ext import commands
from mcipc.query import Client
import asyncio

TOKEN = getenv('TOKEN')

if TOKEN is None:
    try:
        with open('token.txt') as file:
            TOKEN = file.readline()
    except:
        print("Can't find discord token. You need to ether set it as an env variable or put it in a file called token.txt")
        exit()


# TODO: save and read this for a file
servers = []

discord_client = commands.Bot(command_prefix='MCstat ')


@discord_client.command()
async def num_online(ctx, channel: discord.VoiceChannel, mc_ip, mc_port, message):
    if not ctx.message.author.guild_permissions.administrator:
        await ctx.send('need to be admin for that')
    servers.append({
        'channel': channel,
        'ip': mc_ip,
        'port': int(mc_port),
        'message': message})
    await ctx.send('done')


async def update_stats():
    await discord_client.wait_until_ready()

    while not discord_client.is_closed():
        for server in servers:
            try:
                with Client(server['ip'], server['port']) as minecraft_client:
                    stats = minecraft_client.stats(full=True)
                    await server['channel'].edit(name=server['message'].format(stats.num_players))
            except:
                pass
        await asyncio.sleep(5)


discord_client.loop.create_task(update_stats())
discord_client.run(TOKEN)
