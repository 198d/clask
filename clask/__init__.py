import re
import sys
import os
import subprocess
import tempfile
from argparse import ArgumentParser
from time import time

import yaml
from dulwich.repo import Repo
from dulwich.config import StackedConfig
from dulwich.objects import Blob, Tree, Commit
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


_repo = Repo('.')
_config = _repo.get_config_stack()


def init():
    try:
        _repo.refs['refs/heads/clask']
    except KeyError:
        _commit({'.gitkeep': ''}, 'Initialize clask')


def add(slug):
    task_template = "title: {0}\ndescription: [insert description]\n" \
        "state: unstarted\n"
    task = _load_task_from_string(
        _get_input_from_editor(task_template.format(slug)))
    name = _task_filename(slug)

    _commit({name: _dump_task(task)},
        'Create task: {0}'.format(slug))


def move(slug, new_state, finish=False):
    tree_dict = dict()
    tree_entry = _task_filename(slug)

    if finish:
        tree_dict[tree_entry] = None
        tree_entry = _task_filename(slug, finished=True)

    task = _load_task(slug)
    old_state = task['state']
    task['state'] = new_state

    tree_dict[tree_entry] = _dump_task(task)
    _commit(tree_dict, "Change state: {0} -> {1}".format(old_state, new_state))


def edit(slug):
    blob = _get_blob(slug)
    task = _load_task_from_string(_get_input_from_editor(blob.data))
    tree_entry = _task_filename(slug)

    _commit({tree_entry: _dump_task(task)}, "Update task: {0}".format(slug))


def finish(slug):
    move(slug, 'finished', finish=True)


def _get_input_from_editor(default=None):
    editor = os.environ.get('EDITOR', 'vim')
    with tempfile.NamedTemporaryFile(suffix=".yml", delete=False) as temp_file:
        if default:
            temp_file.write(default)
            temp_file.flush()
        subprocess.call([editor, temp_file.name])
    with file(temp_file.name) as f:
        return f.read()


def _commit(tree_dict, message):
    try:
        head = _get_repo_object(_get_clask_head())
        tree = _get_repo_object(head.tree)
    except KeyError:
        head = None
        tree = Tree()

    for name, contents in tree_dict.items():
        if contents is None:
            del tree[name]
        else:
            blob = Blob.from_string(contents)
            _repo.object_store.add_object(blob)
            tree[name] = (0100644, blob.id)

    commit = Commit()
    commit.parents = [head.id] if head else []
    commit.tree = tree.id
    commit.author = commit.committer = "{0} <{1}>".format(
        _config.get('user', 'name'), _config.get('user', 'email'))
    commit.author_time = commit.commit_time = int(time())
    commit.author_timezone = commit.commit_timezone = 0
    commit.encoding = 'UTF-8'
    commit.message = message

    _repo.object_store.add_object(tree)
    _repo.object_store.add_object(commit)

    _repo['refs/heads/clask'] = commit.id


def _get_clask_head():
    return _repo.refs['refs/heads/clask']


def _get_repo_object(id):
    return _repo[id]


def _get_blob(slug):
    tree_entry = _task_filename(slug)
    head = _get_repo_object(_get_clask_head())
    tree = _get_repo_object(head.tree)
    try:
        _, sha = tree[tree_entry]
    except KeyError:
        tree_entry = _task_filename(slug, finished=True)
        _, sha = tree[tree_entry]
    return _get_repo_object(sha)


def _task_filename(slug, finished=False):
    template = '.{0}.yml' if finished else '{0}.yml'
    return template.format(slug)


def _load_task(slug):
    blob = _get_blob(slug)
    return _load_task_from_string(blob.data)


def _load_task_from_string(task):
    return yaml.load(task, Loader=Loader)


def _dump_task(task):
    return yaml.dump(task, Dumper=Dumper, default_flow_style=False)


def main():
    commands = ['init', 'add', 'move', 'edit', 'finish']
    parser = ArgumentParser(
        description="A command-line task manager powered by git.",
        epilog="Available commands: {0}".format(', '.join(commands)))
    parser.add_argument('command')
    parser.add_argument('args', nargs='*')

    args = parser.parse_args()
    if args.command in commands:
        globals()[args.command](*args.args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
