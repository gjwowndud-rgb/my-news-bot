import os
import requests
from google import genai
from datetime import datetime

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def generate_report():
    try:
        # 클라이언트 초기화 시점을 명확히 합니다.
        client = genai.Client(api_key=GEMINI_API_KEY)
        current_date = datetime.now().strftime("%Y년 %m월 %d일")
        
        # 4월 29일에 성공했던 2.0 모델을 사용하되, 
        # 불필요한 토큰 낭비를 막기 위해 프롬프트를 간결하게 최적화했습니다.
        prompt = f"""
        당신은 15년 경력의 글로벌 자산운용사 수석 전략가 '허렌버핏'입니다. ({current_date} 리포트)
        핵심 요약 3줄, 국외 시장 흐름, 국내 증권가 수급, 추천 종목 3개, 경제 일정 순으로 
        냉철한 전문가 톤으로 작성하세요. 부동산 제외. 이모지 활용.
        """

        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )
        
        return response.text if response.text else "⚠️ 응답 본문이 비어있습니다."

    except Exception as e:
        # 429 에러 발생 시 원인을 정확히 파악하기 위해 전체 에러 출력
        return f"⚠️ 생성 실패(원인 파악용): {str(e)}"

def send_telegram_message(text):
    if not text: return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    # 긴 텍스트 전송 시 발생할 수 있는 오류를 방지하기 위해 기본 전송 사용
    payload = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, json=payload)

if __name__ == "__main__":
    report_content = generate_report()
    send_telegram_message(report_content)
