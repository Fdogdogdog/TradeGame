// Start of code

const doc = window.document;

// Get a bunch of elements from the HTML from their ID's
const noscript = doc.querySelector("noscript");    // Gets the first noscript tag
noscript.style.display = "none";    // Sets the display css property to "none"

const dont_show_span = doc.querySelector(".dont_show");    // Gets the first thing in the dont_show class
dont_show_span.style.display = "none";

const lbl_wood_amount = doc.getElementById("lbl_wood_amount"),
    lbl_stone_amount = doc.getElementById("lbl_stone_amount"),
    lbl_iron_amount = doc.getElementById("lbl_iron_amount"),
    lbl_gold_amount = doc.getElementById("lbl_gold_amount"),
    lbl_treasure_amount = doc.getElementById("lbl_treasure_amount");

const lbl_sawmill_amount = doc.getElementById("lbl_sawmill_amount"),
    lbl_stone_mine_amount = doc.getElementById("lbl_stone_mine_amount"),
    lbl_iron_mine_amount = doc.getElementById("lbl_iron_mine_amount"),
    lbl_gold_mine_amount = doc.getElementById("lbl_gold_mine_amount"),
    lbl_storehouse_amount = doc.getElementById("lbl_storehouse_amount"),
    lbl_treasure_room_amount = doc.getElementById("lbl_treasure_room_amount");

const btn_build_sawmill = doc.getElementById("btn_build_sawmill"),
    btn_build_stone_mine = doc.getElementById("btn_build_stone_mine"),
    btn_build_iron_mine = doc.getElementById("btn_build_iron_mine"),
    btn_build_gold_mine = doc.getElementById("btn_build_gold_mine"),
    btn_build_storehouse = doc.getElementById("btn_build_storehouse"),
    btn_build_treasure_room = doc.getElementById("btn_build_treasure_room");

const div_trades = doc.getElementById("div_trades")
const btn_trade_1 = doc.getElementById("trade_1_btn"),
    btn_trade_2 = doc.getElementById("trade_2_btn"),
    btn_trade_3 = doc.getElementById("trade_3_btn");

const btn_next_turn = doc.getElementById("btn_next_turn"),
    btn_open_menu = doc.getElementById("btn_open_menu");

const div_menu = doc.getElementById("menu");
const div_tutorial = doc.getElementById("tutorial");
const div_whats_new = doc.getElementById("whats_new")

const msg_tutorial = doc.getElementById("msg_tutorial");

const div_save_load = doc.getElementById("div_save_load");
const ent_save_code=doc.getElementById("ent_save_code")
const sound = doc.querySelector(".dont_show audio");    // Get the first audio element in an element with class dont_show

let lst_save_code = [],
    str_save_code = "";

let tutorial_current_page = 0;
const tutorial_pages = [
    "Welcome to TradeGame! I bet you couldn't guess it by the name, but this is a game about trading.",
    "Your first goal will be getting a sawmill, however you do not have enough wood.",
    "Find a trade where the export is about 5 stone, and the import is wood. If you don't see one, keep pressing next turn until you find one.",
    "If you don't have enough stone, try to trade a small amount of wood away for stone. Otherwise, click next.",
    "Now that you have the materials, the 'Build Sawmill' button should no longer be greyed-out. Press it to build your first sawmill.",
    "Now that you have built a sawmill, you have infinite wood. You can use this to trade for other resources to build more things.",
    "Press 'Close Tutorial' to exit the tutorial."
];

// Default
let resources = {
    wood: 45,
    stone: 30,
    iron: 0,
    gold: 0,
    treasure: 0
};

const resource_values = {
    wood: 1,
    stone: 2,
    iron: 4,
    gold: 10,
    treasure: 20
};

let buildings = {
    sawmill: 0,
    stone_mine: 0,
    iron_mine: 0,
    gold_mine: 0,
    storehouse: 0,
    treasure_room: 0
};

// DEV save
// 1000/432500/2797500/365000/100000/1000/1000/1000/1000/9999 which is pretty impressive, according to the translator.

// Translator save
// 4306/35100/35100/35100/35100/80/85/147/243/350/23820/2381 which is not as great.

let export_blacklist = [];
let import_blacklist = [];

let trades = [ {    // trade 1
        export: "",
        export_amount: 0,
        import: "",
        import_amount: 0
    },
    {                   // trade 2
        export: "",
        export_amount: 0,
        import: "",
        import_amount: 0
    },
    {                   // trade 3
        export: "",
        export_amount: 0,
        import: "",
        import_amount: 0
} ];

