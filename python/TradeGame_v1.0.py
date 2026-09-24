import tkinter as tk
import tkinter.font as tkFont
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

# Default
resources={
    "wood":45,
    "stone":25,
    "iron":0,
    "gold":0
}

buildings={
    "sawmill":0,
    "stone_mine":0,
    "iron_mine":0,
    "gold_mine":0,
    "storehouse":0
}

# DEV Save
# 1000/432500/2797500/365000/100000/1000/1000/1000/1000

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

    lst_save_code.append(f"{turns_taken}/")

    lst_save_code.append(f"{resources["wood"]}/")
    lst_save_code.append(f"{resources["stone"]}/")
    lst_save_code.append(f"{resources["iron"]}/")
    lst_save_code.append(f"{resources["gold"]}/")

    lst_save_code.append(f"{buildings["sawmill"]}/")
    lst_save_code.append(f"{buildings["stone_mine"]}/")
    lst_save_code.append(f"{buildings["iron_mine"]}/")
    lst_save_code.append(str(buildings["gold_mine"]))

    str_save_code="".join(lst_save_code)
    ent_save_code.delete(0, tk.END)
    ent_save_code.insert(tk.END, str_save_code)

def save_code_read():
    global lst_save_code
    global str_save_code
    global turns_taken

    str_save_code=ent_save_code.get()

    lst_save_code.clear()
    lst_save_code=str_save_code.split("/")

    turns_taken=int(lst_save_code[0])
    
    resources["wood"]=int(lst_save_code[1])
    resources["stone"]=int(lst_save_code[2])
    resources["iron"]=int(lst_save_code[3])
    resources["gold"]=int(lst_save_code[4])

    buildings["sawmill"]=int(lst_save_code[5])
    buildings["stone_mine"]=int(lst_save_code[6])
    buildings["iron_mine"]=int(lst_save_code[7])
    buildings["gold_mine"]=int(lst_save_code[8])

    create_trade_1()
    create_trade_2()
    create_trade_3()

    update()

