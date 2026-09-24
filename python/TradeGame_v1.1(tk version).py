import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox
from random import randint
import os

if os.name == "nt":
    from ctypes import windll
    try:
        windll.shcore.SetProcessDpiAwareness(1)
        
    except Exception:
        windll.user32.SetProcessDPIAware()

can_trade_build_bg="#F0F0F0"
cant_trade_build_bg="#D0D0D0"
can_trade_build_fg="#000000"
cant_trade_build_fg="#505050"

lst_save_code=[]
str_save_code=""

tutorial_current_page=0
tutorial_pages=[
    "Welcome to TradeGame! I bet you couldn't guess it by the name, but this is a game about trading.",
    "Your first goal will be getting a sawmill, however you do not have enough wood.",
    "Find a trade where the export is about 5 stone, and the import is wood. If you don't see one, keep pressing next turn until you find one.",
    "If you don't have enough stone, try to trade a small amount of wood away for stone. Otherwise, click next.",
    "Now that you have the materials, the 'Build Sawmill' button should no longer be greyed-out. Press it to build your first sawmill.",
    "Now that you have built a sawmill, you have infinite wood. You can use this to trade for other resources to build more things.",
    "Press 'Close Tutorial' to exit the tutorial."
]

# Default
resources={
    "wood":45,
    "stone":30,
    "iron":0,
    "gold":0,
    "treasure":0
}

resource_values={
    "wood":1,
    "stone":2,
    "iron":4,
    "gold":10,
    "treasure":20
}

buildings={
    "sawmill":0,
    "stone_mine":0,
    "iron_mine":0,
    "gold_mine":0,
    "storehouse":0
}

# DEV Save
# 1000/432500/2797500/365000/100000/1000/1000/1000/1000/9999

export_blacklist=[]

import_blacklist=[]

trade_1={
    "export":"",
    "export_amount":0,
    "import":"",
    "import_amount":0
}

trade_2={
    "export":"",
    "export_amount":0,
    "import":"",
    "import_amount":0
}

trade_3={
    "export":"",
    "export_amount":0,
    "import":"",
    "import_amount":0
}

turns_taken=0

def save_code_write():
    global lst_save_code
    global str_save_code
    global turns_taken

    lst_save_code.clear()

    # v1.0
    lst_save_code.append(f"{turns_taken}/")

    lst_save_code.append(f"{resources["wood"]}/")
    lst_save_code.append(f"{resources["stone"]}/")
    lst_save_code.append(f"{resources["iron"]}/")
    lst_save_code.append(f"{resources["gold"]}/")

    lst_save_code.append(f"{buildings["sawmill"]}/")
    lst_save_code.append(f"{buildings["stone_mine"]}/")
    lst_save_code.append(f"{buildings["iron_mine"]}/")
    lst_save_code.append(f"{buildings["gold_mine"]}/")

    # v1.1
    lst_save_code.append(f"{buildings["storehouse"]}/")

    lst_save_code.append(f"{resources["treasure"]}")

    str_save_code="".join(lst_save_code)
    ent_save_code.delete(0, tk.END)
    ent_save_code.insert(tk.END, str_save_code)

def save_code_read():
    choice_load=messagebox.askquestion("Load Save?", "All unsaved progress will be overwritten.\nAre you sure you want to load?")
    if choice_load=="yes":
        global lst_save_code
        global str_save_code
        global turns_taken

        str_save_code=ent_save_code.get()

        lst_save_code.clear()
        lst_save_code=str_save_code.split("/")

        # v1.0
        turns_taken=int(lst_save_code[0])
        
        resources["wood"]=int(lst_save_code[1])
        resources["stone"]=int(lst_save_code[2])
        resources["iron"]=int(lst_save_code[3])
        resources["gold"]=int(lst_save_code[4])

        buildings["sawmill"]=int(lst_save_code[5])
        buildings["stone_mine"]=int(lst_save_code[6])
        buildings["iron_mine"]=int(lst_save_code[7])
        buildings["gold_mine"]=int(lst_save_code[8])

        #v1.1
        buildings["storehouse"]=int(lst_save_code[9])

        resources["treasure"]=int(lst_save_code[10])

        create_trade_1()
        create_trade_2()
        create_trade_3()

        update()
    hide_menu()

