import yaml
import cmdr.action

_ANSWER = "< "
_STAT_KEY = 'statement'
_DESC_KEY = 'description'

class ConversionException(Exception):
    def __init__(self, msg):
        super(ConversionException, self).__init__(msg)
        self.msg = msg


def exp(actions):
    """Exports and return the list of action in a yaml format."""
    if not actions:
        return ""
    else:
        return yaml.safe_dump(_exp_dict(actions), default_flow_style=False)


def _exp_dict(actions):
    result = {}
    for action in actions:
        key, data = _exp_action(action)
        result[key] = data
    return result


def _exp_action(action):
    return action.name, [{_DESC_KEY: action.description}, {_STAT_KEY: _exp_statements(action.statements)}]


def _exp_statements(statements):
    converted = []
    for statement in statements:
        converted.append(statement.command)
        for answer in statement.answers:
            converted.append(_ANSWER + answer)
    return converted


def imp(stream):
    """Imports and returns a yaml stream as a list of actions."""
    try:
        dict = yaml.safe_load(stream)
    except yaml.YAMLError as e:
        raise ConversionException(e)

    if dict is None: # empty stream
        return []
    else:
        return _imp_dict(dict)


def _imp_dict(dict):
    result = []
    for key, value in dict.items():
        result.append(_imp_item(key, value))
    return result


def _imp_item(name, value):
    # yaml schema is not available. kwalify is not in python yet. performing manual validation.
    if len(value) != 2:
        raise ConversionException(
            "action '{0}' must have exactly 2 attributes only; '{1}' and '{2}'".format(name, _DESC_KEY, _STAT_KEY))
    if _DESC_KEY not in value[0]:
        raise ConversionException("action '{0}' first attribute key must be '{1}'".format(name, _DESC_KEY))
    if _STAT_KEY not in value[1]:
        raise ConversionException("action '{0}' second attribute key must be '{1}'".format(name, _STAT_KEY))
    return cmdr.action.Action(name, _imp_statements(value[1][_STAT_KEY]), value[0][_DESC_KEY])


def _imp_statements(statements):
    converted = []
    for line in statements:
        if line.startswith(_ANSWER):
            if converted:
                converted[len(converted) - 1].answers.append(line[len(_ANSWER):len(line)])
        else:
            converted.append(cmdr.action.Statement(line))
    return converted