def create_trade_1():
    while True:
        while True:
            random=randint(1, 4)
            if random==1:
                if resources["wood"]>0:
                    trade_1["export"]="wood"
                    break
            
            elif random==2:
                if resources["stone"]>0:
                    trade_1["export"]="stone"
                    break
                
            elif random==3:
                if resources["iron"]>0:
                    trade_1["export"]="iron"
                    break

            elif random==4:
                if resources["gold"]>0:
                    trade_1["export"]="gold"
                    break
        
        while True:
            random=randint(1, 4)
            if random==1:
                trade_1["import"]="wood"
                break
            
            elif random==2:
                trade_1["import"]="stone"
                break
            
            elif random==3:
                trade_1["import"]="iron"
                break
            
            elif random==4:
                trade_1["import"]="gold"
                break
        
        if trade_1["export"]==trade_1["import"]:
            continue

        else:
            break
    
    trade_1["export_amount"]=randint(1, resources[trade_1["export"]]+5)

    #Wood Convert
    if trade_1["export"]=="wood":
        if trade_1["import"]=="stone":
            trade_1["import_amount"]=trade_1["export_amount"]*2
        
        if trade_1["import"]=="iron":
            trade_1["import_amount"]=trade_1["export_amount"]
        
        if trade_1["import"]=="gold":
            trade_1["import_amount"]=int(round(trade_1["export_amount"]*0.2, 0))
    
    #Stone Convert
    if trade_1["export"]=="stone":
        if trade_1["import"]=="wood":
            trade_1["import_amount"]=int(round(trade_1["export_amount"]*0.5, 0))
        
        if trade_1["import"]=="iron":
            trade_1["import_amount"]=int(round(trade_1["export_amount"]*0.5, 0))
        
        if trade_1["import"]=="gold":
            trade_1["import_amount"]=int(round(trade_1["export_amount"]*0.1, 0))
    
    #Iron Convert
    if trade_1["export"]=="iron":
        if trade_1["import"]=="wood":
            trade_1["import_amount"]=trade_1["export_amount"]
        
        if trade_1["import"]=="stone":
            trade_1["import_amount"]=trade_1["export_amount"]*2
        
        if trade_1["import"]=="gold":
            trade_1["import_amount"]=int(round(trade_1["export_amount"]*0.2, 0))
    
    #Gold Convert
    if trade_1["export"]=="gold":
        if trade_1["import"]=="wood":
            trade_1["import_amount"]=trade_1["export_amount"]*5
        
        if trade_1["import"]=="stone":
            trade_1["import_amount"]=trade_1["export_amount"]*10
        
        if trade_1["import"]=="iron":
            trade_1["import_amount"]=trade_1["export_amount"]*5
    
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
    while True:
        while True:
            random=randint(1, 4)
            if random==1:
                if resources["wood"]>0:
                    trade_2["export"]="wood"
                    break
            
            elif random==2:
                if resources["stone"]>0:
                    trade_2["export"]="stone"
                    break
                
            elif random==3:
                if resources["iron"]>0:
                    trade_2["export"]="iron"
                    break

            elif random==4:
                if resources["gold"]>0:
                    trade_2["export"]="gold"
                    break
        
        while True:
            random=randint(1, 4)
            if random==1:
                trade_2["import"]="wood"
                break
            
            elif random==2:
                trade_2["import"]="stone"
                break
            
            elif random==3:
                trade_2["import"]="iron"
                break
            
            elif random==4:
                trade_2["import"]="gold"
                break
        
        if trade_2["export"]==trade_2["import"]:
            continue

        else:
            break
    
    trade_2["export_amount"]=randint(1, resources[trade_2["export"]]+5)

    #Wood Convert
    if trade_2["export"]=="wood":
        if trade_2["import"]=="stone":
            trade_2["import_amount"]=trade_2["export_amount"]*2
        
        if trade_2["import"]=="iron":
            trade_2["import_amount"]=trade_2["export_amount"]
        
        if trade_2["import"]=="gold":
            trade_2["import_amount"]=int(round(trade_2["export_amount"]*0.2, 0))
    
    #Stone Convert
    if trade_2["export"]=="stone":
        if trade_2["import"]=="wood":
            trade_2["import_amount"]=int(round(trade_2["export_amount"]*0.5, 0))
        
        if trade_2["import"]=="iron":
            trade_2["import_amount"]=int(round(trade_2["export_amount"]*0.5, 0))
        
        if trade_2["import"]=="gold":
            trade_2["import_amount"]=int(round(trade_2["export_amount"]*0.1, 0))
    
    #Iron Convert
    if trade_2["export"]=="iron":
        if trade_2["import"]=="wood":
            trade_2["import_amount"]=trade_2["export_amount"]
        
        if trade_2["import"]=="stone":
            trade_2["import_amount"]=trade_2["export_amount"]*2
        
        if trade_2["import"]=="gold":
            trade_2["import_amount"]=int(round(trade_2["export_amount"]*0.2,))
    
    #Gold Convert
    if trade_2["export"]=="gold":
        if trade_2["import"]=="wood":
            trade_2["import_amount"]=trade_2["export_amount"]*5
        
        if trade_2["import"]=="stone":
            trade_2["import_amount"]=trade_2["export_amount"]*10
        
        if trade_2["import"]=="iron":
            trade_2["import_amount"]=trade_2["export_amount"]*5
    
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
    while True:
        while True:
            random=randint(1, 4)
            if random==1:
                if resources["wood"]>0:
                    trade_3["export"]="wood"
                    break
            
            elif random==2:
                if resources["stone"]>0:
                    trade_3["export"]="stone"
                    break
                
            elif random==3:
                if resources["iron"]>0:
                    trade_3["export"]="iron"
                    break

            elif random==4:
                if resources["gold"]>0:
                    trade_3["export"]="gold"
                    break
        
        while True:
            random=randint(1, 4)
            if random==1:
                trade_3["import"]="wood"
                break
            
            elif random==2:
                trade_3["import"]="stone"
                break
            
            elif random==3:
                trade_3["import"]="iron"
                break
            
            elif random==4:
                trade_3["import"]="gold"
                break
        
        if trade_3["export"]==trade_3["import"]:
            continue

        else:
            break
    
    trade_3["export_amount"]=randint(1, resources[trade_3["export"]]+5)

    #Wood Convert
    if trade_3["export"]=="wood":
        if trade_3["import"]=="stone":
            trade_3["import_amount"]=trade_3["export_amount"]*2
        
        if trade_3["import"]=="iron":
            trade_3["import_amount"]=trade_3["export_amount"]
        
        if trade_3["import"]=="gold":
            trade_3["import_amount"]=int(round(trade_3["export_amount"]*0.2, 0))
    
    #Stone Convert
    if trade_3["export"]=="stone":
        if trade_3["import"]=="wood":
            trade_3["import_amount"]=int(round(trade_3["export_amount"]*0.5, 0))
        
        if trade_3["import"]=="iron":
            trade_3["import_amount"]=int(round(trade_3["export_amount"]*0.5, 0))
        
        if trade_3["import"]=="gold":
            trade_3["import_amount"]=int(round(trade_3["export_amount"]*0.1, 0))
    
    #Iron Convert
    if trade_3["export"]=="iron":
        if trade_3["import"]=="wood":
            trade_3["import_amount"]=trade_3["export_amount"]
        
        if trade_3["import"]=="stone":
            trade_3["import_amount"]=trade_3["export_amount"]*2
        
        if trade_3["import"]=="gold":
            trade_3["import_amount"]=int(round(trade_3["export_amount"]*0.2,))
    
    #Gold Convert
    if trade_3["export"]=="gold":
        if trade_3["import"]=="wood":
            trade_3["import_amount"]=trade_3["export_amount"]*5
        
        if trade_3["import"]=="stone":
            trade_3["import_amount"]=trade_3["export_amount"]*10
        
        if trade_3["import"]=="iron":
            trade_3["import_amount"]=trade_3["export_amount"]*5
    
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
    lbl_wood_amount.configure(text=f"Wood: {resources["wood"]}/{(100*buildings["storehouse"])+100}")
    lbl_stone_amount.configure(text=f"Stone: {resources["stone"]}")
    lbl_iron_amount.configure(text=f"Iron: {resources["iron"]}")
    lbl_gold_amount.configure(text=f"Gold: {resources["gold"]}")

    lbl_sawmill_amount.configure(text=f"Sawmills (produces 5 wood per turn): {buildings["sawmill"]}")
    lbl_stone_mine_amount.configure(text=f"Stone Mines (produces 10 stone per turn): {buildings["stone_mine"]}")
    lbl_iron_mine_amount.configure(text=f"Iron Mines (produces 5 iron and 10 stone per turn): {buildings["iron_mine"]}")
    lbl_gold_mine_amount.configure(text=f"Gold Mines (produces 1 gold and 10 stone per turn): {buildings["gold_mine"]}")

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

