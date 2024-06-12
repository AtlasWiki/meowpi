from meowpi_package.utils import parse_domain, parse_dirs
from meowpi_package.shared import all_dirs, dict_report, to_remove, to_add

def api_check():
    for dir in all_dirs[:]:
        *formatted_dir, unformatted_dir = parse_dirs(dir)
    for dir in all_dirs[:]:
        for domain in parse_domain(dir):
            if "api" in domain.lower():
                print(domain)
    