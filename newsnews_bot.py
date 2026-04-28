import feedparser
import requests
import json
import os
import re
from urllib.parse import quote
from datetime import datetime

# GitHub Secrets 환경 변수
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

def get_market_context():
    """뉴스 수집 실패 시에도 빈 결과가 나오지 않도록 보완"""
    try:
        keywords = "미국증시 섹터 한국반도체 서울신축아파트 전세매물부족"
        encoded_query = quote(keywords)
        rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ko&gl=KR&ceid=KR:ko"
        feed = feedparser.parse(rss_url)
        
        # 뉴스 제목만 추출 (최대 15개)
        titles = [f"- {entry.title}" for entry in feed.entries[:15]]
        if not titles:
            return "최근 매크로 경제 지표 및 부동산 시장 동향 (뉴스 수집 제한됨)"
        return "\n".join(titles)
    except:
        return "글로벌 금융 시장 및 수도권 부동산 트렌드"

def analyze_and_send():
    try:
        today_date = datetime.now().strftime("%Y년 %m월 %d일")
        market_data = get_market_context()
        
        # 제미나이 2.5 Flash 호출
        gemini_url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
        
        prompt = f"""
        당신은 32세 투자자를 위한 냉철한 시장 전략가입니다. 아래 데이터를 참고하여 리포트를 작성하세요.
        
        [가이드라인]
        - 날짜: {today_date}
        - 부동산은 단순 뉴스를 넘어 '서울 신축/전세/지방 양극화'라는 주제를 네가 아는 지식과 결합해 심도 있게 다룰 것.
        - 텔레그램 전송 오류 방지를 위해 별표(*)나 샵(#) 등 마크다운 기호를 절대 사용하지 말고, 가독성을 위해 불렛포인트(-)와 줄바꿈만 사용하세요.

        [수집된 데이터]:
        {market_data}
        """

        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        response = requests.post(gemini_url, json=payload, timeout=30)
        result = response.json()
        
        if 'candidates' in result:
            report_text = result['candidates'][0]['content']['parts'][0]['text']
            
            # 텔레그램 전송 (안정성을 위해 parse_mode를 제거한 순수 텍스트 전송)
            telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
            
            # 메시지 분할 전송 (4000자 초과 대비)
            if len(report_text) > 4000:
                report_text = report_text[:3900] + "\n\n(이하 생략)"

            tel_payload = {
                "chat_id": CHAT_ID,
                "text": report_text
            }
            
            res = requests.post(telegram_url, json=tel_payload, timeout=20)
            
            if res.status_code == 200:
                print(f"✅ {today_date} 전송 성공")
            else:
                print(f"❌ 전송 실패: {res.status_code}, {res.text}")
        else:
            print(f"❌ AI 분석 실패: {result}")

    except Exception as e:
        print(f"❗ 시스템 오류: {str(e)}")

if __name__ == "__main__":
    analyze_and_send()
