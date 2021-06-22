from os import getenv
import os
import discord
from discord.ext import commands
from mcstatus import MinecraftServer
import sqlite3
import asyncio

TOKEN = getenv('TOKEN')

if TOKEN is None:
    try:
        with open('token.txt') as file:
            TOKEN = file.readline()
    except:
        print("Can't find discord token. You need to ether set it as an env variable or put it in a file called token.txt")
        exit()


con = sqlite3.connect('data/database.db')
cur = con.cursor()

# if table doesn't exist, make new one
cur.execute('''
CREATE TABLE IF NOT EXISTS servers (
server_ip TEXT NOT NULL,
channel_id INTEGER NOT NULL,
message TEXT NOT NULL
)
''')

discord_client = commands.Bot(command_prefix='MCstat ')


@discord_client.command()
async def num_online(ctx, mc_ip, channel: discord.VoiceChannel, message):
    if not ctx.message.author.guild_permissions.administrator:
        await ctx.send('need to be admin for that')
    cur.execute('''
    INSERT INTO servers (server_ip, channel_id, message)
    VALUES('{}', {}, '{}')
    '''.format(mc_ip, channel.id, message))
    con.commit()
    await ctx.send('done')


async def update_stats():
    await discord_client.wait_until_ready()
    stats_update_cursor = con.cursor()
    while not discord_client.is_closed():
        stats_update_cursor.execute(''' SELECT * FROM servers ''')
        for server in stats_update_cursor.fetchall():
            try:
                status = MinecraftServer.lookup(server[0]).status()
                channel = await discord_client.fetch_channel(server[1])
                await channel.edit(name=server[2].format(status.players.online))
            except:
                pass
        await asyncio.sleep(5 * 60)

discord_client.loop.create_task(update_stats())
discord_client.run(TOKEN)
