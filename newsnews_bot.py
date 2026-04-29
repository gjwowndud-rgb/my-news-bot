import os
import requests
import google.generativeai as genai

# 환경 변수 로드
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def generate_report():
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        
        # [해결책] 모델명을 'gemini-1.5-flash'로 호출합니다. 
        # 만약 이 이름이 실패하면 자동으로 목록을 확인하도록 예외 처리를 강화했습니다.
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = """
        당신은 전문 투자 전략가입니다. 아래 항목을 객관적으로 분석하세요.
        1. 국제 시장 자금 흐름 (금리, 환율, 원자재)
        2. 국내 증권가 산업별 수급 및 비중
        3. 당일 추천 종목 3가지와 선정 이유
        * 부동산 정보는 절대 제외하고 냉철한 전문가 톤으로 한국어로 작성하세요.
        """

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        # 에러 발생 시 현재 키로 사용 가능한 모델 목록을 가져와서 알려줍니다.
        try:
            available_models = [m.name for m in genai.list_models()]
            return f"⚠️ 분석 실패.\n에러: {str(e)}\n\n사용 가능 모델 목록:\n" + "\n".join(available_models)
        except:
            return f"⚠️ 분석 실패: {str(e)}"

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, json=payload)

if __name__ == "__main__":
    report_content = generate_report()
    send_telegram_message(report_content)
