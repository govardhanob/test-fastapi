import unittest

from app.main import app


class AuthOpenAPITest(unittest.TestCase):
    def test_auth_routes_use_bearer_security_scheme(self):
        schema = app.openapi()

        security_schemes = schema["components"].get("securitySchemes")
        self.assertEqual(
            security_schemes,
            {
                "HTTPBearer": {
                    "type": "http",
                    "scheme": "bearer",
                },
            },
        )

        auth_me_operation = schema["paths"]["/auth/me"]["get"]
        self.assertEqual(auth_me_operation["security"], [{"HTTPBearer": []}])

        parameters = auth_me_operation.get("parameters", [])
        self.assertNotIn(
            ("authorization", "header"),
            {(param["name"], param["in"]) for param in parameters},
        )


if __name__ == "__main__":
    unittest.main()
