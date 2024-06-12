from meowpi_package.utils import parse_domain, parse_dirs
from meowpi_package.shared import all_dirs, dict_report, to_remove, to_add

def api_check():
    api_scoreboard = {}
    for url in all_dirs[:]:
        *formatted_dirs, unformatted_dirs = parse_dirs(url)
        for dir in unformatted_dirs: 
            if not "auth" in dir:
                pass
            elif "auth" in dir:
                print(f"[API] [KEYWORD HIT] {url}")
                api_scoreboard.update({f"{url}":1})
            else:
                for domain in parse_domain(url):
                    if "api" in domain.lower():
                        print(f"[API] [KEYWORD HIT] {url}")
                        api_scoreboard.update({f"{url}":1})

    print(api_scoreboard)