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

        # [수정] 404 에러 방지를 위해 2026년 표준 모델인 gemini-2.0-flash를 사용합니다.
        # models/ 접두사를 생략하고 모델 ID만 입력하는 것이 최신 SDK의 표준입니다.
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )
        
        if not response.text:
            return "⚠️ AI가 빈 응답을 반환했습니다. 쿼터 또는 필터링 설정을 확인하세요."
            
        return response.text

    except Exception as e:
        # 상세 에러 메시지를 텔레그램으로 전송하여 즉각 대응 가능하게 함
        return f"⚠️ 허렌버핏 리포트 생성 실패: {str(e)}"

def send_telegram_message(text):
    if not text:
        print("전송할 내용이 없습니다.")
        return
        
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML" 
    }
    try:
        res = requests.post(url, json=payload)
        print(f"텔레그램 전송 결과: {res.status_code}, {res.text}")
    except Exception as e:
        print(f"텔레그램 요청 중 오류 발생: {e}")

if __name__ == "__main__":
    print("🚀 허렌버핏 리포트 생성 시작...")
    report_content = generate_report()
    send_telegram_message(report_content)
    print("✨ 작업 종료.")
