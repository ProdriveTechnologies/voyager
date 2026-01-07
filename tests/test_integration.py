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
        assert 'Downloading test/SourcePackage @ 1 ...' in result.output
        assert os.path.isfile('.voyager/voyager.lock')

    def test_required_ci_variables(self):
        """
        If the bamboo_voyager_CI env var is set, all related env vars are required.
        """

        os.environ['bamboo_voyager_CI'] = "1"
        os.environ['bamboo_voyager_CI_ARCH'] = "Header"
        runner = CliRunner()
        result = runner.invoke(voyager.cli, ['search', 'some package'])
        del os.environ['bamboo_voyager_CI']
        assert result.exception.args == (
            "Missing required environment variable(s): ['bamboo_voyager_CI_API_KEY', 'bamboo_voyager_CI_URL']",
        )


if __name__ == '__main__':
    unittest.main()