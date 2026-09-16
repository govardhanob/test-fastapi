import os
import unittest
from pathlib import Path
from unittest.mock import patch

from app.core import firebase as firebase_config


class FirebaseCredentialConfigTest(unittest.TestCase):
    def test_prefers_firebase_service_account_env_var(self):
        with patch.dict(
            os.environ,
            {
                "FIREBASE_SERVICE_ACCOUNT": "/tmp/firebase-service-account.json",
                "GOOGLE_APPLICATION_CREDENTIALS": "/tmp/google-credentials.json",
            },
        ):
            self.assertEqual(
                firebase_config.get_service_account_path(),
                Path("/tmp/firebase-service-account.json"),
            )

    def test_uses_google_application_credentials_env_var(self):
        with patch.dict(
            os.environ,
            {
                "GOOGLE_APPLICATION_CREDENTIALS": "/tmp/google-credentials.json",
            },
            clear=True,
        ):
            self.assertEqual(
                firebase_config.get_service_account_path(),
                Path("/tmp/google-credentials.json"),
            )

    def test_falls_back_to_local_service_account_file(self):
        with patch.dict(os.environ, {}, clear=True):
            with patch.object(
                firebase_config,
                "GENERIC_SERVICE_ACCOUNT_PATH",
                Path("/tmp/firebase-service-account.json"),
            ):
                with patch.object(Path, "exists", return_value=True):
                    self.assertEqual(
                        firebase_config.get_service_account_path(),
                        Path("/tmp/firebase-service-account.json"),
                    )

    def test_uses_legacy_local_service_account_file_when_generic_is_missing(self):
        with patch.dict(os.environ, {}, clear=True):
            with patch.object(
                firebase_config,
                "GENERIC_SERVICE_ACCOUNT_PATH",
                Path("/tmp/firebase-service-account.json"),
            ):
                with patch.object(
                    firebase_config,
                    "LOCAL_SERVICE_ACCOUNT_PATH",
                    Path("/tmp/local-service-account.json"),
                ):
                    with patch.object(
                        Path,
                        "exists",
                        lambda path: path == Path("/tmp/local-service-account.json"),
                    ):
                        self.assertEqual(
                            firebase_config.get_service_account_path(),
                            Path("/tmp/local-service-account.json"),
                        )

    def test_uses_default_credentials_when_no_local_file_exists(self):
        with patch.dict(os.environ, {}, clear=True):
            with patch.object(Path, "exists", return_value=False):
                self.assertIsNone(firebase_config.get_service_account_path())


if __name__ == "__main__":
    unittest.main()
