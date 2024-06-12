from meowpi_package.statuses import(
    allowed_status_codes, 
    blocked_status_codes, 
    colored_status_codes, 
    one_x_x_codes, 
    two_x_x_codes, 
    three_x_x_codes, 
    four_x_x_codes,
    five_x_x_codes, 
    forbidden_x_x_codes
)
import httpx, time, asyncio
from tqdm import tqdm
from meowpi_package.utils import create_report
from meowpi_package.args import argparser
from meowpi_package.shared import all_dirs, dict_report
from meowpi_package.store_files import write_files



args = argparser()

with open(f'{args.file}','r') as urls:
    for line in urls:
        all_dirs.append(line.strip('\n'))

to_remove = []
to_add = []

async def fetch_dir(client, dir):
    try:
        # initalize parent keys for the dictionary
        dict_report[dir] = {}
        dict_report[dir]['requests'] = {}
        dict_report[dir]['requests']["GET"] = {}
        dict_report[dir]['requests']["POST"] = {}
        dict_report[dir]['requests']["HEAD"] = {}
        dict_report[dir]['requests']["OPTIONS"] = {}
        dict_report[dir]['headers'] = {}
        # get/post requests
        get_response, post_response = await client.get(dir), await client.post(dir)
        get_location, post_location = str(get_response.url), str(post_response.url)
        get_status, post_status = str(get_response.status_code), str(post_response.status_code)
        get_file_type, post_file_type = '', ''

        try:
            get_file_type = get_response.headers.get("Content-Type").split(';')[0]
        except: 
            get_file_type = get_response.headers.get("Content-Type")
        try:
            post_file_type = post_response.headers.get("Content-Type").split(';')[0]
        except: 
            post_file_type = post_response.headers.get("Content-Type")
            

        # get/post messages
        if not (args.stdout): 
            get_status_color, post_status_color= str(colored_status_codes.get(get_status[0])), str(colored_status_codes.get(post_status[0]))
            get_status_colored_message, post_status_colored_message =  get_status_color + get_status, post_status_color + post_status
        # get/post conditions
        get_status_verified, post_status_verified = allowed_status_codes.get(f'{get_status}', False), allowed_status_codes.get(f'{post_status}', False)
        get_status_blocked = blocked_status_codes.get(f'{get_status}', False)
        verified_one_codes_post, verified_one_codes_get = one_x_x_codes.get(post_status, False), one_x_x_codes.get(get_status, False)
        verified_two_codes_post, verified_two_codes_get = two_x_x_codes.get(post_status, False), two_x_x_codes.get(get_status, False)
        verified_three_codes_post, verified_three_codes_get = three_x_x_codes.get(post_status, False), three_x_x_codes.get(get_status, False)
        verified_four_codes_post, verified_four_codes_get = four_x_x_codes.get(post_status, False), four_x_x_codes.get(get_status, False)
        verified_five_codes_post, verified_five_codes_get = five_x_x_codes.get(post_status, False), five_x_x_codes.get(get_status, False)
        verified_forbidden_code_post, verified_forbidden_code_get =  forbidden_x_x_codes.get(post_status, False), forbidden_x_x_codes.get(get_status, False)
        # get/post colored statements
        if not (args.stdout):
            reset_color = '\033[0m'
            verified_message_strip = f"\033[33m[Verified]{reset_color} "
            get_status_full_message = verified_message_strip + f"{get_status_color}[{get_status_colored_message}][GET]{reset_color} "
            post_status_full_message = verified_message_strip + f"{post_status_color}[{post_status_colored_message}][POST]{reset_color} "
            get_and_post_full_message = get_status_full_message + post_status_full_message.replace(verified_message_strip, "")
            get_and_post_full_error_message = verified_message_strip + f"{get_status_blocked}[{get_status}][GET] [{post_status}][POST]{reset_color} "
        
        if (args.mode=='1xx'):
            get_status_verified = verified_one_codes_get
            post_status_verified = verified_one_codes_post
        elif (args.mode=='2xx'):
            get_status_verified = verified_two_codes_get
            post_status_verified = verified_two_codes_post
        elif (args.mode=='3xx'):
            get_status_verified = verified_three_codes_get
            post_status_verified = verified_three_codes_post
        elif (args.mode == '4xx'):
            get_status_verified = verified_four_codes_get
            post_status_verified = verified_four_codes_post
        elif (args.mode == '5xx'):
            get_status_verified = verified_five_codes_get
            post_status_verified = verified_five_codes_post
        elif (args.mode=='forbidden'):
            post_status_verified = verified_forbidden_code_post
            get_status_verified = verified_forbidden_code_get

        if (get_status_verified and post_status_verified):
            head_response, options_response = await client.head(dir), await client.options(dir)
            head_location, options_location = str(head_response.url), str(options_response.url)
            head_status, options_status =  str(head_response.status_code),str(options_response.status_code)
            head_status_verified, options_status_verified = allowed_status_codes.get(f'{head_status}', False), allowed_status_codes.get(f'{options_status}', False)
            if not (args.stdout):
                head_status_color, options_status_color = str(colored_status_codes.get(head_status[0])), str(colored_status_codes.get(options_status[0]))
                head_status_colored_message, options_status_colored_message = head_status_color + head_status, options_status_color + options_status
                head_status_full_message_others = get_and_post_full_message + f"{head_status_color}[{head_status_colored_message}][HEAD]{reset_color} "
                options_status_full_message_others = get_and_post_full_message + f"{options_status_color}[{options_status_colored_message}][OPTIONS]{reset_color} "
                options_head_status_full_message_others = head_status_full_message_others + f"{options_status_color}[{options_status_colored_message}][OPTIONS]{reset_color} "

            if (head_status_verified and options_status_verified):
                if (not args.stdout and args.json_report):
                    # create_report(dir, 'GET', get_status, get_location, headers = get_response.headers)
                    # create_report(dir, 'POST', post_status, post_location)
                    # create_report(dir, 'HEAD', head_status, head_location)
                    # create_report(dir, 'OPTIONS', options_status, options_location)
                    tqdm.write(f'{options_head_status_full_message_others} \033[34m[{get_file_type}]\033[0m  {dir}')
                elif not (args.stdout):
                    tqdm.write(f'{options_head_status_full_message_others} \033[34m[{get_file_type}]\033[0m  {dir}')
                # elif (args.stdout and args.json_report):
                    # create_report(dir, 'GET', get_status, get_location, headers = get_response.headers)
                    # create_report(dir, 'POST', post_status, post_location)
                    # create_report(dir, 'HEAD', head_status, head_location)
                    # create_report(dir, 'OPTIONS', options_status, options_location)

            elif (head_status_verified):
                if (not args.stdout and args.json_report):
                    # create_report(dir, 'GET', get_status, get_location, headers = get_response.headers)
                    # create_report(dir, 'POST', post_status, post_location)
                    # create_report(dir, 'HEAD', head_status, head_location)
                    tqdm.write(f'{head_status_full_message_others} \033[34m[{get_file_type}]\033[0m  {dir}')
                elif not (args.stdout):
                    tqdm.write(f'{head_status_full_message_others} \033[34m[{get_file_type}]\033[0m  {dir}')
                # elif (args.stdout and args.json_report):
                    # create_report(dir, 'GET', get_status, get_location, headers = get_response.headers)
                    # create_report(dir, 'POST', post_status, post_location)
                    # create_report(dir, 'HEAD', head_status, head_location)
                    
            elif (options_status_verified):
                if (not args.stdout and args.json_report):
                    # create_report(dir, 'GET', get_status, get_location, headers = get_response.headers)
                    # create_report(dir, 'POST', post_status, post_location)
                    # create_report(dir, 'HEAD', head_status, head_location)
                    tqdm.write(f'{options_status_full_message_others} \033[34m[{get_file_type}]\033[0m  {dir}')
                elif not (args.stdout):
                    tqdm.write(f'{options_status_full_message_others} \033[34m[{get_file_type}]\033[0m  {dir}')
                # elif (args.stdout and args.json_report):
                    # create_report(dir, 'GET', get_status, get_location, headers = get_response.headers)
                    # create_report(dir, 'POST', post_status, post_location)
                    # create_report(dir, 'HEAD', head_status, head_location)
    
            else:
                if (not args.stdout and args.json_report):
                    # create_report(dir, 'GET', get_status, get_location, headers = get_response.headers)
                    # create_report(dir, 'POST', post_status, post_location, post_file_type)
                    tqdm.write(f'{get_and_post_full_message} \033[34m[{get_file_type}]\033[0m  {dir}')
                elif not (args.stdout):
                    tqdm.write(f'{get_and_post_full_message} \033[34m[{get_file_type}]\033[0m  {dir}')
                # elif (args.stdout and args.json_report):
                    # create_report(dir, 'GET', get_status, get_location, headers = get_response.headers)
                    # create_report(dir, 'POST', post_status, post_location, post_file_type)

        elif(get_status_verified):
            if (not args.stdout and args.json_report):
                # create_report(dir, 'GET', get_status, get_location, headers = get_response.headers)
                tqdm.write(f'{get_status_full_message} \033[34m[{get_file_type}]\033[0m  {dir}')
            elif not (args.stdout):
                tqdm.write(f'{get_status_full_message} \033[34m[{get_file_type}]\033[0m  {dir}')
            # elif (args.stdout and args.json_report):
                # create_report(dir, 'GET', get_status, get_location, headers = get_response.headers)

        elif(post_status_verified):
            if (not args.stdout and args.json_report):
                # create_report(dir, 'POST', post_status, post_location, headers = post_response.headers)
                tqdm.write(f'{post_status_full_message} \033[34m[{post_file_type}]\033[0m  {dir}')
            elif not (args.stdout):
                tqdm.write(f'{post_status_full_message} \033[34m[{post_file_type}]\033[0m  {dir}')
            # elif (args.stdout and args.json_report):
                # create_report(dir, 'POST', post_status, post_location, headers = post_response.headers)
        
        elif (verified_three_codes_get or verified_three_codes_post): 
            get_3xx_response = await client.get((dir), follow_redirects=True)
            colored_3xx_response = str(colored_status_codes.get(str(get_3xx_response.status_code)[0]))
            get_3xx_response_verified = allowed_status_codes.get(f'{get_3xx_response.status_code}', False)
            # create_report(dir, 'GET', get_status, get_3xx_response.url, headers = post_response.headers)
            # create_report(dir, 'POST', get_status, get_location, headers = post_response.headers)
            if (get_3xx_response_verified):
                to_add.append(dir)
            else:
                to_remove.append(dir)
            tqdm.write(f'{get_and_post_full_error_message} \033[95m[Redirect]\033[0m {get_3xx_response.url} {colored_3xx_response}[{str(get_3xx_response.status_code)}] {reset_color}{dir}')
    
        else:
            if (args.mode == "all"):
                if not (args.stdout):
                    tqdm.write(f'{get_and_post_full_error_message} {dir}')
              
                # create_report(dir, 'GET', get_status, get_location, headers = get_response.headers)
                # create_report(dir, 'POST', post_status, post_location)

            if dir[0] != "/" or dir[0] == "/":
                to_remove.append(dir)

    except Exception as e:
        tqdm.write(f"Error processing {dir}: {e}") # for error checking
        to_remove.append(dir)


async def filter_urls():
    start_time = time.time()
    custom_bar_format = "[[\033[94m{desc}\033[0m: [{n}/{total} {percentage:.0f}%] \033[31mTime-Taking:\033[0m [{elapsed}] \033[31mTime-Remaining:\033[0m [{remaining}] ]]"
    total_dir_counts = len(all_dirs)
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}
    tasks = []
    batch_size = args.requests
    if not (args.stdout):
        async with httpx.AsyncClient(follow_redirects=False, headers=headers) as client:
            with tqdm(total=total_dir_counts, desc=" Probing", unit='URL', bar_format=custom_bar_format, position=4, dynamic_ncols=True, leave=False) as pbar:
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

        print("")
        print("  \033[94m" + f"[PROBED]\033[0m {total_dir_counts} urls in {elapsed_time:.2f} seconds\n")

        
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
    for dirs in to_remove:
        all_dirs.remove(dirs)
    for dirs in to_add:
        all_dirs.append(dirs)
    # if (args.merge or args.json_report):
    #     write_files()