def create_trade_1():
    resources_keys=list(resources.keys())
    while True:
        while True:
            trade_1["export"]=resources_keys[randint(0, len(resources_keys)-1)]
            if resources[trade_1["export"]]>0 and trade_1["export"] not in export_blacklist:
                break
            else:
                continue
        
        while True:
            trade_1["import"]=resources_keys[randint(0, len(resources_keys)-1)]
            if trade_1["import"] not in import_blacklist:
                break
            else:
                continue
        
        if trade_1["export"]==trade_1["import"]:
            continue
        else:
            break
    
    trade_1["export_amount"]=randint(1, resources[trade_1["export"]]+5)

    trade_1["import_amount"]=int(round(trade_1["export_amount"]*(resource_values[trade_1["export"]]/resource_values[trade_1["import"]]), 0))

    while True:
        trade_1["import_amount"]+=randint(-5, 5)
        if trade_1["import_amount"]>0:
            break

def do_trade_1():
    if resources[trade_1["export"]]>=trade_1["export_amount"]:
        resources[trade_1["export"]]-=trade_1["export_amount"]
        resources[trade_1["import"]]+=trade_1["import_amount"]
        create_trade_1()
    update()

def create_trade_2():
    resources_keys=list(resources.keys())
    while True:
        while True:
            trade_2["export"]=resources_keys[randint(0, len(resources_keys)-1)]
            if resources[trade_2["export"]]>0 and trade_2["export"] not in export_blacklist:
                break
            else:
                continue
        
        while True:
            trade_2["import"]=resources_keys[randint(0, len(resources_keys)-1)]
            if trade_2["import"] not in import_blacklist:
                break
            else:
                continue
        
        if trade_2["export"]==trade_2["import"]:
            continue
        else:
            break
    
    trade_2["export_amount"]=randint(1, resources[trade_2["export"]]+5)

    trade_2["import_amount"]=int(round(trade_2["export_amount"]*(resource_values[trade_2["export"]]/resource_values[trade_2["import"]]), 0))

    while True:
        trade_2["import_amount"]+=randint(-5, 5)
        if trade_2["import_amount"]>0:
            break

def do_trade_2():
    if resources[trade_2["export"]]>=trade_2["export_amount"]:
        resources[trade_2["export"]]-=trade_2["export_amount"]
        resources[trade_2["import"]]+=trade_2["import_amount"]
        create_trade_2()
    update()

def create_trade_3():
    resources_keys=list(resources.keys())
    while True:
        while True:
            trade_3["export"]=resources_keys[randint(0, len(resources_keys)-1)]
            if resources[trade_3["export"]]>0 and trade_3["export"] not in export_blacklist:
                break
            else:
                continue
        
        while True:
            trade_3["import"]=resources_keys[randint(0, len(resources_keys)-1)]
            if trade_3["import"] not in import_blacklist:
                break
            else:
                continue
        
        if trade_3["export"]==trade_3["import"]:
            continue
        else:
            break
    
    trade_3["export_amount"]=randint(1, resources[trade_3["export"]]+5)

    trade_3["import_amount"]=int(round(trade_3["export_amount"]*(resource_values[trade_3["export"]]/resource_values[trade_3["import"]]), 0))

    while True:
        trade_3["import_amount"]+=randint(-5, 5)
        if trade_3["import_amount"]>0:
            break

def do_trade_3():
    if resources[trade_3["export"]]>=trade_3["export_amount"]:
        resources[trade_3["export"]]-=trade_3["export_amount"]
        resources[trade_3["import"]]+=trade_3["import_amount"]
        create_trade_3()
    update()

