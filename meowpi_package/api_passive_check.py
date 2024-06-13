from meowpi_package.utils import parse_domain, parse_dirs
from meowpi_package.shared import all_dirs
from meowpi_package.api_determine import api_calc, api_update_passive_score
from meowpi_package.api_wordlist import api_keywords, api_paths
from meowpi_package.args import argparser

args = argparser()

def api_pass_check():
    # try:
        if not (args.active):
            print("""\n
█▀ █▀█ ▄▀█ █▀ █▀ █ █░█ █▀▀   █▀▀ █░█ █▀▀ █▀▀ █▄▀ ▀█
█▄ █▀▀ █▀█ ▄█ ▄█ █ ▀▄▀ ██▄   █▄▄ █▀█ ██▄ █▄▄ █░█ ▄█\n""")
            for url in all_dirs[:]:
                api_score = 0
                formatted_dirs, unformatted_dirs = parse_dirs(url)
                # directory checking
                for dir in unformatted_dirs: 
                    for keyword in api_keywords:
                        if keyword in dir.lower():
                            api_score += 1
                            print(f"\033[32m[HIT]\033[0m  {url}  \033[31m[TRIGGER: {keyword}]\033[0m")

                for dir in formatted_dirs:
                    if api_paths.get(dir.lower(), False):
                        print(f"\033[32m[HIT]\033[0m  {url}  \033[31m[TRIGGER: {api_paths.get(dir.lower(), False)}]\033[0m")
                        api_score += 1
                
                # # domain checking
                for domain in parse_domain(url):
                    for keyword in api_keywords:
                        if keyword in domain.lower():
                            print(f"\033[32m[HIT]\033[0m  {url}  \033[31m[TRIGGER: {keyword}]\033[0m")
                            api_score += 1
                        
                api_update_passive_score(url, api_score)
    # except Exception as e:
    #     print(f'Error: {e}')
        api_calc()