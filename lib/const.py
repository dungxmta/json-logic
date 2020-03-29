# action
IGNORE = "IGNORE"
QUERY = "QUERY"
INSERT = "INSERT"
UPDATE = "UPDATE"

# keyword
DO = "do"
AS = "as"
WITH = "with"
IF = "if"
THEN = "then"
AND = "and"
OR = "or"
ALWAYS = "always"  # always exec action then continue to next step
INPUT_TYPE = "input_type"

# input type
FROM = "from"
FROM_ITEM = "key"  # get value from data_input key
FROM_STEP = "result"  # get value from result of previous step
RESULT_FROM_STEP = "step"  # step name

# if_else
OPERATOR = "operator"
CHECK_LEN = "check_len"
KEY = "key"
VALUE = "value"
# operator
LEN = "len"
DIFF = "!="
EQUAL = "="
GREATER = ">"
GREATER_OR_EQUAL = ">="
LESS = "<"
LESS_OR_EQUAL = "=<"
