import base64
import html
import json
import mimetypes
import os
import re
from datetime import date
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="우리가 사랑한 지 300일째",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

START_DATE = date(2026, 1, 29)
SLIDE_DELAY = 8.0

LETTER_BG_NAME = "letter_bg"
LETTER_BG_BLUR = 3
LETTER_BG_WHITE_BLEND = 0.35
BGM_NAME = "bgm"

QUIZZES = [
    {
        "q": "Q1. 우리가 처음 사귀기 시작한 날짜는?",
        "options": ["12월 19일", "12월 29일", "1월 29일", "1월 19일"],
        "answer": 3,
    },
    {
        "q": "Q2. 우리가 처음 만났던 장소는?",
        "options": ["남원", "부산", "평창", "서울"],
        "answer": 3,
    },
    {
        "q": "Q3. 이곳의 장소는?",
        "image": "quiz3",
        "options": ["광한루원", "서울대공원", "올림픽공원", "근린공원"],
        "answer": 3,
    },
    {
        "q": "Q4. 우리가 같이 갔던 곳 중 가장 강렬한 기억이 남는 곳은?",
        "options": ["서울", "강릉", "부산", "대전"],
        "answer": 2,
    },
    {
        "q": "Q5. 이 사진은 우리가 몇 일에 찍었을까??",
        "image": "quiz5",
        "options": ["99", "100", "101"],
        "answer": 2,
    },
    {
        "q": "Q6. 이 사진은 우리가 몇 일에 찍었을까??",
        "image": "quiz6",
        "options": ["199", "200", "201"],
        "answer": 2,
    },
    {
        "q": "Q7. 이 사진은 내가 몇 일에 찍었을까???",
        "image": "quiz7",
        "options": ["300", "301", "302"],
        "answer": 1,
    },
    {
        "q": "Q8. 앞으로도 나랑 오래오래 행복하게 지낼 거지?",
        "options": ["당연하지 ", "무조건이지 ", "평생 함께하자 ", "모두 정답!!!!!!!!!"],
        "answer": 4,
    },
]

CAPTIONS = [
    "특별할 것 없던 평범한 날\n우리는 운명처럼 만난 것 같아",
    "처음 어색하게 웃던 순간이 엊그제 같은데\n어느새 세상에서 가장 가까운 사이가 되었네",
    "수빈이의 존재 자체가\n나에게는 정말 큰 힘이 되어주었어",
    "수빈이와 함께 많은 곳을 여행하고 많은 것을 경험하면서\n추억도 정말 많이 쌓은 거 같아",
    "사소한 것 하나까지 나를 먼저 챙겨주는\n수빈이의 따뜻한 마음에 늘 고마워",
    "같이 함께하며 닮아가는 우리 모습을 보면\n나도 모르게 기분 좋은 미소가 지어져",
    "맛있는 음식, 디저트를 보면 수빈이가 제일 먼저 떠오르고,\n예쁜 풍경이나 장소를 보면 수빈이와 함께 가고 싶어져",
    "어느새 우리는 계절이 바뀌는 걸 함께 느끼면서\n추억들이 차곡차곡 쌓였네",
    "때로는 투덜거릴 때도 있었지만,\n이해해 주고 보듬어 줘서 고마워",
    "언제 어디서나 든든하게 내 편이 되어줘서\n세상 그 누구보다 고맙고 든든해",
    "수빈이와 함께 울고 웃었던 수많은 날들처럼\n앞으로 함께할 날들도 기대가 돼",
    "같이 가고 싶은 곳도 아직 너~무 많고,\n함께 해보고 싶은 것들도 끝이 없네",
    "바쁜 일상 속에서도 늘 변함없이\n사랑해줘서 진심으로 고마워",
    "나만 보고 멀리서 와준 수빈이 덕분에\n지루한 일상이 아니라 재밌고 행복한 일상이었어",
    "매일 붙어있고 매일 일상을 보내도\n조금만 떨어져 있으면 자꾸 보고싶어져",
    "퇴근하고 뭐 먹을지 묻고 집 와서 오늘 있었던 일 말하고\n재밌는 영상 보며 밥 먹는 게 왜이렇게 행복할까?",
    "별일 없어서 기억에 잘 남지 않은 그런 하루\n그런 평범한 하루를 살아가자",
    "우리의 300일을 축하하며\n그동안의 소중한 순간들을 이렇게 모아봤어",
    "앞으로 다가올 1주년, 그리고 그 이후에도\n지금처럼 손 꼭 잡고 예쁜 추억 많이 만들자!",
    "마지막으로 전하고 싶은 말을 써봤어!!",
    "아래의 [💌 편지 보기] 버튼을 눌러봐! 🎉",
]

