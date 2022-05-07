from replit import db
import datetime
import extensions.selector.options_manager as om
# from extensions.selector.options_manager import del_selection as del_data
import extensions.selector.new_selector.register_in_database as rid

def get_data(parameters):
  data = get_data_from_db(get_name(parameters))
  if not data:
    return 'Nome da seleção não existe. Cadastre uma nova seleção com $sel --new [params].\n**$sel -h** para ajuda.'
  data = put_templates(data, parameters)
  update_data(data)
  if data['config']['delete'] == True:
    return (data['t_selection'], True)
  return data['t_selection']
  pass


def get_name(parameters):
  options = ['-mod', '-ii', '-dii', '-rii', '-i', '-di', '-ri', '-si']
  for option in options:
    parameters = parameters.split(option)[0]
  return parameters


def update_data(data):
  deleted_data = om.del_selection(data)
  rid.register_in_database(data)


def get_data_from_db(message):
  try:
    if message.startswith('$sel'):
      name = message.split('$sel')[1].strip()
    else:
      name = message.strip()
    for data in db['colorful_selections']:
      if data['config']['name'] == name:
          return data
    return False
  except:
    return False


def validate_if_private(message, data):
  if data['config']['private'] is False:
    return True
  user_id = discord_get_current_user(message)
  if user_id == data['user']:
    return True
  return False


def discord_get_current_user(message):
    return str(message.author.id)


def put_templates(data: dict, parameters: str):
    data['t_selection'] = selection = data['selection']
    if selection.find('$(date)') != -1:
        data['t_selection']: str = put_date_selection(data['t_selection'])
    if selection.find('$(i)') != -1:
        data: dict = put_increment(data, parameters)
    if selection.find('$(ii)') != -1:
        data: dict = put_daily_increment(data, parameters)
    if selection.find('$(mod)'):
        data['t_selection'] = put_modifications(data['t_selection'], parameters)
    return data

def put_modifications(selection: str, parameters: str):
    pendent_modifications = parameters.split('-mod')
    pendent_modifications.pop(0)
    for modification in pendent_modifications:
        selection = selection.replace('$(mod)', modification.strip(), 1)
    return selection


def put_date_selection(selection):
    has_formatter = False
    formatter = ''
    new_string = ''
    if selection.find('$f(') != -1:
        has_formatter = True
        new_string += selection[:selection.find('$f(')]
        new_string += selection.split('$f(')[1].split(')', maxsplit=1)[1]
        formatter = selection.split('$f(')[1].split(')')[0]
    today = datetime.datetime.today().date().strftime(formatter if has_formatter else '%d/%m/%Y')
    returned_string = new_string if has_formatter else selection
    return returned_string.replace('$(date)', today)

def put_increment(data: dict, parameters: str):
    increment = data.get('increment')
    if increment is None:
        data['increment'] = 1
    else:
        param_op = get_parameter_option(parameters)
        if param_op == 'di' and data['increment'] != 1:
            data['increment'] -= 1
        elif param_op == 'ri':
            data['increment'] = 1
        elif param_op == 'si':
            increment = parameters.split('-si')[1].strip().split(' ')[0]
            if not increment.isdigit():
              increment = int(data['increment']) + 1
            data['increment'] = int(increment)
        else:
            data['increment'] += 1
    data['t_selection'] = data['t_selection'].replace('$(i)', f'{data["increment"]}')
    return data

def put_daily_increment(data: dict, parameters: str):
    today = datetime.datetime.today().date().strftime('%d%m')
    daily_increment = data.get('daily_increment')
    if daily_increment is None or data['daily_increment'][0] != today:
        data['daily_increment'] = (today, 1)
    else:
        if parameters.find('-dii') != -1:
            if data['daily_increment'][1] > 1:
                data['daily_increment'] = (today, data['daily_increment'][1] - 1)
        elif parameters.find('-rii') != -1:
            data['daily_increment'] = (today, 1)
        else:
            data['daily_increment'] = (today, data['daily_increment'][1] + 1)
    data['t_selection'] = data['t_selection'].replace('$(ii)', f'{data["daily_increment"][1]}')
    return data

def get_parameter_option(parameters: str):
    options = ['i', 'di', 'ri', 'si']
    for option in options:
        if (pos := parameters.find(f'-{option}')) != -1 and (pos+2 == len(parameters) or parameters[pos+2] != option):
            return option
    return None