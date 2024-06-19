#!/usr/bin/env python3
from meowpi_package.args import argparser
from meowpi_package.api_active_check import api_act_check
from meowpi_package.shared import all_dirs
from meowpi_package.api_passive_check import api_pass_check 
import asyncio, sys

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
    # try:
    with open(f'{args.file}','r') as urls:
        for line in urls:
            all_dirs.append(line.strip('\n'))
    # except Exception:
    #     for url in sys.stdin:
    #         all_dirs.append(url.strip("\n"))

    if not (args.stdout):
        print(intro_logo)
    if not (args.passive):
        asyncio.run(api_act_check())
    if not (args.no_api_check):
        api_pass_check()