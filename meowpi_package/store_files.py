import asyncio, json, jsbeautifier
from .args import argparser
from .utils import(
    remove_dupes,
    clean_urls
    )
from .shared import(
    all_dirs,
    target,
    dict_report
    )
args = argparser()

def write_files():
    with open(f"""{target["domain"]}/all_urls.txt""", "w", encoding="utf-8") as directories:
        directories.write('')
    with open(f"""{target["domain"]}/all_urls.txt""", "a", encoding="utf-8") as directories:
        print()
        for unique_dir in all_dirs:
            directories.write(clean_urls(unique_dir) + '\n')
    if (args.json_report):
        json_report = json.dumps(dict_report)
        beautified_json_report = jsbeautifier.beautify(str(json_report))
        with open(f"""{target["domain"]}/url_report.json""", "w", encoding="utf-8") as directories:
            directories.write(beautified_json_report)