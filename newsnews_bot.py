import feedparser
import requests
import json
from urllib.parse import quote
from datetime import datetime # 날짜 기능을 위해 추가

# 1. 환경 설정
TELEGRAM_TOKEN = "8579899694:AAHwf39HROL2wnPob9QcQjDP2ysLL-Ogcn0"
CHAT_ID = "5662185496"
GEMINI_API_KEY = "AIzaSyBa0rDiaeyLAfSqS2T9H3h5-wb9CrjLDtg"

def get_market_context():
    try:
        print("1. 최신 시장 데이터 수집 중...")
        # 부동산 이슈를 더 잘 긁어오도록 키워드 보강
        keywords = "미국증시 섹터 실적 한국반도체 수급 서울신축아파트 전세매물부족 지방미분양"
        encoded_query = quote(keywords)
        rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ko&gl=KR&ceid=KR:ko"
        feed = feedparser.parse(rss_url)
        return "\n".join([f"- {entry.title}" for entry in feed.entries[:12]])
    except:
        return "최신 글로벌 매크로 및 부동산 트렌드 활용"

def analyze_and_send():
    try:
        market_data = get_market_context()
        # 오늘 날짜 세팅 (예: 2026년 04월 04일)
        today_date = datetime.now().strftime("%Y년 %m월 %d일")
        
        print(f"2. {today_date} 기준 제미나이 전략 분석 중...")
        
        gemini_url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
        
        prompt = f"""
        너는 32세 자산가 타겟의 글로벌 투자 전략가다. 아래 데이터를 바탕으로 리포트를 작성하라.
        
        [작성 가이드라인]
        - 작성일: {today_date} (반드시 상단에 명시)
        - 대상: 32세 투자자
        
        [리포트 구성 및 요구사항]
        1. **미 증시 섹터 요약**: 직전 미 증시 맵(Heatmap) 기준, 어떤 산업에 돈이 몰렸고 어떤 이슈(금리, 실적 등)가 핵심인지 요약.
        2. **국장 연결고리**: 미 증시 흐름이 오늘 한국 반도체(SK하이닉스, 삼성전자) 및 소부장 수급에 줄 영향 분석.
        3. **부동산 현장 팩트 체크**: 
           - 서울 신축 아파트 신고가 현황 및 매수 심리.
           - 전세가율 상승 및 매물 부족 현상에 따른 갭투자 가능성.
           - 지방 미분양 증감에 따른 수도권 쏠림(양극화) 심화 정도.
        4. **오늘의 추천 테마 2개**: 종목명 또는 섹터를 근거와 함께 제시.

        [데이터 소스]:
        {market_data}
        """

        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        response = requests.post(gemini_url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload))
        result = response.json()
        
        if 'candidates' in result:
            report_text = result['candidates'][0]['content']['parts'][0]['text']
            
            print("3. 텔레그램 최종 전송...")
            telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
            
            # 텍스트가 너무 길면 자르기
            if len(report_text) > 4000:
                report_text = report_text[:3800] + "\n\n(상세 내용 생략...)"

            tel_payload = {
                "chat_id": CHAT_ID,
                "text": report_text
            }
            
            res = requests.post(telegram_url, json=tel_payload)
            
            if res.status_code == 200:
                print(f"✅ {today_date} 리포트 전송 성공!")
            else:
                print(f"❌ 전송 실패: {res.text}")
        else:
            print(f"❌ AI 분석 실패")

    except Exception as e:
        print(f"❗ 시스템 오류: {e}")

if __name__ == "__main__":
    analyze_and_send()