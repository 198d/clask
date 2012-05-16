import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from clask import repo


class Task(dict):
    def __init__(self, slug, task_dict):
        self.slug = slug
        super(Task, self).__init__(task_dict)


def all():
    for slug in repo.all():
        yield load(slug)


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
    task = Task(slug, from_string(repo.get(slug)))
    return task


def source(slug):
    return repo.get(slug)


def from_string(task):
    return yaml.load(task, Loader=Loader)


def dump(task):
    return yaml.dump(task, Dumper=Dumper, default_flow_style=False)
