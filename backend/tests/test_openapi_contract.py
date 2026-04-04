import unittest

from fastapi.testclient import TestClient

from backend.app.main import app


class OpenApiContractTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_openapi_contains_loyalty_contract_routes(self) -> None:
        response = self.client.get("/openapi.json")
        schema = response.json()
        paths = schema["paths"]

        self.assertIn("/api/v1/loyalty/program", paths)
        self.assertIn("/api/v1/payments/{payment_id}/confirm", paths)
        self.assertIn("/api/v1/patients/{patient_id}/wallet", paths)
        self.assertIn("/api/v1/patients/{patient_id}/ledger", paths)
        self.assertIn("/api/v1/redemptions/quote", paths)
        self.assertIn("/api/v1/me/bonus-rules", paths)


if __name__ == "__main__":
    unittest.main()
