# Data and Project Schema
> Created: 2026-08-11 13:53
> Last Updated: 2026-08-15

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
  "mood": {},
  "thumbnail": "projects/<project-id>/work/image/Thumbnail.jpg",
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

## 3. Mood 필드

프로젝트 생성 시 등록된 썸네일을 Pillow로 분석한 결과이며 이후 단계에서 갱신하지 않는다.

| 필드 | 타입 | 설명 |
|:---|:---|:---|
| brightness | number | 평균 휘도 0.0~1.0 |
| saturation | number | 평균 절대 채도(RGB max−min) 0.0~1.0 |
| contrast | number | 휘도 표준편차를 64로 정규화한 값 0.0~1.0 |
| warmth | number | 채도 가중 색상 히스토그램의 난색 비율 0.0~1.0 |
| palette | string[] | 대표 색상 5개의 16진수 표기 |
| tags | string[] | 밝기·채도·대비·색온도 순서의 한글 분위기 태그 4개 |
| summary | string | `tags`를 ` · `로 이은 요약 |
| visualPhrase | string | 화면 인상을 설명하는 영문 구절 |
| musicPhrase | string | Suno 프롬프트에 삽입하는 영문 음악 지시문 |
| width, height | integer | 원본 썸네일 크기 |

HSV 채도는 어두운 색에서도 높게 나오므로 절대 채도를 사용한다. 깊은 남색 야경이 선명한 색감으로 잘못 분류되는 것을 막기 위한 선택이다.

## 4. Track 필드

| 필드 | 타입 | 설명 |
|:---|:---|:---|
| index | integer | 1부터 시작하는 재생 순서 |
| title | string | 곡 제목 |
| vocalMode | string | 홀수 곡은 `vocal`, 짝수 곡은 `instrumental`; 음악 분석 후에도 보존 |
| prompt | string | Suno 생성 프롬프트 |
| providerJobId | string or null | 외부 생성 작업 식별자 |
| status | string | planned, generating, ready, failed |
| sourcePath | string or null | 다운로드된 음원 경로 |
| durationSeconds | number or null | FFprobe로 측정한 길이 |
| chapterStartSeconds | number or null | 첫 세트의 시작 시간 |
| attempts | integer | 생성 시도 횟수 |

## 5. 단계 상태

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

## 6. 폴더 구조

```text
projects/<project-id>/
├── project.json
├── Suno_Prompts.txt
├── Cover_Mood.txt
├── README_FIRST.txt
├── work/
│   ├── tracks/
│   ├── image/
│   │   └── Thumbnail.jpg
│   └── audio/
├── logs/
└── output/
```

썸네일은 프로젝트 생성 요청에서 받은 원본 바이트를 그대로 저장하고, 확장자는 디코딩으로 확인한 실제 형식에서 결정한다.

## 7. 보안

- API 키는 매니페스트에 저장하지 않는다.
- 외부 작업 ID는 저장하되 인증 헤더와 원본 비밀 응답은 저장하지 않는다.
- 출력 경로는 프로젝트 루트 밖으로 벗어나지 않도록 검증한다.
- 업로드된 썸네일은 파일명을 신뢰하지 않고 디코딩 결과로 형식을 판별해 고정된 이름으로 저장한다.

## 8. 확장 조건

다중 사용자, 원격 실행, 작업 검색 또는 클라우드 동기화가 필요해질 때 관계형 데이터베이스 도입을 재검토한다.

## 9. Related Documents

- **Concept_Design**: [Product Specifications](../01_Concept_Design/03_PRODUCT_SPECS.md) - 프로젝트 결과물 정의
- **Technical_Specs**: [Development Principles](./00_DEVELOPMENT_PRINCIPLES.md) - 상태 저장 원칙
- **Technical_Specs**: [API Specifications](./02_API_SPECS.md) - 외부 작업 식별자와 오류 처리
- **Logic_Progress**: [Roadmap](../04_Logic_Progress/00_ROADMAP.md) - 상태 모델 구현 시점
- **QA_Validation**: [Test Scenarios](../05_QA_Validation/01_TEST_SCENARIOS.md) - 복구와 재개 테스트
