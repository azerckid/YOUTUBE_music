# Backlog
> Created: 2026-08-11 13:53
> Last Updated: 2026-08-11 15:51

## ToDo

### [ ] TASK-001: 외부 API 계약과 채널 프로필 확정

- Status: ToDo
- Related Concept Docs:
  - [Collaboration Guide](../01_Concept_Design/00_COLLABORATION_GUIDE.md) - 미확정 사항과 검증 원칙
  - [Product Specifications](../01_Concept_Design/03_PRODUCT_SPECS.md) - 외부 서비스 기능 범위
- Related UI Docs:
  - [Screen Flow](../02_UI_Screens/00_SCREEN_FLOW.md) - 설정 점검과 권한 오류 흐름
- Related HTML Preview:
  - [Main Flow Preview](../02_UI_Screens/previews/01_MAIN_FLOW_PREVIEW.html) - API 준비 상태 표시 기준
- Related Technical Docs:
  - [API Specifications](../03_Technical_Specs/02_API_SPECS.md) - 확인해야 할 Suno와 OpenAI 계약
- Related QA Docs:
  - [QA Checklist](../05_QA_Validation/02_QA_CHECKLIST.md) - 구현 전 Gate
- Implementation Preconditions:
  - [ ] 관련 문서 전체 확인 완료
  - [ ] HTML UI Preview 사용자 확인 및 피드백 기록 완료
  - [ ] 화면/UI 선확인과 사용자 진입·전환·이탈 동선 확인 완료
  - [ ] 화면별 입력·출력 데이터와 상태 변화 확인 완료
  - [ ] 로딩·빈 상태·오류 상태 확인 완료
  - [ ] 데이터 소스, 최소 필드, mutation과 상태 관리 방식 확인 완료
  - [ ] 구현 범위와 문서 요구사항 충돌 없음
  - [ ] Suno Platform 로그인 가능
  - [ ] OpenAI API 계정 확인 가능
  - [ ] 기존 YouTube 채널 확인 가능
- Acceptance Criteria:
  - [ ] Suno 엔드포인트, 인증, 과금, 한도와 다운로드 계약이 공식 근거와 함께 기록됨
  - [ ] OpenAI API 키와 결제 준비 상태가 확인됨
  - [ ] 기존 채널명, 제목·설명 문체와 고정 해시태그가 채널 프로필에 기록됨
  - [ ] 확인되지 않은 비공식 API를 사용하지 않음
- Document Sync Check:
  - [ ] 확인 결과를 API 명세와 제품 명세에 반영
  - [ ] 구현 후 문서와 실제 계약의 불일치 없음

### [ ] TASK-002: 프로젝트 상태와 로컬 미디어 엔진 구현

- Status: ToDo
- Related Concept Docs:
  - [Product Specifications](../01_Concept_Design/03_PRODUCT_SPECS.md) - 곡 분석, 3회 반복과 MP4 요구사항
- Related UI Docs:
  - [UI Design](../02_UI_Screens/01_UI_DESIGN.md) - 진행·오류·완료 상태 표시
- Related HTML Preview:
  - [Main Flow Preview](../02_UI_Screens/previews/01_MAIN_FLOW_PREVIEW.html) - 제작 진행 상태 기준
- Related Technical Docs:
  - [Development Principles](../03_Technical_Specs/00_DEVELOPMENT_PRINCIPLES.md) - FFmpeg, 보안과 재개 원칙
  - [Data Schema](../03_Technical_Specs/01_DB_SCHEMA.md) - 프로젝트 매니페스트 구조
- Related QA Docs:
  - [Test Scenarios](../05_QA_Validation/01_TEST_SCENARIOS.md) - 곡 순서, 반복, 챕터와 재개 테스트
