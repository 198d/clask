from time import time

from dulwich.repo import Repo
from dulwich.config import StackedConfig
from dulwich.objects import Blob, Tree, Commit


_repo = Repo('.')
_config = _repo.get_config_stack()


def init():
    try:
        _repo.refs['refs/heads/clask']
    except KeyError:
        _commit({'.gitkeep': ''}, 'Initialize clask')


def get(slug):
    return _get_blob(slug).data


def put(slug, data, message=None, finish=False):
    tree_dict = dict()
    if finish:
        tree_dict[_tree_entry(slug, True)] = data
        tree_dict[_tree_entry(slug)] = None
    else:
        tree_dict[_tree_entry(slug)] = data

    _commit(tree_dict, message)


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
    tree_entry = _tree_entry(slug)
    head = _get_repo_object(_get_clask_head())
    tree = _get_repo_object(head.tree)
    try:
        _, sha = tree[tree_entry]
    except KeyError:
        tree_entry = _tree_entry(slug, finished=True)
        _, sha = tree[tree_entry]
    return _get_repo_object(sha)


def _tree_entry(slug, finished=False):
    template = '.{0}.yml' if finished else '{0}.yml'
    return template.format(slug)


    return _get_repo_object(sha)
