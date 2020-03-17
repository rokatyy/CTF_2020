import os
import hashlib


tasks = []


def populate_tasks():
    task_groups = ['Crypto', 'Osint', 'Reverse', 'Stegano']
    for task_group in task_groups:
        names = os.listdir('../{:}'.format(task_group))
        for name in names:
            hash_path = '../{:}/{:}/hash.txt'.format(task_group, name)
            secret_path = '../{:}/{:}/secret.txt'.format(task_group, name)
            if os.path.isfile(hash_path):
                hash_file = open(hash_path)
                ans_hash = hash_file.read().rstrip()
                hash_file.close()
                tasks.append({'name': name, 'group': task_group, 'answer': ans_hash})
            elif os.path.isfile(secret_path):
                secret_file = open(secret_path)
                ans = secret_file.read().rstrip()
                ans_hash = hashlib.md5(ans.encode('utf-8')).hexdigest()
                secret_file.close()
                hash_file = open(hash_path, "w")
                print(ans_hash, file=hash_file)
                hash_file.close()
                tasks.append({'name': name, 'group': task_group, 'answer': ans_hash})



if __name__ == '__main__':
    populate_tasks()
