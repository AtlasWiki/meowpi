from meowpi_package.shared import api_active_scoreboard, api_passive_scoreboard, api_scoreboard, api_score


def api_calc():
    print("""\n\n
█▀ ▄▀█ █▀█ █   █▀▀ █▄░█ █▀▄ █▀█ █▀█ █ █▄░█ ▀█▀ █▀ ▀█
█▄ █▀█ █▀▀ █   ██▄ █░▀█ █▄▀ █▀▀ █▄█ █ █░▀█ ░█░ ▄█ ▄█\n""")
    
    for active_endpoint,active_score in api_active_scoreboard.items():
        active_endpoint_verified = api_passive_scoreboard.get(active_endpoint, False)
        if (active_endpoint_verified):
            api_scoreboard[active_endpoint] = active_score + active_endpoint_verified
        elif (active_score >= 2):
            api_scoreboard[active_endpoint] = active_score
    
    for endpoint in api_scoreboard.keys():
        print(f"\033[34m[API]\033[0m  {endpoint}")
    # print(api_scoreboard)
        

def api_update_score(url, points): # active
    api_active_scoreboard.update({f"{url}":api_score + points})

def api_update_passive_score(url, points):
    api_passive_scoreboard.update({f"{url}":api_score + points})