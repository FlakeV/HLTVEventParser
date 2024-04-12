import time

from google_sheets.google_sheet_int import GoogleSheet
from modules.match import save_match_data
from modules.parse_json import export_data_from_json
from modules.team_player import save_team_player_stat

if __name__ == '__main__':
    gs = GoogleSheet()
    while True:
        parse_type = int(input('Enter parse type, 1 - for event, 2 - for match, 3 - for export from json, 0 - exit: '))
        if parse_type == 1:
            try:
                event_id = int(input('Enter event id: '))
                start_time = time.time()
                gs.prepare_sheets_by_parse_type(1)
                print('Getting data...')
                save_team_player_stat(event_id, gs)
                print(f'{time.time() - start_time:.2f} seconds')
            except ValueError:
                print('Wrong input')
                continue
        elif parse_type == 2:
            try:
                match_id = int(input('Enter match id: '))
                start_time = time.time()
                gs.prepare_sheets_by_parse_type(2)
                print('Getting data...')
                save_match_data(match_id, gs)
                print(f'{time.time() - start_time:.2f} seconds')
            except ValueError:
                print('Wrong input')
                continue
        elif parse_type == 3:
            print('export data from json')
            gs.prepare_sheets_by_parse_type(3)
            export_data_from_json(gs)
            print('Done')
        elif parse_type == 0:
            break
        else:
            print('Wrong input')
