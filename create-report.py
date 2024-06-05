import os
import fnmatch
import re

log_line_patt = '([(\d\.)]+) - - \[(.*?)\] "(?:GET|POST) (.*?)" (\d+) - "(.*?)" "(.*?)"'
log_line_reg = re.compile(log_line_patt, re.IGNORECASE)

def run(input, output, input_pattern='access.log*'):
    inputs = []
    for file_name in os.listdir(input):
        if fnmatch.fnmatch(file_name, input_pattern):
            with open(os.path.abspath(os.path.join(input, file_name)), 'r') as _:
                for line in _:
                    if log_line_reg.match(line):
                        inputs.append(parse(line))



import argparse

parser = argparse.ArgumentParser(
    prog='Server access analyzer',
    description='Creates a report for a list of access log file from Nginx or Apache',
    epilog='')  # test at the end of the help

parser.add_argument("input", help='The input directory. All files matching access.log*'
                                  'will be scanned')
parser.add_argument("output", help='the output (html file where the analysis report '
                                   'will be generated')
args = parser.parse_args()

run(args.input, args.output)
