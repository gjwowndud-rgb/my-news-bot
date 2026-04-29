import os
import requests
import google.generativeai as genai
from datetime import datetime
import time

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def generate_report():
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    current_date = datetime.now().strftime("%Y년 %m월 %d일")
    
    prompt = f"""
    당신은 15년 경력의 글로벌 자산운용사 수석 전략가 '허렌버핏'입니다. 
    오늘은 {current_date}입니다. 객관적인 데이터를 바탕으로 리포트를 작성하세요.
    1. 국제 시장의 돈의 흐름 (금리, 환율, 유가)
    2. 국내 증권가 산업별 비중 및 수급 (외인/기관 중심)
    3. 당일 추천 종목 3종목과 선정 이유
    * 부동산 정보 제외, 냉철한 전문가 톤, 한국어 작성.
    """

    # 429 에러 방지를 위한 재시도 로직 (최대 3회)
    for i in range(3):
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            if "429" in str(e) and i < 2:
                print(f"⚠️ 요청 한도 초과. {10 * (i+1)}초 후 재시도합니다...")
                time.sleep(10 * (i+1))
                continue
            return f"⚠️ 허렌버핏 리포트 생성 실패: {str(e)}"

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, json=payload)

if __name__ == "__main__":
    report_content = generate_report()
    send_telegram_message(report_content)
