import os
import requests
import google.generativeai as genai

# 환경 변수 설정
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def generate_report():
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        
        # [핵심 수정] 사용 가능 목록에서 확인된 최신 모델명을 사용합니다.
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        
        prompt = """
        당신은 15년 경력의 글로벌 자산운용사 수석 전략가입니다. 
        객관적인 데이터를 바탕으로 '일간 투자 전략 리포트'를 작성하세요.

        [분석 항목]
        1. 국제 시장의 돈의 흐름: 금리, 환율, 유가 등 거시 지표 변화 분석.
        2. 국내 증권가 산업별 비중 및 수급: 외인/기관 매수 섹터 식별 및 비중 설명.
        3. 당일 추천 종목 (3종목): 선정 이유를 구체적으로 기술.
        
        [규칙]
        - 부동산 정보는 절대 포함하지 마십시오.
        - 냉철하고 객관적인 전문가 톤으로 한국어로 작성하세요.
        - 이모지와 불렛포인트를 활용해 가독성을 높이세요.
        """

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"⚠️ AI 분석 중 오류 발생: {str(e)}"

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
