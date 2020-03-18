"""
This is a CTF answer-checking and scoring bot.
I hope it doesn't die.
"""

import logging
import hashlib
import pickle
import argparse
import task_list
from team import Team
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '991261972:AAHX8Xtq4N6i0vtdTjaVcD3w5CPz5_9CuLg'
# ROSKOMPOZOR
PROXY = "socks5://163.172.152.192:1080"
task_list.populate_tasks()
teams = []
tasks = task_list.tasks

# Configure logging
logging.basicConfig(level=logging.INFO)

# Unpickle data if necessary
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument("--unpickle", help="Unpickle stored data")
args = parser.parse_args()
pickled_teams_file = 'teams.pickle'
pickled_tasks_file = 'tasks.pickle'
if args.unpickle:
    with open(pickled_tasks_file, 'rb') as file:
        tasks = pickle.load(file)
    with open(pickled_teams_file, 'rb') as file:
        teams = pickle.load(file)


# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN, proxy=PROXY)
dp = Dispatcher(bot)


def str_to_html(string):
    return "<pre>" + string + "</pre>"


def result_print(n):
    if n > 1:
        return 'F'
    if n == 1:
        return 'S'
    return 'n'


@dp.message_handler(commands='start')
async def startup(message: types.Message):
    team_id = message.from_user.id
    team_pretty_id = "{:} {:}".format(message.from_user.first_name, message.from_user.last_name)
    message_contents = message.text.split()
    team_name = ''
    if len(message_contents) > 1:
        team_name = message_contents[1]
    team = next((item for item in teams if item.owner == team_id), None)
    if team is not None:
        if team_name is '':
            await message.answer("Your team name is %s" % team.name)
        elif team_name == 'clear':
            teams.remove(team)
            await message.answer("Team cleared")
        else:
            team.name = team_name
            await message.answer("New team name is %s" % team.name)
    else:
        teams.append(Team(team_name=team_name, owner_id=team_id, owner_pretty=team_pretty_id, size=len(tasks)))
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
            result_line = "{:<3}- {:<20}- {:<4}\n".format(i, tasks[i].name, result_print(team.results[i]))
            result_list += result_line
        await message.answer(str_to_html(result_list), parse_mode='HTML')
    else:
        await message.answer("Unknown team (hint: /start)")


@dp.message_handler(commands='list_tasks')
async def list_tasks(message: types.Message):
    task_list = ''
    for i in range(len(tasks)):
        task_line = "{:<3}- {:<20}- {:<4}\n".format(i, tasks[i].name, tasks[i].value)
        task_list += task_line
    file = open('task_ids.txt', 'w')
    print(task_list, file=file)
    file.close()
    await message.answer(str_to_html(task_list), parse_mode='HTML')


@dp.message_handler(commands='stats')
async def all_results(message: types.Message):
    if len(teams) is not 0 and len(list(filter(lambda team: team.name != '', teams))) is not 0:
        await message.answer("Format: 'place - team_name - result'")
        stats = []
        for team in teams:
            if team.name == '':
                continue
            res = 0
            for i in range(len(tasks)):
                res += tasks[i].value * team.results[i]
            stats.append({'name': team.name, 'result': int(res)})
        stats = sorted(stats, key=lambda i: i['result'], reverse=True)
        results = ''
        for i in range(len(stats)):
            results += "{:<3}- {:<18}- {:<4}\n".format(i+1, stats[i]["name"], stats[i]["result"])
        file = open('results.txt', 'w')
        print(results, file=file)
        file.close()
        await message.answer(str_to_html(results), parse_mode='HTML')
    else:
        await message.answer("No teams registered")


@dp.message_handler(commands='stats_det')
async def all_results_detailed(message: types.Message):
    message_contents = message.text.split()
    show_names = 0
    if len(message_contents) == 2 and message_contents[1] == 'names':
        show_names = 1
    if len(teams) is not 0 and len(list(filter(lambda team: team.name != '', teams))) is not 0:
        await message.answer("Format: 'team_name - task_result(by ID)'")
        results = ''
        for team in teams:
            if team.name == '':
                continue
            result_line = "{:<18}- ".format(team.name)
            for result in team.results:
                result_line += "{:<2}".format(result_print(result))
            if show_names:
                result_line += f"{team.owner_pretty}"
            result_line += "\n"
            results += result_line
        if show_names:
            file = open('results_detailed.txt', 'w')
            print(results, file=file)
            file.close()
        await message.answer(str_to_html(results), parse_mode='HTML')
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
            if flag == tasks[task_id].answer:
                if tasks[task_id].first_solver == '':
                    tasks[task_id].first_solver = team.owner
                team.results[task_id] = 1
                if team.owner == tasks[task_id].first_solver:
                    team.results[task_id] += 0.1
                await message.answer("Correct, well done")
                await pickle_data(message)
            else:
                await message.answer("Wrong answer")
    else:
        await message.answer("Unknown team (hint: /start *team_name*)")


@dp.message_handler(commands='help')
async def print_help(message: types.Message):
    help = []
    help.append("This bot is held together with duct tape and prayers. Please do not break it.")
    help.append("Bot is liable to lose your flags. Back them up elsewhere.")
    help.append("Command reference:")
    command_ref = ''
    command_ref += '/start *team_name* - create your team or change team name\n'
    command_ref += '/start clear - clear team name\n'
    command_ref += '/list_tasks - view all tasks and their IDs\n'
    command_ref += '/stats - view global ranking\n'
    command_ref += '/stats_det - view global results by task\n'
    command_ref += '/my_stats - view solved tasks\n'
    command_ref += '/check_flag *task_id* *flag* - check task solution\n'
    command_ref += '/help - print this message\n'
    help.append(command_ref)
    help.append("Stats help: n - not solved, S - solved, F - solved first (1.1)")
    for line in help:
        await message.answer(line)


@dp.message_handler(commands='pickle')
async def pickle_data(message: types.Message):
    with open(pickled_tasks_file, 'wb') as file:
        pickle.dump(tasks, file)
    with open(pickled_teams_file, 'wb') as file:
        pickle.dump(teams, file)
    print("Pickled teams and tasks")


@dp.message_handler(commands='update_tasks')
async def update_tasks(message: types.Message):
    task_list.populate_tasks()
    global tasks
    tasks = task_list.tasks
    print("Updated task list")


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer("Unrecognized command")
    await print_help(message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
