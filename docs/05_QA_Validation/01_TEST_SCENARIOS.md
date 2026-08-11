# Test Scenarios
> Created: 2026-08-11 13:53
> Last Updated: 2026-08-11 15:51

## 1. Rubric Validation

| Criterion | Status | Evidence required |
|:---|:---:|:---|
| Functionality | Pending | 테마부터 결과 폴더까지 전체 테스트 통과 |
| Potential Impact | Pending | 수작업 시간과 개입 횟수 비교 |
| Novelty | Pending | 테마 기반 전체 파이프라인 검증 |
| UX | Pending | 400ms 이내 상태 피드백과 오류 복구 확인 |
| Open-source | Pending | 외부 서비스 어댑터 교체 가능성 확인 |
| Business Plan | Pending | 영상별 API 비용 기록 확인 |

## 2. 핵심 시나리오

### TS-01 정상 제작

- Given: 사용자가 준비한 음악과 대표 이미지, FFmpeg와 충분한 저장 공간
- When: 사용자가 테마를 입력하고 제작을 시작한다.
- Then: MP4, Cover와 업로드 텍스트 파일이 생성되고 자동검사를 통과한다.

### TS-02 곡 순서와 반복

- Given: 순서가 정해진 여러 곡
- When: 오디오 조립을 실행한다.
- Then: 모든 곡이 순서대로 재생되고 전체 세트가 정확히 3회 반복된다.

### TS-03 챕터 정확도

- Given: FFprobe로 확인한 곡 길이
- When: 챕터를 생성한다.
- Then: 첫 곡은 `00:00`이며 이후 시간이 누적 길이와 일치한다.

### TS-04 Suno API 실패

- Given: 일시적 서버 오류 또는 속도 제한
- When: 음악 생성이 실패한다.
- Then: 제한된 재시도를 수행하고 완료 단계는 보존한다.

### TS-05 결제 또는 권한 오류

- Given: API 한도 부족 또는 잘못된 키
- When: 외부 생성 요청을 보낸다.
- Then: 추가 비용을 발생시키는 반복 요청 없이 중단하고 해결 안내를 표시한다.

### TS-06 렌더링 재개

- Given: 음악과 대표 이미지는 완료됐으나 렌더링이 중단됐다.
- When: 프로젝트를 다시 실행한다.
- Then: 음악과 이미지를 다시 생성하지 않고 렌더링부터 재개한다.

### TS-07 결과 규격

- Given: 완성된 영상
- When: FFprobe 검사를 실행한다.
- Then: 1920×1080, 24fps, H.264, AAC 스테레오이며 영상과 오디오 길이가 일치한다.

### TS-08 Cover 재사용

- Given: 완성된 `Cover.jpg`
- When: 결과 폴더를 검사한다.
- Then: 별도 썸네일 파일이 없고 동일한 Cover를 영상 화면과 썸네일로 사용할 수 있다.

### TS-09 API 없는 파일 대기

- Given: 테마 입력은 완료됐지만 음악 또는 이미지가 준비되지 않았다.
- When: 사용자가 영상 만들기를 계속한다.
- Then: 비용이 발생하는 외부 요청 없이 누락된 폴더와 파일을 안내한다.

### TS-10 중복 실행 차단

- Given: 프로젝트가 이미 `running` 또는 `completed` 상태다.
- When: 사용자가 제작 계속 요청을 다시 보낸다.
- Then: 새 작업을 시작하지 않고 충돌 오류를 반환한다.

### TS-11 비정상 종료 복구

- Given: 이전 실행이 `running` 상태에서 종료됐다.
- When: 프로그램을 다시 실행한다.
- Then: 현재 단계를 `failed`로 복구하고 이전 완료 단계는 유지한다.

### TS-12 실패 단계 재개

- Given: 영상은 완료됐지만 메타데이터 단계가 실패했다.
- When: 사용자가 다시 시도한다.
- Then: 기존 영상을 다시 렌더링하지 않고 메타데이터부터 완료한다.

### TS-13 로컬 요청 보안

- Given: 외부 Host 또는 Origin에서 상태 변경을 요청한다.
- When: 로컬 서버가 요청을 검사한다.
- Then: 요청을 거부하고 렌더링이나 Finder 열기를 실행하지 않는다.

### TS-14 교체된 음악 캐시 무효화

- Given: 실패 후 원본보다 오래된 수정 시간을 가진 다른 음악 파일로 교체했다.
- When: 사용자가 실패 단계부터 다시 시도한다.
- Then: 기존 변환 오디오를 재사용하지 않고 교체된 음악으로 다시 생성한다.

## 3. 윤리 및 독창성 검사

- 특정 실존 인물이나 작가의 스타일을 복제하도록 요구하지 않는다.
- 생성 프롬프트와 서비스 이용 조건을 프로젝트 기록에 남긴다.
- 상업적 이용 권한이 확인된 계정과 생성물만 업로드한다.
- 기존 참고 영상은 규격과 운영 흐름의 기준으로만 사용한다.

## 4. Related Documents

- **Concept_Design**: [Product Specifications](../01_Concept_Design/03_PRODUCT_SPECS.md) - 테스트 대상 기능
- **UI_Screens**: [Prototype Review](../02_UI_Screens/02_PROTOTYPE_REVIEW.md) - 사용자 화면 검토 상태
- **Technical_Specs**: [Data Schema](../03_Technical_Specs/01_DB_SCHEMA.md) - 재개 상태 검증
- **Technical_Specs**: [API Specifications](../03_Technical_Specs/02_API_SPECS.md) - API 오류 기준
- **Logic_Progress**: [Execution Plan](../04_Logic_Progress/01_EXECUTION_PLAN.md) - 구현 및 검증 순서
- **QA_Validation**: [QA Checklist](./02_QA_CHECKLIST.md) - 릴리스 기준
