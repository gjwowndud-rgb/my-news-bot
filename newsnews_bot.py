import os
import requests
import google.generativeai as genai

# 1. 환경 변수 설정 (GitHub Secrets에서 안전하게 가져옴)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def generate_report():
    """
    Gemini AI를 사용하여 투자 리포트를 생성합니다.
    """
    # API 키 설정
    genai.configure(api_key=GEMINI_API_KEY)
    
    # 모델 설정: 'models/' 접두사를 붙여 경로 오류(404)를 방지합니다.
    # gemini-1.5-flash는 속도가 빠르고 최신 지표 분석에 능숙합니다.
    model = genai.GenerativeModel('models/gemini-1.5-flash')
    
    prompt = """
    당신은 15년 경력의 글로벌 자산운용사 수석 전략가입니다. 
    오늘의 시장 데이터를 종합하여 투자자를 위한 '일간 자금 흐름 리포트'를 작성하세요.

    [핵심 분석 항목]
    1. 국제 시장의 돈의 흐름: 
       - 미국 국채 금리 변화, 달러 인덱스 추이, 국제 유가 및 원자재 시장의 움직임을 통해 현재 자금이 안전자산과 위험자산 중 어디로 쏠리는지 분석하세요.
    2. 국내 증권가 산업별 비중 및 수급:
       - 코스피/코스닥 시장에서 외국인과 기관의 순매수가 집중되는 핵심 산업 섹터를 식별하고, 비중이 확대되는 산업을 설명하세요.
    3. 당일 추천 종목 (3종목):
       - 위 흐름에 부합하며 모멘텀이 강한 유망 종목 3개를 선정하고, 각각의 선정 이유(수급, 차트, 재료 등)를 구체적으로 기술하세요.
    
    [작성 가이드라인]
    - 부동산 관련 트렌드나 정보는 절대 포함하지 마십시오. (완전 제외)
    - 어조는 냉철하고 객관적인 전문가 톤을 유지하세요.
    - 한국어로 작성하며, 가독성을 위해 이모지와 불렛포인트를 활용하세요.
    """

    try:
        # AI에게 리포트 생성 요청
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI 분석 중 오류 발생: {str(e)}"

def send_telegram_message(text):
    """
    생성된 리포트를 텔레그램으로 전송합니다.
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"  # 글자를 굵게 하거나 이쁘게 보이게 합니다.
    }
    try:
        res = requests.post(url, json=payload)
        return res.json()
    except Exception as e:
        print(f"텔레그램 전송 오류: {e}")
        return None

if __name__ == "__main__":
    print("🚀 투자 전략 리포트 생성 시작...")
    report_content = generate_report()
    
    print("📤 텔레그램으로 리포트 전송 중...")
    send_telegram_message(report_content)
    
    print("✅ 모든 작업이 완료되었습니다!")