let turns_taken = 0;

function save_code_write() {
    lst_save_code = [];

    lst_save_code.push(turns_taken);
    lst_save_code.push(resources.wood);
    lst_save_code.push(resources.stone);
    lst_save_code.push(resources.iron);
    lst_save_code.push(resources.gold);

    lst_save_code.push(buildings.sawmill);
    lst_save_code.push(buildings.stone_mine);
    lst_save_code.push(buildings.iron_mine);
    lst_save_code.push(buildings.gold_mine);

    // new in v1.1
    lst_save_code.push(buildings.storehouse);
    lst_save_code.push(resources.treasure);

    // new in v1.2
    lst_save_code.push(buildings.treasure_room);

    str_save_code=lst_save_code.join("/");
    ent_save_code.value = str_save_code;
}

function save_code_read() {
    if (confirm("Load save? \nAll unsaved progress will be overwritten.\nAre you sure you want to load?")) {
        sound.play()
       
        str_save_code = ent_save_code.value;
        lst_save_code = str_save_code.split("/");

        turns_taken = +(lst_save_code[0]);
        resources.wood = +(lst_save_code[1]);
        resources.stone = +(lst_save_code[2]);    // The unary + operator coerces the value into a number.
        resources.iron = +(lst_save_code[3]);
        resources.gold = +(lst_save_code[4]);

        buildings.sawmill = +(lst_save_code[5]);
        buildings.stone_mine = +(lst_save_code[6]);
        buildings.iron_mine = +(lst_save_code[7]);
        buildings.gold_mine = +(lst_save_code[8]);

        // Optional new in v1.1
        try {
            buildings.storehouse = +(lst_save_code[9]);
        } catch(err) {
            buildings.storehouse = 0;
        }
        try {
            resources.treasure = +(lst_save_code[10]);
        } catch(err) {
            resources.treasure = 0;
        }

        // Optional new in v1.2
        try {
            buildings.treasure_room = +(lst_save_code[11]);
        } catch(err) {
            buildings.treasure_room = 0;
        }

        create_trade(1);
        create_trade(2);
        create_trade(3);

        update();
    }
    hide_menu();
}

function create_trade(num) {
    console.log(`create_trade called with parameter ${num}`);
    if ((typeof num !== "number") && (typeof num !== "bigint")) {
        throw new Error("Ethan, you messed up");
    }

    const trade_creating = trades[num - 1];

    let resources_keys = [];
    for (let resource of Object.keys(resources)) {
        resources_keys.push(resource);
    }

    while (true) { while (true) {
            trade_creating.export = resources_keys[Math.floor(Math.random() * (resources_keys.length -1))];
            if (resources[trade_creating.export] > 0 && !(export_blacklist.includes(trade_creating.export))) {
                break;
            } else {
                continue;
            }
        }
        while (true) {
            trade_creating.import = resources_keys[Math.floor(Math.random() * (resources_keys.length -1))];
            if (!(import_blacklist.includes(trade_creating.import))) {
                break;
            } else {
                continue;
            }
        }
        if (trade_creating.import === trade_creating.export) {
            continue;
        } else {
            break;
        }
    }
    console.log("Cheese");

    trade_creating.export_amount = Math.round(1 + Math.random() * (resources[trade_creating.export] + 5));
    trade_creating.import_amount = Math.round(trade_creating.export_amount * (resource_values[trade_creating.export] / resource_values[trade_creating.import]));

    let count = 0;
    while (true) {
        trade_creating.import_amount += Math.round(Math.random() * 10 - 5);
        if (trade_creating.import_amount > 0) {
            console.log("Breaking loop");
            break;
        }
        count++;
        console.log(`${count} times already!`);
    }
    console.log("confusion");
}

function do_trade_1() {
    if (resources[trades[0].export] >= trades[0].export_amount) {
        resources[trades[0].export] -= trades[0].export_amount;
        resources[trades[0].import] += trades[0].import_amount;
        create_trade(1);
        update();
    }
}
function do_trade_2() {
    if (resources[trades[1].export] >= trades[1].export_amount) {
        resources[trades[1].export] -= trades[1].export_amount;
        resources[trades[1].import] += trades[1].import_amount;
        create_trade(2);
        update();
    }
}
function do_trade_3() {
    if (resources[trades[2].export] >= trades[2].export_amount) {
        resources[trades[2].export] -= trades[2].export_amount;
        resources[trades[2].import] += trades[2].import_amount;
        create_trade(3);
        update();
    }
}

