# Lean Canvas
> Created: 2026-08-11 13:53
> Last Updated: 2026-08-11 13:53

## 1. 문제

- 재즈 영상 제작 과정이 서비스와 편집 도구 사이에서 단절되어 있다.
- 곡 연결, 반복, 챕터 계산과 렌더링이 매번 반복된다.
- 수작업 시간이 길어 채널 운영의 지속성과 제작량이 제한된다.

## 2. 고객군

- 1차 고객: 현재 재즈 YouTube 채널 운영자
- 확장 고객: 정지 이미지 기반 장시간 음악 채널 운영자

## 3. 고유 가치 제안

테마 한 문장만으로 음악과 이미지 생성부터 업로드 직전 장시간 영상 패키지까지 완성한다.

## 4. 솔루션

- Suno API 기반 음악 생성
- OpenAI API 기반 이미지와 업로드 문구 생성
- FFmpeg 기반 음악 분석, 3회 반복, 영상 렌더링 및 검증
- 결과물과 제작 기록의 일관된 폴더 구성

## 5. 핵심 지표

- 영상 한 편 제작에 필요한 사용자 개입 횟수
- 테마 입력부터 결과 완성까지 걸린 시간
- 외부 API 성공률과 자동 재시도 성공률
- 완성 영상 규격 검사 통과율
- 영상 한 편당 API 비용

## 6. 비용 구조

- Suno API 사용료: 로그인 후 공식 과금 확인 필요
- OpenAI API 이미지 및 텍스트 생성 사용료
- 로컬 저장 공간과 렌더링 시간

## 7. 방어력

- 기존 채널의 제목, 이미지, 음악 분위기 규칙을 축적한 채널 프로필
- 생성 프롬프트와 결과 품질 데이터
- 외부 생성 서비스와 FFmpeg를 연결하는 재시도·검증 파이프라인

## 8. 3 Investor Lenses

- Leverage: 한 번 구축한 파이프라인으로 반복 제작 비용을 줄인다.
- Realistic Money Flow: API 비용과 제작량을 영상 단위로 추적한다.
- Defensibility: 채널별 스타일 데이터와 성공 프롬프트가 누적될수록 결과 일관성이 높아진다.

## 9. Related Documents

- **Concept_Design**: [Vision & Core](./01_VISION_CORE.md) - 문제와 핵심 가치
- **Concept_Design**: [Product Specifications](./03_PRODUCT_SPECS.md) - MVP 범위
- **QA_Validation**: [QA Checklist](../05_QA_Validation/02_QA_CHECKLIST.md) - 비용 및 품질 검증 기준

