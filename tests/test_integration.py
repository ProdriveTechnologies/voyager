import unittest

import voyager
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
        runner = CliRunner()
        result = runner.invoke(voyager.cli, ['install'])
        assert 'Downloading API/PA.JtagProgrammer @ >=17.0 ... MSVC.140.DBG.32 @ 18.0.0 OK' in result.output

if __name__ == '__main__':
    unittest.main()