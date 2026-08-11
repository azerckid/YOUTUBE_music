# Data and Project Schema
> Created: 2026-08-11 13:53
> Last Updated: 2026-08-11 15:58

## 1. 저장 전략

MVP에는 서버 데이터베이스를 사용하지 않는다. 한 명의 로컬 사용자가 프로젝트 폴더를 관리하므로 JSON 매니페스트와 미디어 파일을 사용한다.

## 2. Project Manifest

```json
{
  "schemaVersion": 1,
  "projectId": "20260811-midnight-rain-seoul",
  "theme": "비 오는 서울의 깊은 밤에 잠들며 듣는 재즈",
  "status": "in_progress",
  "currentStep": "music_generation",
  "repeatCount": 3,
  "assetSignature": null,
  "runStartedAt": null,
  "channelProfileId": "default",
  "tracks": [],
  "cover": null,
  "video": null,
  "metadata": null,
  "validation": null,
  "createdAt": "2026-08-11T13:53:00+09:00",
  "updatedAt": "2026-08-11T13:53:00+09:00"
}
```

## 3. Track 필드

| 필드 | 타입 | 설명 |
|:---|:---|:---|
| index | integer | 1부터 시작하는 재생 순서 |
| title | string | 곡 제목 |
| vocalMode | string | 홀수 곡은 `vocal`, 짝수 곡은 `instrumental` |
| prompt | string | Suno 생성 프롬프트 |
| providerJobId | string or null | 외부 생성 작업 식별자 |
| status | string | planned, generating, ready, failed |
| sourcePath | string or null | 다운로드된 음원 경로 |
| durationSeconds | number or null | FFprobe로 측정한 길이 |
| chapterStartSeconds | number or null | 첫 세트의 시작 시간 |
| attempts | integer | 생성 시도 횟수 |

## 4. 단계 상태

```text
pending -> running -> completed
                  -> failed -> running
```

각 단계는 입력 파일 해시, 산출물 경로, 시작·완료 시간과 안전한 오류 요약을 가진다.

`assetSignature`는 입력 음악과 이미지의 파일명 및 실제 내용을 SHA-256으로 계산한다. 내용이 달라지면 파일 수정 시간과 관계없이 하위 단계와 변환 오디오 캐시를 무효화한다.

실패 오류는 다음 구조를 사용한다.

```json
{
  "step": "video_render",
  "message": "저장 공간이 부족합니다.",
  "retryable": true,
  "action": "디스크 공간을 확보한 뒤 실패 단계부터 다시 시도해 주세요."
}
```

`running` 상태에서 프로그램이 종료되면 다음 실행 시 현재 단계만 `failed`로 바꾸고 이전 `completed` 단계는 유지한다.

## 5. 폴더 구조

```text
projects/<project-id>/
├── project.json
├── work/
│   ├── tracks/
│   ├── image/
│   └── audio/
├── logs/
└── output/
```

## 6. 보안

- API 키는 매니페스트에 저장하지 않는다.
- 외부 작업 ID는 저장하되 인증 헤더와 원본 비밀 응답은 저장하지 않는다.
- 출력 경로는 프로젝트 루트 밖으로 벗어나지 않도록 검증한다.

## 7. 확장 조건

다중 사용자, 원격 실행, 작업 검색 또는 클라우드 동기화가 필요해질 때 관계형 데이터베이스 도입을 재검토한다.

## 8. Related Documents

- **Concept_Design**: [Product Specifications](../01_Concept_Design/03_PRODUCT_SPECS.md) - 프로젝트 결과물 정의
- **Technical_Specs**: [Development Principles](./00_DEVELOPMENT_PRINCIPLES.md) - 상태 저장 원칙
- **Technical_Specs**: [API Specifications](./02_API_SPECS.md) - 외부 작업 식별자와 오류 처리
- **Logic_Progress**: [Roadmap](../04_Logic_Progress/00_ROADMAP.md) - 상태 모델 구현 시점
- **QA_Validation**: [Test Scenarios](../05_QA_Validation/01_TEST_SCENARIOS.md) - 복구와 재개 테스트
