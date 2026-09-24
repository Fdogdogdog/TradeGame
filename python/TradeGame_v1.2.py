import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkFont
from tkinter import messagebox
from random import randint
import os
import listrandom
from copy import deepcopy
from tkinter.filedialog import askopenfilename, asksaveasfilename
from ast import literal_eval

if os.name == 'nt':
    from ctypes import windll
    try:
        windll.shcore.SetProcessDpiAwareness(1)
        
    except Exception:
        windll.user32.SetProcessDPIAware()

can_trade_build_bg='#F0F0F0'
cant_trade_build_bg='#D0D0D0'
can_trade_build_fg='#000000'
cant_trade_build_fg='#505050'

lst_save_code=[]
str_save_code=''

tutorial_current_page=0
tutorial_pages=[
    'Welcome to TradeGame! I bet you couldn\'t guess it by the name, but this is a game about trading.',
    'Your first goal will be getting a sawmill, however you do not have enough wood.',
    'Find a trade where the export is about 5 stone, and the import is wood. If you don\'t see one, keep pressing next turn until you find one.',
    'If you don\'t have enough stone, try to trade a small amount of wood away for stone. Otherwise, click next.',
    'Now that you have the materials, the \'Build Sawmill\' button should no longer be greyed-out. Press it to build your first sawmill.',
    'Now that you have built a sawmill, you have infinite wood. You can use this to trade for other resources to build more things.',
    'Press \'Close Tutorial\' to exit the tutorial.'
]

# Default
resources={
    'wood':45, # 45
    'stone':30, # 30
    'iron':0,
    'gold':0,
    'treasure':0
}

resource_values={
    'wood':1,
    'stone':2,
    'iron':4,
    'gold':10,
    'treasure':20
}

buildings={
    'sawmill':0,
    'stone_mine':0,
    'iron_mine':0,
    'gold_mine':0,
    'storehouse':0,
    'treasure_room':0
}

# DEV Save
# 1000/432500/2797500/365000/100000/1000/1000/1000/1000/9999

trade_export_blacklist=[]
trade_import_blacklist=['treasure']

quest_export_blacklist=[]
quest_import_blacklist=[]

trade_1={
    'export':'',
    'export_amount':0,
    'import':'',
    'import_amount':0
}

trade_2={
    'export':'',
    'export_amount':0,
    'import':'',
    'import_amount':0
}

trade_3={
    'export':'',
    'export_amount':0,
    'import':'',
    'import_amount':0
}

quest_people={
    # 'Fi':{
    #     'name':'fisherman',
    #     'quests':[]
    # },
    'Bu':{
        'name':'builder',
        'quests':[
            ((('wood', 25), ('stone', 15)), (('sawmill', 1), None)), # sawmill
            ((('stone', 25), ('wood', 15)), (('stone_mine', 1), None)), # stone mine
            ((('stone', 50), ('iron', 25)), (('iron_mine', 1), None)), # iron mine
            ((('iron', 50), ('stone', 25)), (('gold_mine', 1), None)), # gold mine
            ((('wood', 50), ('iron', 15)), (('storehouse', 1), None)), # storehouse
            ((('iron', 40), ('gold', 15)), (('treasure_room', 1), None)), # treasure room
            ]
    },
    # 'Bl':{
    #     'name':'blacksmith',
    #     'quests'
    # },
    # 'M':{
    #     'name':'mason',
    #     'quests'
    # }
}

# * means optional
# (((condition, amount),*(condition, amount)), ((reward, amount),*(reward, amount)))
# *for random amount: (min, max)

quest_1={
    'person':'',
    'quest':None
}

quest_2={
    'person':'',
    'quest':None
}

quest_3={
    'person':'',
    'quest':None
}

turns_taken=0

def open_file():
    filepath=askopenfilename(filetypes=[('Text Files', '*.txt'), ('All Files', '*.*')])
    if not filepath:
        return

    with open(filepath, mode='r') as input_file:
        text=input_file.read()
        window.title(f'TradeGame - {filepath.split('/')[-1][:-4]}')
        return text

def save_file(text):
    filepath=asksaveasfilename(defaultextension='.txt', filetypes=[('Text Files', '*.txt'), ('All Files', '*.*')])
    if not filepath:
        return
    with open(filepath, mode='w') as output_file:
        output_file.write(text)
        window.title(f'TradeGame - {filepath.split('/')[-1][:-4]}')

def save_code_write():
    global lst_save_code
    global str_save_code
    global turns_taken

    lst_save_code.clear()

    # v1.0
    lst_save_code.append(str(turns_taken))

    lst_save_code.append(str(resources['wood']))
    lst_save_code.append(str(resources['stone']))
    lst_save_code.append(str(resources['iron']))
    lst_save_code.append(str(resources['gold']))

    lst_save_code.append(str(buildings['sawmill']))
    lst_save_code.append(str(buildings['stone_mine']))
    lst_save_code.append(str(buildings['iron_mine']))
    lst_save_code.append(str(buildings['gold_mine']))

    # v1.1
    lst_save_code.append(str(buildings['storehouse']))

    lst_save_code.append(str(resources['treasure']))

    # v1.2
    lst_save_code.append(str(buildings['treasure_room']))

    lst_save_code.append(str(quest_1['person']))
    lst_save_code.append(str(quest_1['quest']))

    lst_save_code.append(str(quest_2['person']))
    lst_save_code.append(str(quest_2['quest']))

    lst_save_code.append(str(quest_3['person']))
    lst_save_code.append(str(quest_3['quest']))

    str_save_code='/'.join(lst_save_code)
    save_file(str_save_code)
    hide_menu()

