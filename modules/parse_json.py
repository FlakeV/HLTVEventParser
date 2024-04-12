import json
from typing import Dict, List

from google_sheets.google_sheet_int import GoogleSheet
from config.settings import Settings


def dict_to_list(data: Dict) -> List:
    return [
        data['Team'],
        data['Nickname'],
        data['Kills'],
        data['Deaths'],
        data['Assists'],
        data['adr'],
        data['kast'],
        data['HLTV_2.0']
    ]


def parse_json_file(filename: str) -> List[Dict]:
    with open(filename) as f:
        return json.load(f)


def export_data_from_json(gs: GoogleSheet) -> None:
    json_filename = Settings.json_file_name
    json_file_path = Settings.json_file_path

    try:
        json_data = parse_json_file(f'{json_file_path}/{json_filename}')
    except FileNotFoundError:
        print(f'File {json_filename} not found')
        return

    rows = []
    for data in json_data:
        rows.append(dict_to_list(data))

    gs.add_rows(rows)
