from meowpi_package.shared import api_active_scoreboard, api_passive_scoreboard, api_scoreboard, api_score
from meowpi_package.args import argparser

args = argparser()

def api_calc():
    print("""\n\n
█▀ ▄▀█ █▀█ █   █▀▀ █▄░█ █▀▄ █▀█ █▀█ █ █▄░█ ▀█▀ █▀ ▀█
█▄ █▀█ █▀▀ █   ██▄ █░▀█ █▄▀ █▀▀ █▄█ █ █░▀█ ░█░ ▄█ ▄█\n""")
    
    if not (args.passive):
        for active_endpoint,active_score in api_active_scoreboard.items():
            active_endpoint_verified = api_passive_scoreboard.get(active_endpoint, False)
            if (active_endpoint_verified):
                api_scoreboard[active_endpoint] = active_score + active_endpoint_verified
            elif (active_score >= 1.4):
                api_scoreboard[active_endpoint] = active_score

    if not (args.passive):
        for endpoint,total_points in api_scoreboard.items():
            active_points = api_active_scoreboard.get(endpoint, False)
            passive_points = api_passive_scoreboard.get(endpoint, False)
            if (args.active):
                passive_points = 100
            if (active_points >= 3 and passive_points >= 0):
                print(f"\033[34m[API] \033[95m[multi-method]\033[0m  {endpoint}")
            elif (active_points >= 2 and passive_points >= 0):
                print(f"\033[34m[API] \033[32m[bi-method]\033[0m  {endpoint}")
            elif (active_points < 2 and passive_points >= 2):
                print(f"\033[34m[API] \033[31m[single-method]\033[0m  {endpoint}")
            else:
                print(f"\033[34m[POSSIBLE API] \033[31m[single-method]\033[0m  {endpoint}")

    if (args.passive):
        for endpoint,points in api_passive_scoreboard.items():
            
            if (points == 1):
                print(f"\033[34m[POSSIBLE API]\033[0m  {endpoint}")
                api_scoreboard[endpoint] = points
            elif (points > 1):
                print(f"\033[34m[API]\033[0m  {endpoint}")
                api_scoreboard[endpoint] = points

    print(f' APIs Found: {len(api_scoreboard.keys())}')

  
def api_update_active_score(url, points):
    api_active_scoreboard.update({f"{url}":api_score + points})

def api_update_passive_score(url, points):
    api_passive_scoreboard.update({f"{url}":api_score + points})