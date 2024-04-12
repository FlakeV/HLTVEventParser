from typing import List
from typing import TypedDict

from tqdm import tqdm

from utils import get_parsed_html, BASE_URL


class Team(TypedDict):
    name: str
    link: str


class Player(TypedDict):
    nickname: str
    link: str
    team: str


def get_teams_on_event(event: int) -> List[Team]:
    url = f'{BASE_URL}/stats/teams?event={event}'

    bs_event_teams = get_parsed_html(url)

    params = {
        'class': 'stats-table player-ratings-table'
    }

    team_table = bs_event_teams.find('table', params)
    teams = []
    for team in team_table.find_all('a'):
        teams.append(Team(name=team.text, link=BASE_URL + team['href']))
    return teams


def get_team_players_and_save_stat(teams: List[Team], gs) -> List[Player]:
    players = []
    team_rows = []
    for team in tqdm(teams, desc='Teams'):
        bs_team_html = get_parsed_html(team['link'])
        stat_columns = bs_team_html.find_all('div', {'class': 'columns'})
        team_stat_list = [team['name']]
        for column in stat_columns:
            data = column.find_all('div', {'class': 'large-strong'})
            for el in data:
                team_stat_list.append(el.text)

        # Export to Google Sheet
        team_rows.append(team_stat_list)

        # Players
        players_data = bs_team_html.find('div', {'class': 'grid reset-grid'})
        for player in players_data.find_all('a', {'class': 'image-and-label'}):
            players.append(
                Player(
                    nickname=player.find('div', {'class': 'text-ellipsis'}).text,
                    link=BASE_URL + player['href'],
                    team=team['name']
                )
            )
    gs.add_rows(team_rows)
    return players


def save_player_stat(players, gs):
    players_rows = []

    for player in tqdm(players, desc='Players', dynamic_ncols=True):
        player_stat_list = [player['nickname'], player['team']]

        bs_player_html = get_parsed_html(player['link'])
        container = bs_player_html.find('div', {'class': 'summaryBreakdownContainer'})

        # Full name
        full_name = (
            container
            .find('div', {'class': 'summaryRealname text-ellipsis'})
            .find('div', {'class': 'text-ellipsis'})
            .text
        )
        player_stat_list.append(full_name)

        stat_columns = bs_player_html.find_all('div', {'class': 'col stats-rows standard-box'})[0].find_all('div', {
            'class': 'stats-row'})

        # ADR
        adr = stat_columns[4].find_all('span')[1].text
        player_stat_list.append(adr)
        # Kills
        kills = stat_columns[0].find_all('span')[1].text
        player_stat_list.append(kills)
        # Deaths
        deaths = stat_columns[2].find_all('span')[1].text
        player_stat_list.append(deaths)
        # Headshots
        headshots = stat_columns[1].find_all('span')[1].text
        player_stat_list.append(headshots)

        # Export to Google Sheets
        players_rows.append(player_stat_list)

    gs.add_rows(players_rows)


def save_team_player_stat(event_id: int, gs):
    teams = get_teams_on_event(event_id)
    players = get_team_players_and_save_stat(teams, gs)
    save_player_stat(players, gs)
