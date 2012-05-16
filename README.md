clask
=====

A command-line task manager powered by git.

Usage
-----

### Initializing clask

```
usage: clask init [-h]

Initialize a clask project.

optional arguments:
  -h, --help  show this help message and exit
```

This will initialize a root branch by the name of ```clask``` assuming
the directory this command will be executed in is a git repository. All
other commands related to clask will make changes to files and
directories on that branch.

### Adding a task

```
usage: clask add [-h] slug

Add a task to the current clask project.

positional arguments:
  slug        slug of the task to add

  optional arguments:
    -h, --help  show this help message and exit
```

This will load an editor with the following YAML template:

```
name: <slug>
description: [insert description]
state: unstarted
```

When the editor is closed, the contents of the buffer will be written to
a file with the name: ```<slug>.yml```.

It will also create a commit adding the file and attaching the following
commit message:

```
Create task: <slug>
```

### Changing the state of a task

```
usage: clask move [-h] slug state

Move a task in the current clask project to a new state.

positional arguments:
slug        slug of the task to move
state       new state of the task

optional arguments:
  -h, --help  show this help message and exit
```

This will change the state of the task ```slug``` to ```state``` by simply
updating the ```state``` field of the task file referenced by ```slug```.

It will also create a commit attaching the following commit message
for the modification:

```
Change state: <previous_state> -> <new_state>
```

### Starting a task

```
usage: clask start [-h] slug

Start a task in the current clask project.

positional arguments:
  slug        slug of the task to move

  optional arguments:
    -h, --help  show this help message and exit
```

This is a special case of the ```move``` command. It will change the
state of the task ```slug``` to ```started```.

The commit message attached to the commit created by this command will
be the same as for the ```move``` command.

### Editing a task

```
usage: clask edit [-h] slug

Edit a task in the current clask project.

positional arguments:
  slug        slug of the task to edit

  optional arguments:
    -h, --help  show this help message and exit
```

This will open the task ```slug``` in an editor and allow arbitrary
edits to the task file. The contents of a task file are expected to be
YAML and this command will fail if the edits do not parse as valid YAML.

It will also create a commit attaching the following commit message for
the modification:

```
Update task: <slug>
```

### Finishing a task

```
usage: clask finish [-h] slug

Finish a task in the current clask project.

positional arguments:
  slug        slug of the task to move

  optional arguments:
    -h, --help  show this help message and exit
```

This is a special case of the ```move``` command. It will change the
state of the task ```slug``` to ```finished``` and also move the
task file to ```.<slug>.yml```.

The commit message attached to the commit created by this command will
be the same as for the ```move``` command.
