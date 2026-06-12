# Understanding Docs Index

이 폴더는 WWDC26 세션을 “요약 암기”가 아니라 “문제 구조 이해”로 읽기 위한 문서 모음이다.

읽는 순서는 파일명 순서가 아니라 아래 순서를 권장한다.

## 1. App integrity / risk 먼저 이해

| 먼저 읽을 문서 | 연결 세션 | 왜 읽는가 |
|---|---|---|
| [`app-attest.md`](app-attest.md) | Secure your apps with App Attest | modified/re-signed app, server-side validation, attestation/assertion/counter/fraud metric을 이해한다. |
| [`trust-insights.md`](trust-insights.md) | Meet Trust Insights | app tampering과 다른 social engineering/coercion risk layer를 구분한다. |
| [`agentic-security.md`](agentic-security.md) | Secure your app: mitigate risks to agentic features | indirect prompt injection, untrusted context, risky action을 이해한다. |

## 2. Toolchain / build compatibility 이해

| 문서 | 연결 세션 | 왜 읽는가 |
|---|---|---|
| [`xcode-27-toolchain.md`](xcode-27-toolchain.md) | What’s new in Xcode 27 | Xcode 27을 새 UI 목록이 아니라 build/test/diagnostics/CI workflow 변화로 본다. |
| [`xcode-agents.md`](xcode-agents.md) | Xcode, agents, and you | agent가 project context, build/test, artifacts를 다룰 때 생기는 자동화와 검증 경계를 이해한다. |
| [`swift-compiler.md`](swift-compiler.md) | What’s new in Swift | Swift compiler/language 변화가 transformation compatibility에 주는 의미를 이해한다. |
| [`xcode-cloud.md`](xcode-cloud.md) | Build, deliver, and automate with Xcode Cloud | local build와 cloud build/test/signing/artifact 흐름이 달라질 수 있는 지점을 본다. |

## 3. Verification / diagnostics 이해

| 문서 | 연결 세션 | 왜 읽는가 |
|---|---|---|
| [`instruments-responsiveness.md`](instruments-responsiveness.md) | Profile, fix, and verify: Improve app responsiveness with Instruments | 보호 적용 후 CPU/hang/contention/performance regression을 관측하는 사고 방식을 잡는다. |
| [`device-hub.md`](device-hub.md) | Get the most out of Device Hub | simulator/device/app container/configuration 기반 재현 workflow를 이해한다. |
| [`swift-testing.md`](swift-testing.md) | Migrate to Swift Testing | protection logic, crash/abort path, compatibility scenario를 test로 고정하는 방식을 생각한다. |
| [`metrickit.md`](metrickit.md) | Meet the new MetricKit | lab에서 못 본 real-world hang/performance/diagnostic signal을 보는 관점을 잡는다. |

## 4. Agentic / AI context 이해

| 문서 | 연결 세션 | 왜 읽는가 |
|---|---|---|
| [`foundation-models.md`](foundation-models.md) | What’s new in Foundation Models framework | Foundation Models를 전체 API가 아니라 agentic risk boundary의 배경으로 이해한다. |
| [`agentic-instruments.md`](agentic-instruments.md) | Debug and profile agentic app experiences with Instruments | agentic feature의 context/action/latency 관측을 보안 검토와 연결한다. |

## 5. Skim only

| 문서 | 연결 세션 | 왜 낮은 우선순위인가 |
|---|---|---|
| [`swiftui.md`](swiftui.md) | What’s new in SwiftUI | UI 중심 세션이다. target app compatibility나 App Intents 연결점이 보일 때만 본다. |
| [`uikit.md`](uikit.md) | Modernize your UIKit app | UI modernization 중심이다. scene lifecycle, orientation, adaptive UI가 compatibility와 연결될 때만 본다. |

## 6. 용어가 막힐 때

- [`glossary.md`](glossary.md)

## 7. 읽는 방법

1. 영상을 먼저 완벽히 이해하려고 하지 않는다.
2. `outputs/direct-watch-guide.md`로 볼 장면만 가볍게 본다.
3. 이해는 이 폴더의 문서에서 한다.
4. 각 문서 끝의 “내가 이해했는지 확인하는 질문”에 자기 말로 답해 본다.
5. 마지막에 `outputs/wwdc26-security-brief.md`를 읽어 전체 관점을 다시 압축한다.
