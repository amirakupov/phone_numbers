import json
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_normalize_phone_numbers(client):
    # Test cases with input and expected normalized output
    test_cases = [
        {"input": "067823232", "expected": "+4367823232"},
        {"input": "+43 (0) 23453", "expected": "+4323453"},
        {"input": "+43 (0) 23-45-3", "expected": "+4323453"},
        {"input": "(0043)(0)45839", "expected": "+4345839"},
        {"input": "0043 34923 8923", "expected": "+43349238923"},
        {"input": "01 /23 43566", "expected": "+4312343566"},
    ]

    for test_case in test_cases:
        input_data = {'phone_number': test_case["input"]}
        response = client.post('/normalize-phone', data=json.dumps(input_data), content_type='application/json')
        data = json.loads(response.data)
        assert response.status_code == 200
        assert data['normalized_phone_number'] == test_case["expected"]

if __name__ == '__main__':
    pytest.main()