def update():
    msg_tutorial.configure(text=tutorial_pages[tutorial_current_page])

    if resources["wood"]>(100*buildings["storehouse"])+100:
        resources["wood"]=(100*buildings["storehouse"])+100

    if resources["stone"]>(100*buildings["storehouse"])+100:
        resources["stone"]=(100*buildings["storehouse"])+100
    
    if resources["iron"]>(100*buildings["storehouse"])+100:
        resources["iron"]=(100*buildings["storehouse"])+100
    
    if resources["gold"]>(100*buildings["storehouse"])+100:
        resources["gold"]=(100*buildings["storehouse"])+100
    
    if resources["treasure"]>(100*buildings["storehouse"])+100:
        resources["treasure"]=(100*buildings["storehouse"])+100

    lbl_wood_amount.configure(text=f"Wood: {resources["wood"]}/{(100*buildings["storehouse"])+100}")
    lbl_stone_amount.configure(text=f"Stone: {resources["stone"]}/{(100*buildings["storehouse"])+100}")
    lbl_iron_amount.configure(text=f"Iron: {resources["iron"]}/{(100*buildings["storehouse"])+100}")
    lbl_gold_amount.configure(text=f"Gold: {resources["gold"]}/{(100*buildings["storehouse"])+100}")
    lbl_treasure_amount.configure(text=f"Treasure: {resources["treasure"]}/{(100*buildings["storehouse"])+100}")

    lbl_sawmill_amount.configure(text=f"Sawmills (produces 5 wood per turn): {buildings["sawmill"]}")
    lbl_stone_mine_amount.configure(text=f"Stone Mines (produces 10 stone per turn): {buildings["stone_mine"]}")
    lbl_iron_mine_amount.configure(text=f"Iron Mines (produces 5 iron and 10 stone per turn): {buildings["iron_mine"]}")
    lbl_gold_mine_amount.configure(text=f"Gold Mines (produces 1 gold and 10 stone per turn): {buildings["gold_mine"]}")
    lbl_storehouse_amount.configure(text=f"Storehouses (allows you to hold 100 more of each resource): {buildings["storehouse"]}")

    btn_trade_1.configure(text=f"Export: {trade_1['export_amount']} {trade_1['export']}, Import: {trade_1["import_amount"]} {trade_1['import']}")
    btn_trade_2.configure(text=f"Export: {trade_2['export_amount']} {trade_2['export']}, Import: {trade_2["import_amount"]} {trade_2['import']}")
    btn_trade_3.configure(text=f"Export: {trade_3['export_amount']} {trade_3['export']}, Import: {trade_3["import_amount"]} {trade_3['import']}")

    #build button colours
    if resources["wood"]>=50 and resources["stone"]>=25:
        btn_build_sawmill.configure(bg=can_trade_build_bg, fg=can_trade_build_fg)
    else:
        btn_build_sawmill.configure(bg=cant_trade_build_bg, fg=cant_trade_build_fg)
    
    if resources["stone"]>=50 and resources["wood"]>=25:
        btn_build_stone_mine.configure(bg=can_trade_build_bg, fg=can_trade_build_fg)
    else:
        btn_build_stone_mine.configure(bg=cant_trade_build_bg, fg=cant_trade_build_fg)
    
    if resources["stone"]>=100 and resources["iron"]>=50:
        btn_build_iron_mine.configure(bg=can_trade_build_bg, fg=can_trade_build_fg)
    else:
        btn_build_iron_mine.configure(bg=cant_trade_build_bg, fg=cant_trade_build_fg)
    
    if resources["iron"]>=100 and resources["stone"]>=50:
        btn_build_gold_mine.configure(bg=can_trade_build_bg, fg=can_trade_build_fg)
    else:
        btn_build_gold_mine.configure(bg=cant_trade_build_bg, fg=cant_trade_build_fg)
    
    if resources["wood"]>=100 and resources["iron"]>=25:
        btn_build_storehouse.configure(bg=can_trade_build_bg, fg=can_trade_build_fg)
    else:
        btn_build_storehouse.configure(bg=cant_trade_build_bg, fg=cant_trade_build_fg)

    #trade button colours
    if trade_1["export_amount"]<=resources[trade_1["export"]]:
        btn_trade_1.configure(bg=can_trade_build_bg, fg=can_trade_build_fg)
    else:
        btn_trade_1.configure(bg=cant_trade_build_bg, fg=cant_trade_build_fg)
    
    if trade_2["export_amount"]<=resources[trade_2["export"]]:
        btn_trade_2.configure(bg=can_trade_build_bg, fg=can_trade_build_fg)
    else:
        btn_trade_2.configure(bg=cant_trade_build_bg, fg=cant_trade_build_fg)
    
    if trade_3["export_amount"]<=resources[trade_3["export"]]:
        btn_trade_3.configure(bg=can_trade_build_bg, fg=can_trade_build_fg)
    else:
        btn_trade_3.configure(bg=cant_trade_build_bg, fg=cant_trade_build_fg)

    lbl_turns_taken.configure(text=f"Turns Taken: {turns_taken}")

