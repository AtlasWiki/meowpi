import argparse

# get_py_filename = os.path.basename(__file__)
get_py_filename = "meowpi.py"
def argparser():
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
    intro_logo = ""
    class NewlineFormatter(argparse.RawDescriptionHelpFormatter, argparse.ArgumentDefaultsHelpFormatter):
        pass

    parser = argparse.ArgumentParser(prog= f"python {get_py_filename}", description='\u001b[96mdescription: verifies and filters API urls passively and actively by default', epilog=
    f'''
    \u001b[91mbasic usage:\u001b[0m python {get_py_filename } -i urls.txt
    \u001b[91mfilter requests:\u001b[0m python {get_py_filename } -i urls.txt -m
    \u001b[91mstdout:\u001b[0m python {get_py_filename } -i urls.txt -s
    \u001b[91mjson-reports:\u001b[0m python {get_py_filename } -i urls.txt -j all   
    ''', formatter_class=NewlineFormatter, usage=f'{intro_logo}\n\u001b[32m%(prog)s [options] -i file_name\u001b[0m')

    parser.add_argument("-i", "--file", help="\u001b[96mspecify file/list of urls")
    parser.add_argument("-s", "--stdout", help="stdout friendly, displays urls only in stdout compatibility. also known as silent mode", action="store_true")
    parser.add_argument("-f", "--filter", help="filter modes", choices=['all', '1xx', '2xx', '3xx', '4xx', '5xx', 'forbidden'])
    parser.add_argument("-m", "--method", help="Display method(s) options: all, only_safe, only_unsafe, GET, POST, PATCH, PUT, DELETE, OPTIONS, HEAD. Default is only_safe", nargs="+", default=["only_safe"])
    parser.add_argument("-p", "--passive", help="enables passive API filtering only and disables active API probing", action="store_true")
    parser.add_argument("-a", "--active", help="enables active API probing and disables passive API filtering", action="store_true")
    parser.add_argument("--no-api-check", help="uses only http probing and no api checks", action="store_true")
    parser.add_argument('-j', '--json-report', help="output a file in json to show a report of all endpoints", choices=['all', 'no-http-headers'])
    parser.add_argument("-r", "--requests", help="the number of concurrent/multiple requests per second (it is multiplied by 2 as it does both GET and POST) (default is set to 15 req/sec (without specifying) which would be actually 30)", type=int, default=15)
    parser.add_argument("-n", "--no-logo", help="remove logo", action="store_true")
    parser.add_argument("-x", "--save-html", help="saves an html screenshot of the results", action="store_true")
    args = parser.parse_args()

    if args.method:
        args.method = ",".join(args.method).split(",")
    return args