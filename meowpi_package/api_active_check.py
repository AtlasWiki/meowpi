from meowpi_package.statuses import(
    allowed_status_codes, 
    blocked_status_codes, 
    colored_status_codes, 
    one_x_x_codes, 
    two_x_x_codes, 
    three_x_x_codes, 
    four_x_x_codes,
    five_x_x_codes, 
    forbidden_x_x_codes,
    http_status_codes
)
import httpx, time, asyncio
from tqdm import tqdm
# from meowpi_package.utils import create_report
from meowpi_package.args import argparser
from meowpi_package.utils import parse_domain, parse_dirs
from meowpi_package.shared import all_dirs, to_remove, to_add
from meowpi_package.api_determine import api_update_active_score
from meowpi_package.json_report import report_maker

args = argparser()
if (args.json_report):
    report = report_maker()

async def fetch_dir(client, dir):
    try:
        api_score = 0
        if (args.json_report):
            report = report_maker()
            # initalize parent keys for the dictionary
            report.create_dict(dir)
        # initalize response objects and other variables
        get_response, post_response, patch_response, put_response, delete_response, head_response, options_response = "","","","","","",""
        get_status, post_status, patch_status, put_status, delete_status, head_status, options_status = "","","","","","",""
        get_file_type, post_file_type, patch_file_type, put_file_type, delete_file_type, head_file_type, options_file_type = '','','','','','',''
        # colors
        get_status_color, post_status_color, head_status_color, options_status_color = "","","",""
        put_status_color, patch_status_color, options_status_color = "","",""
        # colored text
        get_status_colored_message, post_status_colored_message, head_status_colored_message, options_status_colored_message = "","","",""
        put_status_colored_message, patch_status_colored_message, delete_status_colored_message = "","",""
        # conditions
        get_status_verified, post_status_verified, head_status_verified, options_status_verified, = "", "", "", ""
        put_status_verified, patch_status_verified, delete_status_verified = "", "", ""
        # message strips
        get_status_message_strip, post_status_message_strip, head_status_colored_message, options_status_colored_message = "","","",""
        put_status_message_strip, patch_status_message_strip, delete_status_message_strip = "","",""
        
        # initalize global message objects
        reset_color = '\033[0m'
        verified_message_strip = f"\033[33m[Verified]{reset_color} "
        http_message = verified_message_strip

        # update respones objects and variables
        if (args.method):
            for method in args.method:

                if (method.lower() == "get" or method.lower() == "only_safe" or method.lower() == "all"):
                    get_response = await client.get(dir)
                    get_status = str(get_response.status_code)
                    get_status_color = str(colored_status_codes.get(get_status[0]))
                    get_status_colored_message =  get_status_color + get_status
                    get_status_verified = allowed_status_codes.get(f'{get_status}', False)
                    # get_status_blocked = blocked_status_codes.get(f'{get_status}', False)
                    try:
                        get_file_type = get_response.headers.get("Content-Type").split(';')[0]
                        if (get_file_type == "application/json"):
                            api_score += 0.2
                    except: 
                        get_file_type = get_response.headers.get("Content-Type")
                    get_status_message_strip = f"{get_status_color}[{get_status_colored_message}][GET]{reset_color} \033[34m[{get_file_type}]\033[0m  "

                if (method.lower() == "post" or method.lower() == "only_safe" or method.lower() == "all"):
                    post_response = await client.post(dir)
                    post_status = str(post_response.status_code)
                    post_status_color = str(colored_status_codes.get(post_status[0]))
                    post_status_colored_message = post_status_color + post_status
                    post_status_verified = allowed_status_codes.get(f'{post_status}', False)
                    try:
                        post_file_type = post_response.headers.get("Content-Type").split(';')[0]
                        if (post_file_type == "application/json"):
                            api_score += 0.2
                    except: 
                        post_file_type = post_response.headers.get("Content-Type")
                    post_status_message_strip = f"{post_status_color}[{post_status_colored_message}][POST]{reset_color} \033[34m[{post_file_type}] \033[0m  "

                if (method.lower() == "patch" or method.lower() == "only_unsafe" or method.lower() == "all"):
                    patch_response = await client.patch(dir)
                    patch_status = str(patch_response.status_code)
                    patch_status_color = str(colored_status_codes.get(patch_status[0]))
                    patch_status_colored_message = patch_status_color + patch_status
                    patch_status_verified = allowed_status_codes.get(f'{patch_status}', False)
                    try:
                        patch_file_type = patch_response.headers.get("Content-Type").split(';')[0]
                        if (patch_file_type == "application/json"):
                            api_score += 0.2
                    except: 
                        patch_file_type = patch_response.headers.get("Content-Type")
                    patch_status_message_strip = f"{patch_status_color}[{patch_status_colored_message}][PATCH]{reset_color} \033[34m[{patch_file_type}] \033[0m  "

                if (method.lower() == "put" or method.lower() == "only_unsafe" or method.lower() == "all"):
                    put_response = await client.put(dir)
                    put_status = str(put_response.status_code)
                    put_status_color = str(colored_status_codes.get(put_status[0]))
                    put_status_colored_message = put_status_color + put_status
                    put_status_verified = allowed_status_codes.get(f'{put_status}', False)
                    try:
                        put_file_type = put_response.headers.get("Content-Type").split(';')[0]
                        if (put_file_type == "application/json"):
                            api_score += 0.2
                    except: 
                        put_file_type = put_response.headers.get("Content-Type")
                    put_status_message_strip = f"{put_status_color}[{put_status_colored_message}][PUT]{reset_color} \033[34m[{put_file_type}] \033[0m  "

                if (method.lower() == "delete" or method.lower() == "only_unsafe" or method.lower() == "all"):
                    delete_response = await client.delete(dir)
                    delete_status = str(delete_response.status_code)    
                    delete_status_color = str(colored_status_codes.get(delete_status[0]))
                    delete_status_colored_message = delete_status_color + delete_status
                    delete_status_verified = allowed_status_codes.get(f'{delete_status}', False)
                    try:
                        delete_file_type = delete_response.headers.get("Content-Type").split(';')[0]
                        if (delete_file_type == "application/json"):
                            api_score += 0.2
                    except: 
                        delete_file_type = delete_response.headers.get("Content-Type")
                    delete_status_message_strip = f"{delete_status_color}[{delete_status_colored_message}][DELETE]{reset_color} \033[34m[{delete_file_type}] \033[0m  "

                if (method.lower() == "head" or method.lower() == "only_safe" or method.lower() == "all"):
                    head_response = await client.head(dir)
                    head_status = str(head_response.status_code)
                    head_status_color = str(colored_status_codes.get(head_status[0]))
                    head_status_colored_message = head_status_color + head_status
                    head_status_verified = allowed_status_codes.get(f'{head_status}', False)
                    try:
                        head_file_type = head_response.headers.get("Content-Type").split(';')[0]
                        if (head_file_type == "application/json"):
                            api_score += 0.2
                    except: 
                        head_file_type = head_response.headers.get("Content-Type")
                    head_status_message_strip = f"{head_status_color}[{head_status_colored_message}][HEAD]{reset_color} \033[34m[{head_file_type}] \033[0m  "

                if (method.lower() == "options" or method.lower() == "only_safe" or method.lower() == "all"):
                    options_response = await client.options(dir)
                    options_status = str(options_response.status_code)
                    options_status_color = str(colored_status_codes.get(options_status[0]))
                    options_status_colored_message = options_status_color + options_status
                    options_status_verified = allowed_status_codes.get(f'{options_status}', False)
                    try:
                        options_file_type = get_response.headers.get("Content-Type").split(';')[0]
                        if (options_file_type == "application/json"):
                            api_score += 0.2
                    except: 
                        options_file_type = options_response.headers.get("Content-Type")
                    options_status_message_strip = f"{options_status_color}[{options_status_colored_message}][OPTIONS]{reset_color} \033[34m[{options_file_type}] \033[0m  "
       
        # set status filter modes
        if (args.filter=='1xx'):
            get_status_verified = one_x_x_codes.get(get_status, False)
            post_status_verified = one_x_x_codes.get(post_status, False)
            head_status_verified = one_x_x_codes.get(head_status, False)
            options_status_verified = one_x_x_codes.get(options_status, False)
            put_status_verified = one_x_x_codes.get(put_status, False)
            patch_status_verified = one_x_x_codes.get(patch_status, False)
            delete_status_verified = one_x_x_codes.get(delete_status, False)
        elif (args.filter=='2xx'):
            get_status_verified = two_x_x_codes.get(get_status, False)
            post_status_verified = two_x_x_codes.get(post_status, False)
            head_status_verified = two_x_x_codes.get(head_status, False)
            options_status_verified = two_x_x_codes.get(options_status, False)
            put_status_verified = two_x_x_codes.get(put_status, False)
            patch_status_verified = two_x_x_codes.get(patch_status, False)
            delete_status_verified = two_x_x_codes.get(delete_status, False)
        elif (args.filter=='3xx'):
            get_status_verified = three_x_x_codes.get(get_status, False)
            post_status_verified = three_x_x_codes.get(post_status, False)
            head_status_verified = three_x_x_codes.get(head_status, False)
            options_status_verified = three_x_x_codes.get(options_status, False)
            put_status_verified = three_x_x_codes.get(put_status, False)
            patch_status_verified = three_x_x_codes.get(patch_status, False)
            delete_status_verified = three_x_x_codes.get(delete_status, False)
        elif (args.filter == '4xx'):
            get_status_verified = four_x_x_codes.get(get_status, False)
            post_status_verified = four_x_x_codes.get(post_status, False)
            head_status_verified = four_x_x_codes.get(head_status, False)
            options_status_verified = four_x_x_codes.get(options_status, False)
            put_status_verified = four_x_x_codes.get(put_status, False)
            patch_status_verified = four_x_x_codes.get(patch_status, False)
            delete_status_verified = four_x_x_codes.get(delete_status, False)
        elif (args.filter == '5xx'):
            get_status_verified = five_x_x_codes.get(get_status, False)
            post_status_verified = five_x_x_codes.get(post_status, False)
            head_status_verified = five_x_x_codes.get(head_status, False)
            options_status_verified = five_x_x_codes.get(options_status, False)
            put_status_verified = five_x_x_codes.get(put_status, False)
            patch_status_verified = five_x_x_codes.get(patch_status, False)
            delete_status_verified = five_x_x_codes.get(delete_status, False)
        elif (args.filter=='forbidden'):
            get_status_verified = forbidden_x_x_codes.get(get_status, False)
            post_status_verified = forbidden_x_x_codes.get(post_status, False)
            head_status_verified = forbidden_x_x_codes.get(head_status, False)
            options_status_verified = forbidden_x_x_codes.get(options_status, False)
            put_status_verified = forbidden_x_x_codes.get(put_status, False)
            patch_status_verified = forbidden_x_x_codes.get(patch_status, False)
            delete_status_verified = forbidden_x_x_codes.get(delete_status, False)

     
        if (get_status_verified):
            if not (args.stdout):
                http_message += get_status_message_strip 
            api_score += 1

        if (post_status_verified):
            if not (args.stdout):
                http_message += post_status_message_strip 
            api_score += 1
        
        if (head_status_verified):
            if not (args.stdout):
                http_message += head_status_message_strip 
            # api_score += 1

        if (options_status_verified):
            if not (args.stdout):
                http_message += options_status_message_strip 
            api_score += 1
        
        if (put_status_verified):
            if not (args.stdout):
                http_message += put_status_message_strip 
            api_score += 1
        
        if (patch_status_verified):
            if not (args.stdout):
                http_message += patch_status_message_strip 
            api_score += 1
        
        if (delete_status_verified):
            if not (args.stdout):
                http_message += delete_status_message_strip 
            api_score += 1
            
        if not (get_status_verified or post_status_verified or head_status_verified or options_status_verified or put_status_verified or patch_status_verified or delete_status_verified):
            if not (args.stdout):          
                if not (args.filter):
                    http_message += f'{get_status_message_strip} '
                    if (three_x_x_codes.get(get_status, False) or three_x_x_codes.get(post_status, False)):
                        get_3xx_response = await client.get((dir), follow_redirects=True)
                        post_3xx_response = await client.post((dir), follow_redirects=True)
                        colored_3xx_response = str(colored_status_codes.get(str(get_3xx_response.status_code)[0]))
                        get_3xx_response_verified = allowed_status_codes.get(f'{get_3xx_response.status_code}', False)

                        if (get_3xx_response_verified):
                            to_add.append(dir)
                            http_message = f'{get_status_message_strip}\033[95m[Redirect]\033[0m [{get_3xx_response.url}] {colored_3xx_response}[{str(get_3xx_response.status_code)}]  {reset_color}'
                        else:
                            http_message = f'{get_status_message_strip}\033[95m[Redirect]\033[0m [{post_3xx_response.url}] {colored_3xx_response}[{str(post_3xx_response.status_code)}]  {reset_color}'
                        tqdm.write(f'{http_message}{dir}')
                    else:
                        if dir[0] != "/" or dir[0] == "/":
                            to_remove.append(dir)
                        http_message=''
        
        else:
            if not (args.stdout):
                tqdm.write(f'{http_message}{dir}')

        api_update_active_score(dir, api_score)
        

        request = []
        if (args.json_report == 'all'):
            request = [('GET', get_status), ('POST', post_status), ('HEAD', head_status), ('OPTIONS', options_status)]
            report.create_report(request, headers = get_response.headers)
        elif(args.json_report == 'no-http-headers'):
            request = [('GET', get_status), ('POST', post_status), ('HEAD', head_status), ('OPTIONS', options_status)]
            
       
    except Exception as e:
        # tqdm.write(f"Error processing {dir}: {e}") # for error checking
        to_remove.append(dir)


