import os
import requests
import google.generativeai as genai

# 1. 환경 변수 설정 (GitHub Secrets에서 가져옴)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def get_market_data():
    """
    분석에 필요한 시장 데이터를 시뮬레이션하거나 크롤링하는 함수입니다.
    실제 증권사 API 연결 대신, AI가 뉴스/지표를 해석할 수 있도록 프롬프트를 구성합니다.
    """
    # 여기에 실제 뉴스 API나 크롤링 코드를 넣을 수 있습니다.
    # 현재는 AI에게 현재 시점의 글로벌/국내 시장 맥락을 분석하도록 유도합니다.
    return "현재 글로벌 금리 추이, 달러 인덱스, 엔화 환율, 국내 코스피/코스닥 수급 및 산업별 등락 지표"

def generate_report():
    genai.configure(api_key=GEMINI_API_KEY)
    
    # 모델 설정 (가장 최신인 gemini-1.5-flash 사용)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    당신은 15년 경력의 시니어 투자 전략가이자 펀드매니저입니다. 
    다음 지표를 바탕으로 전문적인 '일간 투자 전략 리포트'를 작성하세요.

    [분석 요청 사항]
    1. 국제 시장의 돈의 흐름: 
       - 미국 국채 금리, 달러 인덱스, 유가 등 거시 지표 변화에 따른 자산군별(채권 vs 주식 vs 원자재) 자금 이동 상황을 분석하세요.
    2. 국내 증권가 자금 흐름 및 산업별 비중:
       - 외국인과 기관의 매수세가 집중되는 핵심 산업(예: 반도체, AI, 바이오 등)을 식별하고 비중 변화를 설명하세요.
    3. 당일 추천 종목 (3종목):
       - 위 흐름에 부합하는 유망 종목 3개를 선정하고, 기술적/기본적 선정 이유를 구체적으로 기술하세요.
    
    [작성 규칙]
    - 부동산 관련 정보는 절대 포함하지 마십시오.
    - 말투는 냉철하고 객관적인 전문가 톤으로 작성하세요.
    - 가독성을 위해 불렛포인트와 이모지를 적절히 사용하세요.
    - 한국어로 작성하세요.
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI 분석 실패: {str(e)}"

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    res = requests.post(url, json=payload)
    return res.json()

if __name__ == "__main__":
    print("리포트 생성 중...")
    report = generate_report()
    
    print("텔레그램 전송 중...")
    send_telegram_message(report)
    print("완료!")
