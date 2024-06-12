from meowpi_package.args import argparser
from meowpi_package.http_probe import filter_urls
from meowpi_package.shared import all_dirs
from api_passive_check import api_check 
import asyncio

intro_logo = f"""\033[35m
        ▄───▄      
        █▀█▀█
        █▄█▄█
        ─███──▄▄
███╗░░░███╗███████╗░█████╗░░██╗░░░░░░░██╗██████╗░██╗
████╗░████║██╔════╝██╔══██╗░██║░░██╗░░██║██╔══██╗██║
██╔████╔██║█████╗░░██║░░██║░╚██╗████╗██╔╝██████╔╝██║
██║╚██╔╝██║██╔══╝░░██║░░██║░░████╔═████║░██╔═══╝░██║
██║░╚═╝░██║███████╗╚█████╔╝░░╚██╔╝░╚██╔╝░██║░░░░░██║
╚═╝░░░░░╚═╝╚══════╝░╚════╝░░░░╚═╝░░░╚═╝░░╚═╝░░░░░╚═╝

-------------------------------------------------------------------\u001b[0m"""


if __name__ == "__main__":
    args = argparser()
    with open(f'{args.file}','r') as urls:
        for line in urls:
            all_dirs.append(line.strip('\n'))
    if not (args.stdout):
        print(intro_logo)
    asyncio.run(filter_urls())
    api_check()