async def api_act_check():
    start_time = time.time()
    custom_bar_format = "[[\033[94m{desc}\033[0m: [{n}/{total} {percentage:.0f}% {bar}] \033[31mTime-Taking:\033[0m [{elapsed}] \033[31mTime-Remaining:\033[0m [{remaining}] ]]"
    total_dir_counts = len(all_dirs)
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}
    tasks = []
    batch_size = args.requests
    if not (args.stdout):
        print("""\n

█▀ ▄▀█ █▀▀ ▀█▀ █ █░█ █▀▀   █▀▀ █░█ █▀▀ █▀▀ █▄▀ ▀█
█▄ █▀█ █▄▄ ░█░ █ ▀▄▀ ██▄   █▄▄ █▀█ ██▄ █▄▄ █░█ ▄█\n""")
        pbar = tqdm(total=total_dir_counts, desc=" Probing", unit='URL', bar_format=custom_bar_format, position=4, ncols=80, leave=False)
        async with httpx.AsyncClient(follow_redirects=False, headers=headers) as client:
            # with tqdm(total=total_dir_counts, desc=" Probing", unit='URL', bar_format=custom_bar_format, position=4, dynamic_ncols=True, leave=False) as pbar:
                for dir_count in range(0, total_dir_counts, batch_size):
                    # Calculate the end index for the current batch
                    end_index = min(dir_count + batch_size, total_dir_counts)
                    
                    for index in range(dir_count, end_index):
                        if index < len(all_dirs):
                            tasks.append(fetch_dir(client, all_dirs[index]))

                    # Run all tasks concurrently for the current batch
                    for task in asyncio.as_completed(tasks):
                        await task
                        pbar.update(1)  # Update the progress bar for each completed task
                    
                    tasks = []  # Clear the tasks list for the next batch
       
       
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        tqdm.write("  \n\033[94m" + f"[PROBED]\033[0m {total_dir_counts} urls in {elapsed_time:.2f} seconds\n")
        tqdm.write("")
        
    else:
        async with httpx.AsyncClient(follow_redirects=False, headers=headers) as client:
            for dir_count in range(0, total_dir_counts, batch_size):
                # Calculate the end index for the current batch
                end_index = min(dir_count + batch_size, total_dir_counts)
                
                for index in range(dir_count, end_index):
                    if index < len(all_dirs):
                        tasks.append(fetch_dir(client, all_dirs[index]))

                # Run all tasks concurrently for the current batch
                for task in asyncio.as_completed(tasks):
                    await task

                tasks = []  # Clear the tasks list for the next batch
    if (args.json_report):
        report.write_report()
    for dirs in to_remove:
        all_dirs.remove(dirs)
    for dirs in to_add:
        all_dirs.append(dirs)
    if (args.no_api_check):
        for dir in all_dirs:
            tqdm.write(dir)
