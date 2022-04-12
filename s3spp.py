# This file is part of Sims 3 Store Purchase Planner (S3SPP).
# Copyright (C) 2022  SpiredMoth

# S3SPP is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# S3SPP is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
# for more details.

# You should have received a copy of the GNU General Public License
# along with S3SPP. If not, see <https://www.gnu.org/licenses/>.

import datetime
import json
import math
import webbrowser

import PySimpleGUI as sg
import pytz

# import cys


############################################################
#  Global Variables
############################################################

STYLES = {
    "btn_url": {
        "button_color": (sg.theme_element_text_color(), sg.theme_background_color()),
        "font": ("_", 10, "underline"),
        "border_width": 0,
    },
}


############################################################
#  Layout & Secondary Window Generation
############################################################

def about() -> sg.Window:
    layout_about = [
        [sg.Text("Made using Python and PySimpleGUI")],
        [
            sg.Column([
                [sg.Text("Author:")],
                [sg.Text("Source code:")],
                [sg.Text("License:")],
            ]),
            sg.Column([
                [sg.Button("SpiredMoth", key=(
                    "-LINK-", "-ABOUT-", "-AUTHOR-"), **STYLES["btn_url"])],
                [sg.Button("GitHub", key=(
                    "-LINK-", "-ABOUT-", "-SOURCE-"), **STYLES["btn_url"])],
                [sg.Button("GPL-3.0", key=("-LINK-", "-ABOUT-", "-LICENSE-"),
                           **STYLES["btn_url"])],
            ]),
        ],
        [sg.HorizontalSeparator()],
        [sg.Push(), sg.Button("Close"), sg.Push()],
    ]
    win = sg.Window("About S3SA", layout=layout_about, finalize=True)
    return win


def daily_deals(deals: dict, user_tz: str, fmt: str, start_num: int = 1, count: int = 977, cycle: int = None) -> list:
    values = []
    tz = pytz.timezone(user_tz)
    current = int(deals["current"].split(".")[0])
    if cycle is not None:
        current = cycle

    # generate list of DDs to display, including wrapping back to start
    start_num -= 1  # convert 1-indexed argument to 0-indexed
    keys = [f"DD #{(start_num + i) % 977 + 1:0>3}" for i in range(count)]

    for k in keys:
        deal = deals["items"][k]
        row = [
            k,
            deal["name"],
            f'{deal["price"]} / {deal["original"]: >4}',
            f"{deal['savings']}%",
            deal["starts"][current].astimezone(tz).strftime(fmt)
        ]
        values.append(row)
        if k == "DD #977":
            # update to grab proper time on cycle rollover
            current += 1
    return values


def sales_weekly(sales: dict) -> list:
    layout = []
    for prod_id, sale in sales.items():
        row = [
            sale["name"],
            sale["item_type"],
            f'{sale["price"]} / {sale["original"]}',
            f"{sale['savings']}% off"
        ]
        layout.append(row)
    layout.sort()
    return layout


def mmao():
    layout = []
    return layout


