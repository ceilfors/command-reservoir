import os
import shlex
import subprocess
import sys

TAG = '+'
_actions = None

class Action:
    def __init__(self, name, statements, description=""):
        if type(name) is not str:
            raise TypeError("name attribute must be str")
        if type(statements) is not tuple and type(statements) is not list:
            raise TypeError("statements attribute must either be tuple or list")
        if type(description) is not str:
            raise TypeError("description attribute must be str")
        self.name = name
        self.statements = tuple(statements)
        self.description = description

    def __repr__(self):
        return "{0}(name:{1}, description:{2}, statements:{3})".format(
            self.__class__.__name__, self.name, self.description, self.statements)


class Statement:
    def __init__(self, command, answers=None):
        if answers is None:
            answers = []
        if type(command) is not str:
            raise TypeError("statement must be str")
        if type(answers) is not tuple and type(answers) is not list:
            raise TypeError("answers attribute must either be tuple or list")
        self.command = command
        self.answers = answers

    def __repr__(self):
        return "{0}(command:{1}, answers:{2}".format(
            self.__class__.__name__, self.command, self.answers)


def set_actions(actions):
    """Sets the global actions to be managed by this module."""
    global _actions
    _actions = dict([(action.name, action) for action in actions])


def add(action):
    _actions[action.name] = action


def delete(action):
    del _actions[action.name]


def get(name):
    try:
        return _actions[name]
    except KeyError:
        return None


def get_all():
    return _actions.values()[:]


def find(keyword, in_description=False, in_statement=False):
    """Finds a keyword from an action's name.

    Keyword arguments:
    keyword -- the keyword to be used for the searching
    in_description -- this function will find the keyword in the action's description as well
    in_statement -- this function will find the keyword in the action's statement as well

    """
    results = set([action for action in _actions.values() if keyword in action.name])

    if in_description:
        results = results | set(find_in_desc(keyword))
    if in_statement:
        results = results | set(find_in_statement(keyword))
    return results


def find_tag(tag):
    def tag_filter(action):
        for word in action.description.split():
            if word.lower() == TAG + tag.lower():
                return True

    return filter(tag_filter, _actions.values())


def find_in_desc(keyword):
    return [action for action in _actions.values() if keyword in action.description]


def find_in_statement(keyword):
    def statement_filter(action):
        for statement in action.statements:
            if keyword in statement.command:
                return True
            for answer in statement.answers:
                if keyword in answer:
                    return True

    return filter(statement_filter, _actions.values())


def execute(action):
    for statement in action.statements:
        try:
            args = shlex.split(statement.command)
        except Exception:
            args = statement.command
        input = os.linesep.join(statement.answers)
        subprocess.Popen(args, shell=True, stdout=sys.stdout, stdin=subprocess.PIPE, stderr=sys.stdout).communicate(
            input)

def get_default_actions():
    c1 = Action('hello', (Statement("echo 'Hello world!'"),
                                      Statement("echo 'This is command-reservoir!'")),
        'this action is used to say hi to the world!')

    c2 = Action('ls', (Statement('dir'),), 'This +shell command is tagged as "shell"')
    return [c1, c2]