LETTER_TEXT = """To. 세상에서 제일 사랑하는 0순위 내 편 수빈찌에게

안뇽 우리가 처음 손을 잡은 게 엊그제 같은데 어느덧 300일이라는 시간을
함께했네. 수빈이랑 있으면 시간이 2배는 더 빠르게 가는 거 같아 ㅎㅎ

손 편지를 쓸까 하다가 조금 색다른 편지 없을까 고민하던 와중에 파이썬으로 편지를 만들어 봤어. 예쁘게 봐줬으면 좋겠다 :)
만들면서 사진을 하나씩 다시 돌아보니까 우리가 그동안 참 예쁘게 많은 추억을 쌓았다는 생각이 들어 ㅎㅎ

내가 저번에 수빈이에게 많이 실망스러운 모습을 보여주고 그런 내 모습 때문에
수빈이가 많이 힘들었지? 나의 행동 때문에 수빈이의 마음에 깊은 상처 줘서 미안해.
좋은 행동 10가지보다 싫은 행동 1가지가 더 안 좋다는 것을 정말 많이 깨닫고 반성했어. 앞으로 그런 행동 보이지 않을게. 꼭 약속할게

앞으로도 우리 많이 싸우지 말고, 맛있는 거 많이 먹으러 다니면서 오래오래 행복하자. 300일 정말 축하하고, 많이 사랑해!

앞으로 다가올 수많은 날도 지금처럼 서로 아끼고 의지하며 틈틈이 행복하자!!


From. 언제나 수빈이 편인 정훈이가"""

VALID_IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".webp", ".heic")
VALID_AUDIO_EXTS = (".mp3", ".m4a", ".wav", ".ogg", ".aac")
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()


def get_search_dirs():
    dirs = [BASE_DIR]
    try:
        for entry in os.listdir(BASE_DIR):
            full_path = os.path.join(BASE_DIR, entry)
            if os.path.isdir(full_path) and entry.lower() == "photos":
                dirs.append(full_path)
    except Exception:
        pass
    return dirs


def get_files_signature():
    sig = []
    for folder in get_search_dirs():
        if not os.path.exists(folder):
            continue
        try:
            for file in sorted(os.listdir(folder)):
                full_path = os.path.join(folder, file)
                if os.path.isfile(full_path):
                    sig.append((full_path, os.path.getsize(full_path)))
        except Exception:
            pass
    return tuple(sig)


def natural_sort_key(filename):
    return [int(part) if part.isdigit() else part.lower() for part in re.split(r"(\d+)", filename)]


def file_to_data_uri(path):
    ext = os.path.splitext(path)[1].lower()
    mime = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
        ".heic": "image/heic",
        ".mp3": "audio/mpeg",
        ".m4a": "audio/mp4",
        ".wav": "audio/wav",
        ".ogg": "audio/ogg",
        ".aac": "audio/aac",
    }.get(ext) or mimetypes.types_map.get(ext, "application/octet-stream")

    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def make_dummy_svg_data_uri(color_hex, index_num):
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="900" height="560">'
        f'<rect width="100%" height="100%" fill="{color_hex}"/>'
        f'<text x="50%" y="48%" dominant-baseline="middle" text-anchor="middle" '
        f'font-family="-apple-system, sans-serif" font-size="36" fill="#5c4248">'
        f'Photo {index_num}</text>'
        f'<text x="50%" y="58%" dominant-baseline="middle" text-anchor="middle" '
        f'font-family="-apple-system, sans-serif" font-size="18" fill="#7a5b62">'
        f'같은 폴더 또는 photos 폴더에 사진을 넣어주세요</text>'
        f'</svg>'
    )
    encoded = base64.b64encode(svg.encode("utf-8")).decode("ascii")
    return f"data:image/svg+xml;base64,{encoded}"


