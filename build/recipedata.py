def get_item_upgrades(itemdata):
    upgradedata = {}
    for i in itemdata:
        item = itemdata[i]
        if 'ItemResult' in item:
            if item['ItemResult'] in upgradedata:
                print('ERROR')
            else:
                upgradedata[item['ItemResult']] = item['ItemRequirements']
                if item['itemcost'] > 0:
                    upgradedata[item['ItemResult']].append(i)
    return upgradedata

def get_item_cost(item, itemdata, upgradedata):
    if item == 'item_ward_dispenser' or not item in upgradedata:
        return itemdata[item]['itemcost']
    else:
        return sum([get_item_cost(x, itemdata, upgradedata) for x in upgradedata[item]])

def set_item_cost(itemdata):
    upgradedata = get_item_upgrades(itemdata)
    for i in itemdata:
        itemdata[i]['itemcost'] = get_item_cost(i, itemdata, upgradedata)
    return itemdata
