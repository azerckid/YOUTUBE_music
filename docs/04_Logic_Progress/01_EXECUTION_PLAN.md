# Execution Plan
> Created: 2026-08-11 13:53
> Last Updated: 2026-08-11 15:09

## 1. 선행 확인

- [x] 사용자가 HTML 미리보기의 테마 입력 흐름을 확인한다.
- [x] 사용자 피드백을 `02_PROTOTYPE_REVIEW.md`에 기록한다.
- [ ] Suno API 로그인 후 엔드포인트, 인증, 과금과 다운로드 계약을 기록한다.
- [ ] API 키를 코드 밖에서 읽는 로컬 설정 방식을 확정한다.

## 2. 기반 구현

- [x] Python 프로젝트 실행 구조를 만든다.
- [ ] 환경변수 유효성 검사를 만든다.
- [x] 프로젝트 ID와 안전한 출력 경로 생성을 만든다.
- [x] `project.json` 읽기·쓰기와 원자적 갱신을 만든다.
- [x] 단계별 상태 전이와 실패 기록을 만든다.
- [x] 완료된 로컬 중간 파일을 재사용하는 재개 로직을 만든다.

## 3. 로컬 미디어 구현

- [x] FFmpeg와 FFprobe 존재 여부 검사를 만든다.
- [x] 각 곡의 길이 측정을 만든다.
- [x] 파일명 순서 정렬을 만든다.
- [x] 첫 세트 챕터 시작 시간 계산을 만든다.
- [x] 곡 세트 연결을 만든다.
- [x] 전체 세트 3회 반복을 만든다.
- [x] 대표 이미지 크기 조정과 제목 합성을 만든다.
- [x] 1080p, 24fps, H.264, AAC MP4 렌더링을 만든다.
- [x] 결과 MP4의 스트림과 길이 검사를 만든다.

## 4. AI 생성 구현

- [x] API 없는 규칙 기반 테마 제작 방향을 만든다.
- [x] 곡 계획과 곡별 Suno 프롬프트 파일 생성을 만든다.
- [ ] OpenAI 이미지 생성 요청과 파일 저장을 만든다.
- [x] 영상 제목, 설명과 해시태그의 로컬 템플릿 생성을 만든다.
- [ ] 공식 계약에 맞춘 Suno 생성 요청을 만든다.
- [ ] Suno 작업 상태 확인을 만든다.
- [ ] Suno 음원 다운로드와 곡별 저장을 만든다.
- [ ] 재시도 횟수와 비용 보호 로직을 만든다.

## 5. UI와 통합

- [x] 테마 입력 화면을 만든다.
- [x] 설정 점검 결과를 표시한다.
- [x] 현재 제작 단계와 진행률을 표시한다.
- [x] 오류 원인과 재시도 동작을 표시한다.
- [x] 결과 파일 목록과 폴더 열기 기능을 만든다.
- [x] 테마 입력부터 수동 파일 준비와 결과 폴더까지 전체 흐름을 연결한다.

## 6. 검증

- [x] 시간 계산 단위 테스트를 통과한다.
- [x] 실패 후 재개 테스트를 통과한다.
- [ ] API 실패 계약 테스트를 통과한다.
- [x] 짧은 영상 통합 테스트를 통과한다.
- [ ] 장시간 영상 검사를 통과한다.
- [ ] 실제 YouTube 업로드 확인을 기록한다.

## 7. 안정화

- [x] 제작 시작 전 상태를 원자적으로 `running`으로 전환한다.
- [x] 중복 실행과 완료 프로젝트 재실행을 차단한다.
- [x] 비정상 종료 후 `running` 고착 상태를 복구한다.
- [x] 완료 단계와 유효한 산출물을 재사용한다.
- [x] Host, Origin과 loopback 바인딩을 검사한다.
- [x] 렌더링 전 디스크 여유 공간을 검사한다.
- [x] macOS 글꼴 폴백과 사용자 조치 오류를 제공한다.
- [x] 상태·보안·복구 회귀 테스트를 추가한다.

## 8. Related Documents

- **Concept_Design**: [Product Specifications](../01_Concept_Design/03_PRODUCT_SPECS.md) - 구현 대상 기능
- **UI_Screens**: [Screen Flow](../02_UI_Screens/00_SCREEN_FLOW.md) - 사용자 흐름
- **UI_Screens**: [HTML Preview](../02_UI_Screens/previews/01_MAIN_FLOW_PREVIEW.html) - 구현 전 화면 기준
- **Technical_Specs**: [Data Schema](../03_Technical_Specs/01_DB_SCHEMA.md) - 프로젝트 상태 구조
- **Technical_Specs**: [API Specifications](../03_Technical_Specs/02_API_SPECS.md) - 외부 연동 계약
- **QA_Validation**: [Test Scenarios](../05_QA_Validation/01_TEST_SCENARIOS.md) - 검증 시나리오