function update() {
    msg_tutorial.innerHTML = tutorial_pages[tutorial_current_page];
    console.log("\n");
    console.log("Starting update function");

    msg_tutorial.classList.remove("highlighted");
    lbl_wood_amount.classList.remove("highlighted");
    lbl_sawmill_amount.classList.remove("highlighted");
    lbl_stone_amount.classList.remove("highlighted");
    div_trades.classList.remove("highlighted");
    btn_build_sawmill.classList.remove("highlighted");
    btn_next_turn.classList.remove("highlighted");

    console.log("Starting switch function");
    switch (tutorial_current_page) {
        case 1:
            lbl_wood_amount.classList.add("highlighted");
            lbl_sawmill_amount.classList.add("highlighted");
            btn_build_sawmill.classList.add("highlighted");
            break;
        case 2:
            div_trades.classList.add("highlighted");
            lbl_stone_amount.classList.add("highlighted");
            lbl_wood_amount.classList.add("highlighted");
            btn_next_turn.classList.add("highlighted");
            break;
        case 3:
            div_trades.classList.add("highlighted");
            lbl_stone_amount.classList.add("highlighted");
            break;
        case 4:
            btn_build_sawmill.classList.add("highlighted");
            break;
    }

    console.log("Checking for more resources than storehouses");
    if (resources.wood > (buildings.storehouse * 100 + 100)) {
        resources.wood = buildings.storehouse * 100 + 100;
    }
    if (resources.stone > (buildings.storehouse * 100 + 100)) {
        resources.stone = buildings.storehouse * 100 + 100;
    }
    if (resources.iron > (buildings.storehouse * 100 + 100)) {
        resources.iron = buildings.storehouse * 100 + 100;
    }
    if (resources.gold > (buildings.storehouse * 100 + 100)) {
        resources.gold = buildings.storehouse * 100 + 100;
    }
    if (resources.treasure > (buildings.treasure_room * 10 + 10)) {
        resources.treasure = buildings.treasure_room * 10 + 10;
    }

    console.log("Updating resource labels and building labels");
    lbl_wood_amount.innerHTML = `Wood: ${resources.wood}/${100 * buildings.storehouse + 100}`;
    lbl_stone_amount.innerHTML = `Stone: ${resources.stone}/${100 * buildings.storehouse + 100}`;
    lbl_iron_amount.innerHTML = `Iron: ${resources.iron}/${100 * buildings.storehouse + 100}`;
    lbl_gold_amount.innerHTML = `Gold: ${resources.gold}/${100 * buildings.storehouse + 100}`;
    lbl_treasure_amount.innerHTML = `Treasure ${resources.treasure}/${10 * buildings.storehouse + 100}`;

    lbl_sawmill_amount.innerHTML = `Sawmills (produces 5 wood per turn): ${buildings.sawmill}`;
    lbl_stone_mine_amount.innerHTML = `Stone mines (produces 10 stone per turn): ${buildings.stone_mine}`;
    lbl_iron_mine_amount.innerHTML = `Iron mines (produces 5 iron and 10 stone per turn): ${buildings.iron_mine}`;
    lbl_gold_mine_amount.innerHTML = `Gold mines (produces 1 gold and 10 stone per turn): ${buildings.gold_mine}`;
    lbl_storehouse_amount.innerHTML = `Storehouses (allows you to hold 100 more of each resource): ${buildings.storehouse}`;
    lbl_treasure_room_amount.innerHTML = `Treasure rooms (allows you to hold 10 more treasure): ${buildings.treasure_room}`;

    console.log("Updating trade buttons");
    btn_trade_1.innerHTML = `Export: ${trades[0].export_amount} ${trades[0].export}, Import: ${trades[0].import_amount} ${trades[0].import}`;
    btn_trade_2.innerHTML = `Export: ${trades[1].export_amount} ${trades[1].export}, Import: ${trades[1].import_amount} ${trades[1].import}`;
    btn_trade_3.innerHTML = `Export: ${trades[2].export_amount} ${trades[2].export}, Import: ${trades[2].import_amount} ${trades[2].import}`;

    // Build button colours
    if (resources.wood >= 50 && resources.stone >= 25) {
        btn_build_sawmill.classList.add("can_trade_build");
    } else {
        btn_build_sawmill.classList.add("cant_trade_build");
    }
    if (resources.stone >= 50 && resources.wood >= 25) {
        btn_build_stone_mine.classList.add("can_trade_build");
    } else {
        btn_build_stone_mine.classList.add("cant_trade_build");
    }
    if (resources.stone >= 100 && resources.iron >= 50) {
        btn_build_iron_mine.classList.add("can_trade_build");
    } else {
        btn_build_iron_mine.classList.add("cant_trade_build");
    }
    if (resources.iron >= 100 && resources.stone >= 50) {
        btn_build_gold_mine.classList.add("can_trade_build");
    } else {
        btn_build_gold_mine.classList.add("cant_trade_build");
    }
    if (resources.wood >= 100 && resources.iron >= 25) {
        btn_build_storehouse.classList.add("can_trade_build");
    } else {
        btn_build_storehouse.classList.add("cant_trade_build");
    }
    if (resources.iron >= 75 && resources.gold >= 25) {
        btn_build_treasure_room.classList.add("can_trade_build");
    } else {
        btn_build_treasure_room.classList.add("cant_trade_build");
    }

    // Trade button colours
    if (trades[0].export_amount <= resources[trades[0].export]) {
        btn_trade_1.classList.add("can_trade_build");
    } else {
        btn_trade_1.classList.add("cant_trade_build");
    }
    if (trades[1].export_amount <= resources[trades[1].export]) {
        btn_trade_2.classList.add("can_trade_build");
    } else {
        btn_trade_2.classList.add("cant_trade_build");
    }
    if (trades[2].export_amount <= resources[trades[2].export]) {
        btn_trade_3.classList.add("can_trade_build");
    } else {
        btn_trade_3.classList.add("cant_trade_build");
    }
}

