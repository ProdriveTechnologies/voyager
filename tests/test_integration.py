import unittest
import warnings
import os

import voyager.voyager as voyager
from voyager.configfile import ConfigFile
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
        If bamboo_voyager_CI is set, URL and arch are required and at least one credential is required.
        """

        os.environ['bamboo_voyager_CI'] = "1"
        os.environ['bamboo_voyager_CI_ARCH'] = "Header"
        os.environ['bamboo_voyager_CI_URL'] = "https://example.jfrog.io/artifactory"
        runner = CliRunner()
        result = runner.invoke(voyager.cli, ['search', 'some package'])
        del os.environ['bamboo_voyager_CI']
        del os.environ['bamboo_voyager_CI_ARCH']
        del os.environ['bamboo_voyager_CI_URL']
        assert result.exception.args == (
            "Missing required environment variable 'bamboo_voyager_CI_TOKEN'. Alternatively set 'bamboo_voyager_CI_API_KEY', which is deprecated.",
        )

    def test_ci_env_parses_with_token_only(self):
        os.environ['bamboo_voyager_CI'] = "1"
        os.environ['bamboo_voyager_CI_URL'] = "\"https://example.jfrog.io/artifactory\""
        os.environ['bamboo_voyager_CI_ARCH'] = "\"Header;Source\""
        os.environ['bamboo_voyager_CI_TOKEN'] = "\"token-value\""

        conf = ConfigFile()
        conf.parse()
        self.assertEqual(conf.access_token, "token-value")
        self.assertEqual(conf.api_key, "")
        self.assertEqual(conf.get_primary_credential()[0], "token")

        del os.environ['bamboo_voyager_CI']
        del os.environ['bamboo_voyager_CI_URL']
        del os.environ['bamboo_voyager_CI_ARCH']
        del os.environ['bamboo_voyager_CI_TOKEN']

    def test_ci_env_parses_with_api_key_only(self):
        os.environ['bamboo_voyager_CI'] = "1"
        os.environ['bamboo_voyager_CI_URL'] = "\"https://example.jfrog.io/artifactory\""
        os.environ['bamboo_voyager_CI_ARCH'] = "\"Header;Source\""
        os.environ['bamboo_voyager_CI_API_KEY'] = "\"api-key-value\""

        conf = ConfigFile()
        conf.parse()
        self.assertEqual(conf.access_token, "")
        self.assertEqual(conf.api_key, "api-key-value")
        self.assertEqual(conf.get_primary_credential()[0], "api_key")

        del os.environ['bamboo_voyager_CI']
        del os.environ['bamboo_voyager_CI_URL']
        del os.environ['bamboo_voyager_CI_ARCH']
        del os.environ['bamboo_voyager_CI_API_KEY']

    def test_credential_precedence_token_over_api_key(self):
        conf = ConfigFile()
        conf.access_token = "token-value"
        conf.api_key = "api-key-value"

        credential_type, credential_value = conf.get_primary_credential()
        self.assertEqual(credential_type, "token")
        self.assertEqual(credential_value, "token-value")

    def test_ci_env_precedence_token_over_api_key(self):
        os.environ['bamboo_voyager_CI'] = "1"
        os.environ['bamboo_voyager_CI_URL'] = "\"https://example.jfrog.io/artifactory\""
        os.environ['bamboo_voyager_CI_ARCH'] = "\"Header;Source\""
        os.environ['bamboo_voyager_CI_TOKEN'] = "\"token-value\""
        os.environ['bamboo_voyager_CI_API_KEY'] = "\"api-key-value\""

        conf = ConfigFile()
        conf.parse()

        credential_type, credential_value = conf.get_primary_credential()
        self.assertEqual(credential_type, "token")
        self.assertEqual(credential_value, "token-value")

        del os.environ['bamboo_voyager_CI']
        del os.environ['bamboo_voyager_CI_URL']
        del os.environ['bamboo_voyager_CI_ARCH']
        del os.environ['bamboo_voyager_CI_TOKEN']
        del os.environ['bamboo_voyager_CI_API_KEY']


if __name__ == '__main__':
    unittest.main()