from clask import task, repo

def migration_001():
    for task_ in task.all():
        task_['slug'] = task_.slug
        repo.put(task_.slug, task.dump(task_), 'Migration: 001')
