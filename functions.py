import json
import random
def get_problem(difficult):
  with open("problemSet.json") as file:
    json_data = json.loads(file.read())
  num = random.randint(0,2328)
  if difficult not in [1,2,3]:
    return
  while json_data[num]['difficulty']['level'] != difficult or json_data[num]['paid_only'] != False:
    num = random.randint(0,2328)
  problem = json_data[num]['stat']['question__title_slug']
  return problem