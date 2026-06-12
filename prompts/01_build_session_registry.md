# Prompt 01 — Build Session Registry

Apple Developer WWDC26 세션 목록을 기준으로, 이 레포의 목적에 맞는 세션 레지스트리를 보강해라.

입력:

- `registry/seed_sessions.csv`
- 가능하면 Apple Developer WWDC26 video page의 세션 목록

해야 할 일:

1. 기존 seed session을 유지하되, 누락된 관련 세션이 있으면 추가해라.
2. 각 세션에 대해 다음 컬럼을 채워라.
   - priority_seed
   - title
   - url
   - category
   - study_relevance
   - reason
   - review_mode
3. 관련도 기준은 다음이다.
   - Xcode 27 / toolchain / build / agent / plugin / MCP / Agent Client Protocol
   - Swift 6.4 / compiler / runtime / performance / C interop
   - App Attest / Trust Insights / app integrity / anti-tamper
   - signing / entitlement / runtime security / diagnostics
4. UI, 디자인, visionOS, 게임, 마케팅 중심 세션은 과감히 C 또는 Skip으로 내려라.
5. 결과는 `registry/session_registry.csv`로 저장하라.
6. 그 결과를 바탕으로 `outputs/watch-priority.md`도 업데이트하라.

주의:

- URL을 모르면 비워두고 `확인 필요`라고 써라.
- 제목과 URL을 추측하지 마라.
