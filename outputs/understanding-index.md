# Understanding Index

> 목적: 어떤 WWDC26 세션을 어떤 이해 문서로 읽어야 하는지 한눈에 찾기 위한 인덱스다. 영상을 가볍게 보고, 실제 이해는 `docs/understanding/` 문서에서 한다.

## 가장 먼저 볼 것

1. [`outputs/learning-guide.md`](learning-guide.md) — 전체 학습 순서
2. [`docs/understanding/README.md`](../docs/understanding/README.md) — understanding 문서 전체 인덱스
3. [`outputs/direct-watch-guide.md`](direct-watch-guide.md) — 직접 볼 영상/chapter 체크리스트

## A 세션

| Priority | Session | Apple URL | 이해 문서 | 영상은 어떻게 볼까 |
|---|---|---|---|---|
| A | Secure your apps with App Attest | https://developer.apple.com/videos/play/wwdc2026/201/ | [`app-attest.md`](../docs/understanding/app-attest.md) | Full video recommended. 단, 먼저 문서를 읽고 다시 본다. |
| A | What’s new in Xcode 27 | https://developer.apple.com/videos/play/wwdc2026/258/ | [`xcode-27-toolchain.md`](../docs/understanding/xcode-27-toolchain.md) | Coding Agents, Device Hub, Organizer, Instruments, Xcode Cloud chapter 중심. |
| A | Xcode, agents, and you | https://developer.apple.com/videos/play/wwdc2026/259/ | [`xcode-agents.md`](../docs/understanding/xcode-agents.md) | Full video recommended. agent transcript/artifacts flow를 본다. |
| A | What’s new in Swift | https://developer.apple.com/videos/play/wwdc2026/262/ | [`swift-compiler.md`](../docs/understanding/swift-compiler.md) | `@C`, optimizer control, ownership/noncopyable chapter 중심. |
| A | Meet Trust Insights | https://developer.apple.com/videos/play/wwdc2026/379/ | [`trust-insights.md`](../docs/understanding/trust-insights.md) | Transcript first. app tampering과 다른 risk layer만 잡는다. |
| A | Secure your app: mitigate risks to agentic features | https://developer.apple.com/videos/play/wwdc2026/347/ | [`agentic-security.md`](../docs/understanding/agentic-security.md) | Selected chapters. indirect prompt injection과 risky action 중심. |

## B 세션

| Priority | Session | Apple URL | 이해 문서 | 영상은 어떻게 볼까 |
|---|---|---|---|---|
| B | Profile, fix, and verify: Improve app responsiveness with Instruments | https://developer.apple.com/videos/play/wwdc2026/268/ | [`instruments-responsiveness.md`](../docs/understanding/instruments-responsiveness.md) | Selected chapters. profile/fix/verify loop만 본다. |
| B | Get the most out of Device Hub | https://developer.apple.com/videos/play/wwdc2026/260/ | [`device-hub.md`](../docs/understanding/device-hub.md) | Selected chapters. device/container/configuration 재현 흐름 중심. |
| B | Build, deliver, and automate with Xcode Cloud | https://developer.apple.com/videos/play/wwdc2026/261/ | [`xcode-cloud.md`](../docs/understanding/xcode-cloud.md) | Transcript first. CI/signing/artifact 관점으로 본다. |
| B | Migrate to Swift Testing | https://developer.apple.com/videos/play/wwdc2026/267/ | [`swift-testing.md`](../docs/understanding/swift-testing.md) | Transcript first. regression scenario 설계 관점으로 본다. |
| B | Debug and profile agentic app experiences with Instruments | https://developer.apple.com/videos/play/wwdc2026/243/ | [`agentic-instruments.md`](../docs/understanding/agentic-instruments.md) | Agentic feature를 관측하는 방식만 본다. |
| B | Meet the new MetricKit | https://developer.apple.com/videos/play/wwdc2026/222/ | [`metrickit.md`](../docs/understanding/metrickit.md) | Transcript first. field diagnostics 관점으로 본다. |
| B | What’s new in Foundation Models framework | https://developer.apple.com/videos/play/wwdc2026/241/ | [`foundation-models.md`](../docs/understanding/foundation-models.md) | Agentic security 배경으로 필요한 부분만 본다. |

## C 세션

| Priority | Session | Apple URL | 이해 문서 | 영상은 어떻게 볼까 |
|---|---|---|---|---|
| C | What’s new in SwiftUI | https://developer.apple.com/videos/play/wwdc2026/269/ | [`swiftui.md`](../docs/understanding/swiftui.md) | Skim only. compatibility 연결점만 본다. |
| C | Modernize your UIKit app | https://developer.apple.com/videos/play/wwdc2026/278/ | [`uikit.md`](../docs/understanding/uikit.md) | Skim only. scene/adaptive UI 가정 변화만 본다. |

## 읽기 원칙

- 영상은 “흐름 확인”용이다.
- 이해는 `docs/understanding/*.md`에서 한다.
- 세션 노트(`sessions/notes/*.md`)는 Apple session 기준 근거를 확인할 때 사용한다.
- 모르는 용어는 [`glossary.md`](../docs/understanding/glossary.md)로 돌아간다.
- 실제 구현 구조는 공개 자료만으로 단정하지 않고 `확인 필요`로 둔다.
