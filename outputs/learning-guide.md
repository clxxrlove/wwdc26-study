# WWDC26 Understanding Guide

> 이 문서는 세션별 암기 요약이 아니라, WWDC26 내용을 **왜 알아야 하는지 → 어떤 문제를 설명하는지 → 어떤 순서로 이해해야 하는지** 안내하는 메인 학습 지도다.

## 0. 먼저 관점을 바꾼다

WWDC 세션을 볼 때 모든 API 이름을 외울 필요는 없다. 중요한 것은 다음 세 가지다.

1. **위협 모델**: 어떤 공격이나 실패 상황을 다루는가?
2. **신뢰 경계**: 앱, OS, Secure Enclave, Apple server, 앱 backend 중 무엇을 믿고 무엇을 믿지 않는가?
3. **통합 지점**: Xcode build, Swift compiler, signing, runtime, server validation 중 어디와 연결되는가?

이 세 가지 질문에 답하지 못하면 세션 요약을 외워도 실제로는 이해한 것이 아니다.

## 1. 전체 읽기 순서

### 1단계 — App integrity / risk axis

- [`App Attest`](../docs/understanding/app-attest.md): 서버가 어떤 증거를 보고 요청을 신뢰하는지 이해한다.
- [`Trust Insights`](../docs/understanding/trust-insights.md): app tampering과 social engineering/coercion risk를 구분한다.
- [`Agentic security`](../docs/understanding/agentic-security.md): indirect prompt injection과 risky action을 이해한다.

### 2단계 — Toolchain / build axis

- [`Xcode 27 toolchain`](../docs/understanding/xcode-27-toolchain.md): Xcode 27을 build/test/diagnostics/CI workflow 변화로 본다.
- [`Xcode agents`](../docs/understanding/xcode-agents.md): agent가 project context와 build/test를 다룰 때 생기는 자동화와 검증 경계를 본다.
- [`Swift compiler`](../docs/understanding/swift-compiler.md): Swift 6.3/6.4 변화가 transformation compatibility에 주는 의미를 본다.
- [`Xcode Cloud`](../docs/understanding/xcode-cloud.md): local build와 cloud build/test/signing/artifact 흐름의 차이를 본다.

### 3단계 — Verification / diagnostics axis

- [`Instruments responsiveness`](../docs/understanding/instruments-responsiveness.md): profile/fix/verify loop를 이해한다.
- [`Device Hub`](../docs/understanding/device-hub.md): device/container/configuration 기반 재현 workflow를 이해한다.
- [`Swift Testing`](../docs/understanding/swift-testing.md): compatibility scenario를 test로 고정하는 사고 방식을 본다.
- [`MetricKit`](../docs/understanding/metrickit.md): real-world diagnostics를 local 재현으로 되돌리는 흐름을 본다.

### 4단계 — Agentic / AI context

- [`Foundation Models`](../docs/understanding/foundation-models.md): agentic feature의 risk boundary를 이해하기 위한 배경으로 본다.
- [`Agentic Instruments`](../docs/understanding/agentic-instruments.md): agentic feature의 context/action/latency 관측을 이해한다.

### 5단계 — Skim only

- [`SwiftUI`](../docs/understanding/swiftui.md): target app compatibility 연결점이 보일 때만 본다.
- [`UIKit`](../docs/understanding/uikit.md): scene/adaptive UI 가정 변화가 compatibility와 연결될 때만 본다.

용어가 막히면 [`glossary.md`](../docs/understanding/glossary.md)로 돌아간다.

## 2. 영상과 문서의 역할 분리

| 자료 | 역할 | 읽는 시점 |
|---|---|---|
| `outputs/direct-watch-guide.md` | 어떤 영상/chapter를 볼지 정함 | 영상 보기 직전 |
| `docs/understanding/*.md` | 개념과 문제 구조를 이해함 | 영상 전후 모두 |
| `sessions/notes/*.md` | Apple session 기준 근거 확인 | 세부 claim 확인 시 |
| `outputs/wwdc26-security-brief.md` | 전체 관점 압축 | 마지막 |
| `outputs/study-questions.md` | 후속 학습 질문 정리 | 마지막 |

## 3. 각 세션을 볼 때 머릿속에 둘 질문

| 세션 | 외울 것 | 이해해야 할 것 |
|---|---|---|
| Secure your apps with App Attest | API 이름 전체 | 왜 server-side validation이 핵심인지, attestation/assertion/fraud metric이 각각 다른 문제를 푸는 이유 |
| What’s new in Xcode 27 | 모든 새 UI | build, device, diagnostics, CI 흐름이 어떻게 연결되는지 |
| Xcode, agents, and you | agent 기능 목록 | agent가 project context를 읽고 수정할 때 생기는 자동화/정보노출 경계 |
| What’s new in Swift | 새 문법 나열 | compiler output, ABI boundary, optimizer control, ownership model이 compatibility에 주는 영향 |
| Meet Trust Insights | enum/API 이름 | social engineering/coercion risk가 app tampering과 다른 계층인 이유 |
| Secure your app: mitigate risks to agentic features | mitigation bullet | LLM/agent가 action을 호출할 때 왜 untrusted context와 user confirmation이 필요한지 |
| Instruments responsiveness | UI 조작 순서 | profile/fix/verify loop로 regression을 좁히는 방식 |
| Device Hub | 메뉴 위치 | device/container/configuration이 재현성에 주는 영향 |
| Xcode Cloud | 설정 화면 | local build와 cloud build/test/signing 차이 |
| Swift Testing | syntax 전체 | compatibility scenario를 반복 가능한 test로 만드는 방식 |
| MetricKit | payload 이름 전체 | field diagnostics를 local 재현과 수정으로 되돌리는 방식 |
| Foundation Models / agentic Instruments | API 전체 | agentic feature의 context/action boundary와 관측 방식 |
| SwiftUI / UIKit | UI 기능 전체 | target app compatibility와 연결되는 변화만 |

## 4. “이해했다”의 기준

아래 질문에 자기 말로 답할 수 있으면 1차 이해가 된 것이다.

1. App Attest에서 attestation과 assertion은 왜 둘 다 필요한가?
2. modified/re-signed app은 왜 서버 입장에서 위험한가?
3. App Attest가 있어도 앱 내부 anti-tamper가 완전히 불필요해지지 않는 이유는 무엇인가?
4. Xcode agents가 build setting, script, log를 읽을 때 어떤 경계가 필요한가?
5. Swift `@C`는 왜 symbol/ABI/obfuscation 관점에서 신경 써야 하는가?
6. Trust Insights는 왜 app integrity 기능이 아닌가?
7. agentic feature의 indirect prompt injection은 왜 기존 mobile app tampering과 다른 문제인가?
8. Xcode Cloud에서만 깨질 수 있는 build/signing/artifact 문제는 무엇인가?
9. Instruments, Device Hub, MetricKit은 각각 어떤 단계의 문제를 관측하는가?
10. SwiftUI/UIKit 세션을 낮은 우선순위로 두는 이유는 무엇인가?

## 5. 다음 문서

- 세션별 문서 찾기: [`outputs/understanding-index.md`](understanding-index.md)
- 문서 폴더 인덱스: [`docs/understanding/README.md`](../docs/understanding/README.md)
- 직접 시청 가이드: [`outputs/direct-watch-guide.md`](direct-watch-guide.md)

## 6. 주의

- 이 문서들은 공개 Apple session과 일반적인 보안/toolchain 관점에 기반한다.
- 실제 구현 구조는 공개 자료만으로 단정하지 않는다.
- 불확실한 연결은 `추론` 또는 `확인 필요`로 유지한다.
