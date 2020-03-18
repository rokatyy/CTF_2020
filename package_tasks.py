import os
import re
from shutil import copyfile, make_archive, rmtree

task_pack = 'task_pack'
os.makedirs(task_pack, exist_ok=True)


def package():
    task_groups = ['Crypto', 'Osint', 'Reverse', 'Stegano']
    reverse_index = re.compile(r"(\.c|\.cpp|\.py)")
    for task_group in task_groups:
        names = os.listdir('{:}'.format(task_group))
        for name in names:
            name_dir = '{:}/{:}'.format(task_group, name)
            new_name_dir = '{:}/{:}/{:}'.format(task_pack, task_group, name)
            os.makedirs(new_name_dir, exist_ok=True)
            files = os.listdir(name_dir)
            for file in files:
                if file in ['hash.txt', 'secret.txt', 'value.txt'] or 'hidden' in file or reverse_index.search(file):
                    continue
                file_address = '{:}/{:}'.format(name_dir, file)
                new_file_address = '{:}/{:}'.format(new_name_dir, file)
                copyfile(file_address, new_file_address)
    make_archive(task_pack, 'tar', task_pack)
    rmtree(task_pack)


if __name__ == '__main__':
    package()