def save_code_read():
    global lst_save_code
    global str_save_code
    global turns_taken
    str_save_code=open_file()

    if str_save_code:
        lst_save_code.clear()
        lst_save_code=str_save_code.split('/')

        # v1.0
        turns_taken=int(lst_save_code[0])
        
        resources['wood']=int(lst_save_code[1])
        resources['stone']=int(lst_save_code[2])
        resources['iron']=int(lst_save_code[3])
        resources['gold']=int(lst_save_code[4])

        buildings['sawmill']=int(lst_save_code[5])
        buildings['stone_mine']=int(lst_save_code[6])
        buildings['iron_mine']=int(lst_save_code[7])
        buildings['gold_mine']=int(lst_save_code[8])

        # v1.1
        try:
            buildings['storehouse']=int(lst_save_code[9])
        except IndexError:
            buildings['storehouse']=0

        try:
            resources['treasure']=int(lst_save_code[10])
        except IndexError:
            resources['treasure']=0

        # v1.2
        try:
            buildings['treasure_room']=int(lst_save_code[11])
        except IndexError:
            buildings['treasure_room']=0

        try:
            quest_1['person']=lst_save_code[12]
            quest_1['quest']=literal_eval(lst_save_code[13])
        except (IndexError, ValueError, SyntaxError):
            create_quest_1()

        try:
            quest_2['person']=lst_save_code[14]
            quest_2['quest']=literal_eval(lst_save_code[15])
        except (IndexError, ValueError, SyntaxError):
            create_quest_2()

        try:
            quest_3['person']=lst_save_code[16]
            quest_3['quest']=literal_eval(lst_save_code[17])
        except (IndexError, ValueError, SyntaxError):
            create_quest_3()

        create_trade_1()
        create_trade_2()
        create_trade_3()

        update()
    hide_menu()

def create_trade_1():
    resources_keys=list(resources.keys())
    while True:
        while True:
            trade_1['export']=resources_keys[randint(0, len(resources_keys)-1)]
            if resources[trade_1['export']]>0 and trade_1['export'] not in trade_export_blacklist:
                break
            else:
                continue
        
        while True:
            trade_1['import']=resources_keys[randint(0, len(resources_keys)-1)]
            if trade_1['import'] not in trade_import_blacklist:
                break
            else:
                continue
        
        if trade_1['export']==trade_1['import']:
            continue
        else:
            break
    
    trade_1['export_amount']=randint(1, resources[trade_1['export']]+5)

    trade_1['import_amount']=int(round(trade_1['export_amount']*(resource_values[trade_1['export']]/resource_values[trade_1['import']]), 0))

    while True:
        trade_1['import_amount']+=randint(-5, 5)
        if trade_1['import_amount']>0:
            break

def do_trade_1():
    if resources[trade_1['export']]>=trade_1['export_amount']:
        resources[trade_1['export']]-=trade_1['export_amount']
        resources[trade_1['import']]+=trade_1['import_amount']
        create_trade_1()
    update()

def create_trade_2():
    resources_keys=list(resources.keys())
    while True:
        while True:
            trade_2['export']=resources_keys[randint(0, len(resources_keys)-1)]
            if resources[trade_2['export']]>0 and trade_2['export'] not in trade_export_blacklist:
                break
            else:
                continue
        
        while True:
            trade_2['import']=resources_keys[randint(0, len(resources_keys)-1)]
            if trade_2['import'] not in trade_import_blacklist:
                break
            else:
                continue
        
        if trade_2['export']==trade_2['import']:
            continue
        else:
            break
    
    trade_2['export_amount']=randint(1, resources[trade_2['export']]+5)

    trade_2['import_amount']=int(round(trade_2['export_amount']*(resource_values[trade_2['export']]/resource_values[trade_2['import']]), 0))

    while True:
        trade_2['import_amount']+=randint(-5, 5)
        if trade_2['import_amount']>0:
            break

def do_trade_2():
    if resources[trade_2['export']]>=trade_2['export_amount']:
        resources[trade_2['export']]-=trade_2['export_amount']
        resources[trade_2['import']]+=trade_2['import_amount']
        create_trade_2()
    update()

def create_trade_3():
    resources_keys=list(resources.keys())
    while True:
        while True:
            trade_3['export']=resources_keys[randint(0, len(resources_keys)-1)]
            if resources[trade_3['export']]>0 and trade_3['export'] not in trade_export_blacklist:
                break
            else:
                continue
        
        while True:
            trade_3['import']=resources_keys[randint(0, len(resources_keys)-1)]
            if trade_3['import'] not in trade_import_blacklist:
                break
            else:
                continue
        
        if trade_3['export']==trade_3['import']:
            continue
        else:
            break
    
    trade_3['export_amount']=randint(1, resources[trade_3['export']]+5)

    trade_3['import_amount']=int(round(trade_3['export_amount']*(resource_values[trade_3['export']]/resource_values[trade_3['import']]), 0))

    while True:
        trade_3['import_amount']+=randint(-5, 5)
        if trade_3['import_amount']>0:
            break

def do_trade_3():
    if resources[trade_3['export']]>=trade_3['export_amount']:
        resources[trade_3['export']]-=trade_3['export_amount']
        resources[trade_3['import']]+=trade_3['import_amount']
        create_trade_3()
    update()