def settings(config: sg.UserSettings) -> list:
    layout = [
        [sg.Text("Date & Time Display", font=("_", 16, "bold"))],
        [
            sg.Text("Timezone", size=(20, 1), justification="right"),
            sg.Combo(pytz.common_timezones, default_value=config["-timezone-"], key=(
                "-SETTINGS-", "-TIMEZONE-"), enable_events=True)
        ],
        [
            sg.Text("Hour format", size=(20, 1), justification="right"),
            sg.Radio("12 Hour", "-TIME-FORMAT-HOUR-", key=("-SETTINGS-",
                     "-DT_FORMAT-", "-HOUR_12-"), enable_events=True, default=True),
            sg.Radio("24 Hour", "-TIME-FORMAT-HOUR-", key=("-SETTINGS-",
                     "-DT_FORMAT-", "-HOUR_24-"), enable_events=True),
        ],
        [
            sg.Text("Weekday display", size=(20, 1), justification="right"),
            sg.Radio("Short", "-TIME-FORMAT-WEEKDAY-", key=("-SETTINGS-",
                     "-DT_FORMAT-", "-WEEKDAY_SHORT-"), enable_events=True, default=True),
            sg.Radio("Long", "-TIME-FORMAT-WEEKDAY-", key=("-SETTINGS-",
                     "-DT_FORMAT-", "-WEEKDAY_LONG-"), enable_events=True),
            sg.Radio("None", "-TIME-FORMAT-WEEKDAY-", key=("-SETTINGS-",
                     "-DT_FORMAT-", "-WEEKDAY_NONE-"), enable_events=True),
        ],
        [sg.HorizontalSeparator()],
        [sg.Text("Files and Folders", font=("_", 16, "bold"))],
        [
            sg.Text("Downloads folder", size=(20, 1), justification="right"),
            sg.Input(key=("-SETTINGS-", "-DOWNLOAD_DIR-")), sg.FolderBrowse()
        ],
        [
            sg.Text("Image folder", size=(20, 1), justification="right"),
            sg.Input(key=("-SETTINGS-", "-IMAGE_DIR-")), sg.FolderBrowse()
        ],
        [
            sg.Text("Featured Items folder", size=(
                20, 1), justification="right"),
            sg.Input(key=("-SETTINGS-", "-FEATURED_DIR-")), sg.FolderBrowse()
        ],
    ]
    return layout


def blank():
    pass


def item_details() -> list:
    layout = [
        [
            sg.Push(),
            sg.Image("", size=(200, 200), key=(
                "-CATALOG-", "-DETAILS-", "-IMAGE-")),
            sg.Push(),
        ],
        [
            sg.Text("Item Name", key=("-CATALOG-", "-DETAILS-",
                    "-VALUE-", "-NAME-"), font=("_", 10, "bold")),
        ],
        [sg.Text("(item description)", key=(
            "-CATALOG-", "-DETAILS-", "-DESCRIPTION-"))],
        [sg.HorizontalSeparator()],
        [sg.Text("TODO: item details")],
        [
            sg.Column([
                [sg.Text("Price (SP):")],
                [sg.Text("Set(s):", key=(
                    "-CATALOG-", "-DETAILS-", "-LABEL-", "-PARENTS-"))],
            ]),
            sg.Column([
                [sg.Text("Price", key=(
                    "-CATALOG-", "-DETAILS-", "-VALUE-", "-PRICE-"))],
                [sg.Text("Everyday Casual Chic", key=(
                    "-CATALOG-", "-DETAILS-", "-VALUE-", "-PARENTS-"))],
            ]),
        ],
        [sg.Checkbox("Wishlist", key=("-CATALOG-", "-DETAILS-", "-WISHLIST-"))],
    ]
    return layout


############################################################
#  Misc. Utilities
############################################################

def get_store_link(target: str, is_set: bool = False) -> str:
    fixed_links = {
        "-DAILY_DEAL-": "https://store.thesims3.com/dailyDeal.html",
        "-MMAO-": "https://store.thesims3.com/makemeanoffer.html",
        "-SALE-": "https://store.thesims3.com/sale.html",
        "-RIVERVIEW-": "https://store.thesims3.com/riverview.html",
        "-BARNACLE_BAY-": "https://store.thesims3.com/barnacleBay.html",
        "-HIDDEN_SPRINGS-": "https://store.thesims3.com/hiddenSprings.html",
        "-LUNAR_LAKES-": "https://store.thesims3.com/lunarlakes.html",
        "-LUCKY_PALMS-": "https://store.thesims3.com/luckypalms.html",
        "-SUNLIT_TIDES-": "https://store.thesims3.com/sunlittides.html",
        "-MONTE_VISTA-": "https://store.thesims3.com/montevista.html",
        "-AURORA_SKIES-": "https://store.thesims3.com/auroraskies.html",
        "-DRAGON_VALLEY-": "https://store.thesims3.com/dragonvalley.html",
        "-MIDNIGHT_HOLLOW-": "https://store.thesims3.com/midnighthollow.html",
        "-ROARING_HEIGHTS-": "https://store.thesims3.com/roaringheights.html",
    }
    if target in fixed_links:
        return fixed_links[target]
    if is_set:
        return f"https://store.thesims3.com/setsProductDetails.html?productId=OFB-SIM3:{target}"
    return f"https://store.thesims3.com/productDetails.html?productId=OFB-SIM3:{target}"


