from pathlib import Path
from io import BytesIO
import base64
import html
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from content import ROLES, QUESTIONS, display_options, score_answers, result_groups, PAIR_TIPS

ROOT = Path(__file__).resolve().parent
st.set_page_config(page_title='팀냥이 · 팀플 속 나의 고양이', page_icon='🐱', layout='centered')
st.markdown('''<style>
.stApp {background:#FCFAF6;color:#30323B}
.block-container {max-width:800px;padding-top:2rem;padding-bottom:3rem}
h1,h2,h3 {color:#30323B;letter-spacing:-.035em}
div.stButton>button {border-radius:16px;min-height:48px;white-space:normal;text-align:left}
.hero {padding:24px;border:1px solid #E9E4DA;border-radius:24px;background:white;text-align:center;margin:16px 0}
.eyebrow {font-size:12px;letter-spacing:.16em;color:#82766A;font-weight:700}
.muted {color:#756E66;font-size:14px}
.score {margin:16px 0}.track {height:12px;border-radius:8px;background:#EEEAE4;margin-top:8px}
.fill {height:12px;border-radius:8px}
@media(max-width:600px){.block-container{padding:1.4rem 1rem}.hero{padding:18px}}
</style>''', unsafe_allow_html=True)

def reset():
    st.session_state.page = 'intro'
    st.session_state.index = 0
    st.session_state.answers = [None] * len(QUESTIONS)

if 'page' not in st.session_state:
    reset()

def choose(index, key):
    st.session_state.answers[index] = key

def move(step):
    st.session_state.index += step

def finish():
    if all(st.session_state.answers):
        st.session_state.page = 'result'

def start_quiz():
    st.session_state.page = 'quiz'

def edit_last():
    st.session_state.page = 'quiz'
    st.session_state.index = 11

def cat_html(key, size=200):
    encoded = base64.b64encode((ROOT / 'assets' / f'{key}.png').read_bytes()).decode()
    return f'<img src="data:image/png;base64,{encoded}" alt="{ROLES[key]["name"]} 고양이 캐릭터" style="width:min({size}px,100%);height:auto">'

def font(size):
    return ImageFont.truetype(str(ROOT / 'fonts' / 'NotoSansKR-Regular.ttf'), size)

def wrap(draw, text, face, max_width):
    lines, current = [], ''
    for char in text:
        if draw.textlength(current + char, font=face) > max_width and current:
            lines.append(current)
            current = char
        else:
            current += char
    return lines + ([current] if current else [])