- Implementation Preconditions:
  - [ ] 관련 문서 전체 확인 완료
  - [ ] 화면/UI 선확인 완료
  - [ ] HTML UI Preview 사용자 확인 및 피드백 기록 완료
  - [ ] 사용자 진입·전환·이탈 동선 확인 완료
  - [ ] 화면별 입력·출력 데이터와 상태 변화 확인 완료
  - [ ] 로딩·빈 상태·오류 상태 확인 완료
  - [ ] 데이터 소스, 최소 필드, mutation과 상태 관리 방식 확인 완료
  - [ ] 구현 범위와 문서 요구사항 충돌 없음
  - [ ] 프로젝트 상태와 파일 경계 확인 완료
  - [ ] FFmpeg와 FFprobe 실행 가능 확인
  - [ ] 테스트용 짧은 음원과 이미지 준비
- Acceptance Criteria:
  - [ ] 곡 길이와 첫 세트 챕터 시간이 정확히 계산됨
  - [ ] 전체 음악 세트가 순서대로 3회 반복됨
  - [ ] 1920×1080, 24fps, H.264, AAC MP4가 생성됨
  - [ ] 중단 후 완료 산출물을 유지하고 실패 단계부터 재개됨
  - [ ] 파일 경로와 명령 인자가 안전하게 처리됨
- Document Sync Check:
  - [ ] 구현 후 데이터 스키마와 실제 매니페스트 일치
  - [ ] FFmpeg 설정 변경 시 제품 명세와 QA 문서 갱신

### [ ] TASK-003: OpenAI 텍스트·이미지 생성 연결

- Status: ToDo
- Related Concept Docs:
  - [Vision & Core](../01_Concept_Design/01_VISION_CORE.md) - 테마 단일 입력과 채널 일관성
  - [Product Specifications](../01_Concept_Design/03_PRODUCT_SPECS.md) - 테마 분석, 이미지와 업로드 문구 요구사항
- Related UI Docs:
  - [Screen Flow](../02_UI_Screens/00_SCREEN_FLOW.md) - 이미지 생성 진행과 오류 상태
- Related HTML Preview:
  - [Main Flow Preview](../02_UI_Screens/previews/01_MAIN_FLOW_PREVIEW.html) - 생성 단계 진행 표시
- Related Technical Docs:
  - [API Specifications](../03_Technical_Specs/02_API_SPECS.md) - OpenAI 모델, 과금과 오류 계약
- Related QA Docs:
  - [QA Checklist](../05_QA_Validation/02_QA_CHECKLIST.md) - 대표 이미지, 보안과 비용 검사
- Implementation Preconditions:
  - [ ] 관련 문서 전체 확인 완료
  - [ ] HTML UI Preview 사용자 확인 및 피드백 기록 완료
  - [ ] 화면/UI 선확인과 사용자 진입·전환·이탈 동선 확인 완료
  - [ ] 화면별 입력·출력 데이터와 상태 변화 확인 완료
  - [ ] 로딩·빈 상태·오류 상태 확인 완료
  - [ ] 데이터 소스, 최소 필드, mutation과 상태 관리 방식 확인 완료
  - [ ] 구현 범위와 문서 요구사항 충돌 없음
  - [ ] OpenAI API 키와 결제 설정 확인
  - [ ] 구조화 출력 스키마 확인
  - [ ] Cover에 적용할 글꼴과 채널 스타일 확인
- Acceptance Criteria:
  - [ ] 테마에서 곡 계획과 곡별 Suno 프롬프트가 생성됨
  - [ ] 16:9 대표 이미지가 생성되고 안전하게 저장됨
  - [ ] 제목과 보조 문구가 `Cover.jpg`에 정확히 합성됨
  - [ ] 제목, 설명, 챕터 삽입 영역과 해시태그가 생성됨
  - [ ] 별도 썸네일 파일이 생성되지 않음
  - [ ] OpenAI API 키가 로그와 결과물에 노출되지 않음
- Document Sync Check:
  - [ ] 모델 또는 엔드포인트 변경 시 API 명세 갱신
  - [ ] 생성 출력 형식 변경 시 제품 명세와 QA 문서 갱신

### [ ] TASK-004: 공식 Suno API 음악 생성 연결