def justify_table(table: sg.Table, anchors: list):
    widget = table.Widget
    for cid, anchor in enumerate(anchors):
        widget.column(cid, anchor=anchor)


def format_date(config: sg.UserSettings) -> str:
    pieces = {
        "SHORT": "%a",
        "LONG": "%A",
        "12": "%I:%M %p",
        "24": "%H:%M",
    }
    fmt = []
    if config["-weekday-"] in pieces:
        fmt.append(pieces[config.get("-weekday-", "SHORT")])
    fmt.append("%b %d")
    fmt.append(pieces[config.get("-hour-", "12")])
    return " ".join(fmt)


############################################################
#  Event Handlers
############################################################

def handler_link(window: sg.Window, event: tuple, values: dict):
    links = {
        "-ABOUT-": {
            "-AUTHOR-": "https://forums.thesims.com/en_US/profile/SpiredMoth",
            "-SOURCE-": "https://github.com/SpiredMoth/s3spp",
            "-LICENSE-": "https://www.gnu.org/licenses/gpl.html",
            "-PYTHON-": "https://www.python.org/",
            "-PYSIMPLEGUI-": "https://pysimplegui.readthedocs.io/en/latest/",
        },
    }
    if event[1] == "-STORE-":
        target = get_store_link(event[3], event[2])
    else:
        target = links[event[1]][event[2]]
    webbrowser.open(target)


############################################################
#  Startup Functions
############################################################

def fill_dd_data(deals: dict, items: dict):
    # time variables
    utc = pytz.utc
    now = datetime.datetime.now(utc)
    hour = datetime.timedelta(hours=1)
    fmt = "%Y-%m-%d %H:%M:%S"
    hours = {
        1: hour,
        2: 2 * hour,
        3: 3 * hour,
        "cycle": deals["hours"] * hour
    }

    cycle_nums = {int(i.split(".")[0]) for i in deals["starts"].keys()}
    deals["cycles"] = []
    curr_cycle = curr_dd = 0
    cycles = {}
    for c in range(min(cycle_nums), max(cycle_nums) + 5):
        deals["cycles"].append(c)
        d = f"{c}.001"
        if d in deals["starts"]:
            cycles[c] = utc.localize(
                datetime.datetime.strptime(deals["starts"][d], fmt))
        else:
            cycles[c] = cycles[c - 1] + hours["cycle"]
        if c > curr_cycle and cycles[c] <= now:
            curr_cycle = c
    for i in range(977):
        # determine data to work with
        deal_num = f"{i + 1:0>3}"
        deal_id = f"DD #{deal_num}"
        deal = deals["items"][deal_id]
        itm = items[deal["id"]]

        # add to entry's data
        deal["name"] = itm["name"]
        deal["original"] = int(itm["price"])
        deal["savings"] = math.floor(
            100 - deal["price"] * 100 / int(itm["price"]))

        # determine start times
        deal["starts"] = dict()
        for cycle in cycles.keys():
            dt = cycles[cycle]
            deal["starts"][cycle] = dt
            if cycle == curr_cycle and dt <= now:
                curr_dd = i + 1
            # increment time for next entry
            if i < 976:
                cycles[cycle] = dt + hours[deal["duration"]]
                # check for mid-cycle start time changes
                next_deal = f"{cycle}.{i + 2:0>3}"
                if next_deal in deals["starts"]:
                    cycles[cycle] = utc.localize(
                        datetime.datetime.strptime(deals["starts"][next_deal], fmt))

    deals["current"] = f"{curr_cycle}.{curr_dd}"


def fill_sale_data(sales: dict, items: dict):
    for itm_id, price in sales.items():
        item = items[itm_id]
        sale = {
            "name": item["name"],
            "item_type": item["type_store"],
            "original": int(item["price"]),
            "price": price,
            "savings": math.floor(100 - price * 100 / int(item["price"])),
        }
        sales[itm_id] = sale


