""" v1.2
- Almost same as v1
- Diff: func process()
 + now support IF/Else for all Action (not required)
 + INPUT_TYPE is required when used IF
 + if no IF then just do the Action and go to next step
"""

from typing import Any

from lib import action
from lib.const import *

# i.e
json_schema = [
    {
        "name": "01_try_ignore_if_invalid_value",
        DO: IGNORE,
        INPUT_TYPE: {
            FROM: FROM_ITEM
        },
        IF: {
            OR: [
                {
                    CHECK_LEN: False,
                    OPERATOR: EQUAL,
                    KEY: "group",
                    VALUE: "1",
                },
                {
                    CHECK_LEN: True,
                    OPERATOR: EQUAL,
                    KEY: "group",
                    VALUE: 5,
                },
            ]
        }
    },
    {
        "name": "02_query_with_macs",
        DO: QUERY,
        WITH: {
            # identity here!!!
            # TODO: maybe operator here? like add, slice...
            KEY: ["macs"],
        },
    },
    {
        "name": "03_try_ignore_if_found_more_than_1_results",
        DO: IGNORE,
        INPUT_TYPE: {
            FROM: FROM_STEP,
            RESULT_FROM_STEP: "02_query_with_macs"
        },
        IF: {
            OR: [
                {
                    CHECK_LEN: True,
                    OPERATOR: GREATER,
                    VALUE: 1,
                },
            ]
        }
    },
    {
        "name": "04_try_update_if_found_only_1_result",
        DO: UPDATE,
        INPUT_TYPE: {
            FROM: FROM_STEP,
            RESULT_FROM_STEP: "02_query_with_macs"
        },
        IF: {
            OR: [
                {
                    CHECK_LEN: True,
                    OPERATOR: EQUAL,
                    VALUE: 1,
                },
            ]
        }
    },
    {
        "name": "05_try_insert_default",
        DO: INSERT,
    }
]

data_inp = {
    "asset_type": "server",
    "ips": ["1", "2"],
    "macs": ["1", "2"],
    "group": "demo",
    "ext": {
        "A": 1,
        "B": 2,
    },
}


# ========================================= UTILS
def get_action(name):
    if name == IGNORE:
        return action.ignore
    elif name == QUERY:
        return action.query
    elif name == INSERT:
        return action.insert
    elif name == UPDATE:
        return action.update

    raise Exception("Invalid action", name)


def get_value_from_item(item, key):
    # TODO: key.subkey
    v = item.get(key)
    return v


def get_value_from_step(results_map, step):
    v = results_map.get(step)
    return v


def compare(actual_val, operator, with_val, check_len=False):
    if check_len:
        actual_val = len(actual_val)

    if operator == DIFF:
        return actual_val != with_val
    elif operator == EQUAL:
        return actual_val == with_val
    elif operator == GREATER:
        return actual_val > with_val
    elif operator == GREATER_OR_EQUAL:
        return actual_val >= with_val
    elif operator == LESS:
        return actual_val < with_val
    elif operator == LESS_OR_EQUAL:
        return actual_val <= with_val

    raise Exception("Invalid operator", operator)


# ========================================== PROCESS
def if_else(input_type: dict, step_if: dict, results_map: dict) -> bool:
    status = False  # result of these if else logic

    # and, or
    for operator, conds in step_if.items():  # type: str, list
        print("... Operator:", operator)

        if operator == OR:
            for cond in conds:
                # extract item value then compare
                if input_type[FROM] == FROM_ITEM:
                    v = get_value_from_item(data_inp, cond[KEY])
                elif input_type[FROM] == FROM_STEP:
                    v = get_value_from_step(results_map, input_type[RESULT_FROM_STEP])
                else:
                    raise Exception("Invalid input_type", input_type[FROM])

                # compare value
                ok = compare(v, cond[OPERATOR], cond[VALUE], cond[CHECK_LEN])

                print(
                    "... Trying compare: {} {} {} -> {}".format(v, cond[OPERATOR], cond[VALUE], ok)
                    if not cond[CHECK_LEN]
                    else "... Trying compare [len({})]: {} {} {} -> {}".format(len(v), v, cond[OPERATOR],
                                                                               cond[VALUE], ok)
                )

                # return immediately if true
                if ok:
                    return True

        elif operator == AND:
            pass

    return status


def process(step: dict, results_map: dict) -> (bool, Any):
    """
    :param step:
    :param results_map:
    :return: continue execute next step?, result of this step
    """
    if IF in step and INPUT_TYPE not in step:
        raise Exception("Require INPUT_TYPE with IF")

    exec_next_step = True
    results = None

    # get function to execute action
    action_name = step[DO]

    # required IF ELSE
    if action_name == IGNORE:
        if IF not in step:
            raise Exception("Missing IF to do IGNORE")

    do_action = get_action(action_name)

    # just do action if no IF ELSE
    if IF not in step:
        try:
            results = do_action(data_inp)
        except Exception as ex:
            exec_next_step = False
            raise ex

        return exec_next_step, results

    # input type -> get value to compare
    input_type = step[INPUT_TYPE]  # type: dict

    # check if else logic -> do action
    ok = if_else(input_type, step[IF], results_map)
    if ok:
        results = do_action(data_inp)
        # if IGNORE is true then no need to exec next step
        return False, results

    return exec_next_step, results


def run():
    results_map = dict()

    for step in json_schema:
        print(step["name"])

        exec_next_step, results = process(step, results_map)
        if not exec_next_step:
            break

        results_map[step["name"]] = results