def make_card(scores):
    winners, secondary = result_groups(scores)
    bg = ROLES[winners[0]]['pale'] if len(winners) == 1 else '#F4EFE7'
    card = Image.new('RGB', (1080, 1420), bg)
    d = ImageDraw.Draw(card)
    d.rounded_rectangle((50,50,1030,1370), radius=40, fill='white')
    d.text((95,90), 'TEAMNYANG / 팀냥이', font=font(28), fill='#756E66')
    count = len(winners)
    # A 2x2 grid for 3+ tied roles; side by side for two.
    thumb = 360 if count <= 2 else 260
    for i,key in enumerate(winners):
        image = Image.open(ROOT / 'assets' / f'{key}.png').convert('RGBA').resize((thumb,thumb))
        x = (1080-thumb)//2 if count == 1 else (150 + (i % 2) * 430)
        y = 170 if count <= 2 else 150 + (i//2) * 260
        card.paste(image, (x,y), image)
    y = 580 if count <= 2 else 720
    title = ' × '.join(ROLES[k]['name'] for k in winners)
    for line in wrap(d, title, font(54), 890):
        d.text((95,y),line,font=font(54),fill='#30323B'); y += 78
    intro = ROLES[winners[0]]['intro'] if count == 1 else '여러 역할의 성향이 같은 점수로 나타났어요.'
    for line in wrap(d,intro,font(30),890):
        d.text((95,y+15),line,font=font(30),fill='#55515A'); y += 45
    if secondary:
        d.text((95,y+25),'보조 성향: ' + ' · '.join(ROLES[k]['name'] for k in secondary),font=font(27),fill='#756E66'); y += 60
    y += 45
    for key,r in ROLES.items():
        d.text((95,y),f'{r["name"]}  {scores[key]}점',font=font(25),fill=r['color'])
        d.rounded_rectangle((360,y+8,975,y+30),radius=10,fill='#EEEAE4')
        if scores[key]:
            d.rounded_rectangle((360,y+8,360+615*scores[key]/12,y+30),radius=10,fill=r['color'])
        y += 65
    d.text((95,1295),'역할 선호도를 탐색하는 재미용 테스트 · 12문항',font=font(22),fill='#756E66')
    output = BytesIO(); card.save(output,format='PNG'); return output.getvalue()

st.markdown('<div class="eyebrow">TEAMNYANG · TEAM PROJECT PERSONALITY</div>',unsafe_allow_html=True)
st.title('팀플 속 나의 고양이 찾기')

if st.session_state.page == 'intro':
    st.write('아이디어를 내는 나, 꼼꼼히 확인하는 나, 직접 만드는 나, 함께 맞춰가는 나. 팀 프로젝트에서 자주 선택하는 행동으로 나의 고양이를 만나보세요.')
    cols = st.columns(2)
    for i,(key,r) in enumerate(ROLES.items()):
        with cols[i%2]:
            st.markdown(f'<div class="hero" style="background:{r["pale"]}">{cat_html(key,145)}<h3 style="color:{r["color"]}">{r["name"]}</h3></div>',unsafe_allow_html=True)
    st.caption('12문항 · 약 3분 · 정답 없음 · 가입 없이 이용')
    st.button('내 고양이 찾기 →', key='start', type='primary', use_container_width=True,on_click=start_quiz)
    st.caption('성격·역량을 진단하는 검사가 아닌, 팀에서 선호하는 행동을 돌아보는 재미용 테스트예요. 응답은 서버의 현재 세션에만 보관하며 파일이나 데이터베이스에 저장하지 않아요. 페이지를 새로고침하면 초기화될 수 있어요.')

elif st.session_state.page == 'quiz':
    i = st.session_state.index
    answered = sum(a is not None for a in st.session_state.answers)
    st.progress(answered/12, text=f'응답 진행률 · {answered}/12')
    stage, question, _ = QUESTIONS[i]
    st.caption(f'문항 {i+1} / 12 · {stage}')
    st.subheader(question)
    st.write('실제 상황에서 내가 먼저 할 것 같은 행동 하나를 골라주세요.')
    for j,(key,label) in enumerate(display_options(i)):
        selected = st.session_state.answers[i] == key
        st.button(('✓ ' if selected else f'{"ABCD"[j]}. ') + label,key=f'answer_{i}_{key}',type='primary' if selected else 'secondary',use_container_width=True,on_click=choose,args=(i,key))
    left,right = st.columns(2)
    left.button('← 이전',disabled=i==0,on_click=move,args=(-1,),use_container_width=True)
    if i < 11:
        right.button('다음 →',disabled=st.session_state.answers[i] is None,on_click=move,args=(1,),use_container_width=True)
    else:
        right.button('내 고양이 보기 →',disabled=not all(st.session_state.answers),on_click=finish,use_container_width=True)
    st.caption('선택 후 다음 버튼을 눌러주세요. 이전 문항으로 돌아가 답변을 바꿀 수 있어요.')
    with st.expander('테스트 처음부터 다시 시작'):
        st.button('응답을 지우고 처음으로',on_click=reset)

else:
    scores = score_answers(st.session_state.answers)
    winners, secondary = result_groups(scores)
    names = ' × '.join(ROLES[k]['name'] for k in winners)
    cats = ''.join(cat_html(k, 200 if len(winners)<=2 else 145) for k in winners)
    intro = ROLES[winners[0]]['intro'] if len(winners)==1 else '여러 역할의 성향이 같은 점수로 나타났어요. 상황에 따라 이 강점들을 함께 활용해보세요.'
    st.markdown(f'<div class="hero"><div class="eyebrow">YOUR TEAM CAT</div>{cats}<h2>당신은 {names}!</h2><p>{intro}</p></div>',unsafe_allow_html=True)
    if secondary:
        st.write('보조 성향은 **' + ' · '.join(ROLES[k]['name'] for k in secondary) + '**이에요.')
    st.subheader('팀에서 보이는 나의 모습')
    for key in winners:
        if len(winners)>1: st.markdown(f'**{ROLES[key]["name"]}**')
        for item in ROLES[key]['behaviors']: st.write('• ' + item)
    st.subheader('나의 역할 성향 점수')
    for key,r in ROLES.items():
        st.markdown(f'<div class="score"><strong style="color:{r["color"]}">{r["name"]}</strong><span style="float:right">{scores[key]} / 12점</span><div class="track"><div class="fill" style="width:{scores[key]/12*100}%;background:{r["color"]}"></div></div></div>',unsafe_allow_html=True)
    st.caption('선택한 행동에 해당하는 역할에 1점씩 더했어요. 네 역할 점수의 합계는 12점이에요. 이번 답변에서 나타난 역할 선호도이며, 실제 역량이나 맡을 수 있는 역할을 제한하지 않아요.')
    st.subheader('다음 프로젝트에서 활용하기')
    if len(winners)==1 and secondary:
        for second in secondary:
            st.info(f'{ROLES[winners[0]]["name"]} × {ROLES[second]["name"]}\n\n' + PAIR_TIPS[frozenset((winners[0],second))])
    elif len(winners)==2:
        st.info(PAIR_TIPS[frozenset(winners)])
    elif len(winners)>2:
        st.info('여러 역할이 함께 나타났어요. 팀에 필요한 업무와 내가 해보고 싶은 업무를 먼저 확인하고, 역할을 나눠 맡아보세요.')
    for key in winners:
        r=ROLES[key]
        with st.expander(f'{r["name"]}의 구체적인 활용법',expanded=True):
            for task,method in r['tasks']:
                st.markdown(f'**{task}**'); st.write(method)
            st.markdown('**주의할 점**'); st.write(r['caution'])
            st.markdown('**다음 팀플에서 해볼 행동**'); st.write(r['challenge'])
    with st.expander('다른 고양이의 역할도 알아보기'):
        for key,r in ROLES.items():
            if key not in winners:
                st.markdown(f'**{r["name"]}**'); st.write(r['intro'])
                for task,method in r['tasks']: st.write(f'• {task}: {method}')
    st.divider()
    st.download_button('내 고양이 카드 저장하기 · PNG',data=make_card(scores),file_name='teamnyang_result.png',mime='image/png',use_container_width=True)
    a,b=st.columns(2)
    a.button('다시 테스트하기',key='result_reset',on_click=reset,use_container_width=True)
    b.button('마지막 답변 수정하기',key='edit_last',on_click=edit_last,use_container_width=True)
    st.caption('나와 팀원을 한 유형으로 단정하기보다는, 서로의 역할을 이야기하는 출발점으로 활용해보세요.')
