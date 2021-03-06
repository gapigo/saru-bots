from extensions.colorful_selection.new_selection.new_selection import new_selection
import extensions.colorful_selection.new_selection.register_in_database as rid
from extensions.colorful_selection.get_saved_selection import validate_if_private as validate_if_private
from extensions.colorful_selection.get_saved_selection import get_data as get_saved_data
from extensions.colorful_selection.get_saved_selection import get_data_from_db as get_data_from_name
from extensions.colorful_selection.get_saved_selection import get_data_from_db
import extensions.colorful_selection.basic_selection as bs
import extensions.colorful_selection.helper_message as hm
from flask_app import db
from .models import ColorfulSelection

class Message():
  def __init__(self, content, author):
    self.content = content
    self.author = author


async def return_response(message, client, author=None):
  if isinstance(message, str):
    message = Message(message, author)

  parameters = message.content.split('$sel')[1].strip()
  if parameters.startswith('--new'):
    return create_selection(message, parameters)
  
  if parameters.startswith('--mod'):
    return modify_selection(message, parameters)
  
  if parameters.startswith('--list'):
    return await list_selections(client)
  
  if parameters.startswith('--del'):
    name = format_parameters(parameters)[2:]
    data = get_data_from_name(name)
    if data:
      if validate_if_private(message, data) is False:
        return 'Não é possível deletar esta mensagem, pois ela é privada.'
      del_selection(data)
      return f'Seleção **{name}** apagada.'
    return f'A seleção **{name}** não existe. Nada foi deletado.'
  
  if parameters.startswith('--dat'):
    name = format_parameters(parameters)[2:]
    data = get_data_from_name(name)
    return str(data)
  
  if parameters.startswith('-h') or parameters.startswith('--help'):
    return (hm.HELPER_MESSAGE_PT1, hm.HELPER_MESSAGE_PT2)

  if parameters.startswith('-'):
    colors = ['y', 'o', 'l', 'r', 'b', 'g']
    try:
      for color in colors:
        if parameters[1] == color:
          content = parameters.split('-' + color)[1].strip()
          if (counter := content.find('-b') != -1):
            title, body = content.split('-b')
            selection = get_basic_selection(color, title, body)
          else:
            selection = get_basic_selection(color, content)
          return (selection, True)
    except:
      pass

  return get_saved_data('$sel ' + parameters)
  

def modify_selection(message, parameters):
  message.content = message.content.replace('--mod', '')
  creating_data = new_selection(message, register=False)
  data = get_modifying_data(creating_data)
  if validate_if_private(message, data) is False:
    return 'Não é possível modificar esta mensagem, pois ela é privada.'
  deleted_data = del_selection(data)
  parameters = 'new ' + parameters.split('--mod')[1]
  data = new_selection(message)
  if data['config']['error'] == '':
    return 'Modificado com sucesso'
  if rid.register_in_database(deleted_data):
    return 'Ocorreu um erro na modificação, voltei para a seleção passada.'
  return 'Ocorreu um erro na modificação e não foi possível voltar para seleção passada.\nEla foi deletada. Tente criá-la novamente com **$sel --new [parâmetros].**'

def create_selection(message, parameters):
  data = new_selection(message)
  response = ''
  if data['config']['error'] != '':
    return data['config']['error']
  response = 'Seleção salva para **'
  if data['config']['private'] == True:
    response += f'{message.author} apenas.'
  else:
    response += 'todos usarem.'
  response += '**\n' + data['selection']
  response += f'\n**$sel {data["config"]["name"]}** para usar.'
  return response

def del_selection(data):
  name = get_name_from_data(data)
  selections = ColorfulSelection.query.all()
  for selection in selections:
    if selection.name == name:
      db.session.delete(selection)
      db.session.commit()
      return selection

def format_parameters(parameters):
  if parameters.startswith('--new') or parameters.startswith('--mod') or parameters.startswith('--del') or parameters.startswith('--dat'):
    return 'a ' + parameters[5:].strip()

def get_modifying_data(comparing_data):
  name = get_name_from_data(comparing_data)
  if data := get_data_from_db(name):
    return data
  return comparing_data

def get_name_from_data(data):
  return data['config']['name']



async def list_selections(client):
  response = ''
  selections = ColorfulSelection.query.all()
  for selection in selections:
    private = selection.private
    name = selection.name
    user_name = str(await client.fetch_user(int(selection.user)))
    response += f"{name} {' | ** privado de: ' + user_name + '**' if private else ''}\n"
  if response == '':
    response = 'Lista vazia! Tente usar **$sel --new [nome]** para criar uma seleção.'
  return response


def get_basic_selection(color, content, body=None):
  if body == None:
    return bs.get_selection_message(color, content)
  return bs.get_selection_title_body(color, content, body)