- Status: ToDo
- Related Concept Docs:
  - [Collaboration Guide](../01_Concept_Design/00_COLLABORATION_GUIDE.md) - 공식 기능 검증 원칙
  - [Product Specifications](../01_Concept_Design/03_PRODUCT_SPECS.md) - 음악 생성과 다운로드 요구사항
- Related UI Docs:
  - [UI Design](../02_UI_Screens/01_UI_DESIGN.md) - 외부 작업 대기와 오류 상태
- Related HTML Preview:
  - [Main Flow Preview](../02_UI_Screens/previews/01_MAIN_FLOW_PREVIEW.html) - Suno 생성 진행 표시
- Related Technical Docs:
  - [API Specifications](../03_Technical_Specs/02_API_SPECS.md) - 검증 후 구현할 공식 계약
  - [Data Schema](../03_Technical_Specs/01_DB_SCHEMA.md) - 곡 작업 상태와 재시도 기록
- Related QA Docs:
  - [Test Scenarios](../05_QA_Validation/01_TEST_SCENARIOS.md) - API 실패, 결제·권한과 재개 시나리오
- Implementation Preconditions:
  - [ ] TASK-001에서 Suno 공식 계약 확인 완료
  - [ ] 관련 문서 전체 확인 완료
  - [ ] HTML UI Preview 사용자 확인 및 피드백 기록 완료
  - [ ] 화면/UI 선확인과 사용자 진입·전환·이탈 동선 확인 완료
  - [ ] 화면별 입력·출력 데이터와 상태 변화 확인 완료
  - [ ] 로딩·빈 상태·오류 상태 확인 완료
  - [ ] 데이터 소스, 최소 필드, mutation과 상태 관리 방식 확인 완료
  - [ ] 구현 범위와 문서 요구사항 충돌 없음
  - [ ] 비용 상한과 최대 재시도 횟수 확정
  - [ ] 다운로드 파일의 상업적 이용 조건 확인
- Acceptance Criteria:
  - [ ] 곡별 프롬프트로 공식 Suno API 생성 작업을 시작함
  - [ ] 작업 상태를 안전하게 조회하거나 통지받음
  - [ ] 완성 음원을 곡 순서대로 다운로드하고 저장함
  - [ ] 일시적 실패는 제한된 횟수로 재시도함
  - [ ] 결제·권한 오류는 추가 요청 없이 중단함
  - [ ] 비공식 API 또는 취약한 웹 자동화를 사용하지 않음
- Document Sync Check:
  - [ ] 실제 Suno 계약이 API 명세와 일치
  - [ ] API 변경 감지 시 백로그와 테스트 픽스처 갱신

### [ ] TASK-005: 전체 워크플로 UI 통합 및 릴리스 검증

- Status: ToDo
- Related Concept Docs:
  - [Vision & Core](../01_Concept_Design/01_VISION_CORE.md) - 테마에서 업로드 직전까지의 성공 기준
  - [Product Specifications](../01_Concept_Design/03_PRODUCT_SPECS.md) - 12단계 전체 범위
- Related UI Docs:
  - [Screen Flow](../02_UI_Screens/00_SCREEN_FLOW.md) - 전체 사용자 여정
  - [Prototype Review](../02_UI_Screens/02_PROTOTYPE_REVIEW.md) - 사용자 승인과 피드백
- Related HTML Preview:
  - [Main Flow Preview](../02_UI_Screens/previews/01_MAIN_FLOW_PREVIEW.html) - 구현 기준 화면
- Related Technical Docs:
  - [Development Principles](../03_Technical_Specs/00_DEVELOPMENT_PRINCIPLES.md) - 오케스트레이션과 진행 상태 원칙
  - [API Specifications](../03_Technical_Specs/02_API_SPECS.md) - 외부 생성 서비스 계약
- Related QA Docs:
  - [Test Scenarios](../05_QA_Validation/01_TEST_SCENARIOS.md) - 전체 흐름 및 오류 테스트
  - [QA Checklist](../05_QA_Validation/02_QA_CHECKLIST.md) - 릴리스 Gate
