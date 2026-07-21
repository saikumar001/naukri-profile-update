import json
import os
import tempfile
import unittest
from unittest.mock import patch

import update_profile as update_naukri


class LoadCookiesTests(unittest.TestCase):
    def test_loads_from_cookie_file_when_env_missing(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            cookie_path = os.path.join(temp_dir, "cookie.json")
            payload = [{"name": "session", "value": "abc", "domain": "example.com", "path": "/"}]
            with open(cookie_path, "w", encoding="utf-8") as handle:
                json.dump(payload, handle)

            with patch("update_naukri.COOKIE_FILE", cookie_path), patch.dict(os.environ, {}, clear=True):
                cookies = update_naukri.load_cookies()

            self.assertEqual(cookies, payload)

    def test_prefers_env_var_over_cookie_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            cookie_path = os.path.join(temp_dir, "cookie.json")
            file_payload = [{"name": "session", "value": "file-value", "domain": "example.com", "path": "/"}]
            with open(cookie_path, "w", encoding="utf-8") as handle:
                json.dump(file_payload, handle)

            env_payload = [{"name": "session", "value": "env-value", "domain": "example.com", "path": "/"}]
            with patch("update_naukri.COOKIE_FILE", cookie_path), patch.dict(os.environ, {"NAUKRI_COOKIES": json.dumps(env_payload)}, clear=True):
                cookies = update_naukri.load_cookies()

            self.assertEqual(cookies, env_payload)


if __name__ == "__main__":
    unittest.main()
