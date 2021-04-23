import unittest

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


if __name__ == '__main__':
    unittest.main()
