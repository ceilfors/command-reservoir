import os
import cmdr

_FILE_PATH = 'cmdr.yaml'

def load_actions(file_path=_FILE_PATH):
    if not os.path.isfile(file_path):
        actions = cmdr.action.get_default_actions()
        cmdr.action.set_actions(actions)
        save_actions(file_path)
    else:
        file = open(file_path, 'r')
        actions = cmdr.yaml_conversion.imp(file)
        if not actions:
            actions = cmdr.action.get_default_actions()
            cmdr.action.set_actions(actions)
            save_actions(file_path)
        else:
            cmdr.action.set_actions(actions)


def save_actions(file_path=_FILE_PATH):
    file = open(file_path, 'w')
    file.write(cmdr.yaml_conversion.exp(cmdr.action.get_all()))
    file.close()