function next_turn() {
    turns_taken++;

    resources.wood += 5 * buildings.sawmill;
    resources.stone += 10 * buildings.stone_mine;
    resources.iron += 5 * buildings.iron_mine;
    resources.stone += 10 * buildings.iron_mine;
    resources.gold += 1 * buildings.gold_mine;
    resources.stone += 10 * buildings.gold_mine;

    create_trade(1);
    create_trade(2);
    create_trade(3);

    update();
}

function build_sawmill() {
    if (resources.wood >= 50 && resources.stone >= 25) {
        resources.wood -= 50;
        resources.stone -= 25;
        buildings.sawmill++;
    }
    update();
}
function build_stone_mine() {
    if (resources.wood >= 25 && resources.stone >= 50) {
        resources.wood -= 25;
        resources.stone -= 50;
        buildings.stone_mine++;
    }
    update();
}
function build_iron_mine() {
    if (resources.stone >= 100 && resources.iron >= 50) {
        resources.stone -= 100;
        resources.iron -= 50;
        buildings.iron_mine++;
    }
    update();
}
function build_gold_mine() {
    if (resources.iron >= 100 && resources.stone >= 50) {
        resources.iron -= 100;
        resources.stone -= 50;
        buildings.gold_mine++;
    }
    update();
}
function build_storehouse() {
    if (resources.wood >= 100 && resources.iron >= 25) {
        resources.wood -= 100;
        resources.iron -= 25;
        buildings.storehouse++;
    }
    update();
}
function build_treasure_room() {
    if (resources.iron >= 75 && resources.gold >= 25) {
        resources.iron -= 75;
        resources.gold -= 25;
        buildings.treasure_room++;
    }
    update();
}

function show_menu() {
    div_menu.style.display = "block";
}
function hide_menu() {
    div_menu.style.display = "none";
}

function show_tutorial() {
    div_tutorial.style.display = "block";
    hide_menu();
}
function hide_tutorial() {
    div_tutorial.style.display = "none";
    tutorial_current_page = 0;
    update();
}

function show_whats_new() {
    div_whats_new.style.display = "block";
    hide_menu();
}
function hide_whats_new() {
    div_whats_new.style.display = "none";
}

function next_tutorial_page() {
    if (!(tutorial_current_page >= tutorial_pages.length - 1)) {
        tutorial_current_page++;
        update();
    }
}
function prev_tutorial_page() {
    if (!(tutorial_current_page <= 0)) {
        tutorial_current_page--;
        update();
    }
}

let choice;
function quit_game() {
    hide_menu();
    choice = confirm("Quit Game?/nAll unsaved progress will be lost.\nAre you sure you want to quit?");
    if (choice) {
        close();
    }
}


create_trade(1);
create_trade(2);
create_trade(3);
update();

alert("Played Before?\nIf you have not played before, press 'Menu', then press 'Tutorial'");

// End of code