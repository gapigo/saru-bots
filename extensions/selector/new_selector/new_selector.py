import extensions.selector.colorful_selection.new_selector.message_interpreter as mi
import extensions.selector.colorful_selection.new_selector.config_translator as ct
import extensions.selector.colorful_selection.new_selector.register_in_database as rid

def new_selection(message, register=True):
    content = message.content
    content += '\0'
    config = mi.message_interpreter(content)
    data = ct.config_translator(message, config)
    if ct.config_has_errors(data['config']):
        return data
    if register and not rid.register_in_database(data):
      data['config']['error'] = 'O nome dessa seleção já existe, não foi possível cadastrá-la!\nUse **$sel --list** e confira os nomes existentes.'
      return data
    return data
    # return data['Selection'] + '\n**CONFIRMAR?** *($sel sim)* ou *($sel não)*'
