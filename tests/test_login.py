import unittest
from datetime import datetime

import voyager.artifactorylogin as artifactorylogin


class TestLogin(unittest.TestCase):
    def test_build_url(self):
        """
        Test that the build_artifactory_url_from_user_input function works
        """
        art_url = artifactorylogin.build_artifactory_url_from_user_input("artifactory.example.com")
        self.assertEqual(art_url, 'https://artifactory.example.com/artifactory')
        art_url = artifactorylogin.build_artifactory_url_from_user_input("https://artifactory.example.com/ui/packages")
        self.assertEqual(art_url, 'https://artifactory.example.com/artifactory')
        art_url = artifactorylogin.build_artifactory_url_from_user_input("http://artifactory.example.com/ui/packages")
        self.assertEqual(art_url, 'http://artifactory.example.com/artifactory')

    def test_timestamp_is_timezone_aware_iso8601(self):
        timestamp = artifactorylogin._current_timestamp_utc_iso8601()
        parsed = datetime.fromisoformat(timestamp)

        self.assertIsNotNone(parsed.tzinfo)
        self.assertIsNotNone(parsed.utcoffset())


if __name__ == '__main__':
    unittest.main()
