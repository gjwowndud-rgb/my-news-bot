import feedparser
import requests
import json
import os
from urllib.parse import quote
from datetime import datetime

# 1. GitHub Secrets에서 환경 변수 가져오기
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

def get_market_context():
    try:
        print("1. 최신 시장 데이터 수집 중...")
        # 검색 키워드: 미국증시, 한국반도체, 서울 부동산 핵심 이슈
        keywords = "미국증시 섹터 실적 한국반도체 수급 서울신축아파트 전세매물부족 지방미분양"
        encoded_query = quote(keywords)
        rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ko&gl=KR&ceid=KR:ko"
        feed = feedparser.parse(rss_url)
        
        if not feed.entries:
            return "최신 글로벌 매크로 및 부동산 트렌드 활용"
            
        return "\n".join([f"- {entry.title}" for entry in feed.entries[:12]])
    except Exception as e:
        print(f"⚠️ 데이터 수집 오류: {e}")
        return "글로벌 시장 지표 기반 분석"

def analyze_and_send():
    try:
        # 오늘 날짜 생성
        today_date = datetime.now().strftime("%Y년 %m월 %d일")
        market_data = get_market_context()
        
        print(f"2. {today_date} 기준 전략 리포트 생성 중...")
        
        # 제미나이 API 호출 설정 (안정적인 2.5 Flash 모델 사용)
        gemini_url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
        
        prompt = f"""
        너는 32세 자산가 타겟의 글로벌 투자 전략가다. 아래 데이터를 바탕으로 리포트를 작성하라.
        
        [작성 가이드라인]
        - 작성일: {today_date}
        - 대상: 32세 투자자
        
        [리포트 구성 및 요구사항]
        1. **미 증시 섹터 요약**: 직전 미 증시 섹터별 등락과 핵심 이슈 요약.
        2. **국내 증시 연결고리**: 미 증시 흐름이 오늘 한국 반도체 및 주도주 수급에 줄 영향 분석.
        3. **부동산 현장 팩트**: 서울 신축 신고가 현황, 전세가율 상승 및 매물 부족, 지방 양극화 현상 등 실질적 데이터 분석.
        4. **오늘의 추천 테마 2개**: 섹터 혹은 종목을 명확한 근거와 함께 제시.

        [수집 데이터]:
        {market_data}
        
        * 말투는 냉철하고 객관적인 전문가 톤으로, 불렛포인트를 활용해 가독성을 높일 것.
        * 특수문자 충돌 방지를 위해 과도한 마크다운 기호 사용은 자제할 것.
        """

        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        headers = {'Content-Type': 'application/json'}
        
        response = requests.post(gemini_url, headers=headers, data=json.dumps(payload))
        result = response.json()
        
        if 'candidates' in result:
            report_text = result['candidates'][0]['content']['parts'][0]['text']
            
            print("3. 텔레그램 리포트 전송 중...")
            telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
            
            # 메시지 길이 제한(4000자) 대응
            if len(report_text) > 4000:
                report_text = report_text[:3800] + "\n\n(상세 내용 생략...)"

            tel_payload = {
                "chat_id": CHAT_ID,
                "text": report_text,
                "parse_mode": "" # 특수문자 충돌 방지를 위해 일반 텍스트 모드 사용
            }
            
            res = requests.post(telegram_url, json=tel_payload)
            
            if res.status_code == 200:
                print(f"✅ {today_date} 리포트 전송 성공!")
            else:
                print(f"❌ 텔레그램 전송 실패: {res.text}")
        else:
            print(f"❌ AI 분석 실패: {result}")

    except Exception as e:
        print(f"❗ 시스템 오류 발생: {e}")

if __name__ == "__main__":
    analyze_and_send()