def create_quest_1():
    quest_1['person']=listrandom.DictKeys(quest_people)
    quest_1['quest']=deepcopy(listrandom.ListTupleSet(quest_people[quest_1['person']]['quests']))
    conditions=list(deepcopy(quest_1['quest'][0]))
    for condition in conditions:
        if condition:
            if isinstance(condition[1], tuple):
                # is random
                condition_index=conditions.index(condition)
                conditions[condition_index]=list(conditions[condition_index])
                conditions[condition_index][1]=randint(condition[1][0], condition[1][1])
                conditions[condition_index]=tuple(conditions[condition_index])

    rewards=list(deepcopy(quest_1['quest'][1]))
    for reward in rewards:
        if reward:
            if isinstance(reward[1], tuple):
                # is random
                reward_index=rewards.index(reward)
                rewards[reward_index]=list(rewards[reward_index])
                rewards[reward_index][1]=randint(reward[1][0], reward[1][1])
                rewards[reward_index]=tuple(rewards[reward_index])

    quest_1['quest']=list(quest_1['quest'])
    quest_1['quest'][0]=tuple(deepcopy(conditions))
    quest_1['quest'][1]=tuple(deepcopy(rewards))
    quest_1['quest']=tuple(quest_1['quest'])

def do_quest_1():
    conditions=deepcopy(quest_1['quest'][0])
    rewards=deepcopy(quest_1['quest'][1])
    conditions_true=[]
    for condition in conditions:
        if condition:
            if condition[0] in resources:
                if resources[condition[0]]>=condition[1]:
                    conditions_true.append(True)

            elif condition[0] in buildings:
                if buildings[condition[0]]>=condition[1]:
                    conditions_true.append(True)

    if len(conditions_true)==len(conditions):
        for condition in conditions:
            if condition:
                if condition[0] in resources:
                    resources[condition[0]]-=condition[1]

                if condition[0] in buildings:
                    buildings[condition[0]]-=condition[1]

        for reward in rewards:
            if reward:
                if reward[0] in resources:
                    resources[reward[0]]+=reward[1]

                if reward[0] in buildings:
                    buildings[reward[0]]+=reward[1]

        create_quest_1()
    update()

def create_quest_2():
    quest_2['person']=listrandom.DictKeys(quest_people)
    quest_2['quest']=deepcopy(listrandom.ListTupleSet(quest_people[quest_2['person']]['quests']))
    conditions=list(deepcopy(quest_2['quest'][0]))
    for condition in conditions:
        if condition:
            if isinstance(condition[1], tuple):
                # is random
                condition_index=conditions.index(condition)
                conditions[condition_index]=list(conditions[condition_index])
                conditions[condition_index][1]=randint(condition[1][0], condition[1][1])
                conditions[condition_index]=tuple(conditions[condition_index])

    rewards=list(deepcopy(quest_2['quest'][1]))
    for reward in rewards:
        if reward:
            if isinstance(reward[1], tuple):
                # is random
                reward_index=rewards.index(reward)
                rewards[reward_index]=list(rewards[reward_index])
                rewards[reward_index][1]=randint(reward[1][0], reward[1][1])
                rewards[reward_index]=tuple(rewards[reward_index])

    quest_2['quest']=list(quest_2['quest'])
    quest_2['quest'][0]=tuple(deepcopy(conditions))
    quest_2['quest'][1]=tuple(deepcopy(rewards))
    quest_2['quest']=tuple(quest_2['quest'])

def do_quest_2():
    conditions=deepcopy(quest_2['quest'][0])
    rewards=deepcopy(quest_2['quest'][1])
    conditions_true=[]
    for condition in conditions:
        if condition:
            if condition[0] in resources:
                if resources[condition[0]]>=condition[1]:
                    conditions_true.append(True)

            elif condition[0] in buildings:
                if buildings[condition[0]]>=condition[1]:
                    conditions_true.append(True)

    if len(conditions_true)==len(conditions):
        for condition in conditions:
            if condition:
                if condition[0] in resources:
                    resources[condition[0]]-=condition[1]

                if condition[0] in buildings:
                    buildings[condition[0]]-=condition[1]

        for reward in rewards:
            if reward:
                if reward[0] in resources:
                    resources[reward[0]]+=reward[1]

                if reward[0] in buildings:
                    buildings[reward[0]]+=reward[1]

        create_quest_2()
    update()

def create_quest_3():
    quest_3['person']=listrandom.DictKeys(quest_people)
    quest_3['quest']=deepcopy(listrandom.ListTupleSet(quest_people[quest_3['person']]['quests']))
    conditions=list(deepcopy(quest_3['quest'][0]))
    for condition in conditions:
        if condition:
            if isinstance(condition[1], tuple):
                # is random
                condition_index=conditions.index(condition)
                conditions[condition_index]=list(conditions[condition_index])
                conditions[condition_index][1]=randint(condition[1][0], condition[1][1])
                conditions[condition_index]=tuple(conditions[condition_index])

    rewards=list(deepcopy(quest_3['quest'][1]))
    for reward in rewards:
        if reward:
            if isinstance(reward[1], tuple):
                # is random
                reward_index=rewards.index(reward)
                rewards[reward_index]=list(rewards[reward_index])
                rewards[reward_index][1]=randint(reward[1][0], reward[1][1])
                rewards[reward_index]=tuple(rewards[reward_index])

    quest_3['quest']=list(quest_3['quest'])
    quest_3['quest'][0]=tuple(deepcopy(conditions))
    quest_3['quest'][1]=tuple(deepcopy(rewards))
    quest_3['quest']=tuple(quest_3['quest'])

