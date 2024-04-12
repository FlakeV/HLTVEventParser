import time
from typing import List, Any

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from settings import Settings

TEAMS_HEADERS = [
    'team_name',
    'Maps played',
    'Wins / draws / losses',
    'Total kills',
    'Total deaths',
    'Rounds played',
    'K/D Ratio'
]

PLAYERS_HEADERS = [
    'nickname',
    'team_name',
    'full_name',
    'ADR',
    'kills',
    'deaths',
    'headshots',
]

JSON_HEADERS = [
    'Team',
    'Nickname',
    'Kills',
    'Deaths',
    'adr',
    'kast',
    'HLTV_2.0',
]


class GoogleSheet:
    # empty sheets
    player_sheet = None
    team_sheet = None
    match_sheet = None
    parsed_json_sheet = None

    sheets_to_write = []

    def __init__(self):
        print('Connecting to Google Sheets...')
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive.file',
            'https://www.googleapis.com/auth/drive'
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name('google_sheets/credentials.json', scope)
        client = gspread.authorize(creds)
        self.file = client.open(Settings.gs_sheet_name)
        self.teams_stat_sheet_name = 'Команды'
        self.players_stat_sheet_name = 'Игроки'
        self.match_sheet_name = 'Матчи'
        self.parsed_json_sheet_name = 'Матч из JSON'

    def prepare_sheets_by_parse_type(self, parse_type: int):
        if parse_type == 1:
            self._prepare_sheet()
            self.player_sheet = self.file.worksheet(self.players_stat_sheet_name)
            self.team_sheet = self.file.worksheet(self.teams_stat_sheet_name)
        elif parse_type == 2:
            self._prepare_match_sheet()
            self.match_sheet = self.file.worksheet(self.match_sheet_name)
        elif parse_type == 3:
            self._prepare_parsed_json_sheet()
            self.parsed_json_sheet = self.file.worksheet(self.parsed_json_sheet_name)

    def _prepare_sheet(self):
        print('Preparing stat sheets...')
        try:
            self.file.worksheet(self.teams_stat_sheet_name)
        except gspread.exceptions.WorksheetNotFound:
            self.file.add_worksheet(self.teams_stat_sheet_name, 0, 0)
        try:
            self.file.worksheet(self.players_stat_sheet_name)
        except gspread.exceptions.WorksheetNotFound:
            self.file.add_worksheet(self.players_stat_sheet_name, 0, 0)

        player_sheet = self.file.worksheet(self.players_stat_sheet_name)
        player_sheet.clear()
        player_sheet.append_row(PLAYERS_HEADERS)
        team_sheet = self.file.worksheet(self.teams_stat_sheet_name)
        team_sheet.clear()
        team_sheet.append_row(TEAMS_HEADERS)

        self.sheets_to_write = [player_sheet, team_sheet]

    def _prepare_match_sheet(self):
        print('Preparing match sheet...')
        try:
            self.file.worksheet(self.match_sheet_name)
        except gspread.exceptions.WorksheetNotFound:
            self.file.add_worksheet(self.match_sheet_name, 0, 0)
            return

        sheet = self.file.worksheet(self.match_sheet_name)
        sheet.clear()

        self.sheets_to_write = [sheet]

    def _prepare_parsed_json_sheet(self):
        print('Preparing parsed json sheet...')
        try:
            self.file.worksheet(self.parsed_json_sheet_name)
        except gspread.exceptions.WorksheetNotFound:
            self.file.add_worksheet(self.parsed_json_sheet_name, 0, 0)

        sheet = self.file.worksheet(self.parsed_json_sheet_name)
        sheet.clear()

        # add headers to sheet
        sheet.append_row(JSON_HEADERS)

        self.sheets_to_write = [sheet]

    def add_rows(self, rows: List[List[Any]]):
        sheet = self.sheets_to_write.pop()
        sheet.append_rows(rows)
