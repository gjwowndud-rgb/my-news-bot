import os
import requests
import google.generativeai as genai

# 1. 환경 변수 설정
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def generate_report():
    try:
        # API 설정
        genai.configure(api_key=GEMINI_API_KEY)
        
        # [해결책] 가장 에러가 적은 'gemini-pro' 모델을 사용합니다.
        # 1.5-flash에서 발생하는 404 오류를 피하기 위한 가장 확실한 방법입니다.
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = """
        당신은 15년 경력의 시니어 투자 전략가입니다. 아래 항목을 분석하여 리포트를 작성하세요.
        1. 국제 시장 자금 흐름: 금리, 환율, 원자재 지표 분석 및 자산 이동 방향.
        2. 국내 증권가 산업별 수급: 외인/기관 매수 섹터 및 산업별 비중 변화.
        3. 당일 추천 종목 3가지: 선정 이유를 수급과 재료 측면에서 구체적으로 기술.
        
        [규칙]
        - 부동산 정보는 절대 포함하지 마십시오.
        - 냉철한 전문가 톤의 한국어로 작성하세요.
        - 이모지와 불렛포인트를 활용하세요.
        """

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"AI 분석 중 오류 발생: {str(e)}"

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML" 
    }
    try:
        res = requests.post(url, json=payload)
        return res.json()
    except Exception as e:
        return None

if __name__ == "__main__":
    report_content = generate_report()
    send_telegram_message(report_content)
