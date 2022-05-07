# Available states:
# 0 - initial state
# 1 - passive reading
# 2 - get parameter
# 10 - get name -n
# 11 - name await dash
# 12 - name await letter
# 13 - write name in config
# 20 - get color -c
# 21 - color await dash
# 22 - color await letter
# 23 - write color
# 30 - write private in config
# 31 - private error
# 40 - write delete in config
# 41 - delete error
# 50 - get message -m
# 51 - message await dash
# 52 - message await letter
# 53 - write message in config
# 60 - get title -t
# 61 - get body -b
# 62 - title await 'b'
# 63 - title/body error
# 64 - write config title
# 65 - write body
# 66 - body await dash
# 67 - body await letter
# 70 - get outside selection -o
# 71 - outside await dash
# 72 - outside await letter
# 73 - write outside in config

def change_state(state, char, oldChar):
    if state == 0:
        return 1
    temp_state = change_to_get_states(state, char, oldChar)
    if not temp_state:
        temp_state = change_to_await_states(state, char)
    if not temp_state:
        temp_state = change_to_write_states(state, char)
    if not temp_state:
        temp_state = change_to_error_states(state, char)
    return temp_state

def change_to_get_states(state, char, oldChar):

    # Initial get states
    if state == 1 and char == '-':
        return 2
    if state == 2 and char == 'n':
        return 10
    if state == 2 and char == 'c':
        return 20
    if state == 2 and char == 'm':
        return 50
    if state == 2 and char == 't':
        return 60
    if state == 2 and char == 'o':
        return 70

    # If state was in a writing state, it means that it's already in a
    # new parameter to read. Below in the list shows the available writing
    # states.
    if state in get_writing_states():
        if state == 64:
            return 61
        if oldChar == 'p' or oldChar == 'd':
            return change_to_write_states(state=2, char=oldChar)
        return change_to_get_states(state=2, char=oldChar, oldChar=oldChar)

    # Change from await to get
    if state in get_await_states():
        if state == 11 and char != '-':
            return 10
        if state == 12 and char.isalpha() is False:
            return 10
        if state == 51 and char != '-':
            return 50
        if state == 52 and char.isalpha() is False:
            return 50
        if state == 71 and char != '-':
            return 70
        if state == 72 and char.isalpha() is False:
            return 70
        if state == 62 and char != 'b':
            return 60
        if state == 66 and char != '-':
            return 61
        if state == 67 and char.isalpha() is False:
            return 61

    return False

def change_to_await_states(state, char):
    if state == 10 and char == ' ':
        return 11
    if state == 11 and char == '-':
        return 12
    if state == 20 and char == ' ':
        return 21
    if state == 21 and char == '-':
        return 22
    if state == 50 and char == ' ':
        return 51
    if state == 70 and char == ' ':
        return 71
    if state == 51 and char == '-':
        return 52
    if state == 71 and char == '-':
        return 72
    if state == 60 and char == '-':
        return 62
    if state == 61 and char == ' ':
        return 66
    if state == 66 and char == '-':
        return 67

    return False

def change_to_write_states(state, char):
    if state == 12 and char.isalpha():
        return 13
    if state == 22 and char.isalpha():
        return 23
    if state == 2 and char == 'p':
        return 30
    if state == 2 and char == 'd':
        return 40
    if state == 52 and char.isalpha():
        return 53
    if state == 62 and char == 'b':
        return 64
    if state == 67 and char.isalpha():
        return 65
    if state == 72 and char.isalpha():
        return 73

    # End of file
    if state in [10, 11, 12] and char == '\0':
        return 13
    if state in [20, 21, 22] and char == '\0':
        return 23
    if state in [50, 51, 52] and char == '\0':
        return 53
    if state in [70, 71, 72] and char == '\0':
        return 73
    if state in [61, 66, 67] and char == '\0':
        return 65
    return False

def change_to_error_states(state, char):
    return state

def is_in_writing_buffer_state(state):
    if state in [10, 11, 12, 13, 20, 21, 50, 51, 52, 53, 60, 61, 62, 64, 65, 66, 67, 70, 71, 72, 73]:
        return True
    return False

def get_get_states():
    return [10, 20, 30, 40, 50, 60, 61, 70]

def get_writing_states():
    return [13, 23, 30, 40, 53, 64, 65, 73]

def get_error_states():
    return [22, 31, 41, 63,]

def get_await_states():
    return [11, 12, 21, 22, 51, 52, 62, 66, 67, 71, 72]
