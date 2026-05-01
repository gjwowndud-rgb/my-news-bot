import os
import requests
from google import genai
from datetime import datetime

# 환경 변수 설정
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def generate_report():
    try:
        # v1beta 경로 오류를 피하기 위해 클라이언트를 기본값으로 설정
        client = genai.Client(api_key=GEMINI_API_KEY)
        current_date = datetime.now().strftime("%Y년 %m월 %d일")
        
        # 전략가님이 성공하셨던 그 모델, 2.0-flash를 명시합니다.
        model_id = 'gemini-2.0-flash'
        
        prompt = f"""
        당신은 15년 경력의 글로벌 자산운용사 수석 전략가 '허렌버핏'입니다. ({current_date} 리포트)
        
        [작성 필수 구조]
        0. 오늘의 핵심 헤드라인 3줄 요약
        1. 국제 시장의 돈의 흐름 (금리, 환율, 유가 분석)
        2. 국내 증권가 산업별 비중 및 수급 (외인/기관 중심)
        3. 당일 추천 종목 (3종목) 및 선정 이유
        4. 오늘의 주요 경제 캘린더
        
        [작성 규칙]
        - 발행일: {current_date}, 작성자: '허렌버핏'
        - 부동산 정보는 절대 포함하지 말 것.
        - 냉철하고 객관적인 전문가 톤, 한국어 작성.
        - 이모지와 불렛포인트를 활용하여 가독성 확보.
        """

        # models/ 접두사 없이 모델 이름만 전달하여 v1beta 404 에러를 우회합니다.
        response = client.models.generate_content(
            model=model_id,
            contents=prompt
        )
        
        if not response.text:
            return "⚠️ 분석 내용 생성 실패"
            
        return response.text

    except Exception as e:
        # 에러 발생 시 상세 메시지를 텔레그램으로 보냅니다.
        return f"⚠️ 허렌버핏 리포트 생성 실패: {str(e)}"

def send_telegram_message(text):
    if not text: return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, json=payload)

if __name__ == "__main__":
    report_content = generate_report()
    send_telegram_message(report_content)
