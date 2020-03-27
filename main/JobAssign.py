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

def getFilename(person):
    return "../files/" + person + ".txt"

@bot.event
async def on_ready():
    print(
        f'{bot.user.name} has connected to Discord!'
    )

@bot.command(name="assignJob", help="assigns a job to a person")
async def assignJob(ctx, person: str, job: str):
    file = open(getFilename(person[3:21]), "a")
    file.write(job + "\n")
    response = "Job assigned"
    file.close()
    await ctx.send(response)

def getJobs(person):
    file = open(getFilename(person), "r")

    data = file.readlines()
    response = "```\n"
    for line in data:
        response += "-" + line
    file.close()
    response += "```"
    return response

def getInProgJobs(person):
    response = "<@!" + person + "> these are the jobs you have to do: \n"
    response += getJobs(person)
    return response

def getDoneJobs(person):
    response = "<@!" + person + "> has done these jobs: \n"
    response += getJobs(person+"-DONE")
    return response

@bot.command(name="seeJobs", help="gets the jobs for that user")
async def seeJobs(ctx, person: str):
    await ctx.send(getInProgJobs(person[3:21]))

@bot.command(name="seeMyJobs", help="gets you your jobs to do")
async def seeMyJobs(ctx):
    await ctx.send(getInProgJobs(str(ctx.author.id)))

def jobDone(person, job):
    file = open(getFilename(person), "r")
    jobs = file.readlines()
    file.close()

    writeFile = open(getFilename(person), "w")
    jobs2write = ""

    for line in jobs:
        if line != job + "\n":
            jobs2write += line
        else:
            doneFile = open(getFilename(person + "-DONE"), "a")
            doneFile.write(line)
            doneFile.close()

    writeFile.writelines(jobs2write)
    writeFile.close()
    return job + " removed from <@!" + person + ">'s to do list"

@bot.command(name="doneMyJob", help="removes a job you have done")
async def removeMyJob(ctx, job: str):
    await ctx.send(jobDone(str(ctx.author.id), job))

@bot.command(name="jobDone", help="removes a job when it is done")
async def removeJob(ctx, person: str, job: str):
    await ctx.send(jobDone(str(person[3:21]), job))

@bot.command(name="doneJobs", help="gets you the jobs done by that person")
async def doneJobs(ctx, person: str):
    await ctx.send(getDoneJobs(person[3:21]))

@bot.command(name="myDoneJobs", help="gets you the jobs you have done")
async def myDoneJobs(ctx):
    await ctx.send(getDoneJobs(str(ctx.author.id)))

bot.run(TOKEN)