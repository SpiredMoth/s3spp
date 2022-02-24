# Sims 3 Store Purchase Planner
Sims 3 Store content browser, analyzer, and purchase planner.

## Planned Features
Unorganized list of features I plan to add *eventually* ... maybe

- CYS calculation
- Daily Deal list -- filterable, expected CYS, estimated start and end times
- Weekly sale list -- filterable, expected CYS
- Make Me an Offer checker
- Catalog browser
- configurable Downloads folder(s) and timezone
- Inventory
- Wishlist
- Import from S3S Browser -- Inventory, Images, Download folders
- Cheapest path searcher

Once I implement some *useful* features (MMaO checker and/or CYS calculations) I will start making proper releases. Until that time you'll have to follow the **Development** instructions below

## Development
To run the source code you'll need Python 3.6 or later and Git

```
git clone https://github.com/SpiredMoth/s3spp.git
cd s3spp
python -m pip install -r requirements.txt
python s3spp.py
```

> ### Required Python Version Note
> While I try to keep the code's requirements to **Python 3.6** or above, I upgraded to **Python 3.10** not long ago and have been using some newer features during development that I may forget to remove/rewrite.

---

## License
This software is licensed under GNU General Public License version 3 or any later version. You can find a copy of the license in the [LICENSE file](LICENSE).

This software is not endorsed by or affiliated with Electronic Arts, or its licensors. Trademarks are the property of their respective owners. Game content and materials copyright Electronic Arts Inc. and its licensors. All Rights Reserved.


This program makes use of, or will eventually make use of, the following open-source Python packages:

- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/) -- MIT License
- [lxml](https://pypi.org/project/lxml/) -- BSD License
- [PySimpleGUI](https://pypi.org/project/PySimpleGUI/) -- LGPLv3+
- [pytz](https://pypi.org/project/pytz/) -- MIT License
<!-- - [requests](https://pypi.org/project/requests/) -- Apache License 2.0 -->

---

## Credits
- [PySimpleGUI](https://pysimplegui.readthedocs.io/en/latest/) for the easy-to-use Python GUI framework
- [crinrict](https://forums.thesims.com/en_US/profile/crinrict)
    - [S3S Browser](https://sims3.crinrict.com/en/s3s-browser/downloads): inspiration on features, layout, and data
    - `SimsStoreData.xml`: used [with permission](https://forums.thesims.com/en_US/discussion/comment/7204256/#Comment_7204256) to fill out some missing item data
- All the maintainers of the [Daily Deal thread](https://forums.thesims.com/en_US/discussion/866448/daily-deal-dd-2018-rotation-list-and-sales-help/p1)s for the [spreadsheet](https://docs.google.com/spreadsheets/d/1NIeS9yIMAw-fA7VhseLilqCOV5XfKoSJXwbyyKQLJP4/edit#gid=882235701) that served as the initial seed to the catalog data