def do_quest_3():
    conditions=deepcopy(quest_3['quest'][0])
    rewards=deepcopy(quest_3['quest'][1])
    conditions_true=[]
    for condition in conditions:
        if condition:
            if condition[0] in resources:
                if resources[condition[0]]>=condition[1]:
                    conditions_true.append(True)

            elif condition[0] in buildings:
                if buildings[condition[0]]>=condition[1]:
                    conditions_true.append(True)

    if len(conditions_true)==len(conditions):
        for condition in conditions:
            if condition:
                if condition[0] in resources:
                    resources[condition[0]]-=condition[1]

                if condition[0] in buildings:
                    buildings[condition[0]]-=condition[1]

        for reward in rewards:
            if reward:
                if reward[0] in resources:
                    resources[reward[0]]+=reward[1]

                if reward[0] in buildings:
                    buildings[reward[0]]+=reward[1]

        create_quest_3()
    update()

def update():
    msg_tutorial.configure(text=tutorial_pages[tutorial_current_page])
    lbl_wood_amount.configure(bg='#F0F0F0')
    lbl_sawmill_amount.configure(bg='#F0F0F0')
    lbl_stone_amount.configure(bg='#F0F0F0')
    frm_trades_quests.configure(bg='#F0F0F0')
    btn_build_sawmill.configure(style='TButton')
    btn_next_turn.configure(style='Title.TButton')

    if tutorial_current_page==1:
        lbl_wood_amount.configure(bg='#FFFF00')
        lbl_sawmill_amount.configure(bg='#FFFF00')
        btn_build_sawmill.configure(style='Highlight.TButton')
    
    if tutorial_current_page==2:
        frm_trades_quests.configure(bg='#FFFF00')
        lbl_stone_amount.configure(bg='#FFFF00')
        lbl_wood_amount.configure(bg='#FFFF00')
        btn_next_turn.configure(style='Highlight.TButton')
    
    if tutorial_current_page==3:
        frm_trades_quests.configure(bg='#FFFF00')
        lbl_stone_amount.configure(bg='#FFFF00')
    
    if tutorial_current_page==4:
        btn_build_sawmill.configure(style='Highlight.TButton')

    if resources['wood']>(100*buildings['storehouse'])+100:
        resources['wood']=(100*buildings['storehouse'])+100

    if resources['stone']>(100*buildings['storehouse'])+100:
        resources['stone']=(100*buildings['storehouse'])+100
    
    if resources['iron']>(100*buildings['storehouse'])+100:
        resources['iron']=(100*buildings['storehouse'])+100
    
    if resources['gold']>(100*buildings['storehouse'])+100:
        resources['gold']=(100*buildings['storehouse'])+100
    
    if resources['treasure']>(10*buildings['treasure_room'])+10:
        resources['treasure']=(10*buildings['treasure_room'])+10

    lbl_wood_amount.configure(text=f'Wood: {resources['wood']}/{(100*buildings['storehouse'])+100}')
    lbl_stone_amount.configure(text=f'Stone: {resources['stone']}/{(100*buildings['storehouse'])+100}')
    lbl_iron_amount.configure(text=f'Iron: {resources['iron']}/{(100*buildings['storehouse'])+100}')
    lbl_gold_amount.configure(text=f'Gold: {resources['gold']}/{(100*buildings['storehouse'])+100}')
    lbl_treasure_amount.configure(text=f'Treasure: {resources['treasure']}/{(10*buildings['treasure_room'])+10}')

    lbl_sawmill_amount.configure(text=f'Sawmills (produces 5 wood per turn): {buildings['sawmill']}')
    lbl_stone_mine_amount.configure(text=f'Stone Mines (produces 10 stone per turn): {buildings['stone_mine']}')
    lbl_iron_mine_amount.configure(text=f'Iron Mines (produces 5 iron and 10 stone per turn): {buildings['iron_mine']}')
    lbl_gold_mine_amount.configure(text=f'Gold Mines (produces 1 gold and 10 stone per turn): {buildings['gold_mine']}')
    lbl_storehouse_amount.configure(text=f'Storehouses (allows you to hold 100 more of each resource): {buildings['storehouse']}')
    lbl_treasure_room_amount.configure(text=f'Treasure Rooms (allows you to hold 10 more treasure): {buildings['treasure_room']}')

    btn_trade_1.configure(text=f'Export: {trade_1['export_amount']} {trade_1['export']}, Import: {trade_1['import_amount']} {trade_1['import']}')
    btn_trade_2.configure(text=f'Export: {trade_2['export_amount']} {trade_2['export']}, Import: {trade_2['import_amount']} {trade_2['import']}')
    btn_trade_3.configure(text=f'Export: {trade_3['export_amount']} {trade_3['export']}, Import: {trade_3['import_amount']} {trade_3['import']}')

    # quest_1_stuff
    quest_1_conditions=[]
    for condition in quest_1['quest'][0]:
        if condition:
            quest_1_conditions.append(f'{condition[1]} {condition[0].replace('_', ' ')}')

    quest_1_rewards=[]
    for reward in quest_1['quest'][1]:
        if reward:
            quest_1_rewards.append(f'{reward[1]} {reward[0].replace('_', ' ')}{"s" if reward[1]>1 else ""}')

    # quest_2_stuff
    quest_2_conditions=[]
    for condition in quest_2['quest'][0]:
        if condition:
            quest_2_conditions.append(f'{condition[1]} {condition[0].replace('_', ' ')}')

    quest_2_rewards=[]
    for reward in quest_2['quest'][1]:
        if reward:
            quest_2_rewards.append(f'{reward[1]} {reward[0].replace('_', ' ')}{"s" if reward[1]>1 else ""}')

    # quest_3_stuff
    quest_3_conditions=[]
    for condition in quest_3['quest'][0]:
        if condition:
            quest_3_conditions.append(f'{condition[1]} {condition[0].replace('_', ' ')}')

    quest_3_rewards=[]
    for reward in quest_3['quest'][1]:
        if reward:
            quest_3_rewards.append(f'{reward[1]} {reward[0].replace('_', ' ')}{"s" if reward[1]>1 else ""}')

    btn_quest_1.configure(text=f'The {quest_people[quest_1['person']]['name']} wants {' and '.join(quest_1_conditions)}. In return they will give you {' and '.join(quest_1_rewards)}.')
    btn_quest_2.configure(text=f'The {quest_people[quest_2['person']]['name']} wants {' and '.join(quest_2_conditions)}. In return they will give you {' and '.join(quest_2_rewards)}.')
    btn_quest_3.configure(text=f'The {quest_people[quest_3['person']]['name']} wants {' and '.join(quest_3_conditions)}. In return they will give you {' and '.join(quest_3_rewards)}.')

    # build button colours
    if resources['wood']>=50 and resources['stone']>=25:
        btn_build_sawmill.configure(state='normal')
    else:
        btn_build_sawmill.configure(state='disabled')
    
    if resources['stone']>=50 and resources['wood']>=25:
        btn_build_stone_mine.configure(state='normal')
    else:
        btn_build_stone_mine.configure(state='disabled')
    
    if resources['stone']>=100 and resources['iron']>=50:
        btn_build_iron_mine.configure(state='normal')
    else:
        btn_build_iron_mine.configure(state='disabled')
    
    if resources['iron']>=100 and resources['stone']>=50:
        btn_build_gold_mine.configure(state='normal')
    else:
        btn_build_gold_mine.configure(state='disabled')
    
    if resources['wood']>=100 and resources['iron']>=25:
        btn_build_storehouse.configure(state='normal')
    else:
        btn_build_storehouse.configure(state='disabled')

    if resources['iron']>=75 and resources['gold']>=25:
        btn_build_treasure_room.configure(state='normal')
    else:
        btn_build_treasure_room.configure(state='disabled')

    # trade button colours
    if trade_1['export_amount']<=resources[trade_1['export']]:
        btn_trade_1.configure(state='normal')
    else:
        btn_trade_1.configure(state='disabled')
    
    if trade_2['export_amount']<=resources[trade_2['export']]:
        btn_trade_2.configure(state='normal')
    else:
        btn_trade_2.configure(state='disabled')
    
    if trade_3['export_amount']<=resources[trade_3['export']]:
        btn_trade_3.configure(state='normal')
    else:
        btn_trade_3.configure(state='disabled')

    # quest button colours
    quest_1_conditions=deepcopy(quest_1['quest'][0])
    quest_2_conditions=deepcopy(quest_2['quest'][0])
    quest_3_conditions=deepcopy(quest_3['quest'][0])

    quest_1_conditions_true=[]
    quest_2_conditions_true=[]
    quest_3_conditions_true=[]

    # quest_1
    for condition in quest_1_conditions:
        if condition:
            if condition[0] in resources:
                if resources[condition[0]]>=condition[1]:
                    quest_1_conditions_true.append(True)

            elif condition[0] in buildings:
                if buildings[condition[0]]>=condition[1]:
                    quest_1_conditions_true.append(True)

    if len(quest_1_conditions_true)==len(quest_1_conditions):
        btn_quest_1.configure(state='normal')
    else:
        btn_quest_1.configure(state='disabled')

    # quest_2
    for condition in quest_2_conditions:
        if condition:
            if condition[0] in resources:
                if resources[condition[0]]>=condition[1]:
                    quest_2_conditions_true.append(True)

            elif condition[0] in buildings:
                if buildings[condition[0]]>=condition[1]:
                    quest_2_conditions_true.append(True)

    if len(quest_2_conditions_true)==len(quest_2_conditions):
        btn_quest_2.configure(state='normal')
    else:
        btn_quest_2.configure(state='disabled')

    # quest_3
    for condition in quest_3_conditions:
        if condition:
            if condition[0] in resources:
                if resources[condition[0]]>=condition[1]:
                    quest_3_conditions_true.append(True)

            elif condition[0] in buildings:
                if buildings[condition[0]]>=condition[1]:
                    quest_3_conditions_true.append(True)

    if len(quest_3_conditions_true)==len(quest_3_conditions):
        btn_quest_3.configure(state='normal')
    else:
        btn_quest_3.configure(state='disabled')

    lbl_turns_taken.configure(text=f'Turns Taken: {turns_taken}')

