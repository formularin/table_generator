import unittest
import table_generator
import subprocess

def get_data(file):
    
    with open(file, 'r') as f:
        data = [row.split(',') for row in f.read().split('\n')]

    return data


class TestTableGenerator(unittest.TestCase):

    def test_generate_html(self):
        
        # obtain test output
        csv_data = get_data('test.csv')
        test_output = table_generator.Table(csv_data).generate_html(True, True)
        
        # obtain accurate output
        with open('table.html', 'r') as f:
            html_output = f.read()

        self.assertEqual(test_output, html_output)
        
    def test_args(self):
        
        real_file = 'test.csv'
        fake_file = 'data.csv'

        try:
            subprocess.call(["./table_generator.sh", real_file, '-h', '-c'])
        except subprocess.CalledProcessError as e:
            print(e)


if __name__ == "__main__":
    unittest.main()
