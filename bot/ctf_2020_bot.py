"""
This is a CTF answer-checking and scoring bot.
I hope it doesn't die.
"""

import logging
import hashlib
import task_list
from team import Team
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '991261972:AAHX8Xtq4N6i0vtdTjaVcD3w5CPz5_9CuLg'
# ROSKOMPOZOR
PROXY = "socks5://163.172.152.192:1080"
task_list.populate_tasks()
tasks = task_list.tasks

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN, proxy=PROXY)
dp = Dispatcher(bot)
teams = []


@dp.message_handler(commands='start')
async def startup(message: types.Message):
    team_id = message.from_user.id
    message_contents = message.text.split()
    team_name = ''
    if len(message_contents) > 1:
        team_name = message_contents[1]
    team = next((item for item in teams if item.owner == team_id), None)
    if team is not None:
        if team_name is '':
            await message.answer("Your team name is %s" % team.name)
        else:
            team.name = team_name
            await message.answer("New team name is %s" % team.name)
    else:
        teams.append(Team(team_name=team_name, owner_id=team_id))
        await message.answer("New team created")
        await print_help(message)
        if team_name is not '':
            await message.answer("Team name: %s" % team_name)
        else:
            await message.answer("Team name empty (hint: /start *team_name*)")


@dp.message_handler(commands='my_stats')
async def team_results(message: types.Message):
    team = next((item for item in teams if item.owner == message.from_user.id), None)
    if team is not None:
        result_list = ''
        for i in range(len(tasks)):
            result_line = "{:<2}- {:<15}\n".format(team.results[i], tasks[i]['name'])
            result_list += result_line
            print(result_list)
        await message.answer(result_list)
    else:
        await message.answer("Unknown team (hint: /start)")


@dp.message_handler(commands='list_tasks')
async def list_tasks(message: types.Message):
    task_list = ''
    for i in range(len(tasks)):
        task_line = "{:<3}- {:<14}\n".format(i, tasks[i]['name'])
        task_list += task_line
    await message.answer(task_list)


@dp.message_handler(commands='stats')
async def all_results(message: types.Message):
    if len(teams) is not 0:
        await message.answer("Format: 'place - team_name - result(number of solved tasks)'")
        stats = []
        for team in teams:
            stats.append({'name': team.name, 'result': sum(team.results)})
        stats = sorted(stats, key=lambda i: i['result'], reverse=True)
        results = ''
        for i in range(len(stats)):
            results += "{:<3}- {:<14}- {:<3}\n".format(i+1, stats[i]["name"], stats[i]["result"])
        await message.answer(results)
    else:
        await message.answer("No teams registered")


@dp.message_handler(commands='stats_det')
async def all_results_detailed(message: types.Message):
    if len(teams) is not 0:
        await message.answer("Format: 'team_name - task_result(by ID)'")
        results = ''
        for team in teams:
            result_line = "{:<14}- ".format(team.name)
            for result in team.results:
                result_line += "{:<2}".format(result)
            result_line += "\n"
            results += result_line
        await message.answer(results)
    else:
        await message.answer("No teams registered")


@dp.message_handler(commands='check_flag')
async def check_flag(message: types.Message):
    team = next((item for item in teams if item.owner == message.from_user.id), None)
    hint = "Format: '/check_flag task_id *flag*'"
    if team is not None:
        message_contents = message.text.split()
        if len(message_contents) is not 3 or not message_contents[1].isdigit():
            await message.answer("Wrong format")
            await message.answer(hint)
        else:
            task_id = int(message_contents[1])
            if task_id >= len(tasks):
                await message.answer("Task ID out of range (hint: /list_tasks)")
                return
            flag = hashlib.md5(message_contents[2].encode('utf-8')).hexdigest()
            if flag == tasks[task_id]['answer']:
                team.results[task_id] = 1
                await message.answer("Correct, well done")
            else:
                await message.answer("Wrong answer")
    else:
        await message.answer("Unknown team (hint: /start *team_name*)")


@dp.message_handler(commands='help')
async def print_help(message: types.Message):
    help = []
    help.append("This bot is held together with duct tape and prayers. Please do not break it.")
    help.append("Command reference:")
    command_ref = ''
    command_ref += '/start *team_name* - create your team or change team name\n'
    command_ref += '/list_tasks - view all tasks and their IDs\n'
    command_ref += '/stats - view global ranking\n'
    command_ref += '/stats_det - view global results by task\n'
    command_ref += '/my_stats - view solved tasks\n'
    command_ref += '/check_flag *task_id* *flag* - check task solution\n'
    command_ref += '/help - print this message\n'
    help.append(command_ref)
    for line in help:
        await message.answer(line)


@dp.message_handler()
async def echo(message: types.Message):
    message_hash = hashlib.md5(message.text.encode('utf-8'))
    await message.answer(message_hash.hexdigest())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
