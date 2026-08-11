# Main Flow Prototype Review
> Created: 2026-08-11 13:53
> Last Updated: 2026-08-11 14:34

## 1. HTML UI Preview

- Preview: [Main Flow Preview](./previews/01_MAIN_FLOW_PREVIEW.html)
- 확인 방식: 로컬 브라우저에서 HTML 파일 열람
- 확인 목적: 테마 입력, 제작 진행과 결과 확인 흐름 검토

## 2. Key User Flows

- 테마 입력 후 제작 시작
- 12개 자동화 단계의 진행 상태 확인
- API 오류 발생 시 실패 단계 재시도
- 완료 후 결과 폴더 열기

## 3. Screen States

- Default: 테마 입력과 제작 시작
- Loading: 현재 단계와 진행률
- Empty: 테마 예시 안내
- Error: 실패 원인과 재시도
- Permission denied: API 키 누락 안내

## 4. Data Flow

- Inputs: 테마 한 문장
- Displayed data: 채널 프로필, 현재 단계, 진행률, 결과 파일
- Mutations: 프로젝트 생성, 외부 API 요청, 로컬 파일 생성
- External dependencies: 1차 버전은 FFmpeg만 자동 실행하며 Suno와 이미지 서비스는 사용자가 직접 사용

## 5. User Confirmation

- 화면/UI 선확인 여부: 확인 완료
- HTML Preview 확인 여부: 확인 완료
- 확인자: 프로젝트 사용자
- 확인 일시: 2026-08-11 14:10 KST
- 보완 필요 사항: 입력과 진행 영역의 좌우 배치를 세로 순차 흐름으로 변경

## 6. Feedback and Improvements

- 사용자 확인 의견: 테마를 입력하고 시작하면 제작 진행이 입력 영역 아래에서 차례대로 진행되고, 마지막에 완료 결과가 표시되어야 한다.
- 반영 내용: 단일 페이지의 세로 흐름으로 변경하고 단계 상태와 완료 결과가 순차적으로 나타나는 동작형 Preview로 수정한다.
- 수정 시안 최종 확인 상태: 완료
- 최종 확인 근거: 사용자가 2026-08-11 14:34 KST에 API 없이 구현을 진행하도록 지시함

## 7. Related Documents

- **Concept_Design**: [Product Specifications](../01_Concept_Design/03_PRODUCT_SPECS.md) - 화면 기능 요구사항
- **UI_Screens**: [Screen Flow](./00_SCREEN_FLOW.md) - 전체 사용자 흐름
- **UI_Screens**: [UI Design](./01_UI_DESIGN.md) - 화면 및 상태 기준
- **UI_Screens**: [HTML Preview](./previews/01_MAIN_FLOW_PREVIEW.html) - 브라우저 확인용 프로토타입
- **Technical_Specs**: [Development Principles](../03_Technical_Specs/00_DEVELOPMENT_PRINCIPLES.md) - 구현 전 기술 기준