def next_turn():
    global turns_taken

    turns_taken+=1

    for i in range(buildings["sawmill"]):
        resources["wood"]+=5
    
    for i in range(buildings["stone_mine"]):
        resources["stone"]+=10

    for i in range(buildings["iron_mine"]):
        resources["iron"]+=5
        resources["stone"]+=10

    for i in range(buildings["gold_mine"]):
        resources["gold"]+=1
        resources["stone"]+=10
    
    create_trade_1()
    create_trade_2()
    create_trade_3()

    update()

def build_sawmill():
    if resources["wood"]>=50 and resources["stone"]>=25:
        resources["wood"]-=50
        resources["stone"]-=25
        buildings["sawmill"]+=1
    update()

def build_stone_mine():
    if resources["stone"]>=50 and resources["wood"]>=25:
        resources["stone"]-=50
        resources["wood"]-=25
        buildings["stone_mine"]+=1
    update()

def build_iron_mine():
    if resources["stone"]>=100 and resources["iron"]>=50:
        resources["stone"]-=100
        resources["iron"]-=50
        buildings["iron_mine"]+=1
    update()

def build_gold_mine():
    if resources["iron"]>=100 and resources["stone"]>=50:
        resources["iron"]-=100
        resources["stone"]-=50
        buildings["gold_mine"]+=1
    update()

def build_storehouse():
    if resources["wood"]>=100 and resources["iron"]>=25:
        resources["wood"]-=100
        resources["iron"]-=25
        buildings["storehouse"]+=1
    update()

def show_menu():
    tlv_menu.deiconify()

def hide_menu():
    tlv_menu.withdraw()

def show_tutorial():
    tlv_tutorial.deiconify()
    hide_menu()

def hide_tutorial():
    tlv_tutorial.withdraw()

def show_whats_new():
    tlv_whats_new.deiconify()
    hide_menu()

def hide_whats_new():
    tlv_whats_new.withdraw()

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
    choice_quit=messagebox.askquestion("Quit Game?", "All unsaved progress will be lost.\nAre you sure you want to quit?")
    if choice_quit=="yes":
        window.destroy()

def resize_msg_tutorial(event):
    if event.widget == tlv_tutorial:
        msg_tutorial.config(width=event.width)

def resize_msg_whats_new(event):
    if event.widget == tlv_whats_new:
        msg_whats_new.config(width=event.width)

window=tk.Tk()
window.title("TradeGame")

tlv_menu=tk.Toplevel(window)
tlv_menu.title("Menu - TradeGame")
tlv_menu.withdraw()
tlv_menu.protocol("WM_DELETE_WINDOW", hide_menu)

tlv_tutorial=tk.Toplevel(window)
tlv_tutorial.title("Tutorial - TradeGame")
tlv_tutorial.withdraw()
tlv_tutorial.protocol("WM_DELETE_WINDOW", hide_tutorial)
tlv_tutorial.bind('<Configure>', resize_msg_tutorial)

tlv_whats_new=tk.Toplevel(window)
tlv_whats_new.title("What's New? - TradeGame")
tlv_whats_new.withdraw()
tlv_whats_new.protocol("WM_DELETE_WINDOW", hide_whats_new)
tlv_whats_new.bind('<Configure>', resize_msg_whats_new)


fnt_title=tkFont.Font(size=12, weight="bold")
fnt_main=tkFont.Font(size=12)

window.resizable(width=True, height=False)
tlv_menu.resizable(width=True, height=False)
tlv_tutorial.resizable(width=True, height=False)
tlv_whats_new.resizable(width=True, height=False)

window.columnconfigure([0,1,2], weight=1)
window.rowconfigure([0,1,2], weight=1)

tlv_menu.columnconfigure(0, weight=1)
tlv_menu.rowconfigure([0,1,2,3,4], weight=1)

tlv_tutorial.columnconfigure([0,1], weight=1)
tlv_tutorial.rowconfigure([0,1,2], weight=1)

tlv_whats_new.columnconfigure(0, weight=1)
tlv_whats_new.rowconfigure([0,1], weight=1)

frm_buildings=tk.Frame(window, padx=10, pady=10)
frm_resources=tk.Frame(window, padx=10, pady=10)
frm_trades=tk.Frame(window, padx=10, pady=10)
frm_next_turn=tk.Frame(window, padx=10, pady=10)
frm_save_load=tk.Frame(tlv_menu, padx=10, pady=10)

