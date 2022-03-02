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


# TODO: incorporate deal times somehow
def daily_deals(deals: dict, items: dict, start_num: int = 1, count: int = 977) -> list:
    values = []
    col_widths = [7, 50, 10, 9, 7]

    # generate list of DDs to display as well as a start time for first
    start_num -= 1  # convert 1-indexed argument to 0-indexed
    keys = [f"DD #{(start_num + i) % 977 + 1:0>3}" for i in range(count)]

    for k in keys:
        deal = deals["items"][k]
        key = deal["id"]
        name = items[key]["name"]
        price = items[key]["price"]
        if price == "-":
            price = int(items[key]["worth"])
        else:
            price = int(price)
        sale = deal["price"]
        savings = math.floor(100 - sale / price * 100)
        row = [k, name, price, sale, f"{savings}%"]
        values.append(row)
        # dynamic column widths
        # row = [str(v) for v in row]
        # for i, v in enumerate(row):
        #     col_widths[i] = max(col_widths[i], len(v))
    values.sort()
    # print(f"{col_widths=}")

    table_config = {
        "headings": ["Deal #", "Item Name", "Regular Price", "Sale Price", "Savings"],
        "expand_y": True,
        "justification": "left",
        "auto_size_columns": False,
        "col_widths": col_widths,
        "num_rows": 20,
        "alternating_row_color": "#333333",
    }
    table = sg.Table(values, **table_config)
    return table


def sales_weekly(sales: dict, items: dict) -> list:
    layout = []
    layout.append([sg.Text("TODO: sales controls")])
    for i in sales:
        name = items[i]["name"]
        price = int(items[i]["price"])
        sale = int(sales[i])
        savings = math.floor(100 - sale / price * 100)
        row = [sg.Text(name, expand_x=True)]
        row.append(sg.Text(f"{sale} / {price} ({savings}% off)"))
        layout.append(row)
    return layout


def mmao():
    layout = []
    return layout


def settings(tz: str = "UTC") -> list:
    layout = [
        [sg.Text("TODO: Application Settings")],
        [
            sg.Column([
                [sg.Text("Timezone")],
                [sg.Text("Image folder")],
                [sg.Text("Downloads folder")],
            ]),
            sg.Column([
                [sg.Combo(pytz.all_timezones, default_value=tz, key=(
                    "-SETTINGS-", "-TIMEZONE-"), enable_events=True)],
                [sg.Input(key=("-SETTINGS-", "-IMAGE_DIR-")), sg.FolderBrowse()],
                [sg.Input(key=("-SETTINGS-", "-DOWNLOAD_DIR-")),
                 sg.FolderBrowse()],
            ]),
        ]
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
                [sg.Text("Price", key=("-CATALOG-", "-DETAILS-", "-VALUE-", "-PRICE-"))],
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


def handler_navigation(window: sg.Window, event: tuple, values: dict):
    # tab layout generator mapping
    new_tabs = {
        "-DAILY_DEAL-": blank,
        "-SALES-": blank,
        "-MMAO-": blank,
        "-WISHLIST-": blank,
    }

    if event in new_tabs:
        # add tab to tab group
        pass
    pass


############################################################
#  Main Function
############################################################

def main():
    config = sg.UserSettings()
    config.load()
    win_loc = (config.get("-win_x-", default=None),
               config.get("-win_y-", default=None))
    timezone = config.get("-timezone-", default="UTC")

    # load Store data
    store = dict()
    for itm in ["items", "sets", "deals"]:
        with open(f"data/store_{itm}.json", "r", encoding="UTF-8") as f:
            store[itm] = json.loads(f.read())

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
            sg.Column([
                [sg.Text("Current Daily Deal")],
                [sg.Image("", key=("-DD-", "-CURRENT-",
                          "-IMAGE-"), size=(200, 200))],
                [sg.Text("TODO: upcoming (and recent?) deals list")],
            ], vertical_alignment="top"),
            sg.Column([
                [sg.Text("Search:"), sg.Input(key=("-DD-", "-SEARCH-"))],
                [daily_deals(store["deals"]["daily_deal"], store["items"])],
            ]),
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
                [sg.Frame("Items", [
                    [sg.Text("TODO: list of items in set")],
                    [sg.Checkbox("Item name"), sg.Text(
                        "price", size=(5, 1)), sg.Input("paid", size=(5, 1))],
                ], expand_y=True)],
                [sg.Frame("Contained Sets", [
                    [sg.Text("TODO: list of smaller sets in set")],
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
                        [sg.Column(sales_weekly(store["deals"]["sale"], store["items"]),
                                   scrollable=True, vertical_scroll_only=True)],
                    ]),
                    sg.Tab("Calculators", layout_calcs),
                    sg.Tab("Wish List", [
                        [sg.Text("TODO: Wish List browser")],
                    ]),
                    sg.Tab("Settings", settings(tz=timezone)),
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

    # familiar Ctrl+Q -> Exit keybind
    win_main.bind("<Control-q>", "Exit")

    while True:
        win, event, values = sg.read_all_windows()
        if event in ("Exit", "Close", sg.WINDOW_CLOSED):
            if win == win_main:
                if win_about is not None:
                    win_about.close()
                break
            elif win == win_about:
                win.close()
                win_about = None
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
            if event[0] == "-SETTINGS-":
                if event[1] == "-TIMEZONE-":
                    timezone = values[event]

    win_main.close()

    # Post-window close cleanup
    config["-win_x-"] = win_loc[0]
    config["-win_y-"] = win_loc[1]
    config["-timezone-"] = timezone

    # write updated Store data back to file
    # with open("data/store_items.json", "w", encoding="UTF-8") as f:
    #     f.write(json.dumps(store["items"], indent=4))
    # with open("data/store_sets.json", "w", encoding="UTF-8") as f:
    #     f.write(json.dumps(store["sets"], indent=4))


if __name__ == "__main__":
    main()
