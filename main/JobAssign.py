#Job assign bot
#Made by AARON Ramsey (aaronramsey2000@gmail.com)

import os

import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')
client = discord.Client()

@bot.event
async def on_ready():
    print(
        f'{bot.user.name} has connected to Discord!'
    )

@bot.command(name="assignJob", help="assigns a job to a person")
async def assignJob(ctx, person: str, job: str):
    file = open("../files/" + person[3:21] + ".txt", "a")
    file.write(job + "\n")
    response = "Job assigned"
    file.close()
    await ctx.send(response)

def getJobs(person):
    file = open("../files/" + person + ".txt", "r")

    response = "<@!" + person + "> these are the jobs you have to do \n"
    data = file.readlines()
    for line in data:
        response += line
    return response

@bot.command(name="seeJobs", help="gets the jobs for that user")
async def seeJobs(ctx, person: str):
    await ctx.send(getJobs(person[3:21]))

@bot.command(name="seeMyJobs", help="gets you your jobs to do")
async def seeMyJobs(ctx):
    await ctx.send(getJobs(str(ctx.author.id)))

@bot.command(name="jobDone", help="removes a job when it is done")

bot.run(TOKEN)