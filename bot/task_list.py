import os
import hashlib

tasks = []


class Task:
    type: str = "task"

    def __init__(self, name, group, answer, value):
        self.name: str = name
        self.group: str = group
        self.answer: str = answer
        self.value: int = value
        self.first_solver: str = ''


def populate_tasks():
    global tasks
    tasks = []
    task_groups = ['Crypto', 'Osint', 'Reverse', 'Stegano']
    for task_group in task_groups:
        names = os.listdir('../{:}'.format(task_group))
        for name in names:
            hash_path = '../{:}/{:}/hash.txt'.format(task_group, name)
            secret_path = '../{:}/{:}/secret.txt'.format(task_group, name)
            value_path = '../{:}/{:}/value.txt'.format(task_group, name)
            ans_hash = ''
            value = 100
            if os.path.isfile(hash_path):
                hash_file = open(hash_path)
                ans_hash = hash_file.read().rstrip()
                hash_file.close()
            elif os.path.isfile(secret_path):
                secret_file = open(secret_path)
                ans = secret_file.read().rstrip()
                ans_hash = hashlib.md5(ans.encode('utf-8')).hexdigest()
                secret_file.close()
                hash_file = open(hash_path, "w")
                print(ans_hash, file=hash_file)
                hash_file.close()
            else:
                print("Task with no answer: {:}".format(name))
            if os.path.isfile(value_path):
                value_file = open(value_path)
                value = int(value_file.read().rstrip())
                value_file.close()
            else:
                value_file = open(value_path, 'w')
                print(value, file=value_file)
                value_file.close()
            tasks.append(Task(name, task_group, ans_hash, value))


if __name__ == '__main__':
    populate_tasks()
    print(tasks)