def load_store_data() -> dict:
    data = dict()

    for itm in ["items", "sets", "deals"]:
        with open(f"data/store_{itm}.json", "r", encoding="UTF-8") as f:
            data[itm] = json.loads(f.read())

    fill_dd_data(data["deals"]["daily_deal"], data["items"])
    fill_sale_data(data["deals"]["weekly"], data["items"])

    return data


############################################################
#  Main Function
############################################################

def main():
    config_defaults = {
        # "-win_x-": None,
        # "-win_y-": None,
        "-timezone-": "GMT",
        "-hour-": "12",
        "-weekday-": "SHORT",
    }
    table_config = {
        "expand_y": True,
        "justification": "left",
        "auto_size_columns": False,
        "num_rows": 20,
        "alternating_row_color": "#333333",
    }

    config = sg.UserSettings()
    config.load()
    for k, v in config_defaults.items():
        if config.get(k, False) is False:
            config[k] = v
    win_loc = (config["-win_x-"], config["-win_y-"])
    timezone = config["-timezone-"]
    dt_fmt = format_date(config)

    # load Store data
    store = load_store_data()
    dd_items = store["deals"]["daily_deal"]["items"]
    dd_cycle, dd_current = [
        int(i) for i in store["deals"]["daily_deal"]["current"].split(".")]
    dd_cycle_display = dd_cycle

    # Layouts
    # TODO: clean up layouts
    # some are old and unused, some have changed
    layout_summary = [
        [sg.Text("TODO: Store Catalog summary")],
        [sg.Text(f"Items in Store: {len(store['items'])}")],
    ]
    layout_dd = [
        [sg.Button("Daily Deal (Store page)", key=(
            "-LINK-", "-STORE-", "_", "-DAILY_DEAL-"), **STYLES["btn_url"])],
        [
            sg.Text("Current Daily Deal:"),
            sg.Text(f'Cycle {dd_cycle}, deal #{dd_current}', key=("-DD-", "-CURRENT-"))
        ],
        [
            sg.Text("Search:"),
            sg.Input(key=("-DD-", "-SEARCH-")),
            # ],
            # [
            sg.Push(),
            sg.Text("Cycle:"),
            # TODO: cycle control should be spindown-like
            sg.Input(dd_cycle, key=("-DD-", "-CYCLE-"),
                     size=(3, 1), enable_events=True),
            sg.Text("Timezone:"),
            sg.Combo(pytz.common_timezones, default_value=timezone, key=(
                "-DD-", "-TIMEZONE-"), enable_events=True)
        ],
        [
            sg.Table([[]],
                     headings=["Deal #", "Item Name",
                               "Price", "Savings", "Start Time"],
                     key=("-DD-", "-TABLE-"),
                     col_widths=[7, 50, 10, 7, 17],
                     **table_config)
        ],
    ]
    layout_itm_list = [
        [sg.Text("TODO: item list and controls")],
        [
            sg.Frame("Search", [[
                sg.Column([
                    [sg.Text("ID")],
                    [sg.Input(key=("-CATALOG-", "-SEARCH-", "-ID-"), size=(5, 1))],
                ]),
                sg.Column([
                    [sg.Text("Name")],
                    [sg.Input(key=("-CATALOG-", "-SEARCH-", "-NAME-"))],
                ]),
            ]])
        ],
        [sg.Listbox([], key=("-CATALOG-", "-SEARCH-", "-RESULTS-"),
                    expand_x=True, expand_y=True)],
    ]
    layout_catalog = [
        [sg.Text("TODO: Store catalog browser")],
        [
            sg.Column(layout_itm_list, expand_x=True, expand_y=True),
            sg.Column(item_details(), expand_y=True),
        ],
    ]
    layout_cys = [
        [sg.Text("TODO: Complete Your Set listings")],
        [
            sg.Column([
                [sg.Text("Set name:", size=(12, 1)),
                 sg.Input(key=("-CYS-", "-SET_NAME-"))],
                [sg.Text("Owned items:", size=(12, 1)), sg.Input(
                    key=("-CYS-", "-OWNED-"), size=(5, 1))],
                [sg.Text("Set price:", size=(12, 1)), sg.Input(
                    key=("-CYS-", "-SET_PRICE-"), size=(5, 1))],
                [sg.Frame("CYS", [
                    [sg.Text("TODO: Set CYS prices")],
                    [sg.Text("Set name"), sg.Text("price source"),
                     sg.Text("CYS price / purchase price")],
                ])],
            ], vertical_alignment="top"),
            sg.Column([
                [sg.Frame("Contained Sets", [
                    [sg.Text("TODO: list of sets that overlap")],
                    [sg.Checkbox("Item name"), sg.Text(
                        "price", size=(5, 1)), sg.Input("paid", size=(5, 1))],
                ], expand_y=True)],
                [sg.Frame("Items", [
                    [sg.Text("TODO: list of items in set")],
                    [sg.Checkbox("Item name"), sg.Text(
                        "price", size=(5, 1)), sg.Input("paid", size=(5, 1))],
                ], expand_y=True)],
            ]),
        ],
    ]
    layout_mmao = [
        [sg.Button("Make Me an Offer (Store page)", key=(
            "-LINK-", "-STORE-", "_", "-MMAO-"), **STYLES["btn_url"])],
        [sg.Text("TODO: Make Me an Offer checking UI")],
    ]
    layout_calcs = [
        [sg.TabGroup([
            [sg.Tab("CYS", layout_cys, expand_y=True)],
            [sg.Tab("Make Me an Offer", layout_mmao, expand_y=True)],
        ])]
    ]
    layout = [
        [sg.Push(), sg.Text("Sims 3 Store Purchase Planner",
                            font=("_", 24, "bold")), sg.Push()],
        [
            sg.Column([
                [sg.Button("Items", key=("-NAVIGATION-",
                           "-ITEMS-"), expand_x=True)],
                [sg.Button("Sets", key=("-NAVIGATION-", "SETS"), expand_x=True)],
                [sg.Button("Complete Your Set", key=(
                    "-NAVIGATION-", "-CYS-"), expand_x=True)],
                [sg.Button("Make Me an Offer", key=(
                    "-NAVIGATION-", "-MMAO-"), expand_x=True)],
                [sg.Button("Sales", key=("-NAVIGATION-",
                           "-SALES-"), expand_x=True)],
                [sg.Button("Wish List", key=(
                    "-NAVIGATION-", "-WISHLIST-"), expand_x=True)],
                [sg.VPush()],
                [sg.Button("About", key=("-NAVIGATION-",
                           "-ABOUT-"), expand_x=True)],
            ], expand_y=True),
            sg.Column([
                [sg.TabGroup([[
                    sg.Tab("Summary", layout_summary),
                    sg.Tab("Catalog", layout_catalog,
                           element_justification="center", expand_x=True),
                    sg.Tab("Daily Deals", layout_dd),
                    sg.Tab("Sales", [
                        [sg.Button("Sales (Store page)", key=(
                            "-LINK-", "-STORE-", "_", "-SALE-"), **STYLES["btn_url"])],
                        [sg.Table(
                            [[]],
                            headings=["Item Name", "Item Type",
                                      "Price", "Savings"],
                            col_widths=[50, 10, 10, 7],
                            key=("-WEEKLY-", "-TABLE-"),
                            **table_config)],
                    ]),
                    sg.Tab("Calculators", layout_calcs),
                    sg.Tab("Wish List", [
                        [sg.Text("TODO: Wish List browser")],
                    ]),
                    sg.Tab("Settings", settings(config)),
                ]])],
            ]),
        ],
    ]

    # if win_loc != (None, None):
    #     win_main = sg.Window("Sims 3 Store Purchase Planner", layout,
    #                          finalize=True, location=win_loc, resizable=True)
    # else:
    #     win_main = sg.Window("Sims 3 Store Purchase Planner",
    #                          layout, finalize=True, resizable=True)
    win_main = sg.Window("Sims 3 Store Purchase Planner", layout,
                         finalize=True, resizable=True)
    win_about = None
    refresh = {"dd", "weekly"}

    # Last-minute element configuration
    win_main[("-SETTINGS-", "-DT_FORMAT-",
              f"-HOUR_{config['-hour-']}-")].update(value=True)
    win_main[("-SETTINGS-", "-DT_FORMAT-",
              f"-WEEKDAY_{config['-weekday-']}-")].update(value=True)
    # familiar Ctrl+Q -> Exit keybind
    win_main.bind("<Control-q>", "Exit")

    # TODO: timeout or thread to live update current DD
    while True:
        # determine currently active Daily Deal
        now = datetime.datetime.now(tz=pytz.utc)
        while now >= dd_items[f"DD #{dd_current % 977 + 1:0>3}"]["starts"][dd_cycle]:
            refresh.add("dd")
            dd_current = dd_current % 977 + 1
            if dd_current == 1:
                if dd_cycle == dd_cycle_display:
                    refresh.add("cycle")
                dd_cycle += 1
            win_main[("-DD-", "-CURRENT-")
                     ].update(f"Cycle {dd_cycle}, deal #{dd_current:0>3}")

        # refresh elements of window
        print(f"{refresh=}")
        if "cycle" in refresh:
            dd_cycle_display = dd_cycle
            refresh.discard("cycle")
        if "dd" in refresh:
            dt_fmt = format_date(config)
            win_main[("-DD-", "-TABLE-")].update(
                values=daily_deals(store["deals"]["daily_deal"],
                                   timezone,
                                   dt_fmt,
                                   cycle=dd_cycle_display)
            )
            justify_table(win_main[("-DD-", "-TABLE-")],
                          ["w", "w", "e", "center", "w"])
            refresh.discard("dd")
        if "weekly" in refresh:
            win_main[("-WEEKLY-", "-TABLE-")
                     ].update(values=sales_weekly(store["deals"]["weekly"]))
            justify_table(win_main[("-WEEKLY-", "-TABLE-")],
                          ["w", "w", "e", "center"])
            refresh.discard("weekly")

        win, event, values = sg.read_all_windows()
        if event in ("Exit", "Close", sg.WINDOW_CLOSED):
            if win == win_about:
                win_about.close()
                win_about = None
            if win == win_main:
                break
        win_loc = win_main.current_location()

        if isinstance(event, tuple):
            if event[0] == "-NAVIGATION-":
                # sidebar buttons
                if event[1] == "-ABOUT-" and win_about is None:
                    win_about = about()
                if event[1] != "-ABOUT-":
                    pass
            if event[0] == "-LINK-":
                handler_link(win, event, values)
            if event[0] == "-STORE-":
                webbrowser.open(get_store_link(event[1]))
            if event[0] == "-DD-":
                if event[1] == "-TIMEZONE-" and values[event] in pytz.common_timezones:
                    timezone = values[event]
                    refresh.add("dd")
                if event[1] == "-CYCLE-":
                    if values[event][-1] not in "1234567890":
                        win[event].update(values[event][:-1])
                    else:
                        cycle = int(values[event])
                        if cycle in store["deals"]["daily_deal"]["cycles"]:
                            dd_cycle_display = cycle
                            refresh.add("dd")
            if event[0] == "-SETTINGS-":
                if event[1] == "-TIMEZONE-":
                    config["-timezone-"] = values[event]
                if event[1] == "-DT_FORMAT-":
                    refresh.add("dd")
                    if event[2].startswith("-WEEKDAY_"):
                        weekday = event[2][9:-1]
                        config["-weekday-"] = weekday
                    if event[2].startswith("-HOUR_"):
                        hour = event[2][6:-1]
                        config["-hour-"] = hour

    win_main.close()

    # Post-window close cleanup
    config["-win_x-"] = win_loc[0]
    config["-win_y-"] = win_loc[1]


if __name__ == "__main__":
    main()
