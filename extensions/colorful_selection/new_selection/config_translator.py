import extensions.colorful_selection.basic_selection as basic_selection


def config_translator(message, config):
    data = dict()
    data['selection'] = config_to_selection(config)
    data['config'] = config
    data['user'] = discord_get_current_user(message)
    return data


def discord_get_current_user(message):
    return str(message.author.id)


def config_to_selection(config):
    config = config_formatter(config)
    config = config_get_error(config)
    if config_has_errors(config):
        return 'erro!\n' + config['error']
    if has_key(config, 'message'):
        selection = basic_selection.get_selection_message(color=config['color'], message=config['message'])
    else:
        selection = basic_selection.get_selection_title_body(color=config['color'], title=config['title'], body=config['body'])
    if config.get('outside'):
        selection += f"\n{config['outside']}"
    return selection


def config_has_errors(config):
    if config['error'] != '':
        return True


def config_get_error(config):
    error_messages = get_dict_error_messages()

    if config_has_errors(config):
        return config
    if not has_key(config, 'name'):
        config['error'] = error_messages['not_has_name']
        return config
    if not has_key(config, 'color'):
        config['error'] = error_messages['not_has_color']
        return config
    if not has_key(config, 'message') and not has_key(config, 'title'):
        config['error'] = error_messages['not_has_message_nor_title']
        return config
    if has_key(config, 'message') and has_key(config, 'title'):
        config['error'] = error_messages['has_message_and_title']
        return config
    if has_key(config, 'title') and not has_key(config, 'body'):
        config['error'] = error_messages['has_title_and_not_body']
        return config
    if not has_key(config, 'title') and has_key(config, 'body'):
        config['error'] = error_messages['has_body_and_not_title']
        return config
    # config['color'] = string_formatter(config['color'])
    if not is_in_available_colors(config['color']):
        config['error'] = error_messages['invalid_color']
        return config
    return config


def has_key(config, key):
    try:
        var = config[key]
        return True
    except KeyError:
        return False


def get_dict_error_messages():
    available_colors = "'-c o' para **color orange** (laranja)\n" \
                       "'-c y' para **color yellow** (amarelo)\n" \
                       "'-c r' para **color red** (vermelho)\n" \
                       "'-c g' para **color green** (verde)\n" \
                       "'-c l' para **color light green** (verde claro)\n" \
                       "'-c b' para **color blue** (azul)\n"
    error_messages = {
        'not_has_name': "É necessário definir um parâmetro de nome '-n [nome]' " \
                          "(colchetes só para ilustração, é possível escrever sem eles).",
        'not_has_color': "É necessário escolher uma cor entre as disponíveis: \n" + available_colors,
        'not_has_message_nor_title': "É necessário definir uma mensagem. Defina com '-m **mensagem**' " \
                          "ou '-t **titulo** -b **corpo**'\n" \
                          "Lembrando que é necessário escolher **APENAS** um dos dois e que o título " \
                          "precisa necessariamente conter um body (corpo) e estar nesta ordem específica.",
        'has_message_and_title': 'Ou escolhe o parâmetro -m \'mensagem\' ou o parâmetro -t \'titulo\'. ' \
                          'Não é possível escolher os dois.',
        'has_title_and_not_body': "Não foi possível encontrar o parâmetro '-b **body**' depois do título!",
        'has_body_and_not_title': "Não foi possível encontrar o parâmetro '-t **title**' antes do body '-b'!",
        'invalid_color': "Cor inválida, escolha um parâmetro que esteja dentro das opções abaixo: \n" \
                          + available_colors
    }
    return error_messages


def is_in_available_colors(color):
    color = color.lower()
    available_colors = ['o', 'y', 'r', 'g', 'l', 'b']
    if color in available_colors:
        return True
    return False


# {'error': '',
#  'private': True,
#  'delete': False,
#  'name': 'n noticia_gapigal -p',
#  'color': ' b ',
#  'message': ' Semana s{incremento}\x00'}

def config_formatter(config):
    if has_key(config, 'name') and config['name'].startswith('n '):
        config['name'] = delete_first_word(config['name'])

    if has_key(config, 'title') and config['title'].startswith('t '):
        config['title'] = delete_first_word(config['name'])

    if has_key(config, 'message') and config['message'].startswith('m '):
        config['title'] = delete_first_word(config['name'])

    if has_key(config, 'color') and config['color'].startswith('c '):
        config['color'] = delete_first_word(config['color'])

    for key in config.keys():
        if isinstance(config[key], str):
            config[key] = string_formatter(config[key])

    return config


def delete_first_word(field):
    lista = field.split(' ')
    return ' '.join(lista[1:])


def string_formatter(string):
    string = string.replace('\x00', '')
    end_parameters = ['-n', '-c', '-t', '-b', '-m', '-p', '-o']

    # REPEATED ON PURPOSE TO ELIMINATE 'noticia_gapigal            -p -c' CASES
    for parameter in end_parameters:
        if string.endswith(parameter):
            string = string[:-2]
    for parameter in end_parameters:
        if string.endswith(parameter):
            string = string[:-2]

    string = string.strip()
    return string