- Implementation Preconditions:
  - [ ] TASK-002, TASK-003, TASK-004 완료
  - [ ] 관련 문서 전체 확인 완료
  - [ ] HTML UI Preview 사용자 승인 완료
  - [ ] HTML UI Preview 사용자 피드백 기록 완료
  - [ ] 화면/UI 선확인과 사용자 진입·전환·이탈 동선 확인 완료
  - [ ] 화면별 입력·출력 데이터와 상태 변화 확인 완료
  - [ ] 로딩·빈 상태·오류 상태 확인 완료
  - [ ] 데이터 소스, 최소 필드, mutation과 상태 관리 방식 확인 완료
  - [ ] 구현 범위와 문서 요구사항 충돌 없음
- Acceptance Criteria:
  - [ ] 테마 한 문장으로 전체 제작이 시작됨
  - [ ] 진행·대기·오류·완료 상태가 정확히 표시됨
  - [ ] 실패 단계부터 재시도할 수 있음
  - [ ] 지정된 결과 파일과 `Generated_Tracks`가 생성됨
  - [ ] 자동검사 결과가 UI와 로그에 표시됨
  - [ ] 실제 장시간 영상이 YouTube Studio에 수동 업로드됨
- Document Sync Check:
  - [ ] 구현 후 화면과 HTML Preview의 의도하지 않은 불일치 없음
  - [ ] 코드, 제품 명세, API 명세와 QA 결과 동기화 완료

## In Progress

현재 진행 중인 구현 작업 없음. 실제 장시간 미디어 검증과 채널 프로필 확인이 남아 있다.

## Done

- [x] 합의된 자동화 12단계를 제품 문서로 정리함

### [x] TASK-006: API 없는 로컬 제작 MVP 구현

- Status: Done
- Related Concept Docs:
  - [Product Specifications](../01_Concept_Design/03_PRODUCT_SPECS.md) - 1차 버전 수동 경계와 결과물
- Related UI Docs:
  - [Screen Flow](../02_UI_Screens/00_SCREEN_FLOW.md) - 세로형 제작 흐름과 파일 대기 상태
  - [Prototype Review](../02_UI_Screens/02_PROTOTYPE_REVIEW.md) - 사용자 확인과 구현 지시
- Related HTML Preview:
  - [Main Flow Preview](../02_UI_Screens/previews/01_MAIN_FLOW_PREVIEW.html) - 단일 화면 진행 구조
- Related Technical Docs:
  - [Development Principles](../03_Technical_Specs/00_DEVELOPMENT_PRINCIPLES.md) - Python, FFmpeg와 파일 상태 원칙
  - [API Specifications](../03_Technical_Specs/02_API_SPECS.md) - 로컬 HTTP 경계와 외부 API 보류
- Related QA Docs:
  - [API-Free MVP Test Report](../05_QA_Validation/04_API_FREE_MVP_TEST_REPORT.md) - 단위 및 짧은 미디어 통합검사
- Implementation Preconditions:
  - [x] 관련 문서 전체 확인 완료
  - [x] HTML UI Preview 사용자 확인 및 피드백 기록 완료
  - [x] 세로형 화면과 사용자 동선 확인 완료
  - [x] 파일 대기, 진행, 오류와 완료 상태 확인 완료
  - [x] JSON 매니페스트와 로컬 파일 데이터 소스 확인 완료
  - [x] API 없는 1차 범위에 대한 사용자 구현 지시 확인 완료
- Acceptance Criteria:
  - [x] 테마로 Suno와 이미지 제작 지시서가 생성됨
  - [x] 음악 파일을 이름순으로 분석하고 첫 세트 챕터를 계산함
  - [x] 전체 음악 세트가 세 번 반복됨
  - [x] 1920x1080, 24fps, H.264, AAC MP4가 생성됨
  - [x] Cover와 업로드 텍스트 파일이 결과 폴더에 생성됨
  - [x] 짧은 미디어 통합검사와 로컬 서버 기동검사를 통과함