window=tk.Tk()
window.title("TradeGame")

fnt_title=tkFont.Font(size=12, weight="bold")
fnt_main=tkFont.Font(size=12)

window.resizable(width=True, height=False)

window.columnconfigure([0,1,2], weight=1)
window.rowconfigure([0,1,2], weight=1)

frm_buildings=tk.Frame(window, padx=10, pady=10)
frm_resources=tk.Frame(window, padx=10, pady=10)
frm_trades=tk.Frame(window, padx=10, pady=10)
frm_next_turn=tk.Frame(window, padx=10, pady=10)
frm_save_load=tk.Frame(window, padx=10, pady=10)

frm_buildings.columnconfigure(0, weight=1)
frm_buildings.rowconfigure([0,1,2,3,4,5,6,7,8], weight=1)

frm_resources.columnconfigure(0, weight=1)
frm_resources.rowconfigure([0,1,2,3,4], weight=1)

frm_trades.columnconfigure(0, weight=1)
frm_trades.rowconfigure([0,1,2,3], weight=1)

frm_next_turn.columnconfigure(0, weight=1)
frm_next_turn.rowconfigure([0,1], weight=1)

frm_save_load.columnconfigure([0,1], weight=1)
frm_save_load.rowconfigure([0,1,2], weight=1)

lbl_buildings=tk.Label(frm_buildings, text="Buildings:", font=fnt_title)

btn_build_sawmill=tk.Button(frm_buildings, text="Build Sawmill (Cost: 50 wood, 25 stone)", command=build_sawmill, font=fnt_main)
btn_build_stone_mine=tk.Button(frm_buildings, text="Build Stone Mine (Cost: 50 stone, 25 wood)", command=build_stone_mine, font=fnt_main)
btn_build_iron_mine=tk.Button(frm_buildings, text="Build Iron Mine (Cost: 100 stone, 50 iron)", command=build_iron_mine, font=fnt_main)
btn_build_gold_mine=tk.Button(frm_buildings, text="Build Gold Mine (Cost: 100 iron, 50 stone)", command=build_gold_mine, font=fnt_main)

