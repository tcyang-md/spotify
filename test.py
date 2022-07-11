import json
f = open('data.json')
data = json.load(f)

recent = []

for thing in data['items']:
    songs = {
        'name' : thing['name']
    }
    uri = {
        'uri' : thing['uri']
    }
    songs['uri'] = thing['uri']
    recent.append(songs)

print(recent[0])