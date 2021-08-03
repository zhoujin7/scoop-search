import logging
from pathlib import Path
from shutil import copy2

import requests

db = Path(__file__).resolve().parent.joinpath('scoop_directory.db')
db_bak = Path(__file__).resolve().parent.joinpath('scoop_directory.db.bak')
if Path(db).exists() and Path(db).stat().st_size != 0:
    copy2(db, db_bak)
with open(db, 'wb') as file:
    try:
        response = requests.get(
            'https://raw.githubusercontent.com/zhoujin7/crawl-scoop-directory/master/scoop_directory.db')
    except Exception as e:
        logging.warning(e)
        if Path(db_bak).exists():
            copy2(db_bak, db)
    else:
        if response.content:
            file.write(response.content)
