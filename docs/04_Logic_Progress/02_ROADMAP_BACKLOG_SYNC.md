# Roadmap and Backlog Sync
> Created: 2026-08-11 13:53
> Last Updated: 2026-08-11 13:53

## 1. 목적

로드맵의 단계, 백로그의 실행 티켓과 실제 구현 상태가 서로 어긋나지 않도록 관리한다.

## 2. 동기화 규칙

- [ ] 로드맵 항목을 시작할 때 대응 백로그 티켓을 `In Progress`로 변경한다.
- [ ] 티켓 착수 전에 모든 Related 문서와 구현 선행조건을 확인한다.
- [ ] 구현 중 요구사항이 바뀌면 코드보다 문서를 먼저 갱신한다.
- [ ] 티켓 완료 시 수용 기준과 QA 결과를 기록한다.
- [ ] 완료된 티켓에 문서 동기화 확인을 표시한다.
- [ ] 로드맵 단계 완료 시 미완료 티켓이 없는지 확인한다.

## 3. 상태 매핑

| Roadmap | Backlog | 의미 |
|:---|:---|:---|
| Pending | ToDo | 선행조건 또는 착수 대기 |
| Active | In Progress | 구현 또는 검증 진행 |
| Complete | Done | 수용 기준과 문서 동기화 완료 |

## 4. Related Documents

- **Logic_Progress**: [Roadmap](./00_ROADMAP.md) - 단계별 목표
- **Logic_Progress**: [Backlog](./00_BACKLOG.md) - 실행 티켓
- **Logic_Progress**: [Execution Plan](./01_EXECUTION_PLAN.md) - 원자적 작업 순서
- **QA_Validation**: [QA Checklist](../05_QA_Validation/02_QA_CHECKLIST.md) - 완료 검증 기준

