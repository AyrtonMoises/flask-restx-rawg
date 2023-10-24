import requests
from datetime import datetime, timedelta
import os


BASE_URL_RAWG = os.getenv('BASE_URL_RAWG')
API_KEY_RAWG = os.getenv('API_KEY_RAWG')


class ApiRAWG:

    def __init__(self):
        self._base_url = BASE_URL_RAWG
        self._params = {"key": API_KEY_RAWG}
        self.current_date = datetime.now()

    def game_search(self, game_name):
        """Get a list of games matching the given name."""
        url = f"{self._base_url}/games"
        
        params = {
            "search": game_name,
            "page_size": 10
        }
        params.update(self._params)

        response = requests.get(url, params=params)
        response.raise_for_status()
        json_data_game = response.json()
        data_results = []
        for game in json_data_game['results']:
            platforms = [] if game.get('platforms',[]) is None else game['platforms']
            data = {
                'id': game['id'],
                'name': game['name'],
                'metacritic': game['metacritic'],
                'released': game['released'],
                'background_image': game['background_image'],
                'platforms': [platform['platform']['slug'] for platform in platforms]
            }
            data_results.append(data)
        return data_results, response.status_code

    def game_details(self, id_game):
        """Get details of a specific game by ID"""
        url = f"{self._base_url}/games/{id_game}"
        
        response = requests.get(url, params=self._params)

        if response.status_code == 404:
            return {}

        json_data_game = response.json()
        data = {
            'id': json_data_game['id'],
            'name': json_data_game['name'],
            'metacritic': json_data_game['metacritic'],
            'released': json_data_game['released'],
            'background_image': json_data_game['background_image'],
            'platforms': [platform['platform']['slug'] for platform in json_data_game['platforms']]
            
        }
        return data

    def game_screenshots(self, id_game):
        """Get screenshots of game by ID"""
        url = f"{self._base_url}/games/{id_game}/screenshots"
        
        response = requests.get(url, params=self._params)
        response.raise_for_status()

        json_data_game = response.json()
        list_games = [photo['image'] for photo in json_data_game['results']]
        return list_games

    def games_most_popular_by_current_year(self):
        """Get game most popular by current year"""
        url = f"{self._base_url}/games?dates={self.current_date.year}-01-01,{self.current_date.year}-12-31&ordering=-added"
        params = {"page_size": 15}
        params.update(self._params)

        response = requests.get(url, params=params)
        response.raise_for_status()
        json_data_game = response.json()
        games = []
        for game in json_data_game['results']:
            game_dict = {}
            game_dict['id'] = game['id']
            game_dict['name'] = game['name']
            game_dict['metacritic'] = game['metacritic']
            game_dict['released'] = game['released']
            game_dict['background_image'] = game['background_image']
            game_dict['platforms'] = [
                platform['platform']['slug'] for platform in game['platforms']
            ]
            games.append(game_dict)
        return games

    def games_most_awaited_by_current_year(self):
        """Get game most awaited by current year"""
        today = datetime.today().strftime('%Y-%m-%d')
        url = f"{self._base_url}/games?dates={today},{self.current_date.year}-12-31&ordering=-added"
        params = {"page_size": 15}
        params.update(self._params)

        response = requests.get(url, params=params)
        response.raise_for_status()
        json_data_game = response.json()
        games = []
        for game in json_data_game['results']:
            game_dict = {}
            game_dict['id'] = game['id']
            game_dict['name'] = game['name']
            game_dict['metacritic'] = game['metacritic']
            game_dict['released'] = game['released']
            game_dict['background_image'] = game['background_image']
            game_dict['platforms'] = [
                platform['platform']['slug'] for platform in game['platforms']
            ]
            games.append(game_dict)
        return games

    def games_most_popular_released_last_30_days(self):
        """Get games most popular released last 30 days on main platforms"""

        """ Platforms
            4 - PC
            1 - Xbox One
            186 - Xbox Series
            18 - Playstation 4
            187 - Plastation 5
            7 - Nintendo Switch
        """
        all_platforms = (
            (4, "pc"),
            (1, "xbox-one"),
            (186, "xbox-series-x"),
            (18, "playstation4"),
            (187, "playstation5"),
            (7, "nintendo-switch")
        )

        params = {"page_size": 5}
        params.update(self._params)

        date_initial = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        data_final = self.current_date.strftime('%Y-%m-%d')

        data_results = {}

        for id_platform, slug in all_platforms:
            data_results[slug] = []
            url = f"{self._base_url}/games?dates={date_initial},{data_final}&platforms={id_platform}&ordering=-added"

            response = requests.get(url, params=params)
            response.raise_for_status()
            json_data_game = response.json()
            
            for game in json_data_game['results']:
                game_dict = {}
                game_dict['id'] = game['id']
                game_dict['name'] = game['name']
                game_dict['metacritic'] = game['metacritic']
                game_dict['released'] = game['released']
                game_dict['background_image'] = game['background_image']
                
                data_results[slug].append(game_dict)

        return data_results
