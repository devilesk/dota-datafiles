import argparse
import json
import vdf
import yaml
import datetime
import math
from common import *
import schema
import mapping
import recipedata
import sys
try:
    sys.path.insert(0, '../trivia')
    import triviaquestions
except:
    triviaquestions = False

folders = ['../source', '../dist', '../yaml']
file_data = [
    ('npc_heroes', 'DOTAHeroes', 'npc_dota_hero_base'),
    ('npc_abilities', 'DOTAAbilities', 'ability_base'),
    ('npc_units', 'DOTAUnits', 'npc_dota_units_base'),
    ('items', 'DOTAAbilities', None),
    ('dota_english', 'lang', None)
]
MAX_ABILITY_LEVEL = 25

items = ["abyssal_blade","ultimate_scepter","courier","arcane_boots","armlet","assault","boots_of_elves","bfury","belt_of_strength","black_king_bar","blade_mail","blade_of_alacrity","blades_of_attack","blink","bloodstone","boots","travel_boots","bottle","bracer","broadsword","buckler","butterfly","chainmail","circlet","clarity","claymore","cloak","lesser_crit","greater_crit","dagon","demon_edge","desolator","diffusal_blade","rapier","ancient_janggo","dust","eagle","energy_booster","ethereal_blade","cyclone","skadi","flying_courier","force_staff","gauntlets","gem","ghost","gloves","hand_of_midas","headdress","flask","heart","heavens_halberd","helm_of_iron_will","helm_of_the_dominator","hood_of_defiance","hyperstone","branches","javelin","sphere","maelstrom","magic_stick","magic_wand","manta","mantle","mask_of_madness","medallion_of_courage","mekansm","mithril_hammer","mjollnir","monkey_king_bar","lifesteal","mystic_staff","necronomicon","null_talisman","oblivion_staff","ward_observer","ogre_axe","orb_of_venom","orchid","pers","phase_boots","pipe","platemail","point_booster","poor_mans_shield","power_treads","quarterstaff","quelling_blade","radiance","reaver","refresher","ring_of_aquila","ring_of_basilius","ring_of_health","ring_of_protection","ring_of_regen","robe","rod_of_atos","relic","sobi_mask","sange","sange_and_yasha","satanic","sheepstick","ward_sentry","shadow_amulet","invis_sword","shivas_guard","basher","slippers","smoke_of_deceit","soul_booster","soul_ring","staff_of_wizardry","stout_shield","talisman_of_evasion","tango","tpscroll","tranquil_boots","ultimate_orb","urn_of_shadows","vanguard","veil_of_discord","vitality_booster","vladmir","void_stone","wraith_band","yasha","crimson_guard","enchanted_mango","lotus_orb","glimmer_cape","guardian_greaves","moon_shard","silver_edge","solar_crest","octarine_core","aether_lens","faerie_fire","iron_talon","dragon_lance","echo_sabre","infused_raindrop","blight_stone","wind_lace","tome_of_knowledge","bloodthorn","hurricane_pike"]

def parse_vdf_to_json(filename, src_dir, out_dir):
    print 'parse', filename
    with open(src_dir + filename, 'r') as f:
        data = vdf.loads(f.read())
    with open(out_dir + filename.replace('txt','json'),'w') as g:
        g.write(json.dumps(data,indent=1,sort_keys=True))
    
def parse_all_vdf_to_json(src_dir, out_dir):
    print 'parse_all_vdf_to_json', src_dir, out_dir
    for data in file_data:
        parse_vdf_to_json(data[0] + '.txt', src_dir, out_dir)

def merge_base_class(data, ROOT, BASE_CLASS):
    print 'merge_base_class', ROOT, BASE_CLASS
    output = {}
    if BASE_CLASS:
        BASE_DICT = data[ROOT][BASE_CLASS]
        output[ROOT] = {k: dict(BASE_DICT.items() + data[ROOT][k].items()) for k in data[ROOT].keys() if k != BASE_CLASS and k != 'Version'}
    else:
        output[ROOT] = {k: data[ROOT][k] for k in data[ROOT].keys() if k != BASE_CLASS and k != 'Version'}
    return output
        
