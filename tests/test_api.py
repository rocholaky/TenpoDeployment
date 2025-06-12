import unittest
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from api.server import app


class TestPredictEndpoint(unittest.TestCase):
    def setUp(self):
        # Patch torch.jit.load before app startup (lifespan event)
        patcher = patch("api.server.torch.jit.load")
        self.mock_load = patcher.start()
        self.addCleanup(patcher.stop)

        # Mock the model's behaviour
        mock_model = MagicMock()
        mock_model.return_value.tolist.return_value = [2.0, 4.0]
        self.mock_load.return_value = mock_model

        # Store the client
        app.state.model = mock_model
        self.client = TestClient(app)

    def test_predict_valid_input(self):
        response = self.client.post("/predict", json={"inputs": [1.0, 2.0]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"result": [2.0, 4.0]})

    def test_predict_empty_input(self):
        response = self.client.post("/predict", json={"inputs": []})
        self.assertEqual(response.status_code, 422)  # validation error

    def test_predict_invalid_type(self):
        response = self.client.post("/predict", json={"inputs": ["a", "b"]})
        self.assertEqual(response.status_code, 422)

    def test_predict_missing_inputs(self):
        response = self.client.post("/predict", json={})
        self.assertEqual(response.status_code, 422)

    def test_model_raises_error(self):
        # Force model to raise an error
        self.client.app.state.model.side_effect = Exception("Model error")
        response = self.client.post("/predict", json={"inputs": [1.0, 2.0]})
        self.assertEqual(response.status_code, 500)
        self.assertIn("error", response.json())


if __name__ == "__main__":
    unittest.main()
