import requests
import logging as log
from datetime import date, timedelta
from time import sleep


PLAYER_ID = 8477404 # Jake Guentzel
API_URL = f"https://statsapi.web.nhl.com/api/v1/people/{PLAYER_ID}/stats?stats=gameLog"
REQUEST_TIME = "23:59:00"
TASK_SCHEDULE = True # Disables loop, set True if using Windows Task Scheduler to run .py

log.basicConfig(
    filename='log.log',
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=log.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')


if __name__ == "__main__":
    while True:
        response = requests.get(API_URL, params={"Content-Type": "application/json"})
        data = response.json()
        
        last_game: dict = data["stats"][0]["splits"][0]
        game_date: str = last_game["date"]
        
        if (game_date == date.today):
            goals: int = last_game["stat"]["goals"]
            if (goals > 0):
                log.info(f"{goals} goals scored! Scheduling text push for tomorrow.")
            else:
                log.info("No goals today")
        else:
            log.info("No game held today")
        
        if TASK_SCHEDULE:
            break
        else:
            time_til_next_request = (date.now() + timedelta(days=1)).seconds
            log.DEBUG(f"Sleeping for {time_til_next_request}s")
            sleep(time_til_next_request)
