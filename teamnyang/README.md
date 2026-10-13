# 팀냥이 · 팀플 속 나의 고양이 찾기

12개의 팀 프로젝트 상황에 답하면 기획냥·분석냥·실행냥·조율냥을 만나는 Streamlit 앱입니다.

## 포함된 기능

- 시작 화면과 색상이 다른 고양이 4종
- 12문항 / 4지선다 / 응답 진행률 / 이전·다음 / 답변 수정
- 무응답 상태에서 다음 단계 차단
- 역할별 점수와 가로 막대그래프
- 공동 1위 및 공동 보조 성향 처리
- 역할 설명, 대표 행동, 담당 업무, 구체적 활용법, 주의할 점, 다음 도전
- 주 성향과 보조 성향을 연결한 업무 제안
- 한글이 포함된 결과 카드 PNG 다운로드
- 다시 시작, 모바일 화면 대응

실제 역량이나 성격을 진단하는 검사가 아닙니다. 결과는 답변에서 나타난 역할 선호도입니다. 답변은 현재 Streamlit 세션에만 보관하며 파일·DB에 저장하지 않습니다. 새로고침하면 초기화될 수 있습니다. API 키나 외부 AI 서비스가 필요하지 않습니다.

## GitHub에 올리는 방법 (웹 브라우저)

1. ZIP을 컴퓨터에 다운로드하고 압축을 풉니다.
2. https://github.com 에 로그인합니다.
3. 오른쪽 위 `+` → `New repository`를 선택합니다.
4. Repository name에 `teamnyang-test`를 입력합니다. 직접 제출용으로 공유할 경우 Public을 선택할 수 있습니다. 비공개 과제라면 Private을 선택하고 Streamlit에서 접근 권한을 연결하세요.
5. `Add a README file`을 선택한 뒤 `Create repository`를 누릅니다.
6. 저장소에서 `Add file` → `Upload files`로 들어갑니다.
7. 압축을 푼 `teamnyang` 폴더 **안의 파일과 하위 폴더**를 한꺼번에 업로드 영역으로 끌어놓습니다. 상위 `teamnyang` 폴더 자체나 ZIP을 올리는 방식이 아닙니다.
8. `assets`와 `fonts`는 폴더째 끌어놓아 경로를 유지하세요. 일반 파일 선택 창은 하위 폴더를 한꺼번에 선택하지 못할 수 있습니다.
9. 설명을 `Add Teamnyang app`로 입력하고 `Commit changes`(또는 `Propose changes`)를 눌러 반영합니다. 변경 제안으로 올렸다면 pull request를 main에 병합해야 배포에서 읽을 수 있습니다.
10. 저장소 첫 화면에 `app.py`, `content.py`, `requirements.txt`, `README.md`, `assets`, `fonts`가 보이는지 확인합니다.

## 파일 위치

| 위치 | 용도 |
|---|---|
| `app.py` | Streamlit 실행 파일 |
| `content.py` | 12문항, 결과 설명, 점수 계산 |
| `requirements.txt` | 설치할 Python 패키지 |
| `README.md` | 배포 설명서 |
| `assets/plan.png` | 주황색 기획냥 |
| `assets/analysis.png` | 회색 분석냥 |
| `assets/action.png` | 갈색 실행냥 |
| `assets/coord.png` | 크림색 조율냥 |
| `fonts/NotoSansKR-Regular.ttf` | 저장 카드의 한글 폰트 |
| `fonts/OFL.txt` | 폰트 라이선스 |

`app.py`와 `requirements.txt`는 저장소 최상위에 놓습니다. assets와 fonts 내부 파일을 최상위로 흩어놓지 마세요.

## Streamlit Community Cloud 배포

1. https://share.streamlit.io 에 로그인하고 GitHub 계정을 연결합니다.
2. `Create app`을 누릅니다.
3. 기존 앱 여부를 물으면 `Yup, I have an app`을 선택합니다.
4. 아래 값을 입력합니다.

| 입력 항목 | 입력할 값 |
|---|---|
| Repository | `내 GitHub 아이디/teamnyang-test` |
| Branch | `main` |
| Main file path | `app.py` |
| App URL | 원하는 이름. 이미 사용 중이면 다른 이름을 선택 |
| Advanced settings → Python version | `3.12` |
| Secrets | 입력하지 않음 |

5. `Deploy`를 누르고 설치와 실행이 끝날 때까지 기다립니다.
6. 앱이 열리면 표시된 실제 `https://…streamlit.app/` 주소를 복사해 과제 제출에 사용합니다.
7. 다른 사람이 접속해야 한다면 앱의 공유 설정에서 접근 가능 여부를 확인하고, 로그아웃한 브라우저나 시크릿 창에서 제출 URL을 열어보세요. GitHub 저장소의 공개 여부와 앱 접근 설정은 별도로 확인합니다.

## 배포 후 확인

- 시작 화면에서 네 고양이 이미지가 표시되는지
- 답변하지 않으면 다음 버튼이 비활성화되는지
- 이전 문항으로 돌아가 답변을 수정할 수 있는지
- 12문항 완료 후 네 점수의 합이 12인지
- 결과 페이지의 활용법과 PNG 저장이 동작하는지
- 휴대폰에서 문항과 버튼을 읽을 수 있는지

## 오류가 생기면

| 오류 | 확인할 내용 |
|---|---|
| Main file을 찾지 못함 | 저장소 최상위의 app.py, 배포 Branch가 main인지 확인 |
| content를 찾지 못함 | content.py가 app.py 옆에 있는지 확인 |
| 이미지 / 폰트를 찾지 못함 | assets, fonts 폴더와 파일 이름·대소문자 확인 |
| 패키지 설치 오류 | requirements.txt가 올라갔는지, Python 3.12인지 확인 |
| 수정이 반영되지 않음 | 배포한 저장소와 branch에 변경 사항이 커밋됐는지 확인 |

상위 폴더까지 올려 app.py가 `teamnyang/app.py`에 있다면 Main file path를 `teamnyang/app.py`로 바꿔 배포할 수도 있습니다. 다만 처음에는 안내한 최상위 구조를 권장합니다.

## 로컬 실행 (선택 사항)

Python 3.12 환경에서 압축을 푼 폴더로 이동한 뒤 실행합니다.

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## 수정과 채점 방식

문항과 설명은 content.py에서 수정합니다. 각 문항의 원본 선택지 순서는 기획→분석→실행→조율입니다. 화면에서는 문항별로 순서를 순환시켜 동일한 알파벳이 항상 같은 역할을 의미하지 않게 했습니다. 선택 1개당 해당 역할에 1점, 총 12점입니다. 가장 높은 점수를 받은 역할은 모두 공동 1위로 표시합니다. 단독 1위일 때만 다음으로 높은 양수 점수의 역할을 보조 성향으로 표시합니다.

## 사용한 자료

- Streamlit 공식 배포 안내: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy
- GitHub 공식 업로드 안내: https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository
- Noto Sans KR: SIL Open Font License 1.1. fonts/OFL.txt 참조.
- 고양이 일러스트: 이 앱용으로 직접 구성한 그래픽. 외부 이미지 호출 없음.

앱 파일을 준비한 단계이며 GitHub 업로드와 실제 계정에서의 Cloud 배포는 사용자가 진행합니다.