def next_turn():
    global turns_taken

    turns_taken+=1

    resources['wood']+=5*buildings['sawmill'] 
    resources['stone']+=10*buildings['stone_mine']
    resources['iron']+=5*buildings['iron_mine']
    resources['stone']+=10*buildings['iron_mine']
    resources['gold']+=1*buildings['gold_mine']
    resources['stone']+=10*buildings['gold_mine']
    
    create_trade_1()
    create_trade_2()
    create_trade_3()

    update()

def build_sawmill():
    if resources['wood']>=50 and resources['stone']>=25:
        resources['wood']-=50
        resources['stone']-=25
        buildings['sawmill']+=1
    update()

def build_stone_mine():
    if resources['stone']>=50 and resources['wood']>=25:
        resources['stone']-=50
        resources['wood']-=25
        buildings['stone_mine']+=1
    update()

def build_iron_mine():
    if resources['stone']>=100 and resources['iron']>=50:
        resources['stone']-=100
        resources['iron']-=50
        buildings['iron_mine']+=1
    update()

def build_gold_mine():
    if resources['iron']>=100 and resources['stone']>=50:
        resources['iron']-=100
        resources['stone']-=50
        buildings['gold_mine']+=1
    update()

def build_storehouse():
    if resources['wood']>=100 and resources['iron']>=25:
        resources['wood']-=100
        resources['iron']-=25
        buildings['storehouse']+=1
    update()

