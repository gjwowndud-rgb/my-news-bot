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
        # 최신 google-genai 클라이언트 초기화
        client = genai.Client(api_key=GEMINI_API_KEY)
        current_date = datetime.now().strftime("%Y년 %m월 %d일")
        
        prompt = f"""
        당신은 15년 경력의 글로벌 자산운용사 수석 전략가 '허렌버핏'입니다. 
        오늘은 {current_date}입니다. 객관적인 데이터를 바탕으로 리포트를 작성하세요.

        [분석 항목]
        1. 국제 시장의 돈의 흐름 (금리, 환율, 유가 등 거시 지표)
        2. 국내 증권가 산업별 비중 및 수급 (외인/기관 중심)
        3. 당일 추천 종목 (3종목) 및 선정 이유
        
        [작성 규칙]
        - 발행일은 {current_date}, 작성자는 '허렌버핏'으로 명시.
        - 부동산 정보는 절대 포함하지 말 것.
        - 냉철하고 객관적인 전문가 톤의 한국어로 작성.
        - 가독성을 위해 이모지와 불렛포인트를 활용하여 가독성 확보.
        """

        # 최신 SDK 문법: models.generate_content 사용
        # 일일 쿼터가 넉넉한 gemini-1.5-flash 모델을 기본으로 설정합니다.
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=prompt
        )
        
        return response.text

    except Exception as e:
        # 에러 발생 시 내용을 리턴하여 텔레그램으로 원인을 확인할 수 있게 함
        return f"⚠️ 허렌버핏 리포트 생성 실패: {str(e)}"

def send_telegram_message(text):
    if not text:
        print("전송할 텍스트가 없습니다.")
        return
        
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML" 
    }
    try:
        res = requests.post(url, json=payload)
        # GitHub Actions 로그에서 전송 결과를 확인할 수 있도록 출력
        print(f"텔레그램 전송 결과: {res.status_code}, {res.text}")
    except Exception as e:
        print(f"텔레그램 요청 중 오류 발생: {e}")

if __name__ == "__main__":
    print("🚀 허렌버핏 리포트 생성 및 전송 시작...")
    report_content = generate_report()
    send_telegram_message(report_content)
    print("✨ 작업 종료.")
