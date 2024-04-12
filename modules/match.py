from utils import get_parsed_html, BASE_URL


def side_generator():
    sides = ['all', 'ct', 't']
    i = 0
    while True:
        yield sides[i]
        if i == 2:
            i = 0
        else:
            i += 1


def get_match_data(match_id: int, gs):
    url = f'{BASE_URL}/matches/{match_id}/page'

    bs_event_teams = get_parsed_html(url)
    rows_to_write = [['map', 'side', 'team', 'player', 'K-D', '+/-', 'ADR', 'KAST', 'Rating']]
    # getmaps from match
    maps = []
    for csmap in bs_event_teams.find_all('div', {'class': 'stats-menu-link'}):
        maps.append(csmap.find_all('div')[1].text)

    # get match data
    for csmap, csmap_stat in zip(maps, bs_event_teams.find_all('div', {'class': 'stats-content'})):
        side_gen = side_generator()
        for table in csmap_stat.find_all('table'):
            side = next(side_gen)
            team = table.find('a', {'class': 'teamName team'}).text
            for row in table.find_all('tr')[1:]:
                player_stat = []
                for cell in row.find_all('td'):
                    name = cell.find('span', {'class': 'player-nick'})
                    if name:
                        player_stat.append(name.text.strip())
                    else:
                        player_stat.append(cell.text.strip())
                rows_to_write.append([csmap, side, team] + player_stat)
    gs.add_rows(rows_to_write)


def save_match_data(match_id, gs):
    get_match_data(match_id, gs)
