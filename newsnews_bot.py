import os
import requests
import google.generativeai as genai

# 환경 변수 로드
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def generate_report():
    try:
        # API 설정
        genai.configure(api_key=GEMINI_API_KEY)
        
        # [핵심 수정] 모델 경로를 풀 네임으로 지정하여 404 오류를 방지합니다.
        # gemini-1.5-flash는 현재 구글에서 가장 권장하는 모델입니다.
        model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')
        
        prompt = """
        당신은 글로벌 자산운용사 전략가입니다. 아래 항목을 객관적으로 분석하세요.
        1. 국제 시장 자금 흐름: 금리, 환율, 원자재 지표 분석 및 자산 이동 방향.
        2. 국내 증권가 산업별 비중 및 수급: 외인/기관 매수 섹터 및 비중 변화 설명.
        3. 당일 추천 종목 (3종목): 선정 이유를 수급과 모멘텀 측면에서 기술.
        
        [규칙]
        - 부동산 정보는 절대 제외할 것.
        - 냉철한 전문가 톤의 한국어로 작성.
        - 이모지와 불렛포인트를 사용하여 가독성 확보.
        """

        # 분석 생성
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        # 에러 발생 시 원인을 구체적으로 텔레그램에 전달
        return f"⚠️ AI 분석 중 오류 발생:\n{str(e)}"

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
        print(f"전송 실패: {e}")

if __name__ == "__main__":
    report_content = generate_report()
    send_telegram_message(report_content)
