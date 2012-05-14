import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from clask import repo


def add(slug, task):
    repo.put(slug, dump(task), 'Create task: {0}'.format(slug))


def move(slug, new_state, finish=False):
    task = load(slug)
    old_state = task['state']
    task['state'] = new_state

    repo.put(slug, dump(task),
        "Change state: {0} -> {1}".format(old_state, new_state), finish)


def update(slug, task):
    repo.put(slug, dump(task), 'Update task: {0}'.format(slug))


def load(slug):
    return from_string(repo.get(slug))


def source(slug):
    return repo.get(slug)


def from_string(task):
    return yaml.load(task, Loader=Loader)


def dump(task):
    return yaml.dump(task, Dumper=Dumper, default_flow_style=False)
