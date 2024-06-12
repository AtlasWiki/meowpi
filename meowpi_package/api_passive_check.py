from meowpi_package.utils import parse_domain, parse_dirs
from meowpi_package.shared import all_dirs
from meowpi_package.api_determine import api_calc, api_update_passive_score


def api_pass_check():
    
    print("""\n
█▀ █▀█ ▄▀█ █▀ █▀ █ █░█ █▀▀   █▀▀ █░█ █▀▀ █▀▀ █▄▀ ▀█
█▄ █▀▀ █▀█ ▄█ ▄█ █ ▀▄▀ ██▄   █▄▄ █▀█ ██▄ █▄▄ █░█ ▄█\n""")
    
    for url in all_dirs[:]:
        api_score = 0
        *formatted_dirs, unformatted_dirs = parse_dirs(url)
        # directory checking
        for dir in unformatted_dirs: 
            if not "auth" in dir:
                print(f"\033[31m[NO MATCH]\033[0m  {url}")
                pass
            elif "auth" in dir:
                print(f"\033[32m[KEYWORD HIT]\033[0m  {url}")
                api_score += 1
                # api_update_passive_score(url, 1)
            elif "rest" in dir:
                api_score += 1
                print(f"\033[32m[KEYWORD HIT]\033[0m  {url}")
           
        # domain checking
        for domain in parse_domain(url):
            if "api" in domain.lower():
                print(f"\033[32m[KEYWORD HIT]\033[0m  {url}")
                api_score += 1
                # api_update_passive_score(url, 1)
        api_update_passive_score(url, api_score)

    api_calc()