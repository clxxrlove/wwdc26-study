# Direct Watch Guide

이 파일은 WWDC26 영상을 직접 볼 때 사용할 체크리스트다. 모든 세션을 영상으로 볼 필요는 없지만, 아래 세션은 화면 흐름이나 threat flow를 직접 보는 편이 학습 효율이 높다. 직접 본 세션도 `sessions/notes/` 요약본은 유지한다.

## 1. Full video recommended

### Secure your apps with App Attest

- URL: https://developer.apple.com/videos/play/wwdc2026/201/
- Note: `sessions/notes/secure-your-apps-with-app-attest.md`

중점적으로 볼 것:

- modified/re-signed app이 서버에 valid-looking request를 보내는 위협 모델
- Team Identifier + bundle identifier + relying party identifier 관계
- iOS 27 launch validation category와 bundle version signal
- Secure Enclave-bound key generation
- attestation vs assertion 차이
- assertion counter가 anti-replay signal로 쓰이는 방식
- fraud metric을 차단 기준이 아니라 investigation signal로 쓰는 이유

보면서 적을 질문:

- app 내부 anti-tamper와 App Attest server validation은 어떤 관계인가?
- 보호 적용 후 App Attest relying party / bundle / signing 정보가 깨질 수 있는가?
- 앱 backend가 어느 수준까지 책임져야 하는가?

### Xcode, agents, and you

- URL: https://developer.apple.com/videos/play/wwdc2026/259/
- Note: `sessions/notes/xcode-agents-and-you.md`

중점적으로 볼 것:

- agent transcript와 artifacts UI
- project exploration 방식
- Apple Document Search가 최신 framework knowledge를 보완하는 방식
- plan mode에서 code 작성 전 architecture를 잡는 방식
- build / preview / test validation flow
- sub-agent orchestration이 어떤 작업에 쓰이는지

보면서 적을 질문:

- agent가 protection config, logs, build scripts를 읽을 수 있다면 어떤 정보가 노출될 수 있는가?
- tool CLI/report가 agent-friendly해야 하는가?
- 대상 앱이 Xcode agent로 build settings를 바꾸면 toolchain integration이 깨질 수 있는가?

## 2. Watch key chapters

### What’s new in Xcode 27

- URL: https://developer.apple.com/videos/play/wwdc2026/258/
- Note: `sessions/notes/whats-new-in-xcode-27.md`

볼 chapter:

- Coding Agents in the Editor
- Device Hub
- Organizer
- Instruments & Top Functions
- Xcode Cloud

중점적으로 볼 것:

- Xcode 27이 compiler 자체보다 developer workflow를 어떻게 바꾸는지
- Device Hub가 대상 환경 이슈 재현에 어떤 도움을 줄 수 있는지
- Organizer storage/hitches/Metric Goals가 보호 적용 후 regression 설명에 쓸 수 있는지
- Instruments Top Functions로 protection runtime/helper overhead를 볼 수 있는지
- Xcode Cloud에서 signing/license/artifact/dSYM 문제가 생길 가능성

### What’s new in Swift

- URL: https://developer.apple.com/videos/play/wwdc2026/262/
- Note: `sessions/notes/whats-new-in-swift.md`

볼 chapter:

- Swift-C Interoperability (`@C`)
- Performance Tuning
- Optimizer Control: `@inline(always)` / `@specialized`
- Ownership System & Noncopyable Types
- Borrow/Mutate Accessors

중점적으로 볼 것:

- Swift code가 C boundary로 노출될 때 protection/obfuscation 관점에서 무엇이 달라지는지
- optimizer control이 binary size/performance tradeoff에 어떤 영향을 줄 수 있는지
- ownership/noncopyable/borrow semantics가 transformation correctness에 어떤 제약을 줄 수 있는지

## 3. Transcript first, video optional

### Meet Trust Insights

- URL: https://developer.apple.com/videos/play/wwdc2026/379/
- Note: `sessions/notes/meet-trust-insights.md`

중점적으로 볼 것:

- coercion/social engineering이 app tampering과 다른 threat layer라는 점
- entitlement/API/feedback/privacy 요구사항
- unknown/medium/high 같은 risk signal을 어떻게 해석해야 하는지

### Secure your app: mitigate risks to agentic features

- URL: https://developer.apple.com/videos/play/wwdc2026/347/
- Note: `sessions/notes/secure-your-app-mitigate-risks-to-agentic-features.md`

중점적으로 볼 것:

- indirect prompt injection
- untrusted context source
- tool result와 action side effect
- user confirmation / device unlock / authentication checkpoint
- App Intents action surface가 보안 review 대상이 되는 이유

## 4. Later selected chapters

### Profile, fix, and verify: Improve app responsiveness with Instruments

- URL: https://developer.apple.com/videos/play/wwdc2026/268/
- 목적: 보호 적용 후 CPU/hang/contention/performance regression 분석 방법 확인.

### Get the most out of Device Hub

- URL: https://developer.apple.com/videos/play/wwdc2026/260/
- 목적: simulator/physical device/app container/configuration 기반 대상 환경 이슈 재현 workflow 확인.

### Build, deliver, and automate with Xcode Cloud

- URL: https://developer.apple.com/videos/play/wwdc2026/261/
- 목적: cloud CI에서 toolchain integration, signing, artifacts, dSYM, TestFlight/App Store delivery compatibility 확인.
