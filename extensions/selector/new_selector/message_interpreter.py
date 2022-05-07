import extensions.selector.new_selector.states_manager as states_manager

debug = False

def message_interpreter(message):
    message = message.strip()
    configs = {'error': '', 'private': False, 'delete': False}
    buffer = ''
    state = 0
    oldChar = ''
    for char in message:
        state = states_manager.change_state(state, char, oldChar)
        is_in_writing_state = states_manager.is_in_writing_buffer_state(state)
        buffer = buffer_writer(is_in_writing_state, buffer, char)
        configs, buffer = config_writer(state, configs, buffer)

        if debug:
            print(f'Char = {char} | oldChar = {oldChar} | State = {state} \n Buffer = {buffer} \n Configs = {configs}')
            print(f'-----------------------------------------------------------')
        if configs['error'] != '':
            break
        oldChar = char
    return configs


def buffer_writer(reading_state, buffer, char):
    if not reading_state:
        return buffer
    return buffer + char


def config_writer(state, configs, buffer):
    # colocar um char para ver se é '\0' e alterar a lógica de seleção
    if state in states_manager.get_writing_states():
        if state == 13:
            configs['name'] = buffer
        elif state == 23:
            configs['color'] = buffer
        elif state == 30:
            configs['private'] = True
        elif state == 40:
            configs['delete'] = True
        elif state == 53:
            configs['message'] = buffer
        elif state == 64:
            configs['title'] = buffer
        elif state == 65:
            configs['body'] = buffer
        elif state == 73:
            configs['outside'] = buffer
        buffer = ''
    return configs, buffer

