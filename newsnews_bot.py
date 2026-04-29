import os
import requests
import google.generativeai as genai

# 1. 환경 변수 설정
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def generate_report():
    """
    Gemini AI를 사용하여 투자 리포트를 생성합니다.
    """
    try:
        # API 키 설정
        genai.configure(api_key=GEMINI_API_KEY)
        
        # 모델 설정: 'gemini-1.5-flash'를 기본 모델로 사용합니다.
        # 만약 이 이름이 계속 404가 뜨면 'gemini-1.5-pro'로 바꿔볼 수 있습니다.
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = """
        당신은 15년 경력의 글로벌 자산운용사 수석 전략가입니다. 
        오늘의 시장 데이터를 종합하여 투자자를 위한 '일간 자금 흐름 리포트'를 작성하세요.

        [핵심 분석 항목]
        1. 국제 시장의 돈의 흐름: 금리, 환율, 원자재 지표 분석 및 자산군별 이동 방향.
        2. 국내 증권가 산업별 비중 및 수급: 외인/기관의 매수 섹터 분석 및 산업별 전망.
        3. 당일 추천 종목 (3종목): 위 흐름에 부합하는 종목 선정 및 이유.
        
        [작성 규칙]
        - 부동산 관련 정보는 '절대' 포함하지 마십시오.
        - 냉철한 전문가 톤으로 한국어로 작성하세요.
        - 가독성을 위해 이모지와 불렛포인트를 활용하세요.
        """

        # AI 리포트 생성
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        # 에러 발생 시 원인을 상세히 리턴하여 텔레그램으로 보냅니다.
        return f"AI 분석 중 오류 발생: {str(e)}"

def send_telegram_message(text):
    """
    생성된 리포트를 텔레그램으로 전송합니다.
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        # MarkdownV2 대신 일반 텍스트 모드로 보내서 특수문자 에러를 방지합니다.
        "parse_mode": "HTML" 
    }
    try:
        res = requests.post(url, json=payload)
        return res.json()
    except Exception as e:
        print(f"텔레그램 전송 오류: {e}")
        return None

if __name__ == "__main__":
    print("🚀 리포트 생성 및 전송 시작...")
    report_content = generate_report()
    
    # 텔레그램 메시지 전송
    send_telegram_message(report_content)
    print("✅ 모든 작업 완료!")