def strip_comments(src):
    with open(src, 'r') as f:
        lines = f.readlines()
    with open(src, 'w') as f:    
        for line in lines:
            l = line.lstrip()
            if l[:2] != '//':
                f.write(line)

def copy_source_from_dotabuff(dotabuff_dir, dotabuff_branch):
    copy_source_txt_from_dotabuff(dotabuff_dir, dotabuff_branch)
    copy_source_json_from_dotabuff(dotabuff_dir, dotabuff_branch)
  
def copy_source_txt_from_dotabuff(dotabuff_dir, dotabuff_branch):
    download_file_from('https://raw.githubusercontent.com/dotabuff/d2vpkr/' + dotabuff_branch + '/dota/scripts/npc/npc_heroes.txt', dotabuff_dir + 'npc_heroes.txt')
    strip_comments(dotabuff_dir + 'npc_heroes.txt')
    download_file_from('https://raw.githubusercontent.com/dotabuff/d2vpkr/' + dotabuff_branch + '/dota/scripts/npc/npc_abilities.txt', dotabuff_dir + 'npc_abilities.txt')
    strip_comments(dotabuff_dir + 'npc_abilities.txt')
    download_file_from('https://raw.githubusercontent.com/dotabuff/d2vpkr/' + dotabuff_branch + '/dota/scripts/npc/npc_units.txt', dotabuff_dir + 'npc_units.txt')
    strip_comments(dotabuff_dir + 'npc_units.txt')
    download_file_from('https://raw.githubusercontent.com/dotabuff/d2vpkr/' + dotabuff_branch + '/dota/scripts/npc/items.txt', dotabuff_dir + 'items.txt')
    strip_comments(dotabuff_dir + 'items.txt')
    download_file_from('https://raw.githubusercontent.com/dotabuff/d2vpkr/' + dotabuff_branch + '/dota/resource/dota_english.txt', dotabuff_dir + 'dota_english.txt')
    strip_comments(dotabuff_dir + 'dota_english.txt')
    print 'copy txt from dotabuff'
    
def copy_source_json_from_dotabuff(dotabuff_dir, dotabuff_branch):
    download_file_from('https://raw.githubusercontent.com/dotabuff/d2vpkr/' + dotabuff_branch + '/dota/scripts/npc/npc_heroes.json', dotabuff_dir + 'npc_heroes.json')
    download_file_from('https://raw.githubusercontent.com/dotabuff/d2vpkr/' + dotabuff_branch + '/dota/scripts/npc/npc_abilities.json', dotabuff_dir + 'npc_abilities.json')
    download_file_from('https://raw.githubusercontent.com/dotabuff/d2vpkr/' + dotabuff_branch + '/dota/scripts/npc/npc_units.json', dotabuff_dir + 'npc_units.json')
    download_file_from('https://raw.githubusercontent.com/dotabuff/d2vpkr/' + dotabuff_branch + '/dota/scripts/npc/items.json', dotabuff_dir + 'items.json')
    download_file_from('https://raw.githubusercontent.com/dotabuff/d2vpkr/' + dotabuff_branch + '/dota/resource/dota_english.json', dotabuff_dir + 'dota_english.json')
    print 'copy json from dotabuff'

