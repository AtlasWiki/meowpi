from meowpi_package.shared import dict_report
from meowpi_package.statuses import http_status_codes

def clean_urls(url):
    if(url[:4] == "http"):    
        return url
    if (url[0] != "/"):
        url = "/" + url
        return url
    else:
        return url
  
def parse_domain(http_url):
    url_pieces = http_url.split("/", 3)
    domain = url_pieces[2]
    domain_labels = domain.split('.')
    return domain_labels
    # registered_domain = domain_labels[-2] + "." + domain_labels[-1] 
    #return registered_domain

def parse_dirs(url):
    url_pieces = url.split("/")
    formatted_dirs = url_pieces[3::]

    for dir in formatted_dirs[:]:
        if (dir == ''):
           formatted_dirs.remove('')
    unformatted_dirs = formatted_dirs.copy()
    
    for index,value in enumerate(formatted_dirs[:]):
        formatted_dirs[index] = "/" + value
    return formatted_dirs,unformatted_dirs

def remove_dupes(all_dirs):
    all_dirs[:] = list(dict.fromkeys(all_dirs))

def create_report(url, request, status_code, final_location, **headers):
    dict_report[url]['requests'][request]['code'] = status_code
    dict_report[url]['requests'][request]['message'] = http_status_codes.get(status_code, False)
    dict_report[url]['final_location'] = str(final_location)
    http_dict = headers["headers"]
    http_keys = []
    http_values = []

    for key in http_dict.keys():
        http_keys.append(key)

    for value in http_dict.values():
        http_values.append(value)

    header_dict = dict(zip(http_keys, http_values))
    dict_report[url]['headers'] = header_dict
