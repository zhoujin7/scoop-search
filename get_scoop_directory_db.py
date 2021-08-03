import logging
import requests
from pathlib import Path
from shutil import copy2

scoop_directory_db = Path(__file__).resolve().parent.joinpath('scoop_directory.db')
scoop_directory_db_bak = Path(__file__).resolve().parent.joinpath('scoop_directory.db.bak')
if Path(scoop_directory_db).exists() and Path(scoop_directory_db).stat().st_size != 0:
    copy2(scoop_directory_db, scoop_directory_db_bak)
with open(scoop_directory_db, 'wb') as file:
    try:
        response = requests.get(
            'https://raw.githubusercontent.com/zhoujin7/crawl-scoop-directory/master/scoop_directory.db')
    except Exception as e:
        logging.warning(e)
        if Path(scoop_directory_db_bak).exists():
            copy2(scoop_directory_db_bak, scoop_directory_db)
    else:
        if response.content:
            file.write(response.content)
