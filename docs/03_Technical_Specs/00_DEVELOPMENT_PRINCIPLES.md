# Development Principles
> Created: 2026-08-11 13:53
> Last Updated: 2026-08-11 15:51

## 1. 기술 방향

- 실행 환경: 로컬 macOS
- 핵심 언어: Python 3
- 미디어 처리: FFmpeg 및 FFprobe
- 외부 서비스: 1차 버전 자동 연동 없음. Suno와 이미지 생성 서비스는 사용자가 직접 사용
- 상태 저장: 프로젝트별 JSON 매니페스트와 파일 시스템
- 사용자 인터페이스: Python 표준 라이브러리 기반 localhost 서버와 단일 HTML 화면

## 2. 아키텍처 원칙

```text
UI
-> Workflow Orchestrator
-> Theme Planner
-> Manual Asset Intake
-> Audio Analyzer / Image Composer / Video Renderer
-> Quality Validator
-> Project Store
```

- 1차 버전은 외부 서비스 어댑터를 만들지 않고 제작 지시서와 입력 폴더를 제공한다.
- 단계마다 입력, 출력과 상태를 매니페스트에 기록한다.
- 완료된 산출물은 재실행 시 재사용한다.
- 입력 음악과 이미지의 내용 해시가 변경되면 하위 완료 단계와 변환 오디오 캐시를 무효화한다.
- 프로그램 시작 시 `running`으로 고착된 프로젝트를 재시도 가능한 `failed` 상태로 복구한다.
- 렌더링 명령과 파일 경로는 배열 인자로 전달해 셸 인젝션을 방지한다.
- 1차 버전은 API 키를 저장하거나 읽지 않는다.

## 3. 오류 처리

- 재시도 가능한 오류: 일시적 네트워크 오류, 속도 제한, 외부 작업 지연
- 사용자 조치 오류: API 키 누락, 결제·한도 부족, 권한 없음
- 복구 불가 입력 오류: 비어 있는 테마, 손상된 중간 파일
- 각 오류에는 서비스, 단계, 재시도 가능 여부와 해결 안내를 기록한다.
- 오류는 `step`, `message`, `retryable`, `action` 구조로 매니페스트에 저장한다.

## 4. 파일 및 이름 규칙

- 프로젝트 식별자는 날짜와 안전한 영문 슬러그로 만든다.
- 생성 곡은 `01_title.ext` 형식을 사용한다.
- 최종 결과 파일명은 제품 명세에 고정된 이름을 사용한다.
- API 응답 원문에는 민감정보가 포함될 수 있으므로 안전한 필드만 로그에 보존한다.

## 5. 성능 원칙

- UI는 제작 시작 요청에 400ms 이내로 상태 변화를 보여준다.
- 장시간 작업은 백그라운드에서 실행하고 진행 상태를 갱신한다.
- 정지 영상에 적합한 H.264 인코딩 설정으로 기존 MOV보다 파일 크기를 줄인다.
- 디스크 여유 공간을 렌더링 전에 확인한다.
- 로컬 서버는 loopback 주소에서만 실행하고 Host, Origin과 `Sec-Fetch-Site`를 검사한다.

## 6. 테스트 원칙

- 순수 계산 로직은 단위 테스트로 검증한다.
- 외부 API는 계약 테스트와 기록된 응답 픽스처로 검증한다.
- FFmpeg 파이프라인은 짧은 미디어 픽스처로 통합 테스트한다.
- 실제 장시간 영상은 릴리스 후보 단계에서 검증한다.

## 7. TODO

- [TODO][High] Suno API 로그인 후 공식 스키마와 과금 확인
- [TODO][Low] 외부 API 도입 시 공식 계약과 인증 저장 방식 확정
- [TODO][Medium] 기존 채널 제목·설명 스타일 분석
- [TODO][Medium] 영상 비트레이트 또는 CRF 기준 비교 테스트

## 8. Related Documents

- **Concept_Design**: [Product Specifications](../01_Concept_Design/03_PRODUCT_SPECS.md) - 기능 및 비기능 요구사항
- **UI_Screens**: [UI Design](../02_UI_Screens/01_UI_DESIGN.md) - UI 상태와 반응성 기준
- **Technical_Specs**: [Data Schema](./01_DB_SCHEMA.md) - 파일 기반 상태 모델
- **Technical_Specs**: [API Specifications](./02_API_SPECS.md) - 외부 서비스 경계
- **Logic_Progress**: [Execution Plan](../04_Logic_Progress/01_EXECUTION_PLAN.md) - 구현 절차
