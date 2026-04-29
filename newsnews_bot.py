import os
import requests
import google.generativeai as genai
from datetime import datetime

# 환경 변수 설정
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def generate_report():
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        
        # [핵심] 확인된 최신 모델명을 사용합니다.
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        
        current_date = datetime.now().strftime("%Y년 %m월 %d일")
        
        prompt = f"""
        당신은 15년 경력의 글로벌 자산운용사 수석 전략가 '허렌버핏'입니다. 
        오늘은 {current_date}입니다. 객관적인 데이터를 바탕으로 리포트를 작성하세요.

        [분석 항목]
        1. 국제 시장의 돈의 흐름: 거시 지표(금리, 환율, 유가) 변화 분석.
        2. 국내 증권가 산업별 비중 및 수급: 외인/기관 매수 섹터 및 비중 설명.
        3. 당일 추천 종목 (3종목): 수급과 실적 기반의 선정 이유.
        
        [작성 규칙]
        - 발행일은 {current_date}, 작성자는 '허렌버핏'으로 명시할 것.
        - 부동산 정보는 절대 포함하지 마십시오.
        - 냉철하고 객관적인 전문가 톤으로 한국어로 작성하세요.
        - 가독성을 위해 이모지와 불렛포인트를 활용하세요.
        """

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"⚠️ 허렌버핏 리포트 생성 실패: {str(e)}"

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML" 
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"전송 오류: {e}")

if __name__ == "__main__":
    report_content = generate_report()
    send_telegram_message(report_content)
