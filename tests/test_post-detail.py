import requests
import pytest
import re

# 테스트 타겟 설정
API_BASE = "http://localhost:3333"
TARGET_POST_ID = 92
# TARGET_POST_ID = 44 
# 44번 게시글의 댓글 데이터 중에,
# 일부러 이메일 형식이 잘 못되도록 db에 수정해 둠. 바꿔서 해볼것.

# 이메일 정규표현식 패턴 (가장 표준적인 패턴)
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

def test_comments_email_format_verification():
    """
    postId별 댓글 조회 시 각 댓글의 이메일 형식이 유효한지 정규표현식으로 검증
    """
    # 1. API 호출
    url = f"{API_BASE}/comments?postId={TARGET_POST_ID}"
    response = requests.get(url)
    
    # 2. 기본 상태 코드 검증
    assert response.status_code == 200, f"API 호출 실패: {response.status_code}"
    
    comments = response.json()
    
    # 3. 데이터 존재 여부 확인 (테스트 안정성)
    assert isinstance(comments, list), "응답 데이터가 배열 형식이 아닙니다."
    assert len(comments) > 0, f"postId {TARGET_POST_ID}에 대한 댓글이 없습니다."

    ###
    # 4. 각 댓글의 이메일 전수 검증 (핵심)
    for comment in comments:
        email = comment.get("email", "")
        comment_id = comment.get("id")
        
        print(email)
        # 정규표현식 매칭 확인
        is_valid = re.match(EMAIL_REGEX, email)
        
        # 검증 실패 시 어떤 데이터가 틀렸는지 명시적으로 출력
        assert is_valid, f"부적절한 이메일 형식 발견! (댓글 ID: {comment_id}, 이메일: {email})"

def test_comment_schema_integrity():
    """
    댓글 객체의 필수 필드 누락 여부 및 데이터 타입 검증 (스키마 검증)
    """
    response = requests.get(f"{API_BASE}/comments?postId={TARGET_POST_ID}")
    comments = response.json()
    
    for comment in comments:
        # 필수 키 존재 확인
        assert "postId" in comment
        assert "id" in comment
        assert "email" in comment
        
        # 데이터 타입 확인
        assert isinstance(comment["postId"], int)
        assert isinstance(comment["email"], str)