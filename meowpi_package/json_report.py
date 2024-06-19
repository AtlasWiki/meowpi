from meowpi_package.shared import dict_report
from meowpi_package.statuses import http_status_codes
from meowpi_package.args import argparser
import json, jsbeautifier

args = argparser()

class report_maker:
    def create_dict(self, url):
        self.url = url
        dict_report[url] = {}
        dict_report[url]['requests'] = {}
        dict_report[url]['requests']["GET"] = {}
        dict_report[url]['requests']["POST"] = {}
        dict_report[url]['requests']["HEAD"] = {}
        dict_report[url]['requests']["OPTIONS"] = {}
        if args.json_report == "all":
            dict_report[url]['headers'] = {}
       

    def create_report(self, request, **headers):
        for method, status_code in request:
            dict_report[self.url]['requests'][method]['code'] = status_code
            dict_report[self.url]['requests'][method]['message'] = http_status_codes.get(str(status_code), "")
            if args.json_report == "all":
                http_dict = headers["headers"]
                http_keys = []
                http_values = []

                for key in http_dict.keys():
                    http_keys.append(key)

                for value in http_dict.values():
                    http_values.append(value)

                header_dict = dict(zip(http_keys, http_values))
                dict_report[self.url]['headers'] = header_dict
            

    def write_report(self):
        json_report = json.dumps(dict_report)
        beautified_json_report = jsbeautifier.beautify(json_report)
        with open(f"""url_report.json""", "w", encoding="utf-8") as directories:
            directories.write(beautified_json_report)


