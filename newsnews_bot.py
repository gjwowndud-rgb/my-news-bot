import os
import requests
import google.generativeai as genai

# 1. 환경 변수 설정
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def generate_report():
    try:
        # API 키 설정
        genai.configure(api_key=GEMINI_API_KEY)
        
        # [수정] 가장 범용적인 'gemini-1.5-flash' 이름을 사용합니다.
        # 이 코드는 최신 라이브러리 버전(0.8.3 이상)에서 가장 잘 작동합니다.
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = """
        당신은 15년 경력의 글로벌 자산운용사 수석 전략가입니다. 
        아래 항목을 중심으로 '일간 투자 전략 리포트'를 작성하세요.

        1. 국제 시장의 돈의 흐름: 금리, 환율, 원자재 지표 분석 및 자산군별 이동 방향.
        2. 국내 증권가 산업별 비중 및 수급: 외인/기관 매수 섹터 및 산업별 전망.
        3. 당일 추천 종목 (3종목): 위 흐름에 부합하는 종목과 선정 이유.
        
        [작성 규칙]
        - 부동산 정보는 절대 포함하지 마십시오.
        - 냉철한 전문가 톤으로 한국어로 작성하세요.
        - 이모지와 불렛포인트를 활용해 가독성을 높이세요.
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
