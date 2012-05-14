import os
import subprocess
import tempfile
from argparse import ArgumentParser

from clask import repo, task


def init(args):
    repo.init()


def add(args):
    slug = args.slug
    task_template = "title: {0}\ndescription: [insert description]\n" \
        "state: unstarted\n"
    task_ = task.from_string(_get_input_from_editor(task_template.format(slug)))
    task.add(slug, task_)


def move(args, finish=False):
    slug, new_state = (args.slug, args.state)
    task.move(slug, new_state, finish)


def edit(args):
    slug = args.slug
    task_ = task.from_string(_get_input_from_editor(task.source(slug)))
    task.update(slug, task_)


def finish(args):
    args.state = 'finished'
    move(args, finish=True)


def start(args):
    args.state = 'started'
    move(args)


def _get_input_from_editor(default=None):
    editor = os.environ.get('EDITOR', 'vim')
    with tempfile.NamedTemporaryFile(suffix=".yml", delete=False) as temp_file:
        if default:
            temp_file.write(default)
            temp_file.flush()
        subprocess.call([editor, temp_file.name])
    with file(temp_file.name) as f:
        return f.read()


def main():
    parser = ArgumentParser(
        description="A command-line task manager powered by git.")
    subparsers = parser.add_subparsers(title='Commands')

    init_parser = subparsers.add_parser('init',
        help='Initialize a clask project',
        description='Initialize a clask project.')
    init_parser.set_defaults(func=init)

    add_parser = subparsers.add_parser('add',
        help='Add a task to the current clask project',
        description='Add a task to the current clask project.')
    add_parser.add_argument('slug', help='slug of the task to add')
    add_parser.set_defaults(func=add)

    move_parser = subparsers.add_parser('move',
        help='Move a task in the current clask project to a new state',
        description='Move a task in the current clask project to a new state.')
    move_parser.add_argument('slug', help='slug of the task to move')
    move_parser.add_argument('state', help='new state of the task')
    move_parser.set_defaults(func=move)

    start_parser = subparsers.add_parser('start',
        help='Start a task in the current clask project',
        description='Start a task in the current clask project.')
    start_parser.add_argument('slug', help='slug of the task to move')
    start_parser.set_defaults(func=start)

    edit_parser = subparsers.add_parser('edit',
        help='Edit a task in the current clask project',
        description='Edit a task in the current clask project.')
    edit_parser.add_argument('slug', help='slug of the task to edit')
    edit_parser.set_defaults(func=edit)

    finish_parser = subparsers.add_parser('finish',
        help='Finish a task in the current clask project',
        description='Finish a task in the current clask project.')
    finish_parser.add_argument('slug', help='slug of the task to move')
    finish_parser.set_defaults(func=finish)

    args = parser.parse_args()
    args.func(args)
