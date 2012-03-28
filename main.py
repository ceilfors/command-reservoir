import os
import signal
import sys
import imp

signal.signal(signal.SIGINT, lambda signal, frame: sys.exit(0))
import argparse
import cmdr.action
import cmdr.action_file
import cmdr.yaml_conversion
import cmdr.pyperclip

## http://www.py2exe.org/index.cgi/HowToDetermineIfRunningFromExe
def main_is_frozen():
    return (hasattr(sys, "frozen") or # new py2exe
            hasattr(sys, "importers") # old py2exe
            or imp.is_frozen("__main__")) # tools/freeze


def get_main_dir():
    if main_is_frozen():
        return os.path.realpath(os.path.dirname(sys.executable))
    return os.path.realpath(os.path.dirname(sys.argv[0]))
## end of http://www.py2exe.org/index.cgi/HowToDetermineIfRunningFromExe

_FILE_PATH = os.path.join(get_main_dir(), "cmdr.yaml")
_BACKUP_FILE_PATH = os.path.join(get_main_dir(), "cmdr.yamlbak")

def get(args):
    action = cmdr.action.get(args.name)
    if action is None:
        print "Action '{0}' is not available".format(args.name)
    else:
        print_actions([action])


def backup_actions():
    cmdr.action_file.save_actions(_BACKUP_FILE_PATH)
    print "Backed up actions to: '{0}'".format(_BACKUP_FILE_PATH)


def add(args):
    print "Adding a new action. A new action can easily be added directly to the yaml file as well."
    name = none_empty_input("Name: ")

    if cmdr.action.get(name) is not None:
        print "Action with the same name already exist. It will be overwritten."

    description = raw_input("Description: ")
    statements = []
    first_command = none_empty_input("Command: ")
    statements.append(cmdr.action.Statement(first_command))
    printing_help = True
    while True:
        if printing_help:
            print "Enter 'a' to provide automatic answer to the previously entered command"
            print "Enter 'c' to add another command to this action"
            print "Enter 'e' to conclude and end this new action"
            printing_help = False
        choice = raw_input("[a/c/e]: ").lower()
        if choice == 'a':
            answer = raw_input("Answer: ")
            statements[len(statements) - 1].answers.append(answer)
        elif choice == 'c':
            command = none_empty_input("Command: ")
            statements.append(cmdr.action.Statement(command))
        elif choice == 'e':
            break
        else:
            printing_help = True

    print
    new_action = cmdr.action.Action(name, statements, description)
    print "New action created:"
    print_actions([new_action])
    print
    choice = query_yes_no("Save action '{0}'?".format(new_action.name)).lower()
    if choice == "yes":
        backup_actions()
        cmdr.action.add(new_action)
        cmdr.action_file.save_actions(_FILE_PATH)
        print "Action added."


def delete(args):
    action = cmdr.action.get(args.name)
    if action is None:
        print "Action '{0}' is not available".format(args.name)
        return

    choice = query_yes_no("Delete action '{0}'?".format(args.name)).lower()
    if choice == "yes":
        backup_actions()
        cmdr.action.delete(action)
        cmdr.action_file.save_actions(_FILE_PATH)
        print "Action deleted."


def none_empty_input(prompt):
    while True:
        value = raw_input(prompt)
        if not value:
            print "Empty value is not accepted"
        else:
            return value


def all(args):
    print_actions(cmdr.action.get_all())


def find(args):
    print_actions(cmdr.action.find(args.keyword, args.description, args.statement))


def tag(args):
    print_actions(cmdr.action.find_tag(args.tag))


def execute(args):
    action = cmdr.action.get(args.name)
    if action is None:
        print "Action '{0}' is not available".format(args.name)
    else:
        cmdr.action.execute(action)


def copy(args):
    action = cmdr.action.get(args.name)
    if action is None:
        print "Action '{0}' is not available".format(args.name)
    else:
        if args.verbose:
            cmdr.pyperclip.setcb(cmdr.yaml_conversion.exp([action]))
        else:
            commands = []
            for statement in action.statements:
                commands.append(statement.command)
            cmdr.pyperclip.setcb(os.linesep.join(commands))


def print_actions(actions):
    if actions:
        print cmdr.yaml_conversion.exp(actions)


def print_hints():
    print ("-- Hint --\n"
           "* Please use the following format in the yaml file including the whitespaces and the indentations:\n"
           "{action name}:\n"
           "- description: {the description} # 1 space after '-'\n"
           "- statement:\n"
           "  - {statement 1} # 2 spaces for indentation\n"
           "  - {statement 2}\n"
           "  - < {answer for statement 2} # 1 space after '-' and '<'\n")
    print "* Use yaml scalar when statements contains unintended yaml syntax"
    print '* Instead of adding action to the file manually, "add" command can be used'

## {{{ http://code.activestate.com/recipes/577058/ (r2)
def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes": "yes", "y": "yes", "ye": "yes",
             "no": "no", "n": "no"}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while 1:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return default
        elif choice in valid.keys():
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

## end of http://code.activestate.com/recipes/577058/ }}}

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='actions')

    parser_get = subparsers.add_parser('get', help='print an action')
    parser_get.add_argument('name', type=str, help='the name of the action to be printed out')
    parser_get.set_defaults(func=get)

    parser_add = subparsers.add_parser('add', help='create a new action')
    parser_add.set_defaults(func=add)

    parser_delete = subparsers.add_parser('del', help='delete an action')
    parser_delete.add_argument('name', type=str, help='the name of the action to be deleted')
    parser_delete.set_defaults(func=delete)

    parser_all = subparsers.add_parser('all', help='print all actions')
    parser_all.set_defaults(func=all)

    parser_find = subparsers.add_parser('find', help='find actions matched with the keyword specified')
    parser_find.add_argument('keyword', type=str, help='the keyword to be matched with the actions')
    parser_find.add_argument('-d', '--description', help="find keyword in actions' description", action='store_true')
    parser_find.add_argument('-s', '--statement', help="find keyword in actions' statements", action='store_true')
    parser_find.set_defaults(func=find)

    parser_tag = subparsers.add_parser('tag', help='find actions tagged with the specified tag')
    parser_tag.add_argument('tag', type=str, help='the tag name to be searched for')
    parser_tag.set_defaults(func=tag)

    parser_execute = subparsers.add_parser('exe', help='execute an action')
    parser_execute.add_argument('name', type=str, help='the name of the action to be executed')
    parser_execute.set_defaults(func=execute)

    parser_copy = subparsers.add_parser('copy', help="copy an action's command to the clipboard")
    parser_copy.add_argument('name', type=str, help='the name of the action to be copied')
    parser_copy.add_argument('-v', '--verbose', help="copy all action's details", action='store_true')
    parser_copy.set_defaults(func=copy)

    try:
        cmdr.action_file.load_actions(_FILE_PATH)
    except cmdr.yaml_conversion.ConversionException as e:
        print "Error while loading actions:"
        print e.msg
        print_hints()
        sys.exit(1)

    try:
        args = parser.parse_args()
        args.func(args)
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == '__main__':
    main()