frm_buildings.columnconfigure(0, weight=1)
frm_buildings.rowconfigure([0,1,2,3,4,5,6,7,8,9,10], weight=1)

frm_resources.columnconfigure(0, weight=1)
frm_resources.rowconfigure([0,1,2,3,4,5], weight=1)

frm_trades.columnconfigure(0, weight=1)
frm_trades.rowconfigure([0,1,2,3], weight=1)

frm_next_turn.columnconfigure(0, weight=1)
frm_next_turn.rowconfigure([0,1], weight=1)

frm_save_load.columnconfigure([0,1], weight=1)
frm_save_load.rowconfigure([0,1,2], weight=1)

# main window
lbl_buildings=tk.Label(frm_buildings, text="Buildings:", font=fnt_title)

btn_build_sawmill=tk.Button(frm_buildings, text="Build Sawmill (Cost: 50 wood, 25 stone)", command=build_sawmill, font=fnt_main)
btn_build_stone_mine=tk.Button(frm_buildings, text="Build Stone Mine (Cost: 50 stone, 25 wood)", command=build_stone_mine, font=fnt_main)
btn_build_iron_mine=tk.Button(frm_buildings, text="Build Iron Mine (Cost: 100 stone, 50 iron)", command=build_iron_mine, font=fnt_main)
btn_build_gold_mine=tk.Button(frm_buildings, text="Build Gold Mine (Cost: 100 iron, 50 stone)", command=build_gold_mine, font=fnt_main)
btn_build_storehouse=tk.Button(frm_buildings, text="Build Storehouse (Cost: 100 wood, 25 iron)", command=build_storehouse, font=fnt_main)

lbl_sawmill_amount=tk.Label(frm_buildings, font=fnt_main)
lbl_stone_mine_amount=tk.Label(frm_buildings, font=fnt_main)
lbl_iron_mine_amount=tk.Label(frm_buildings, font=fnt_main)
lbl_gold_mine_amount=tk.Label(frm_buildings, font=fnt_main)
lbl_storehouse_amount=tk.Label(frm_buildings, font=fnt_main)

lbl_resources=tk.Label(frm_resources, text="Resources:", font=fnt_title)

lbl_wood_amount=tk.Label(frm_resources, font=fnt_main)
lbl_stone_amount=tk.Label(frm_resources, font=fnt_main)
lbl_iron_amount=tk.Label(frm_resources, font=fnt_main)
lbl_gold_amount=tk.Label(frm_resources, font=fnt_main)
lbl_treasure_amount=tk.Label(frm_resources, font=fnt_main)

lbl_trades=tk.Label(frm_trades, text="Trades:", font=fnt_title)

btn_trade_1=tk.Button(frm_trades, command=do_trade_1, font=fnt_main)
btn_trade_2=tk.Button(frm_trades, command=do_trade_2, font=fnt_main)
btn_trade_3=tk.Button(frm_trades, command=do_trade_3, font=fnt_main)

btn_next_turn=tk.Button(frm_next_turn, text="Next Turn", command=next_turn, font=fnt_title)
lbl_turns_taken=tk.Label(frm_next_turn, font=fnt_main)

btn_open_menu=tk.Button(window, text="Menu", command=show_menu, font=fnt_title)

# menu
btn_open_tutorial=tk.Button(tlv_menu, text="Tutorial", command=show_tutorial, font=fnt_title)

btn_open_whats_new=tk.Button(tlv_menu, text="What's New?", command=show_whats_new, font=fnt_title)

lbl_save_code=tk.Label(frm_save_load, text="Save Code:", font=fnt_title)
ent_save_code=tk.Entry(frm_save_load, font=fnt_main)
btn_save_code_write=tk.Button(frm_save_load, text="Save", command=save_code_write, font=fnt_main)
btn_save_code_read=tk.Button(frm_save_load, text="Load", command=save_code_read, font=fnt_main)

btn_close_menu=tk.Button(tlv_menu, text="Close Menu", command=hide_menu, font=fnt_title)
btn_quit_game=tk.Button(tlv_menu, text="Quit Game", command=quit_game, font=fnt_title)

# tutorial
msg_tutorial=tk.Message(tlv_tutorial, font=fnt_main)

btn_prev_tutorial=tk.Button(tlv_tutorial, text="Previous", font=fnt_title, command=prev_tutorial_page)
btn_next_tutorial=tk.Button(tlv_tutorial, text="Next", font=fnt_title, command=next_tutorial_page)

