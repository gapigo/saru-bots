from replit import db

def register_in_database(data):
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
