import os
import requests
from google import genai
from datetime import datetime

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def generate_report():
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        current_date = datetime.now().strftime("%Y년 %m월 %d일")
        
        # [안정성 최우선] 2.0 모델보다 쿼터가 수십 배 넉넉한 1.5-flash를 사용합니다.
        model_id = 'gemini-1.5-flash'
        
        prompt = f"""
        당신은 15년 경력의 글로벌 자산운용사 수석 전략가 '허렌버핏'입니다. ({current_date} 리포트)
        0. 오늘의 핵심 헤드라인 3줄 요약
        1. 국제 시장의 돈의 흐름 (금리, 환율, 유가)
        2. 국내 증권가 산업별 비중 및 수급
        3. 당일 추천 종목 (3종목) 및 선정 이유
        4. 오늘의 주요 경제 캘린더
        * 부동산 제외, 냉철한 전문가 톤, 한국어 작성.
        """

        response = client.models.generate_content(model=model_id, contents=prompt)
        return response.text if response.text else "⚠️ AI 응답이 비어있습니다."

    except Exception as e:
        # 쿼터 초과 시 더 이상 시도하지 않도록 메시지 반환
        return f"⚠️ 리포트 생성 실패: {str(e)}"

def send_telegram_message(text):
    if not text: return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, json=payload)

if __name__ == "__main__":
    report_content = generate_report()
    send_telegram_message(report_content)