def build_treasure_room():
    if resources['iron']>=75 and resources['gold']>=25:
        resources['iron']-=75
        resources['gold']-=25
        buildings['treasure_room']+=1
    update()

def show_menu():
    tlv_menu.deiconify()

def hide_menu():
    tlv_menu.withdraw()

def show_tutorial():
    tlv_tutorial.deiconify()
    hide_menu()

def hide_tutorial():
    global tutorial_current_page
    tlv_tutorial.withdraw()
    tutorial_current_page=0
    update()

def show_whats_new():
    tlv_whats_new.deiconify()
    hide_menu()

def hide_whats_new():
    tlv_whats_new.withdraw()

def show_credits():
    tlv_credits.deiconify()
    hide_menu()

def hide_credits():
    tlv_credits.withdraw()

def next_tutorial_page():
    global tutorial_current_page
    if tutorial_current_page>=len(tutorial_pages)-1:
        pass
    else:
        tutorial_current_page+=1
        update()

def prev_tutorial_page():
    global tutorial_current_page
    if tutorial_current_page<=0:
        pass
    else:
        tutorial_current_page-=1
        update()

def quit_game():
    hide_menu()
    choice_quit=messagebox.askquestion('Quit Game?', 'All unsaved progress will be lost.\nAre you sure you want to quit?')
    if choice_quit=='yes':
        window.destroy()

def resize_msg_tutorial(event):
    if event.widget == tlv_tutorial:
        msg_tutorial.config(width=event.width)

def resize_msg_whats_new(event):
    if event.widget == tlv_whats_new:
        msg_whats_new.config(width=event.width)

def resize_msg_credits(event):
    if event.widget == tlv_credits:
        msg_credits.config(width=event.width)

window=tk.Tk()
window.title('TradeGame')

window.configure(background='#F0F0F0')

tlv_menu=tk.Toplevel(window)
tlv_menu.title('Menu - TradeGame')
tlv_menu.withdraw()
tlv_menu.protocol('WM_DELETE_WINDOW', hide_menu)

tlv_tutorial=tk.Toplevel(window)
tlv_tutorial.title('Tutorial - TradeGame')
tlv_tutorial.withdraw()
tlv_tutorial.protocol('WM_DELETE_WINDOW', hide_tutorial)
tlv_tutorial.bind('<Configure>', resize_msg_tutorial)

tlv_whats_new=tk.Toplevel(window)
tlv_whats_new.title('What\'s New? - TradeGame')
tlv_whats_new.withdraw()
tlv_whats_new.protocol('WM_DELETE_WINDOW', hide_whats_new)
tlv_whats_new.bind('<Configure>', resize_msg_whats_new)

tlv_credits=tk.Toplevel(window)
tlv_credits.title('Credits - TradeGame')
tlv_credits.withdraw()
tlv_credits.protocol('WM_DELETE_WINDOW', hide_credits)
tlv_credits.bind('<Configure>', resize_msg_credits)

fnt_title=tkFont.Font(size=12, weight='bold')
fnt_main=tkFont.Font(size=12)

sty_title_lbl=ttk.Style()
sty_title_lbl.theme_use('clam')
sty_title_lbl.configure('Title.TLabel', font=fnt_title, anchor='center', justify='center', background='#F0F0F0')

sty_title_btn=ttk.Style()
sty_title_btn.theme_use('clam')
sty_title_btn.configure('Title.TButton', font=fnt_title, anchor='center', justify='center', background='#F0F0F0')

sty_main=ttk.Style()
sty_main.theme_use('clam')
sty_main.configure('.', font=fnt_main, anchor='center', background='#F0F0F0')

sty_main_btn=ttk.Style()
sty_main_btn.configure('TButton', font=fnt_main, background='#F0F0F0')
sty_main_btn.map('TButton',
                 foreground=[('!disabled', can_trade_build_fg),('disabled', cant_trade_build_fg)],
                 background=[('!disabled', can_trade_build_bg), ('disabled', cant_trade_build_bg)])

sty_main_btn_highlight=ttk.Style()
sty_main_btn_highlight.configure('Highlight.TButton', font=fnt_main, background='#FFFF00')
sty_main_btn_highlight.map('Highlight.TButton',
                 foreground=[('!disabled', can_trade_build_fg),('disabled', cant_trade_build_fg)],
                 background=[('!disabled', '#FFFF00'), ('disabled', '#A3A000')])

window.resizable(width=True, height=False)
tlv_menu.resizable(width=True, height=False)
tlv_tutorial.resizable(width=True, height=False)
tlv_whats_new.resizable(width=True, height=False)
tlv_credits.resizable(width=True, height=False)

window.columnconfigure([0,1,2], weight=1)
window.rowconfigure([0,1,2], weight=1)

tlv_menu.columnconfigure(0, weight=1)
tlv_menu.rowconfigure([0,1,2,3,4], weight=1)

