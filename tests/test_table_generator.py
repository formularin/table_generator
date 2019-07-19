import os
import sys
import unittest

package_dir = '/'.join(os.path.dirname(__file__).split('/')[:-1])
if package_dir not in sys.path:
    sys.path.append(package_dir)

from table_generator import generate_html

def get_data(file):
    
    with open(file, 'r') as f:
        data = [row.split(',') for row in f.read().split('\n')]

    return data


class TestTableGenerator(unittest.TestCase):

    def test_generate_html(self):
        
        # obtain test output
        csv_data = get_data(f'{os.getcwd()}/tests/test.csv')
        test_output = generate_html(csv_data, True, True, False)
        
        # obtain accurate output
        with open(f'{os.getcwd()}/tests/table.html', 'r') as f:
            html_output = f.read()

        self.assertEqual(test_output, html_output)

        pretty_test_output = generate_html(csv_data, True, True, True)

        with open(f'{os.getcwd()}/tests/pretty_table.html', 'r') as f:
            pretty_html_output = f.read()

        for real, test in zip(
            *[i.split('\n') for i in [pretty_html_output, pretty_test_output]]):
            self.assertEqual(test, real)


if __name__ == "__main__":
    unittest.main()
