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

        [작성 필수 구조]
        0. 오늘의 핵심 헤드라인 3줄 요약: 리포트 최상단에 오늘 가장 중요한 흐름 3가지를 한 줄씩 요약하여 배치.
        1. 국제 시장의 돈의 흐름: 금리, 환율, 유가 등 거시 지표 변화 분석.
        2. 국내 증권가 산업별 비중 및 수급: 외인/기관 매수 섹터 중심 설명.
        3. 당일 추천 종목 (3종목): 선정 이유를 수급과 실적 기반으로 구체적 기술.
        4. 오늘의 주요 경제 캘린더: 지표 발표나 실적 일정을 3가지 내외로 정리.
        
        [작성 규칙]
        - 발행일: {current_date}, 작성자: '허렌버핏'.
        - 부동산 정보는 절대 포함하지 말 것.
        - 냉철하고 객관적인 전문가 톤의 한국어로 작성.
        - 가독성을 위해 이모지와 볼렛포인트를 적절히 사용.
        - 텔레그램 가독성을 위해 섹션 사이를 확실히 구분할 것.
        """

        # 2026년 표준 모델인 gemini-2.0-flash를 사용하여 안정성을 확보합니다.
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )
        
        if not response.text:
            return "⚠️ AI 분석 내용 생성 실패. 잠시 후 다시 시도해 주세요."
            
        return response.text

    except Exception as e:
        return f"⚠️ 허렌버핏 리포트 생성 실패: {str(e)}"

def send_telegram_message(text):
    if not text:
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
        print(f"텔레그램 전송 오류: {e}")

if __name__ == "__main__":
    print("🚀 허렌버핏 리포트(3줄 요약 포함) 생성 시작...")
    report_content = generate_report()
    send_telegram_message(report_content)
    print("✨ 작업 종료.")
