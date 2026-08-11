# Roadmap
> Created: 2026-08-11 13:53
> Last Updated: 2026-08-11 13:53

## Phase 0. 구현 전 검증

- [ ] HTML UI Preview를 사용자에게 보여주고 피드백을 기록한다.
- [ ] Suno Platform에 로그인해 API 과금과 공식 스키마를 확인한다.
- [ ] OpenAI API 키와 과금 상태를 확인한다.
- [ ] 기존 채널명과 제목·설명 스타일을 확인해 채널 프로필을 작성한다.

## Phase 1. 로컬 미디어 엔진

- [ ] 프로젝트 매니페스트와 폴더 저장소를 구현한다.
- [ ] 음원 길이 분석과 챕터 계산을 구현한다.
- [ ] 곡 세트 연결과 3회 반복을 구현한다.
- [ ] 정지 이미지 기반 MP4 렌더링을 구현한다.
- [ ] FFprobe 기반 결과 검사를 구현한다.

## Phase 2. 생성 서비스 연결

- [ ] OpenAI 텍스트 생성 어댑터를 구현한다.
- [ ] OpenAI 이미지 생성 어댑터를 구현한다.
- [ ] 이미지 제목 합성과 `Cover.jpg` 생성을 구현한다.
- [ ] 검증된 공식 계약에 따라 Suno 어댑터를 구현한다.

## Phase 3. 전체 워크플로와 UI

- [ ] 테마 입력 화면을 구현한다.
- [ ] 12단계 오케스트레이터와 재개 기능을 구현한다.
- [ ] 진행·오류·결과 화면을 구현한다.
- [ ] 결과 폴더와 업로드 문구 생성을 통합한다.

## Phase 4. 실제 영상 검증

- [ ] 짧은 테스트 미디어로 전체 흐름을 검증한다.
- [ ] 장시간 테스트 영상을 생성한다.
- [ ] 참고 영상 3편과 규격·용량·음질을 비교한다.
- [ ] 실제 YouTube Studio 수동 업로드를 검증한다.

## 5. Related Documents

- **Concept_Design**: [Product Specifications](../01_Concept_Design/03_PRODUCT_SPECS.md) - 로드맵 범위
- **UI_Screens**: [Prototype Review](../02_UI_Screens/02_PROTOTYPE_REVIEW.md) - UI Gate 승인 상태
- **Technical_Specs**: [Development Principles](../03_Technical_Specs/00_DEVELOPMENT_PRINCIPLES.md) - 구현 기술 원칙
- **Technical_Specs**: [API Specifications](../03_Technical_Specs/02_API_SPECS.md) - API 검증 선행조건
- **Logic_Progress**: [Backlog](./00_BACKLOG.md) - 원자적 실행 티켓
- **QA_Validation**: [QA Checklist](../05_QA_Validation/02_QA_CHECKLIST.md) - 릴리스 조건