btn_close_tutorial=tk.Button(tlv_tutorial, text="Close Tutorial", command=hide_tutorial, font=fnt_title)

# whats new
msg_whats_new=tk.Message(tlv_whats_new, text="TradeGame v1.1\n\nAdded:\nStorehouses (buildings[storehouse])\nTreasure (resources[treasure])\nImport/export blacklist (import_blacklist)(export_blacklist)\nMenu (tlv_menu)\nTutorial (tlv_tutorial)\nWhat's New? (tlv_whats_new)\n\nChanged:\nMoved save/load to menu\nReworked trade system & resource values (create_trade_1(), create_trade_2(), create_trade_3())(resource_values)\n\nRemoved:\nNothing\n\nFixed:\nNothing", font=fnt_main)

btn_close_whats_new=tk.Button(tlv_whats_new, text="Close What's New", font=fnt_title, command=hide_whats_new)

# main window
lbl_buildings.grid(column=0, row=0, sticky="ew")

btn_build_sawmill.grid(column=0, row=1, sticky="ew")
btn_build_stone_mine.grid(column=0, row=2, sticky="ew")
btn_build_iron_mine.grid(column=0, row=3, sticky="ew")
btn_build_gold_mine.grid(column=0, row=4, sticky="ew")
btn_build_storehouse.grid(column=0, row=5, sticky="ew")

lbl_sawmill_amount.grid(column=0, row=6, sticky="ew")
lbl_stone_mine_amount.grid(column=0, row=7, sticky="ew")
lbl_iron_mine_amount.grid(column=0, row=8, sticky="ew")
lbl_gold_mine_amount.grid(column=0, row=9, sticky="ew")
lbl_storehouse_amount.grid(column=0, row=10, sticky="ew")

lbl_resources.grid(column=0, row=0, sticky="ew")

lbl_wood_amount.grid(column=0, row=1, sticky="ew")
lbl_stone_amount.grid(column=0, row=2, sticky="ew")
lbl_iron_amount.grid(column=0, row=3, sticky="ew")
lbl_gold_amount.grid(column=0, row=4, sticky="ew")
lbl_treasure_amount.grid(column=0, row=5, sticky="ew")

lbl_trades.grid(column=0, row=0, sticky="nsew")

btn_trade_1.grid(column=0, row=1, sticky="nsew")
btn_trade_2.grid(column=0, row=2, sticky="nsew")
btn_trade_3.grid(column=0, row=3, sticky="nsew")

btn_next_turn.grid(column=0, row=0, sticky="ew")
lbl_turns_taken.grid(column=0, row=1, sticky="ew")

frm_buildings.grid(column=0, row=0, rowspan=3, sticky="ew")
frm_resources.grid(column=1, row=0, sticky="ew")
frm_next_turn.grid(column=1, row=1, sticky="ew")
btn_open_menu.grid(column=1, row=2, sticky="ew")
frm_trades.grid(column=2, row=0, rowspan=3, sticky="nsew")

# menu
lbl_save_code.grid(column=0, row=0, columnspan=2, sticky="ew")

ent_save_code.grid(column=0, row=1, columnspan=2, sticky="ew")
btn_save_code_write.grid(column=0, row=2, sticky="ew")
btn_save_code_read.grid(column=1, row=2, sticky="ew")

btn_open_tutorial.grid(column=0, row=0, sticky="ew")
btn_open_whats_new.grid(column=0, row=1, sticky="ew")
frm_save_load.grid(column=0, row=2, sticky="ew")
btn_close_menu.grid(column=0, row=3, sticky="ew")
btn_quit_game.grid(column=0, row=4, sticky="ew")

# tutorial
msg_tutorial.grid(column=0, row=0, columnspan=2, sticky="nsew")

btn_prev_tutorial.grid(column=0, row=1, sticky="sew")
btn_next_tutorial.grid(column=1, row=1, sticky="sew")

btn_close_tutorial.grid(column=0, row=2, columnspan=2, sticky="sew")

# whats new
msg_whats_new.grid(column=0, row=0, sticky="ew")
btn_close_whats_new.grid(column=0, row=1, sticky="nsew")

create_trade_1()
create_trade_2()
create_trade_3()
update()
messagebox.showinfo("Played Before?", "If you have not played before, press 'Menu', then press 'Tutorial'")
window.mainloop()