import requests

API_BASE = "http://localhost:3333"

def test_get_posts_schema_simple():
    # 1. Status Code 검증
    response = requests.get(f"{API_BASE}/posts")
    assert response.status_code == 200
    
    data = response.json()
    
    # 2. 스키마 검증 (리스트 형태인지, 필수 키가 있는지)
    assert isinstance(data, list)
    for post in data:
        assert "id" in post
        assert "title" in post
        assert "userId" in post
        
        
        
