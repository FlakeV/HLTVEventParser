import time

from google_sheets.google_sheet_int import GoogleSheet
from modules.parse_json import export_data_from_json
from modules.parse_match import save_match_data
from modules.parse_teams_players import save_team_player_stat


class Choice:
    EVENT = 1
    MATCH = 2
    EXPORT_JSON = 3
    EXIT = 0


class App:
    gs = GoogleSheet()

    def run(self):
        while True:
            parse_type = int(
                input('Enter parse type, 1 - for event, 2 - for match, 3 - for export from json, 0 - exit: ')
            )
            if parse_type == Choice.EVENT:
                try:
                    event_id = int(input('Enter event id: '))
                    self.gs.prepare_sheets_by_parse_type(1)
                    save_team_player_stat(event_id, self.gs)
                except ValueError:
                    print('Wrong input')
                    continue
            elif parse_type == Choice.MATCH:
                try:
                    match_id = int(input('Enter match id: '))
                    self.gs.prepare_sheets_by_parse_type(2)
                    print('Getting data...')
                    save_match_data(match_id, self.gs)
                except ValueError:
                    print('Wrong input')
                    continue
            elif parse_type == Choice.EXPORT_JSON:
                print('export data from json')
                self.gs.prepare_sheets_by_parse_type(3)
                export_data_from_json(self.gs)
                print('Done')
            elif parse_type == Choice.EXIT:
                break
            else:
                print('Wrong input')


if __name__ == '__main__':
    app = App()
    app.run()
