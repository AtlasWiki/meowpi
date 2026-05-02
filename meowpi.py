#!/usr/bin/env python3
from meowpi_package.args import argparser
from meowpi_package.api_active_check import api_act_check
from meowpi_package.shared import all_dirs, http_messages, dict_report, api_scoreboard
from meowpi_package.api_passive_check import api_pass_check 
import asyncio, sys, json, os
from ansi2html import Ansi2HTMLConverter

intro_logo = f"""\033[35m
        ▄───▄      
        █▀█▀█
        █▄█▄█
        ─███──▄▄
███╗░░░███╗███████╗░█████╗░░██╗░░░░░░░██╗██████╗░██╗
████╗░████║██╔════╝██╔══██╗░██║░░██╗░░██║██╔══██╗██║
██╔████╔██║█████╗░░██║░░██║░╚██╗████╗██╔╝██████╔╝██║
██║╚██╔╝██║██▔══╝░░██║░░██║░░████╔═████║░██╔═══╝░██║
██║░╚═╝░██║███████╗╚█████╔╝░░╚██╔╝░╚██╔╝░██║░░░░░██║
╚═╝░░░░░╚═╝╚══════╝░╚════╝░░░░╚═╝░░░╚═╝░░╚═╝░░░░░╚═╝

-------------------------------------------------------------------\u001b[0m"""


def export_urlmapper_json(output_path="urlmapper_data.json"):
    """
    Exports a structured JSON file for urlmapper.html to consume.
    Merges dict_report (active HTTP probe data) with api_scoreboard (passive scores).
    """
    export = {
        "endpoints": {},
        "api_scores": dict(api_scoreboard)
    }

    for url, data in dict_report.items():
        entry = {
            "url": url,
            "requests": {},
            "headers": data.get("headers", {}),
            "final_location": data.get("final_location", ""),
            "is_api": url in api_scoreboard,
            "api_score": api_scoreboard.get(url, 0)
        }

        for method, method_data in data.get("requests", {}).items():
            if method_data:  # skip empty method dicts
                entry["requests"][method] = {
                    "code": method_data.get("code", None),
                    "message": method_data.get("message", ""),
                    # content-type pulled from top-level headers (shared across methods in current design)
                    "content_type": data.get("headers", {}).get("Content-Type", 
                                    data.get("headers", {}).get("content-type", ""))
                }

        export["endpoints"][url] = entry

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(export, f, indent=2)

    if not args.stdout:
        print(f"\n\033[32m[urlmapper]\033[0m  Exported {len(export['endpoints'])} endpoints → \033[96m{output_path}\033[0m")
        print(f"\033[32m[urlmapper]\033[0m  Open \033[96murlmapper.html\033[0m and load this file to visualize.\n")


if __name__ == "__main__":
    args = argparser()

    # Load URLs from file
    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8", errors="ignore") as urls:
                for line in urls:
                    line = line.strip()
                    if line:
                        all_dirs.append(line)

        except Exception as e:
            if not args.stdout:
                print(intro_logo)
            print(f"\n\033[31m[ERROR]\033[0m Failed to open input file: {args.file}")
            print(f"\033[31m[ERROR]\033[0m Reason: {e}\n")
            sys.exit(1)

    # If no file was given, read stdin
    else:
        if not args.stdout:
            print(intro_logo)
            print("\033[33m[INFO]\033[0m No input file provided, reading from stdin...")
            print("\033[33m[INFO]\033[0m Paste URLs then press CTRL+Z + Enter (Windows) or CTRL+D (Linux/Mac)\n")

        for url in sys.stdin:
            url = url.strip()
            if url:
                all_dirs.append(url)

    # Print logo only once
    if not (args.stdout or args.no_logo):
        print(intro_logo)

    # Run checks
    if not args.passive:
        asyncio.run(api_act_check())

    if not args.no_api_check:
        api_pass_check()

    # Export JSON
    if args.json_report:
        export_urlmapper_json()

    # Optional HTML output
    if args.save_html:
        http_messages_str = "\n".join(http_messages)
        converter = Ansi2HTMLConverter()
        html = converter.convert(http_messages_str)

        with open("target-urls.html", "w", encoding="utf-8") as file:
            file.write(html)