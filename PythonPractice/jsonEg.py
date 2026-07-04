#Reading a JSON File
import json

with open('data.json', 'r') as file:
    data = json.load(file)
    print(data)

# Writing to a JSON File
# import json

person = {'name': 'John', 'sal': 30}
with open('output.json', 'w') as file:
    json.dump(person, file, indent=4)


#Reading a JSON File
import json

with open('data.json', 'r') as file:
    data = json.load(file)
    print(data)

# Writing to a JSON File
# import json

person = [{'name': 'John', 'sal': 30},{'name': 'Janet', 'sal': 60}]
with open('output.json', 'w') as file:
    json.dump(person, file, indent=4)