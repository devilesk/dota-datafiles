ability_schema = {
    'AbilityType':'abilitytype',
    'AbilityBehavior':'behavior',
    'AbilityCooldown':'cooldown',
    'AbilityDamage':'damage',
    'AbilityManaCost':'manacost',
    'AbilitySpecial':'attributes',
    'AbilityUnitDamageType':'abilityunitdamagetype'
    }

hero_schema = {
    'AbilityLayout':'abilitylayout',
    'ArmorPhysical':'armorphysical',
    'MagicalResistance':'magicalresistance',
    'AttackCapabilities':'attacktype',
    'AttackDamageMin':'attackdamagemin',
    'AttackDamageMax':'attackdamagemax',
    'AttackRate':'attackrate',
    'AttackAnimationPoint':'attackpoint',
    'AttackRange':'attackrange',
    'ProjectileSpeed':'projectilespeed',
    'AttributePrimary':'attributeprimary',
    'AttributeBaseStrength':'attributebasestrength',
    'AttributeStrengthGain':'attributestrengthgain',
    'AttributeBaseIntelligence':'attributebaseintelligence',
    'AttributeIntelligenceGain':'attributeintelligencegain',
    'AttributeBaseAgility':'attributebaseagility',
    'AttributeAgilityGain':'attributeagilitygain',
    'MovementSpeed':'movementspeed',
    'MovementTurnRate':'movementturnrate',
    'StatusHealth':'statushealth',
    'StatusHealthRegen':'statushealthregen',
    'StatusMana':'statusmana',
    'StatusManaRegen':'statusmanaregen',
    'VisionDaytimeRange':'visiondaytimerange',
    'VisionNighttimeRange':'visionnighttimerange',
    'Team':'team',
    'Role':'role'
    }

unit_schema = {
    'AbilityLayout':'abilitylayout',
    'ArmorPhysical':'armorphysical',
    'MagicalResistance':'magicalresistance',
    'AttackCapabilities':'attacktype',
    'AttackDamageMin':'attackdamagemin',
    'AttackDamageMax':'attackdamagemax',
    'AttackRate':'attackrate',
    'AttackAnimationPoint':'attackpoint',
    'AttackRange':'attackrange',
    'ProjectileSpeed':'projectilespeed',
    'AttributePrimary':'attributeprimary',
    'AttributeBaseStrength':'attributebasestrength',
    'AttributeStrengthGain':'attributestrengthgain',
    'AttributeBaseIntelligence':'attributebaseintelligence',
    'AttributeIntelligenceGain':'attributeintelligencegain',
    'AttributeBaseAgility':'attributebaseagility',
    'AttributeAgilityGain':'attributeagilitygain',
    'MovementSpeed':'movementspeed',
    'MovementTurnRate':'movementturnrate',
    'StatusHealth':'statushealth',
    'StatusHealthRegen':'statushealthregen',
    'StatusMana':'statusmana',
    'StatusManaRegen':'statusmanaregen',
    'VisionDaytimeRange':'visiondaytimerange',
    'VisionNighttimeRange':'visionnighttimerange',
    'AttackDamageType':'abilityunitdamagetype', 
    'BountyGoldMax':'bountygoldmax', 
    'BountyGoldMin':'bountygoldmin', 
    'BountyXP':'bountyxp',
    'Level':'unitlevel'
    }

item_schema = {
    'ID':'id',
    'AbilityDamage':'damage',
    'ItemCost':'itemcost',
    'AbilityDuration':'duration',
    'AbilitySpecial':'attributes',
    'AbilityManaCost':'manacost',
    'AbilityCooldown':'cooldown'
    }

hero_additional_properties = [
    'bio',
    'displayname',
    'name',
    'level',
    'items',
    'hype'
    ]

unit_additional_properties = [
    'displayname',
    'name',
    'level',
    'activated',
    'items'
    ]