def process(src_dir, subset_dir, yaml_dir):
    hero_data, ability_data, unit_data, item_data, tooltip_data = [merge_base_class(open_json(src_dir + x[0] + '.json'), x[1], x[2]) for x in file_data]
    
    tooltip_data_tokens = tooltip_data['lang']['Tokens']
    for k in tooltip_data_tokens:
        if k != k.lower() and k.lower() in tooltip_data_tokens:
            raise Exception()
    tooltip_data_tokens = dict((k.lower(), v) for k,v in tooltip_data_tokens.iteritems())
  
    heroeslist = {'data': []}
    hero_data_subset = {}
    for h in hero_data['DOTAHeroes']:
        if h == 'npc_dota_hero_target_dummy':
            continue
        heroeslist['data'].append(h.replace('npc_dota_hero_', ''))
        hero_data_subset[h] = subset(schema.hero_schema, hero_data['DOTAHeroes'][h])

    ability_data_subset = {}
    for a in ability_data['DOTAAbilities']:
        ability_data_subset[a] = subset(schema.ability_schema, ability_data['DOTAAbilities'][a])

    unit_data_subset = {}
    for h in unit_data['DOTAUnits']:
        unit_data_subset[h] = subset(schema.unit_schema, unit_data['DOTAUnits'][h])

    item_data_subset = {}
    for a in item_data['DOTAAbilities']:
        item_data_subset[a] = subset(schema.item_schema, item_data['DOTAAbilities'][a])
        
    for h in hero_data_subset:
        for k in hero_data_subset[h]:
            if ' ' in hero_data_subset[h][k] or '|' in hero_data_subset[h][k] or ',' in hero_data_subset[h][k]:
                print hero_data_subset[h][k]
            elif is_number(hero_data_subset[h][k]):
                hero_data_subset[h][k] = format_num(float(hero_data_subset[h][k]))

    def process_ability_special(data):
        attributes = []
        for x in data:
            for y in x:
                if y != 'var_type':
                    abilityspecial_data = {}
                    abilityspecial_data['name'] = y
                    if is_number(x[y]):
                        abilityspecial_data['value'] = [x[y]]
                    else:
                        abilityspecial_data['value'] = [format_num(float(i)) if is_number(i) else i for i in x[y]]
                    if 'dota_tooltip_ability_' + a + '_' + y in tooltip_data_tokens:
                        abilityspecial_data['tooltip'] = tooltip_data_tokens['dota_tooltip_ability_' + a + '_' + y]
                    attributes.append(abilityspecial_data)
        return attributes
    
    for a in ability_data_subset:
        for k in ability_data_subset[a]:
            if k == 'AbilityBehavior':
                ability_data_subset[a][k] = [x.strip() for x in ability_data_subset[a][k].split('|')]
            elif ' ' in ability_data_subset[a][k] or '|' in ability_data_subset[a][k] or ',' in ability_data_subset[a][k]:
                ability_data_subset[a][k] = [format_num(float(x)) if is_number(x) else x.replace('|','') for x in ability_data_subset[a][k].split() if x != '|']
            elif k != 'AbilitySpecial' and is_number(ability_data_subset[a][k]):
                if k == 'AbilityManaCost' or k == 'AbilityCooldown':
                    ability_data_subset[a][k] = [format_num(float(ability_data_subset[a][k]))]
                else:
                    ability_data_subset[a][k] = format_num(float(ability_data_subset[a][k]))
            elif k == 'AbilitySpecial':
                ability_data_subset[a][k] = process_ability_special(ability_data_subset[a][k])

    for h in unit_data_subset:
        for k in unit_data_subset[h]:
            if ' ' in unit_data_subset[h][k] or '|' in unit_data_subset[h][k] or ',' in unit_data_subset[h][k]:
                print unit_data_subset[h][k]
            elif is_number(unit_data_subset[h][k]):
                unit_data_subset[h][k] = format_num(float(unit_data_subset[h][k]))

    itemslist = {'data': {}}
    for a in item_data_subset:
        if a.replace('item_', '') in items:
            itemslist['data'][a.replace('item_', '')] = tooltip_data_tokens['dota_tooltip_ability_' + a]
        for k in item_data_subset[a]:
            if ' ' in item_data_subset[a][k] or '|' in item_data_subset[a][k] or ',' in item_data_subset[a][k]:
                item_data_subset[a][k] = [format_num(float(x)) if is_number(x) else x.replace('|','') for x in item_data_subset[a][k].split() if x != '|']
            elif k != 'AbilitySpecial' and k != 'ItemRequirements' and is_number(item_data_subset[a][k]):
                if k == 'AbilityCooldown' or k == 'AbilityManaCost':
                    item_data_subset[a][k] = [format_num(float(item_data_subset[a][k]))]
                else:
                    item_data_subset[a][k] = format_num(float(item_data_subset[a][k]))
            elif k == 'AbilitySpecial':
                item_data_subset[a][k] = process_ability_special(item_data_subset[a][k])
            elif k == 'ItemRequirements':
                itemrequirements_data = []
                for x in item_data_subset[a][k]:
                    if x != item_data_subset[a]['ItemResult']:
                        itemrequirements_data = [i for i in x.strip(';').split(';')]
                item_data_subset[a][k] = itemrequirements_data
    ##print item_data_subset['item_broadsword']['AbilitySpecial']
    
    tooltip_data_subset = {}
    for h in hero_data_subset:
        tooltip_data_subset[h] = {}
        tooltip_data_subset[h]['DisplayName'] = tooltip_data_tokens[h]
        
        if h + '_bio' in tooltip_data_tokens:
            tooltip_data_subset[h]['Bio'] = tooltip_data_tokens[h + '_bio']
        else:
            print 'MISSING', h + '_bio'

        if h + '_hype' in tooltip_data_tokens:
            tooltip_data_subset[h]['Hype'] = tooltip_data_tokens[h + '_hype']
        else:
            print 'MISSING', h + '_hype'
            
    for a in ability_data_subset:
        if 'dota_tooltip_ability_' + a in tooltip_data_tokens:
            tooltip_data_subset[a] = {}
            tooltip_data_subset[a]['DisplayName'] = tooltip_data_tokens['dota_tooltip_ability_' + a]
        elif 'dota_tooltip_modifier_' + a in tooltip_data_tokens:
            tooltip_data_subset[a] = {}
            tooltip_data_subset[a]['DisplayName'] = tooltip_data_tokens['dota_tooltip_modifier_' + a]
        else:
            print 'MISSING', 'dota_tooltip_ability_' + a
            print 'MISSING', 'dota_tooltip_modifier_' + a
            
        if 'dota_tooltip_ability_' + a + '_description' in tooltip_data_tokens:
            tooltip_data_subset[a]['Description'] = tooltip_data_tokens['dota_tooltip_ability_' + a + '_description']
        elif 'dota_tooltip_modifier_' + a +'_description' in tooltip_data_tokens:
            tooltip_data_subset[a]['Description'] = tooltip_data_tokens['dota_tooltip_modifier_' + a + '_description']
        else:
            print 'MISSING', 'dota_tooltip_ability_' + a + '_description'
            print 'MISSING', 'dota_tooltip_modifier_' + a + '_description'
            
        if 'dota_tooltip_ability_' + a + '_lore' in tooltip_data_tokens:
            tooltip_data_subset[a]['Lore'] = tooltip_data_tokens['dota_tooltip_ability_' + a + '_lore']
        else:
            print 'MISSING', 'dota_tooltip_ability_' + a + '_lore'
            
    for h in unit_data_subset:
        if h in tooltip_data_tokens:
            tooltip_data_subset[h] = {}
            tooltip_data_subset[h]['DisplayName'] = tooltip_data_tokens[h]
        else:
            print 'MISSING', h
            
    for a in item_data_subset:
        if 'dota_tooltip_ability_' + a in tooltip_data_tokens:
            tooltip_data_subset[a] = {}
            tooltip_data_subset[a]['DisplayName'] = tooltip_data_tokens['dota_tooltip_ability_' + a]
        else:
            print 'MISSING', a
            
        if 'dota_tooltip_ability_' + a + '_description' in tooltip_data_tokens:
            tooltip_data_subset[a]['Description'] = tooltip_data_tokens['dota_tooltip_ability_' + a + '_description']
        else:
            print 'MISSING', 'dota_tooltip_ability_' + a + '_description'
            
        if 'dota_tooltip_ability_' + a + '_lore' in tooltip_data_tokens:
            tooltip_data_subset[a]['Lore'] = tooltip_data_tokens['dota_tooltip_ability_' + a + '_lore']
        else:
            print 'MISSING', 'dota_tooltip_ability_' + a + '_lore'
                        
    def mapkeys(schema, data):
        for x in data:
            for k in schema:
                if k in data[x]:
                    data[x][schema[k]] = data[x].pop(k)

    mapkeys(mapping.ability_schema, ability_data_subset)
    mapkeys(mapping.hero_schema, hero_data_subset)
    mapkeys(mapping.item_schema, item_data_subset)
    mapkeys(mapping.unit_schema, unit_data_subset)

    if 'Ability6' in hero_data_subset['npc_dota_hero_ursa'] and hero_data_subset['npc_dota_hero_ursa']['Ability6'] == 'ursa_enrage':
        hero_data_subset['npc_dota_hero_ursa']['Ability4'] = 'ursa_enrage'
        del hero_data_subset['npc_dota_hero_ursa']['Ability6']
    if 'Ability6' in hero_data_subset['npc_dota_hero_gyrocopter'] and hero_data_subset['npc_dota_hero_gyrocopter']['Ability6'] == 'gyrocopter_call_down':
        hero_data_subset['npc_dota_hero_gyrocopter']['Ability4'] = 'gyrocopter_call_down'
        del hero_data_subset['npc_dota_hero_gyrocopter']['Ability6']
    if 'Ability6' in hero_data_subset['npc_dota_hero_morphling'] and hero_data_subset['npc_dota_hero_morphling']['Ability6'] == 'morphling_morph':
        del hero_data_subset['npc_dota_hero_morphling']['Ability6']
    if 'Ability9' in hero_data_subset['npc_dota_hero_rubick'] and hero_data_subset['npc_dota_hero_rubick']['Ability9'] == 'rubick_hidden1':
        del hero_data_subset['npc_dota_hero_rubick']['Ability9']
    if 'Ability10' in hero_data_subset['npc_dota_hero_rubick'] and hero_data_subset['npc_dota_hero_rubick']['Ability10'] == 'rubick_hidden2':
        del hero_data_subset['npc_dota_hero_rubick']['Ability10']
    if 'Ability11' in hero_data_subset['npc_dota_hero_rubick'] and hero_data_subset['npc_dota_hero_rubick']['Ability11'] == 'rubick_hidden3':
        del hero_data_subset['npc_dota_hero_rubick']['Ability11']
                
    abilitytooltip_data = {}
    for a in ability_data_subset:
        ability_data_subset[a]['name'] = a
        ability_data_subset[a]['level'] = 0
        if 'attributes' not in ability_data_subset[a]:
            ability_data_subset[a]['attributes'] = []
        if a in tooltip_data_subset and 'DisplayName' in tooltip_data_subset[a]:
            ability_data_subset[a]['displayname'] = tooltip_data_subset[a]['DisplayName']
            
        abilitytooltip_data[a] = {}
        if a in tooltip_data_subset and 'Description' in tooltip_data_subset[a]:
            abilitytooltip_data[a]['description'] = tooltip_data_subset[a]['Description']
        if a in tooltip_data_subset and 'Lore' in tooltip_data_subset[a]:
            abilitytooltip_data[a]['lore'] = tooltip_data_subset[a]['Lore']

    for a in item_data_subset:
        item_data_subset[a]['name'] = a
        item_data_subset[a]['level'] = 0
        if 'attributes' not in item_data_subset[a]:
            item_data_subset[a]['attributes'] = []
        if 'cooldown' not in item_data_subset[a]:
            item_data_subset[a]['cooldown'] = []
        if 'manacost' not in item_data_subset[a]:
            item_data_subset[a]['manacost'] = []
        if a in tooltip_data_subset and 'DisplayName' in tooltip_data_subset[a]:
            item_data_subset[a]['displayname'] = tooltip_data_subset[a]['DisplayName']
        if a in tooltip_data_subset and 'Description' in tooltip_data_subset[a]:
            item_data_subset[a]['description'] = tooltip_data_subset[a]['Description']
        else:
            item_data_subset[a]['description'] = None
        if a in tooltip_data_subset and 'Lore' in tooltip_data_subset[a]:
            item_data_subset[a]['lore'] = tooltip_data_subset[a]['Lore']
        else:
            item_data_subset[a]['lore'] = None

    herobio_data = {}
    for h in hero_data_subset:
        abilities = []
        talents = [[], [], [], []]
        talentCount = 0
        for x in range(1,MAX_ABILITY_LEVEL):
            if 'Ability' + str(x) in hero_data_subset[h]:
                if 'special_bonus_' in hero_data_subset[h]['Ability' + str(x)]:
                    talents[int(math.floor(talentCount/2))].append(ability_data_subset[hero_data_subset[h]['Ability' + str(x)]])
                    talentCount = talentCount + 1
                else:
                    abilities.append(ability_data_subset[hero_data_subset[h]['Ability' + str(x)]])
                del hero_data_subset[h]['Ability' + str(x)]
        hero_data_subset[h]['abilities'] = abilities
        hero_data_subset[h]['talents'] = talents
        hero_data_subset[h]['level'] = 0
        hero_data_subset[h]['items'] = []
        hero_data_subset[h]['displayname'] = tooltip_data_subset[h]['DisplayName']
        hero_data_subset[h]['name'] = h
        
        herobio_data[h] = {}
        if 'Bio' in tooltip_data_subset[h]:
            herobio_data[h]['bio'] = tooltip_data_subset[h]['Bio']
        #if 'Hype' in tooltip_data_subset[h]:
        #    hero_data_subset[h]['hype'] = tooltip_data_subset[h]['Hype']
                    
    for h in unit_data_subset:
        abilities = []
        for x in range(1,MAX_ABILITY_LEVEL):
            if 'Ability' + str(x) in unit_data_subset[h]:
                if unit_data_subset[h]['Ability' + str(x)] in ability_data_subset:
                    abilities.append(ability_data_subset[unit_data_subset[h]['Ability' + str(x)]])
                else:
                    print "WARNING:", unit_data_subset[h]['Ability' + str(x)], "NOT IN ability_data_subset"
                del unit_data_subset[h]['Ability' + str(x)]
        unit_data_subset[h]['abilities'] = abilities
        unit_data_subset[h]['level'] = 0
        unit_data_subset[h]['name'] = h
        if h in tooltip_data_subset and 'DisplayName' in tooltip_data_subset[h]:
            unit_data_subset[h]['displayname'] = tooltip_data_subset[h]['DisplayName']

    item_data_subset = recipedata.set_item_cost(item_data_subset)
  
    print 'writing subset files'
    write_json(hero_data_subset, subset_dir + 'herodata.json')
    write_json(herobio_data, subset_dir + 'herobiodata.json')
    write_json(ability_data_subset, subset_dir + 'abilitydata.json')
    write_json(abilitytooltip_data, subset_dir + 'abilitytooltipdata.json')
    write_json(unit_data_subset, subset_dir + 'unitdata.json')
    write_json(item_data_subset, subset_dir + 'itemdata.json')
    write_json(tooltip_data_subset, subset_dir + 'tooltipdata.json')
    write_json(itemslist, subset_dir + 'items.json')
    write_json(heroeslist, subset_dir + 'heroes.json')
    with open(yaml_dir + 'herodata.yaml','w') as g:
        g.write(yaml.safe_dump(hero_data_subset))
    print 'done'

