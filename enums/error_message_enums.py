from enum import Enum
class ReasonErrorMessages(Enum):
    KEY_ID_NOT_FOUND = "[json.exception.out_of_range.403] key 'id' not found"
    KEY_METHOD_NOT_FOUND = "[json.exception.out_of_range.403] key 'method' not found"
    KEY_NAME_NOT_FOUND = "[json.exception.out_of_range.403] key 'name' not found"
    KEY_SURNAME_NOT_FOUND = "[json.exception.out_of_range.403] key 'surname' not found"
    KEY_PHONE_NOT_FOUND = "[json.exception.out_of_range.403] key 'phone' not found"
    KEY_AGE_NOT_FOUND = "[json.exception.out_of_range.403] key 'age' not found"

    # "reason": "[json.exception.out_of_range.403] key 'age' not found",
    # "reason": "[json.exception.out_of_range.403] key 'name' not found"
    # ...
    # "reason": "[json.exception.type_error.302] type must be number, but is string",
    # "reason": "[json.exception.parse_error.101] parse error at line 6, column 5: syntax error while parsing object key - unexpected '}'; expected string literal",
    # "reason": "[json.exception.parse_error.101] parse error at line 5, column 15: syntax error while parsing value - unexpected ','; expected '[', '{', or a literal"
    # "reason": "[json.exception.type_error.302] type must be string, but is null"
