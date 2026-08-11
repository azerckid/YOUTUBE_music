# Collaboration Guide
> Created: 2026-08-11 13:53
> Last Updated: 2026-08-11 13:53

## 1. 목적

이 문서는 YouTube 재즈 영상 자동화 프로젝트에서 사용자와 AI가 같은 전제를 유지하기 위한 협업 기준을 정의한다.

## 2. 확정된 기준

- 운영 목적은 테마 한 문장을 입력해 YouTube 업로드 직전 결과물을 자동 완성하는 것이다.
- 음악은 Suno를 통해 생성한다.
- 이미지는 OpenAI 이미지 생성 API를 통해 생성한다.
- 사용자는 최종 결과를 확인한 뒤 YouTube Studio에 직접 업로드한다.
- 영상은 기존 참고 영상 3편과 같은 정지 이미지 기반 장시간 음악 영상이다.
- 별도 썸네일을 만들지 않고 `Cover.jpg`를 영상 화면과 썸네일에 함께 사용한다.
- 전체 곡 세트는 3회 반복한다.

## 3. 의사결정 규칙

1. 한 번에 하나의 제작 단계를 검토한다.
2. 외부 서비스 기능은 공식 문서로 가능 여부와 과금을 확인한 뒤 확정한다.
3. 확인되지 않은 API 동작은 구현 전제에 포함하지 않고 `검증 필요`로 표시한다.
4. 사용자에게 이미 확인받은 사항을 다시 결정 대상으로 제시하지 않는다.
5. 문서 변경 시 관련 문서와 백로그를 함께 동기화한다.

## 4. 현재 검증 필요 사항

- Suno API의 기존 월정액 포함 여부와 별도 과금 구조
- Suno API의 생성 상태 조회, 파일 다운로드, 동시 요청 한도 및 오류 형식
- 기존 YouTube 채널의 실제 채널명, 제목·설명 문체 및 고정 해시태그
- OpenAI API 키와 결제 설정
- Suno API 키와 결제 설정

## 5. Related Documents

- **Concept_Design**: [Vision & Core](./01_VISION_CORE.md) - 프로젝트 목적과 성공 기준
- **Concept_Design**: [Product Specifications](./03_PRODUCT_SPECS.md) - 확정된 제품 범위
- **Logic_Progress**: [Backlog](../04_Logic_Progress/00_BACKLOG.md) - 문서 기반 구현 작업