def trivia(subset_dir, trivia_dir):
    if triviaquestions:
        print 'trivia'
        triviaquestions.generate(subset_dir, trivia_dir)
    else:
        print 'no trivia module'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--clean", action='store_true')
    parser.add_argument("--make_dirs", action='store_true')
    parser.add_argument("--dotabuff", action='store_true')
    parser.add_argument("--dotabuff_branch", default='master')
    parser.add_argument("--dotabuff_in", default='../source/')
    parser.add_argument("--parse", action='store_true')
    parser.add_argument("--parse_in", default='../source/')
    parser.add_argument("--parse_out", default='../json/')
    parser.add_argument("--process", action='store_true')
    parser.add_argument("--process_in", default='../source/')
    parser.add_argument("--process_subset_dir", default='../dist/')
    parser.add_argument("--process_yaml_dir", default='../yaml/')
    parser.add_argument("--trivia", action='store_true')
    parser.add_argument("--trivia_dir", default='../trivia/')
    parser.add_argument("--move", action='store_true')
    args = parser.parse_args()

    if args.clean:
        clean(folders)
    if args.make_dirs:
        make_dirs(folders)
    if args.dotabuff:
        copy_source_from_dotabuff(args.dotabuff_in, args.dotabuff_branch)
    if args.parse:
        parse_all_vdf_to_json(args.parse_in, args.parse_out)
    if args.process:
        process(args.process_in, args.process_subset_dir, args.process_yaml_dir)
    if args.trivia:
        trivia(args.process_subset_dir, args.trivia_dir)
        
if __name__ == "__main__":
    main()