def format_portuguese_accents(message):
    message = message.replace('á', 'a').replace('à', 'a').replace('Á', 'A').replace('À', 'A')
    message = message.replace('é', 'e').replace('É', 'E').replace('ê', 'e').replace('Ê', 'E')
    message = message.replace('ã', 'a').replace('Ã', 'A').replace('Õ', 'O').replace('õ', 'o')
    message = message.replace('í', 'i').replace('Í', 'I')
    message = message.replace('ó', 'o').replace('ô', 'o').replace('Ó', 'O').replace('Ô', 'O')
    message = message.replace('Ú', 'U').replace('ú', 'u')
    return message


def get_selection_message(color, message, one_line=False):
    if color == 'o':
        return orange(message)
    if color == 'y' and one_line is False:
        return yellow_selection(message)
    if color == 'y' and one_line is True:
        return yellow_selection_one_line(message)
    if color == 'r':
        return red_selection(message)
    if color == 'l':
        return light_green(message)
    if color == 'g':
        return green(message)
    if color == 'b':
        return blue(message)
    return 'Cor não encontrada.'


def get_selection_title_body(color, title, body):
    selection = get_selection_message(color, title, one_line=True)
    selection = selection[:-3]
    selection += body
    selection += '\n```'
    return selection


def mount_selection(language, message):
    return f'```{language}\n' \
           f'{message}\n' \
           f'```'


def include_symbol_at_start(symbol, message):
    message_list = message.split('\n')
    message_list[0] = f'{symbol} ' + message_list[0]
    message_with_symbol = f'\n{symbol} '.join(message_list)
    return message_with_symbol


def include_symbol_at_start_and_end(start_symbol, message, end_symbol):
    message_list = message.split('\n')
    for count, line in enumerate(message_list):
        message_list[count] = f'{start_symbol} ' + line + f' {end_symbol}'
    message_with_symbol = '\n'.join(message_list)
    return message_with_symbol


def yellow_selection(message):
    return mount_selection('fix', message)


def yellow_selection_one_line(message):
    message = message.strip().replace(' ', '_')
    message = format_portuguese_accents(message)
    message = include_symbol_at_start_and_end('{', message, '}')
    message = include_symbol_at_start('%', message)
    return mount_selection('apache', message)


def red_selection(message):
    message = include_symbol_at_start('-', message)
    return mount_selection('diff', message)


def light_green(message):
    message = include_symbol_at_start('+', message)
    return mount_selection('diff', message)


def green(message):
    message = f'" {message} "'
    return mount_selection('bash', message)


def blue(message):
    message = include_symbol_at_start('#', message)
    return mount_selection('md', message)


def orange(message):
    message = include_symbol_at_start_and_end(start_symbol='[', message=message, end_symbol=']')
    return mount_selection('css', message)


# teste = '''Teste de mensagem
#     será que o enter é uma quebra de linha?
#     vamos ver'''
# print(yellow_selection(teste))
# print(red_selection(teste))
# print(light_green(teste))
# print(green(teste))
# print(blue(teste))
# print(orange(teste))
# print(yellow_selection_one_line(teste))
# print(get_selection_title_body('b', 'Titulo', 'corpo'))


