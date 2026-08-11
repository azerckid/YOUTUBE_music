# Vision and Core Values
> Created: 2026-08-11 13:53
> Last Updated: 2026-08-11 13:53

## 1. 문제

장시간 YouTube 재즈 영상 한 편을 만들려면 테마 기획, 음악 생성과 다운로드, 이미지 생성, 음악 연결, 반복 편집, 영상 렌더링, 챕터 계산, 제목과 설명 작성이 반복된다. 현재 방식은 사람의 시간이 많이 들고 누락과 계산 오류가 발생하기 쉽다.

## 2. 비전

사용자가 테마 한 문장을 입력하면 자동화 프로그램이 음악, 이미지, 장시간 영상, 업로드 문구를 생성하고 사용자는 완성본 확인과 YouTube 업로드만 수행한다.

```text
테마 입력 -> 자동 제작 -> 결과 확인 -> YouTube 직접 업로드
```

## 3. 핵심 사용자

- 기존 YouTube 재즈 채널 운영자
- 반복적인 영상 편집 시간을 줄이고 싶은 1인 콘텐츠 제작자
- 기존 채널의 시각적·음악적 일관성을 유지하면서 제작량을 늘리려는 사용자

## 4. 핵심 가치

- 기능성: 실제 업로드 가능한 MP4와 부속 자료를 완성한다.
- 영향력: 영상 한 편당 반복 작업 시간을 크게 줄인다.
- 차별성: 파일 결합 도구가 아니라 테마에서 최종 패키지까지 연결한다.
- 사용성: 실행 시 핵심 입력은 테마 한 문장으로 제한한다.
- 재사용성: 외부 생성 서비스와 렌더링 단계를 교체 가능한 모듈로 분리한다.
- 지속성: 생성 비용과 실패 재시도를 기록하여 채널 운영비를 관리한다.

## 5. 성공 기준

- 테마 입력 후 수동 편집 없이 업로드 가능한 결과 폴더가 생성된다.
- 영상은 1920×1080, 24fps, H.264, AAC 규격을 만족한다.
- 곡 세트가 정해진 순서로 3회 반복된다.
- 챕터가 실제 첫 번째 세트의 곡 시작 시간과 일치한다.
- `Cover.jpg`가 영상 화면과 썸네일에 함께 사용된다.
- 외부 API 실패 시 원인과 재시도 상태를 사용자가 알 수 있다.

## 6. Related Documents

- **Concept_Design**: [Collaboration Guide](./00_COLLABORATION_GUIDE.md) - 협업과 의사결정 기준
- **Concept_Design**: [Lean Canvas](./02_LEAN_CANVAS.md) - 가치와 운영 구조
- **Concept_Design**: [Product Specifications](./03_PRODUCT_SPECS.md) - MVP 기능 명세
- **UI_Screens**: [Screen Flow](../02_UI_Screens/00_SCREEN_FLOW.md) - 사용자 여정
- **Technical_Specs**: [Development Principles](../03_Technical_Specs/00_DEVELOPMENT_PRINCIPLES.md) - 기술 구현 원칙

