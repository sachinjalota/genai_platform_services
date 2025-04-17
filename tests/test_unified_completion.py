import pytest  
from fastapi.testclient import TestClient  
from src.main import app  
  
client = TestClient(app)  
  
@pytest.fixture  
def headers():  
    return {"X-Session-ID": "test-session", "X-Usecase-ID": "test-usecase"}  
  
def test_text_completion(headers):  
    response = client.post("/api/v1/chat_completion", json={  
        "model_name": "gemini-1.5-flash",  
        "user_prompt": "Hello, how are you?"  
    }, headers=headers)  
    assert response.status_code == 200  
    assert "choices" in response.json()  
  
def test_image_completion(headers):  
    response = client.post("/api/v1/chat_completion", json={  
        "model_name": "gemini-1.5-flash",  
        "user_prompt": "Describe this image",  
        "image_url": "https://general-purpose-public.s3.ap-south-1.amazonaws.com/gemini_test_images/aadharCard.jpeg"  
    }, headers=headers)  
    assert response.status_code == 200  
    assert "choices" in response.json()  
  
def test_missing_headers():  
    response = client.post("/api/v1/chat_completion", json={  
        "model_name": "gemini-1.5-flash",  
        "user_prompt": "Hello"  
    })  
    assert response.status_code == 422  