lbl_sawmill_amount=tk.Label(frm_buildings, font=fnt_main)
lbl_stone_mine_amount=tk.Label(frm_buildings, font=fnt_main)
lbl_iron_mine_amount=tk.Label(frm_buildings, font=fnt_main)
lbl_gold_mine_amount=tk.Label(frm_buildings, font=fnt_main)

lbl_resources=tk.Label(frm_resources, text="Resources:", font=fnt_title)

lbl_wood_amount=tk.Label(frm_resources, font=fnt_main)
lbl_stone_amount=tk.Label(frm_resources, font=fnt_main)
lbl_iron_amount=tk.Label(frm_resources, font=fnt_main)
lbl_gold_amount=tk.Label(frm_resources, font=fnt_main)

lbl_trades=tk.Label(frm_trades, text="Trades:", font=fnt_title)

btn_trade_1=tk.Button(frm_trades, command=do_trade_1, font=fnt_main)
btn_trade_2=tk.Button(frm_trades, command=do_trade_2, font=fnt_main)
btn_trade_3=tk.Button(frm_trades, command=do_trade_3, font=fnt_main)

btn_next_turn=tk.Button(frm_next_turn, text="Next Turn", command=next_turn, font=fnt_title)
lbl_turns_taken=tk.Label(frm_next_turn, font=fnt_main)

lbl_save_code=tk.Label(frm_save_load, text="Save Code:", font=fnt_title)
ent_save_code=tk.Entry(frm_save_load, font=fnt_main)
btn_save_code_write=tk.Button(frm_save_load, text="Save", command=save_code_write, font=fnt_main)
btn_save_code_read=tk.Button(frm_save_load, text="Load", command=save_code_read, font=fnt_main)

lbl_buildings.grid(column=0, row=0, sticky="ew")

btn_build_sawmill.grid(column=0, row=1, sticky="ew")
btn_build_stone_mine.grid(column=0, row=2, sticky="ew")
btn_build_iron_mine.grid(column=0, row=3, sticky="ew")
btn_build_gold_mine.grid(column=0, row=4, sticky="ew")

lbl_sawmill_amount.grid(column=0, row=5, sticky="ew")
lbl_stone_mine_amount.grid(column=0, row=6, sticky="ew")
lbl_iron_mine_amount.grid(column=0, row=7, sticky="ew")
lbl_gold_mine_amount.grid(column=0, row=8, sticky="ew")

lbl_resources.grid(column=0, row=0, sticky="ew")

lbl_wood_amount.grid(column=0, row=1, sticky="ew")
lbl_stone_amount.grid(column=0, row=2, sticky="ew")
lbl_iron_amount.grid(column=0, row=3, sticky="ew")
lbl_gold_amount.grid(column=0, row=4, sticky="ew")

lbl_trades.grid(column=0, row=0, sticky="nsew")

btn_trade_1.grid(column=0, row=1, sticky="nsew")
btn_trade_2.grid(column=0, row=2, sticky="nsew")
btn_trade_3.grid(column=0, row=3, sticky="nsew")

btn_next_turn.grid(column=0, row=0, sticky="ew")
lbl_turns_taken.grid(column=0, row=1, sticky="ew")

lbl_save_code.grid(column=0, row=0, columnspan=2, sticky="ew")

ent_save_code.grid(column=0, row=1, columnspan=2, sticky="ew")
btn_save_code_write.grid(column=0, row=2, sticky="ew")
btn_save_code_read.grid(column=1, row=2, sticky="ew")

frm_buildings.grid(column=0, row=0, rowspan=3, sticky="ew")
frm_resources.grid(column=1, row=0, sticky="ew")
frm_next_turn.grid(column=1, row=1, sticky="ew")
frm_save_load.grid(column=1, row=2, sticky="ew")
frm_trades.grid(column=2, row=0, rowspan=3, sticky="nsew")

create_trade_1()
create_trade_2()
create_trade_3()
update()
window.mainloop()