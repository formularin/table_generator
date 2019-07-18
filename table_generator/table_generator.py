"""Converts csv to html table

Usage: ./table_generator.py file.csv [-chp]

-c: adds html elements to write complete file, not just table, such as <!DOCTYPE html> and <html></html> tags

-h: turns first row into heaser tags

-p: pretty prints html code

-a: following arg is path to json file that contains html attirbutes and corresponding values
"""


import sys
import os.path
import lxml.etree as etree


# html templates for inserting children
DOCUMENT = '<!DOCTYPE html><html><head></head><body>%s</body></html>'
TABLE = '<table>%s</table>'
TR = '<tr>%s</tr>'
TH = '<th>%s</th>'
TD = '<td>%s</td>'


class Table:
    """Table object for generating html code"""

    def __init__(self, data):
        
        self.data = data

    def generate_html(self, complete_file, header):
        """Generates code for html table from self.data"""

        table_children = ''  # rows to be added here
        
        if header:
            # generate code from first row as header row
            header_row = ''
            for header in self.data[0]:
                header_row += TH % header

            table_children += TR % header_row

        # determines whether to use whole list or exclude first row
        starting_index = 0
        if header:
            starting_index = 1

        data_rows = ''
        for row in self.data[starting_index:]:
            row_element = ''
            for value in row:
                row_element += TD % value
            data_rows += TR % row_element

        table_children += data_rows

        html_table = TABLE % table_children

        if complete_file:

            return DOCUMENT % html_table

        else:

            return html_table


def main(filepath, complete_file, header, pretty, attrs):
    
    with open(filepath, 'r') as f:
        data = [row.split(',') for row in f.read().split('\n')]

    if complete_file == 'True':
        complete_file = True

    if header == 'True':
        header = True

    table = Table(data)

    html = table.generate_html(complete_file, header)

    if attrs:
        
        attrs_strings = []
        for key, val in attrs.items():
            attrs_strings.append(f'{key}="{val}"')

        attrs_string = ' '.join(attrs_strings)

        html = html.replace('<table>', f'<table {attrs_string}') 

    if pretty:
        
        i = 0
        tmp = f'{i}.txt'
        while os.path.isfile(tmp):
            i += 1
            tmp = f'{i}.txt'

        with open('quick.html', 'w+') as f:
            f.write(html)
        
        x = etree.parse("quick.html")
        print(etree.tostring(x, pretty_print=True).decode())

    else:

        print(html)


if __name__ == "__main__":
    
    args = sys.argv[1:]

    correct_usage = True
    for arg in args:
        if not os.path.isfile(arg) and arg not in ['-h', '--help', '-c', '-p', '-a']:
            raise ValueError('Unknown option: "%s". Call with --help option for usage' % arg)

    if '--help' in args:
        print(__doc__)

    else:
        
        file = ''
        for arg in args:
            if os.path.isfile(arg) and '.csv' in arg:
                file = os.path.abspath(arg)

        if file == '':
            raise FileNotFoundError('Either no file specified or '
                                    'file did not exist. Call with --help for usage')

        header = False
        if '-h' in args:
            header = True

        complete_file = False
        if '-c' in args:
            complete_file = True

        pretty = False
        if '-p' in args:
            pretty = True

        attrs = False
        if '-a' in args:
            json_file = args[args.index('-a') + 1]
            with open(json_file, 'r') as f:
                attrs = eval(f.read())

        main(file, complete_file, header, pretty, attrs)

