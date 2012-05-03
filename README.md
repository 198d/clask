clask
=====

A command-line task manager powered by git.

Usage
-----

### Initializing clask

```
$ clask init
```

This will initialize a root branch by the name of ```clask``` assuming
the directory this command will be executed in is a git repository. All
other commands related to clask will make changes to files and
directories on that branch.

### Adding a task

```
$ clask add <slug>
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
$ clask move <slug> <new_state>
```

This will change the state of the task ```<slug>``` to
```<new_state>``` by simply updating the ```state``` field of the task
file referenced by ```<slug>```.

It will also create a commit attaching the following commit message
for the modification:

```
Change state: <previous_state> -> <new_state>
```

### Editing a task

```
$ clask edit <slug>
```

This will open the task ```<slug>``` in an editor and allow arbitrary
edits to the task file. The contents of a task file are expected to be
YAML and this command will fail if the edits do not parse as valid YAML.

It will also create a commit attaching the following commit message for
the modification:

```
Update task: <slug>
```

### Finishing a task

```
$ clask finish <slug>
```

This is a special case of the ```move``` command. It will change the
state of the task ```<slug>``` to ```finished``` and also move the
task file to ```.<slug>.yml```.

The commit message attached to the commit created by this command will
be the same as for the ```move``` command.
