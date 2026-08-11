# QA Checklist
> Created: 2026-08-11 13:53
> Last Updated: 2026-08-11 15:58

## 1. Global Rubric Scorecard

| Criterion | Status (Pass/Fail) | Evidence |
|:---|:---:|:---|
| Functionality | Pending | 전체 흐름 및 코드 품질 검증 예정 |
| Potential Impact | Pending | 제작 시간 절감 측정 예정 |
| Novelty | Pending | 전체 자동화 차별성 검증 예정 |
| UX | Pending | 반응성·오류 복구 검증 예정 |
| Open-source | Pending | 어댑터 모듈성 검증 예정 |
| Business Plan | Pending | 영상별 API 비용 검증 예정 |

## 2. 구현 전 Gate

- [x] HTML UI Preview를 사용자가 확인했다.
- [x] 사용자 피드백이 Prototype Review에 기록됐다.
- [x] 1차 버전은 외부 API를 사용하지 않는 것으로 확정됐다.
- [ ] 기존 채널 프로필이 확인됐다.

## 3. 기능 검사

- [x] 테마 입력만으로 프로젝트가 생성된다.
- [x] 곡 계획과 Suno 프롬프트가 생성된다.
- [x] 1·3·5·7번은 가사·보컬곡, 2·4·6·8번은 연주곡으로 안내된다.
- [x] 사용자가 준비한 곡을 이름순으로 불러온다.
- [x] 대표 이미지와 제목 합성이 정상이다.
- [x] 음악 세트가 정확히 3회 반복된다.
- [x] 짧은 검사에서 MP4와 업로드 텍스트 파일이 생성된다.
- [x] 별도 썸네일이 생성되지 않는다.

## 4. 미디어 검사

- [x] 영상은 1920×1080이다.
- [x] 영상은 24fps H.264이다.
- [x] 오디오는 AAC 스테레오이다.
- [x] 영상과 오디오 길이가 일치한다.
- [ ] 긴 무음이나 손상된 구간이 없다.
- [ ] 첫 세트의 챕터 시간이 정확하다.
- [ ] 파일 크기가 정지 영상 용도에 합리적이다.

## 5. 안전과 비용 검사

- [x] 1차 버전은 API 키를 읽거나 저장하지 않는다.
- [x] 1차 버전은 비용이 발생하는 외부 요청을 보내지 않는다.
- [x] 경로 이탈과 셸 인젝션을 방지한다.
- [x] 외부 Host, Origin과 cross-site 상태 변경 요청을 거부한다.
- [x] 렌더링 전에 디스크 여유 공간을 검사한다.
- [x] 글꼴 누락 오류에 해결 방법을 표시한다.

## 6. 운영 검사

- [x] 중단 후 실패 단계부터 재개할 수 있다.
- [x] 중복 실행과 완료 프로젝트 재실행을 차단한다.
- [x] 비정상 종료 후 `running` 상태를 복구한다.
- [x] 완료된 음악과 이미지를 불필요하게 다시 생성하지 않는다.
- [x] 결과 폴더를 Finder에서 열 수 있다.
- [ ] YouTube Studio에 수동 업로드할 수 있다.
- [ ] 제목, 설명, 챕터와 Cover를 그대로 사용할 수 있다.

## 7. Related Documents

- **Concept_Design**: [Vision & Core](../01_Concept_Design/01_VISION_CORE.md) - 성공 기준
- **Concept_Design**: [Product Specifications](../01_Concept_Design/03_PRODUCT_SPECS.md) - 기능 요구사항
- **UI_Screens**: [UI Design](../02_UI_Screens/01_UI_DESIGN.md) - UX 검증 기준
- **Technical_Specs**: [Development Principles](../03_Technical_Specs/00_DEVELOPMENT_PRINCIPLES.md) - 보안과 품질 원칙
- **Logic_Progress**: [Backlog](../04_Logic_Progress/00_BACKLOG.md) - 구현 완료 상태
- **QA_Validation**: [Test Scenarios](./01_TEST_SCENARIOS.md) - 상세 테스트 시나리오
