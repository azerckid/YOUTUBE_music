# External API Specifications
> Created: 2026-08-11 13:53
> Last Updated: 2026-08-11 15:09

## 1. 원칙

외부 API의 공식 문서로 확인된 기능만 구현 계약으로 확정한다. 인증 후에만 볼 수 있는 Suno 상세 스키마는 검증 전까지 논리 인터페이스로만 정의한다.

1차 버전은 유료 외부 API를 호출하지 않는다. 아래 Suno 및 이미지 API 계약은 추후 완전 자동화 단계까지 보류한다.

## 2. 로컬 HTTP 경계

- 바인딩: `127.0.0.1`
- `GET /api/health`: FFmpeg와 FFprobe 준비 상태
- `GET /api/latest`: 마지막 로컬 프로젝트 상태
- `POST /api/projects`: 테마로 프로젝트와 수동 제작 지시서 생성
- `GET /api/projects/{projectId}`: 진행 상태 조회
- `POST /api/projects/{projectId}/continue`: 준비된 음악과 이미지로 영상 제작 시작
- `POST /api/projects/{projectId}/open`: Finder에서 허용된 프로젝트 하위 폴더 열기

이는 로컬 프로그램 내부 통신이며 외부 서비스 과금 API가 아니다.

- `continue`는 `waiting_for_files` 또는 `failed` 상태에서만 허용한다.
- 실행 응답 전에 매니페스트 상태를 `running`으로 저장하여 중복 요청을 차단한다.
- 완료된 프로젝트의 재실행은 거부하고 새 프로젝트 생성을 안내한다.

## 3. Suno Adapter

### 확인된 기능

- 공식 Suno Platform은 단일 프롬프트로 음악을 생성하는 REST API를 제공한다.
- 기존 Suno 계정과 연결된 Google 계정으로 API 계정을 관리한다.

### 논리 인터페이스

```text
create_track(prompt, title) -> provider_job_id
get_track_status(provider_job_id) -> pending | completed | failed
download_track(provider_job_id, destination) -> local_path
```

### 구현 전 확인 항목

- 실제 엔드포인트와 인증 헤더
- 생성 결과 개수와 선택 방식
- 폴링 또는 웹훅 지원 여부
- 오디오 다운로드 URL과 만료 시간
- 속도 제한, 동시 작업 수와 재시도 헤더
- 기존 웹 월정액과 API 과금의 관계
- 상업적 이용 조건의 API 생성물 적용 범위

확인 전에는 비공식 Suno API나 웹 화면 자동화를 기본 경로로 사용하지 않는다.

## 4. 이미지 및 텍스트 생성 Adapter

### 이미지 생성

- 권장 모델: `gpt-image-2`
- 공식 이미지 생성 엔드포인트 사용
- 입력: 테마 기반 프롬프트, 16:9에 가까운 가로 형식, 품질 설정
- 출력: 생성 이미지 데이터 또는 파일

### 텍스트 생성

- 용도: 테마 분석, 곡 계획, 곡 제목, Suno 프롬프트, 영상 제목·설명·해시태그
- 출력은 JSON 스키마로 검증 가능한 구조를 사용한다.

### 과금

OpenAI API는 ChatGPT 구독과 별도로 관리되고 사용량 기준으로 과금된다.

## 5. 공통 오류 계약

| 오류 | 처리 |
|:---|:---|
| 인증 실패 | 즉시 중단하고 설정 안내 |
| 결제 또는 한도 부족 | 즉시 중단하고 계정 확인 안내 |
| 속도 제한 | 서버 재시도 지시를 존중해 지연 재시도 |
| 일시적 서버 오류 | 제한된 횟수로 지수 백오프 재시도 |
| 작업 시간 초과 | 작업 ID를 보존하고 이후 상태 조회 |
| 유효하지 않은 결과 | 해당 곡 또는 이미지만 다시 생성 |

## 6. 보안

- `SUNO_API_KEY`, `OPENAI_API_KEY`는 환경변수로 관리한다.
- UI와 로그에 전체 키를 표시하지 않는다.
- 로컬 서버는 `127.0.0.1` 또는 `localhost`에만 바인딩한다.
- 모든 요청의 Host를 검사하고 상태 변경 요청의 Origin과 `Sec-Fetch-Site`를 검사한다.
- API 요청 프롬프트와 비용 정보는 저장할 수 있으나 인증정보는 저장하지 않는다.

## 7. 비용 보호

- 실행 전 예상 곡 수와 이미지 수를 표시한다.
- 프로젝트별 API 요청 횟수를 기록한다.
- 무한 재시도를 금지하고 단계별 최대 시도 횟수를 둔다.
- 비용 한도 초과 가능성이 있으면 새 요청 전에 중단한다.

## 8. Related Documents

- **Concept_Design**: [Product Specifications](../01_Concept_Design/03_PRODUCT_SPECS.md) - 외부 생성 기능 요구사항
- **Technical_Specs**: [Development Principles](./00_DEVELOPMENT_PRINCIPLES.md) - 어댑터 및 오류 처리 원칙
- **Technical_Specs**: [Data Schema](./01_DB_SCHEMA.md) - 외부 작업 상태 저장
- **Logic_Progress**: [Backlog](../04_Logic_Progress/00_BACKLOG.md) - API 검증 및 구현 작업
- **QA_Validation**: [Test Scenarios](../05_QA_Validation/01_TEST_SCENARIOS.md) - API 실패 시나리오
