import unittest
import warnings
import os

import voyager.voyager as voyager
from click.testing import CliRunner

class TestIntegration(unittest.TestCase):
    def test_voyager_config(self):
        """
        Test that if the voyager config command prints out the config
        """
        runner = CliRunner()
        result = runner.invoke(voyager.cli, ['config'])
        # Check if arch is in the output
        assert 'ARCH' in result.output

    def test_voyager_install(self):
        """
        Test that voyager install finishes with the last to download library
        """
        wd = os.getcwd()
        if 'tests' in wd:  # depends from where tests are started
            os.chdir('./files')
        else:
            os.chdir('./tests/files')
        wd = os.getcwd()
        print(wd)
        # Disable annoying warnings that screw up the test output
        warnings.filterwarnings(action="ignore", message="unclosed", 
                         category=ResourceWarning)
        runner = CliRunner()
        result = runner.invoke(voyager.cli, ['install'])
        print(result.output)
        assert 'Downloading API/PA.JtagProgrammer @ >=17.0 ...' in result.output
        assert os.path.isfile('.voyager/voyager.lock')

if __name__ == '__main__':
    unittest.main()