tlv_tutorial.columnconfigure([0,1], weight=1)
tlv_tutorial.rowconfigure([0,1,2], weight=1)

tlv_whats_new.columnconfigure(0, weight=1)
tlv_whats_new.rowconfigure([0,1], weight=1)

tlv_credits.columnconfigure(0, weight=1)
tlv_credits.rowconfigure([0,1], weight=1)

frm_buildings=ttk.Frame(window, padding=10)
frm_resources=ttk.Frame(window, padding=10)
frm_trades_quests=tk.Frame(window, padx=10, pady=10)
frm_next_turn=ttk.Frame(window, padding=10)
frm_save_load=ttk.Frame(tlv_menu, padding=10)

frm_buildings.columnconfigure(0, weight=1)
frm_buildings.rowconfigure([0,1,2,3,4,5,6,7,8,9,10], weight=1)

frm_resources.columnconfigure(0, weight=1)
frm_resources.rowconfigure([0,1,2,3,4,5], weight=1)

frm_trades_quests.columnconfigure(0, weight=1)
frm_trades_quests.rowconfigure([0,1,2,3,4,5,6,7], weight=1)

frm_next_turn.columnconfigure(0, weight=1)
frm_next_turn.rowconfigure([0,1], weight=1)

frm_save_load.columnconfigure([0,1], weight=1)
frm_save_load.rowconfigure(0, weight=1)

# main window
lbl_buildings=tk.Label(frm_buildings, text='Buildings:', font=fnt_title)

btn_build_sawmill=ttk.Button(frm_buildings, text='Build Sawmill (Cost: 50 wood, 25 stone)', command=build_sawmill)
btn_build_stone_mine=ttk.Button(frm_buildings, text='Build Stone Mine (Cost: 50 stone, 25 wood)', command=build_stone_mine)
btn_build_iron_mine=ttk.Button(frm_buildings, text='Build Iron Mine (Cost: 100 stone, 50 iron)', command=build_iron_mine)
btn_build_gold_mine=ttk.Button(frm_buildings, text='Build Gold Mine (Cost: 100 iron, 50 stone)', command=build_gold_mine)
btn_build_storehouse=ttk.Button(frm_buildings, text='Build Storehouse (Cost: 100 wood, 25 iron)', command=build_storehouse)
btn_build_treasure_room=ttk.Button(frm_buildings, text='Build Treasure Room (Cost: 75 iron, 25 gold)', command=build_treasure_room)

lbl_sawmill_amount=tk.Label(frm_buildings, font=fnt_main)
lbl_stone_mine_amount=tk.Label(frm_buildings, font=fnt_main)
lbl_iron_mine_amount=tk.Label(frm_buildings, font=fnt_main)
lbl_gold_mine_amount=tk.Label(frm_buildings, font=fnt_main)
lbl_storehouse_amount=tk.Label(frm_buildings, font=fnt_main)
lbl_treasure_room_amount=tk.Label(frm_buildings, font=fnt_main)

lbl_resources=tk.Label(frm_resources, text='Resources:', font=fnt_title)

lbl_wood_amount=tk.Label(frm_resources, font=fnt_main)
lbl_stone_amount=tk.Label(frm_resources, font=fnt_main)
lbl_iron_amount=tk.Label(frm_resources, font=fnt_main)
lbl_gold_amount=tk.Label(frm_resources, font=fnt_main)
lbl_treasure_amount=tk.Label(frm_resources, font=fnt_main)

lbl_trades=tk.Label(frm_trades_quests, text='Trades:', font=fnt_title)

btn_trade_1=ttk.Button(frm_trades_quests, command=do_trade_1)
btn_trade_2=ttk.Button(frm_trades_quests, command=do_trade_2)
btn_trade_3=ttk.Button(frm_trades_quests, command=do_trade_3)

lbl_quests=tk.Label(frm_trades_quests, text='Quests:', font=fnt_title)

btn_quest_1=ttk.Button(frm_trades_quests, command=do_quest_1)
btn_quest_2=ttk.Button(frm_trades_quests, command=do_quest_2)
btn_quest_3=ttk.Button(frm_trades_quests, command=do_quest_3)

btn_next_turn=ttk.Button(frm_next_turn, text='Next Turn', command=next_turn, style='Title.TButton')
lbl_turns_taken=ttk.Label(frm_next_turn)

btn_open_menu=ttk.Button(window, text='Menu', command=show_menu, style='Title.TButton')

# menu
btn_open_tutorial=ttk.Button(tlv_menu, text='Tutorial', command=show_tutorial, style='Title.TButton')

btn_open_whats_new=ttk.Button(tlv_menu, text='What\'s New?', command=show_whats_new, style='Title.TButton')

lbl_save_code=tk.Label(frm_save_load, text='Save Code:', font=fnt_title)
ent_save_code=ttk.Entry(frm_save_load)
btn_save_code_write=ttk.Button(frm_save_load, text='Save', command=save_code_write)
btn_save_code_read=ttk.Button(frm_save_load, text='Load', command=save_code_read)

btn_open_credits=ttk.Button(tlv_menu, text='Credits', command=show_credits, style='Title.TButton')

btn_close_menu=ttk.Button(tlv_menu, text='Close Menu', command=hide_menu, style='Title.TButton')
btn_quit_game=ttk.Button(tlv_menu, text='Quit Game', command=quit_game, style='Title.TButton')

# tutorial
msg_tutorial=tk.Message(tlv_tutorial, font=fnt_main)