def make_quiz_placeholder_uri(name):
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="720" height="400">'
        f'<rect width="100%" height="100%" rx="18" fill="#fce8ef"/>'
        f'<text x="50%" y="46%" dominant-baseline="middle" text-anchor="middle" '
        f'font-family="-apple-system, sans-serif" font-size="24" fill="#8f4b63">'
        f'{name}.jpg 사진을 찾지 못했어요</text>'
        f'<text x="50%" y="60%" dominant-baseline="middle" text-anchor="middle" '
        f'font-family="-apple-system, sans-serif" font-size="16" fill="#a86d81">'
        f'같은 폴더 또는 photos 폴더에 {name}.jpg / .png 파일을 넣어주세요</text>'
        f'</svg>'
    )
    encoded = base64.b64encode(svg.encode("utf-8")).decode("ascii")
    return f"data:image/svg+xml;base64,{encoded}"


def load_media():
    search_dirs = get_search_dirs()
    slide_uris = []
    letter_bg_uri = None
    bgm_uri = ""
    fallback_bgm_uri = ""
    quiz_img_uris = {}

    quiz_img_stems = set()
    for q in QUIZZES:
        img_name = q.get("image")
        if img_name:
            quiz_img_stems.add(os.path.splitext(img_name)[0].lower())

    for folder in search_dirs:
        if not os.path.exists(folder):
            continue
        try:
            files = sorted(os.listdir(folder), key=natural_sort_key)
        except Exception:
            continue

        for file in files:
            stem, ext = os.path.splitext(file)
            ext_lower = ext.lower()
            img_path = os.path.join(folder, file)
            if not os.path.isfile(img_path):
                continue

            stem_lower = stem.lower()

            if ext_lower in VALID_AUDIO_EXTS:
                if stem_lower == BGM_NAME.lower() and not bgm_uri:
                    try:
                        bgm_uri = file_to_data_uri(img_path)
                    except Exception:
                        pass
                elif not fallback_bgm_uri:
                    try:
                        fallback_bgm_uri = file_to_data_uri(img_path)
                    except Exception:
                        pass
                continue

            if ext_lower not in VALID_IMAGE_EXTS:
                continue

            if stem_lower == LETTER_BG_NAME.lower():
                if letter_bg_uri is None:
                    try:
                        letter_bg_uri = file_to_data_uri(img_path)
                    except Exception:
                        pass
                continue

            if stem_lower in quiz_img_stems:
                if stem_lower not in quiz_img_uris:
                    try:
                        quiz_img_uris[stem_lower] = file_to_data_uri(img_path)
                    except Exception:
                        pass
                continue

            try:
                slide_uris.append(file_to_data_uri(img_path))
            except Exception:
                pass

    if not bgm_uri:
        bgm_uri = fallback_bgm_uri

    if not slide_uris:
        colors = ["#FFB6C1", "#FFD1DC", "#FFC0CB", "#E6E6FA", "#FFF0F5", "#FFE4E1"]
        for i in range(len(CAPTIONS)):
            slide_uris.append(make_dummy_svg_data_uri(colors[i % len(colors)], i + 1))

    if letter_bg_uri is None:
        letter_bg_uri = slide_uris[-1]

    prepared_quizzes = []
    for q in QUIZZES:
        item = {
            "q": q["q"],
            "options": q["options"],
            "answer": q["answer"],
        }
        img_name = q.get("image")
        if img_name:
            key = os.path.splitext(img_name)[0].lower()
            item["image_uri"] = quiz_img_uris.get(key, make_quiz_placeholder_uri(os.path.splitext(img_name)[0]))
        prepared_quizzes.append(item)

    return slide_uris, letter_bg_uri, prepared_quizzes, bgm_uri


