import json
import yaml
from common import *

make_sure_path_exists('yaml')
make_sure_path_exists('yaml/heroes')

herodata = open_json('subset/herodata.json')

print herodata.keys()
for h in herodata:
    hero = {}
    hero['hero'] = herodata[h]['name']
    hero['header'] = herodata[h]['displayname']
    hero['title'] = herodata[h]['displayname']
    hero['description'] = 'Dota 2 Hero Page for ' + herodata[h]['displayname']
    with open('yaml/heroes/' + herodata[h]['name'].replace('npc_dota_hero_', '') + '.html', 'w') as g:
        g.write(yaml.safe_dump_all((hero, ''), explicit_start=True, default_flow_style=False))
