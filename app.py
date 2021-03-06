import hashlib
import hmac
import os
import sqlite3
import subprocess
from pathlib import Path

from flask import Flask, request

app = Flask(__name__)


@app.route('/search', methods=['POST'])
def search():
    app_name = request.get_json().get('app_name')
    if app_name:
        scoop_directory_db = Path(__file__).resolve().parent.joinpath('scoop_directory.db')
        conn = sqlite3.connect(scoop_directory_db)
        with conn:
            scoop_apps = conn.execute(
                "SELECT * FROM main.app WHERE name LIKE ? ORDER BY version DESC", ('%' + app_name + '%',)
            ).fetchall()
        conn.close()

        def max_length_of_line(arr):
            max_len = 0
            for line in arr:
                if len(line) > max_len:
                    max_len = len(line)
            return max_len

        def format_arr(arr):
            max_len = max_length_of_line(arr)
            for i in range(len(arr)):
                line = arr[i]
                if len(line) != max_len:
                    arr[i] = f"{line}{' ' * (max_len - len(line))}"

        app_names = []
        app_versions = []
        app_bucket_repos = []
        app_names.append('app_name')
        app_versions.append('app_version')
        app_bucket_repos.append('bucket_repo')
        for scoop_app in scoop_apps:
            app_names.append(scoop_app[1])
            app_versions.append(scoop_app[2])
            app_bucket_repos.append(scoop_app[5])
        format_arr(app_names)
        format_arr(app_versions)
        format_arr(app_bucket_repos)

        query_result = ''
        i = 0
        while i < len(app_names):
            if i < len(app_names) - 1:
                query_result += f'{app_names[i]}\t{app_versions[i]}\t{app_bucket_repos[i]}' + '\n'
            else:
                query_result += f'{app_names[i]}\t{app_versions[i]}\t{app_bucket_repos[i]}'
            i += 1
        return query_result
    else:
        return ''


@app.route('/update_db', methods=['POST'])
def update_db():
    secret = os.environ.get("GITHUB_WEBHOOK_SECRET")
    signature_header = request.headers.get('X-Hub-Signature')
    if is_validated(secret, signature_header, request.data):
        get_scoop_directory_db = Path(__file__).resolve().parent.joinpath('get_scoop_directory_db.py')
        subprocess.Popen(['python3', get_scoop_directory_db])
        return {'result': 'success'}
    return {'result': 'fail'}


def is_validated(secret, signature_header, payload):
    key = bytes(secret, 'utf-8')
    signature = hmac.new(key=key, msg=payload, digestmod=hashlib.sha1).hexdigest()
    if signature_header:
        req_signature = signature_header.partition('=')[2]
        if req_signature == signature:
            return True
    return False


if __name__ == '__main__':
    app.run()