btn_prev_tutorial=ttk.Button(tlv_tutorial, text='Previous', command=prev_tutorial_page)
btn_next_tutorial=ttk.Button(tlv_tutorial, text='Next', command=next_tutorial_page)

btn_close_tutorial=ttk.Button(tlv_tutorial, text='Close Tutorial', command=hide_tutorial, style='Title.TButton')

# whats new
msg_whats_new=tk.Message(tlv_whats_new, text='TradeGame v1.1\n\nAdded:\nTreasure Room (buildings[\'treasure_room\'])\nQuests (quest_people, quest_1, quest_2, quest_3, create_quest_1(), create_quest_2(), create_quest_3(), do_quest_1(), do_quest_2(), do_quest_3())\n\nChanged:\nSaves are now saved as files\n\nRemoved:\nSave code (lbl_save_code.grid(), ent_save_code.grid())\nCredits (tlv_credts)\n\nFixed:\nNothing', font=fnt_main)

btn_close_whats_new=ttk.Button(tlv_whats_new, text='Close What\'s New', command=hide_whats_new, style='Title.TButton')

# whats new
msg_credits=tk.Message(tlv_credits, text='Coded with Python\nUI made with Tkinter module\nPython Programmer: Frank\nWeb Translator: Ethan\nWeb Programmers: Ethan & Frank', font=fnt_main)

btn_close_credits=ttk.Button(tlv_credits, text='Close Credits', command=hide_credits, style='Title.TButton')

# main window
lbl_buildings.grid(column=0, row=0, sticky='ew')

btn_build_sawmill.grid(column=0, row=1, sticky='ew')
btn_build_stone_mine.grid(column=0, row=2, sticky='ew')
btn_build_iron_mine.grid(column=0, row=3, sticky='ew')
btn_build_gold_mine.grid(column=0, row=4, sticky='ew')
btn_build_storehouse.grid(column=0, row=5, sticky='ew')
btn_build_treasure_room.grid(column=0, row=6, sticky='ew')

lbl_sawmill_amount.grid(column=0, row=7, sticky='ew')
lbl_stone_mine_amount.grid(column=0, row=8, sticky='ew')
lbl_iron_mine_amount.grid(column=0, row=9, sticky='ew')
lbl_gold_mine_amount.grid(column=0, row=10, sticky='ew')
lbl_storehouse_amount.grid(column=0, row=11, sticky='ew')
lbl_treasure_room_amount.grid(column=0, row=12, sticky='ew')

lbl_resources.grid(column=0, row=0, sticky='ew')

lbl_wood_amount.grid(column=0, row=1, sticky='ew')
lbl_stone_amount.grid(column=0, row=2, sticky='ew')
lbl_iron_amount.grid(column=0, row=3, sticky='ew')
lbl_gold_amount.grid(column=0, row=4, sticky='ew')
lbl_treasure_amount.grid(column=0, row=5, sticky='ew')

lbl_trades.grid(column=0, row=0, sticky='nsew')

btn_trade_1.grid(column=0, row=1, sticky='nsew')
btn_trade_2.grid(column=0, row=2, sticky='nsew')
btn_trade_3.grid(column=0, row=3, sticky='nsew')

lbl_quests.grid(column=0, row=4, sticky='nsew')

btn_quest_1.grid(column=0, row=5, sticky='nsew')
btn_quest_2.grid(column=0, row=6, sticky='nsew')
btn_quest_3.grid(column=0, row=7, sticky='nsew')

btn_next_turn.grid(column=0, row=0, sticky='ew')
lbl_turns_taken.grid(column=0, row=1, sticky='ew')

frm_buildings.grid(column=0, row=0, rowspan=3, sticky='ew')
frm_resources.grid(column=1, row=0, sticky='ew')
frm_next_turn.grid(column=1, row=1, sticky='ew')
btn_open_menu.grid(column=1, row=2, sticky='ew')
frm_trades_quests.grid(column=2, row=0, rowspan=3, sticky='nsew')

# menu
# lbl_save_code.grid(column=0, row=0, columnspan=2, sticky='ew')

# ent_save_code.grid(column=0, row=1, columnspan=2, sticky='ew')
btn_save_code_write.grid(column=0, row=0, sticky='ew', padx=(0, 5))
btn_save_code_read.grid(column=1, row=0, sticky='ew', padx=(5, 0))

btn_open_tutorial.grid(column=0, row=0, sticky='ew')
btn_open_whats_new.grid(column=0, row=1, sticky='ew')
frm_save_load.grid(column=0, row=2, sticky='ew')
btn_open_credits.grid(column=0, row=3, sticky='ew')
btn_close_menu.grid(column=0, row=4, sticky='ew')
btn_quit_game.grid(column=0, row=5, sticky='ew')

# tutorial
msg_tutorial.grid(column=0, row=0, columnspan=2, sticky='nsew')

btn_prev_tutorial.grid(column=0, row=1, sticky='sew')
btn_next_tutorial.grid(column=1, row=1, sticky='sew')

btn_close_tutorial.grid(column=0, row=2, columnspan=2, sticky='sew')

# whats new
msg_whats_new.grid(column=0, row=0, sticky='ew')
btn_close_whats_new.grid(column=0, row=1, sticky='nsew')

# credits
msg_credits.grid(column=0, row=0, sticky='ew')
btn_close_credits.grid(column=0, row=1, sticky='nsew')

create_trade_1()
create_trade_2()
create_trade_3()

create_quest_1()
create_quest_2()
create_quest_3()

update()
messagebox.showinfo('Played Before?', 'If you have not played before, press \'Menu\', then press \'Tutorial\'')
window.mainloop()