- Document Sync Check:
  - [x] 제품, UI, 기술과 실행 문서에 API 없는 1차 범위를 반영함
  - [x] 구현과 로컬 매니페스트 및 출력 파일명이 일치함

### [x] TASK-007: 상태 복구와 로컬 보안 안정화

- Status: Done
- Related Concept Docs:
  - [Product Specifications](../01_Concept_Design/03_PRODUCT_SPECS.md) - FR-10 실패 단계 재시작 요구사항
- Related UI Docs:
  - [Screen Flow](../02_UI_Screens/00_SCREEN_FLOW.md) - 파일 대기와 실패 복구 흐름
  - [UI Design](../02_UI_Screens/01_UI_DESIGN.md) - 오류 원인과 사용자 조치 표시
- Related HTML Preview:
  - [Main Flow Preview](../02_UI_Screens/previews/01_MAIN_FLOW_PREVIEW.html) - 진행 상태 정보 위계
- Related Technical Docs:
  - [Development Principles](../03_Technical_Specs/00_DEVELOPMENT_PRINCIPLES.md) - 재개, 디스크와 로컬 보안 원칙
  - [Data Schema](../03_Technical_Specs/01_DB_SCHEMA.md) - 상태 및 구조화 오류
  - [API Specifications](../03_Technical_Specs/02_API_SPECS.md) - 실행 상태와 요청 가드
- Related QA Docs:
  - [Test Scenarios](../05_QA_Validation/01_TEST_SCENARIOS.md) - 중복, 복구, 재개와 보안 시나리오
  - [API-Free MVP Test Report](../05_QA_Validation/04_API_FREE_MVP_TEST_REPORT.md) - 16개 자동검사 결과
- Implementation Preconditions:
  - [x] 사용자 코드 리뷰와 수정 승인 확인 완료
  - [x] 관련 제품, UI, 기술과 QA 문서 확인 완료
  - [x] HTML UI Preview 사용자 확인과 피드백 기록 완료
  - [x] 화면/UI 선확인과 사용자 진입·전환·이탈 동선 확인 완료
  - [x] 파일 대기, 실행, 실패와 완료 상태 확인 완료
  - [x] 로딩·빈 상태·오류 상태 확인 완료
  - [x] JSON 매니페스트 상태 전이와 로컬 HTTP mutation 확인 완료
  - [x] 화면별 입력·출력 데이터와 최소 필드 확인 완료
  - [x] 기존 산출물 보존과 재실행 범위 확인 완료
- Acceptance Criteria:
  - [x] 실행 응답 전에 상태가 `running`으로 저장됨
  - [x] 중복 실행과 완료 프로젝트 재실행이 차단됨
  - [x] 비정상 종료 후 현재 단계만 `failed`로 복구됨
  - [x] 재시도에서 완료된 영상과 중간 산출물을 재사용함
  - [x] 외부 Host와 Origin 요청이 거부됨
  - [x] 저장 공간과 글꼴 오류가 사용자 조치와 함께 기록됨
  - [x] 경로, 상태, 복구, 재개와 보안 테스트가 통과함
- Document Sync Check:
  - [x] 상태 머신, 로컬 HTTP와 오류 스키마 문서 갱신
  - [x] 화면 실패 상태와 실제 구조화 오류 표시 일치

## 4. Related Documents

- **Concept_Design**: [Product Specifications](../01_Concept_Design/03_PRODUCT_SPECS.md) - 백로그의 제품 근거
- **UI_Screens**: [Prototype Review](../02_UI_Screens/02_PROTOTYPE_REVIEW.md) - UI Gate 상태
- **Technical_Specs**: [Development Principles](../03_Technical_Specs/00_DEVELOPMENT_PRINCIPLES.md) - 구현 원칙
- **Logic_Progress**: [Roadmap](./00_ROADMAP.md) - 단계별 진행 계획
- **Logic_Progress**: [Execution Plan](./01_EXECUTION_PLAN.md) - 원자적 실행 목록
- **QA_Validation**: [QA Checklist](../05_QA_Validation/02_QA_CHECKLIST.md) - 완료 조건
