#!/usr/bin/env python3
from meowpi_package.args import argparser
from meowpi_package.api_active_check import api_act_check
from meowpi_package.shared import all_dirs, http_messages
from meowpi_package.api_passive_check import api_pass_check 
import asyncio, sys
from ansi2html import Ansi2HTMLConverter
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
    try:
        with open(f'{args.file}','r') as urls:
            for line in urls:
                all_dirs.append(line.strip('\n'))
    except Exception:
        if not (args.stdout):
            print(intro_logo)
            print("If stuck hanging insert CTRL + D or CTRL + Z or even CTRL + C. This likely happens due to invalid stdin/input/args")
        for url in sys.stdin:
            all_dirs.append(url.strip("\n"))
    if not (args.stdout or args.no_logo):
        print(intro_logo)
    if not (args.passive):
        asyncio.run(api_act_check())
    if not (args.no_api_check):
        api_pass_check()

if args.save_html:
    http_messages = '\n'.join(http_messages)
    converter = Ansi2HTMLConverter()
    html = converter.convert(http_messages)
    with open('target-urls.html', 'w') as file:
        file.write(html)
