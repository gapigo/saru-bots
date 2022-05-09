# from replit import db

class d:
  def __init__(self):
    self.keys = [1, 2, 3, 4]

db = d()
def register_in_database(data):
  print('BULCE')
  print(data)
  if "colorful_selections" in db.keys():
    if selection_name_exists(data['config']['name']):
      return False
    colorful_selections = db["colorful_selections"]
    colorful_selections.append(data)
    db["colorful_selections"] = colorful_selections
  else:
    db["colorful_selections"] = [data]
  return True

def selection_name_exists(name):
  for selection in db['colorful_selections']:
    if selection['config']['name'] == name:
        return True
  return False
