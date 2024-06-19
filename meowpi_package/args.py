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
    class NewlineFormatter(argparse.RawDescriptionHelpFormatter, argparse.ArgumentDefaultsHelpFormatter):
        pass

    parser = argparse.ArgumentParser(prog= f"python {get_py_filename}", description='\u001b[96mdescription: verifies and filters API urls passively and actively by default', epilog=
    f'''
    \u001b[91mbasic usage:\u001b[0m python {get_py_filename } urls.txt
    \u001b[91mfilter requests:\u001b[0m python {get_py_filename } urls.txt -m
    \u001b[91mstdout:\u001b[0m python {get_py_filename } urls.txt -S   
    ''', formatter_class=NewlineFormatter, usage=f'{intro_logo}\n\u001b[32m%(prog)s [options] file_name\u001b[0m')

    # parser.add_argument("file", help="\u001b[96mspecify file/list of urls")
    parser.add_argument("file", help="\u001b[96mspecify file/list of urls")
    parser.add_argument("-s", "--stdout", help="stdout friendly, displays urls only in stdout compatibility. also known as silent mode", action="store_true")
    parser.add_argument("-m", "--mode", help="filter modes", choices=['all', '1xx', '2xx', '3xx', '4xx', '5xx', 'forbidden'])
    parser.add_argument("-p", "--passive", help="enables passive API filtering only and disables active API probing", action="store_true")
    parser.add_argument("-a", "--active", help="enables active API probing and disables passive API filtering", action="store_true")
    parser.add_argument("--no-api-check", help="uses only http probing and no api checks", action="store_true")
    parser.add_argument("-r", "--requests", help="the number of concurrent/multiple requests per second (it is multiplied by 2 as it does both GET and POST) (default is set to 15 req/sec (without specifying) which would be actually 30)", type=int, default=15)
    
    args = parser.parse_args()
    return args