@st.cache_data(show_spinner=False)
def build_html(files_sig):
    slide_uris, letter_bg_uri, prepared_quizzes, bgm_uri = load_media()
    days_count = (date.today() - START_DATE).days + 1
    letter_blur_px = max(0, LETTER_BG_BLUR * 2)
    letter_white_alpha = max(0.0, min(1.0, LETTER_BG_WHITE_BLEND))
    safe_target = max(1, len(prepared_quizzes))

    slides_json = json.dumps(slide_uris, ensure_ascii=False)
    captions_json = json.dumps(CAPTIONS, ensure_ascii=False)
    quizzes_json = json.dumps(prepared_quizzes, ensure_ascii=False)
    bgm_json = json.dumps(bgm_uri, ensure_ascii=False)
    letter_html = html.escape(LETTER_TEXT)

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />
  <meta name="apple-mobile-web-app-capable" content="yes" />
  <meta name="apple-mobile-web-app-status-bar-style" content="default" />
  <title>우리가 사랑한 지 {days_count}일째</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html, body {{
      width: 100%;
      height: 100%;
      overflow: hidden;
      font-family: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Noto Sans KR", sans-serif;
      background: #fcf7f5;
      color: #38292e;
      -webkit-user-select: none;
      user-select: none;
    }}
    .hidden {{ display: none !important; }}

    #musicBtn {{
      position: fixed;
      top: max(12px, env(safe-area-inset-top));
      left: 14px;
      z-index: 100;
      border: 1.5px solid rgba(255, 130, 165, 0.35);
      border-radius: 999px;
      background: rgba(255, 255, 255, 0.88);
      color: #402e33;
      font-size: 14px;
      font-weight: 700;
      padding: 8px 14px;
      cursor: pointer;
      box-shadow: 0 4px 14px rgba(60, 35, 42, 0.12);
      backdrop-filter: blur(8px);
      -webkit-backdrop-filter: blur(8px);
      transition: transform 0.12s ease, background 0.2s ease;
    }}
    #musicBtn:active {{
      transform: scale(0.95);
    }}

    #quizScreen {{
      position: fixed;
      inset: 0;
      z-index: 20;
      background: linear-gradient(155deg, #fff5f7 0%, #fdeef2 50%, #f8eef9 100%);
      display: flex;
      align-items: center;
      justify-content: center;
      padding: max(56px, calc(env(safe-area-inset-top) + 46px)) 18px max(16px, env(safe-area-inset-bottom));
    }}
    .quiz-card {{
      width: min(92vw, 640px);
      max-height: calc(100dvh - 76px);
      overflow-y: auto;
      -webkit-overflow-scrolling: touch;
      background: rgba(255, 255, 255, 0.92);
      border-radius: 26px;
      padding: clamp(20px, 3.5vw, 34px);
      box-shadow: 0 18px 44px rgba(120, 60, 80, 0.12);
      display: flex;
      flex-direction: column;
      gap: 16px;
      text-align: center;
    }}
    .quiz-header {{
      font-size: clamp(20px, 2.8vw, 26px);
      font-weight: 800;
      color: #3d2730;
    }}
    .quiz-sub {{
      font-size: 15px;
      color: #7d5d68;
      margin-top: 6px;
    }}
    .gauge-wrap {{
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}
    .gauge-info {{
      display: flex;
      justify-content: space-between;
      font-size: 14px;
      font-weight: 700;
      color: #b84a6f;
    }}
    .gauge-track {{
      width: 100%;
      height: 18px;
      background: #f5dde6;
      border-radius: 999px;
      overflow: hidden;
      box-shadow: inset 0 1px 4px rgba(120, 50, 75, 0.12);
    }}
    .gauge-fill {{
      width: 0%;
      height: 100%;
      background: linear-gradient(90deg, #ff8fab 0%, #ff5d8f 100%);
      border-radius: 999px;
      transition: width 0.45s cubic-bezier(0.22, 1, 0.36, 1);
    }}
    .question-text {{
      font-size: clamp(18px, 2.5vw, 22px);
      font-weight: 700;
      line-height: 1.5;
      color: #2f2026;
      padding: 4px;
    }}
    .quiz-image {{
      display: block;
      max-width: 100%;
      max-height: 240px;
      width: auto;
      height: auto;
      margin: 4px auto 12px;
      border-radius: 14px;
      object-fit: contain;
      box-shadow: 0 8px 22px rgba(60, 35, 42, 0.14);
    }}
    .options {{
      display: grid;
      grid-template-columns: 1fr;
      gap: 10px;
    }}
    .option-btn {{
      width: 100%;
      border: 2px solid #f2dce4;
      border-radius: 16px;
      background: #ffffff;
      color: #3c2a31;
      font-size: 17px;
      font-weight: 600;
      padding: 13px 18px;
      cursor: pointer;
      transition: transform 0.12s ease, background 0.2s ease, border-color 0.2s ease;
    }}
    .option-btn:active {{
      transform: scale(0.98);
    }}
    .option-btn.correct {{
      background: #e8f8ef;
      border-color: #38b26f;
