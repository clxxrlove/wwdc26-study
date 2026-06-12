# Watch Priority

이 파일은 WWDC26 전체 요약표가 아니라, **iOS 앱 보안 솔루션 / Xcode Toolchain / Swift Compiler / LLVM Pass** 보안/toolchain 관점의 학습 우선순위표다. 공개 출처 기반의 일반 기술 표현만 사용한다.

## 재검토 기준

- 핵심 질문: “새 Xcode/Swift/iOS SDK 변화가 compile-time protection, build integration, app integrity/anti-tamper, target-app compatibility에 어떤 영향을 줄 수 있는가?”
- A 세션은 transcript 기반 요약 노트를 만들고, 일부는 사용자가 직접 영상을 보는 것을 권장한다.
- B 세션은 transcript 또는 selected video chapter로 보조 학습한다.
- C 세션은 UI/framework 변화가 보안·toolchain 맥락과 연결될 때만 skim한다.
- 구현 구조는 아직 가정이므로 build phase, LLVM IR pass, linker, post-build binary rewriting 등 구체 지점은 **확인 필요**로 둔다.

## A — Must review

| Session | URL | Why for this study | Review mode | Status |
|---|---|---|---|---|
| What’s new in Xcode 27 | https://developer.apple.com/videos/play/wwdc2026/258/ | Xcode agents, Device Hub, Organizer, Instruments, Xcode Cloud가 build/diagnostics/CI compatibility와 연결됨. | Transcript note + key chapters video | NOTE DRAFTED |
| Xcode, agents, and you | https://developer.apple.com/videos/play/wwdc2026/259/ | Xcode agent가 project context, Apple docs, build/preview/test tools, sub-agents를 다루는 방식이 developer tooling/security workflow와 연결됨. | Full video recommended | NOTE DRAFTED |
| What’s new in Swift | https://developer.apple.com/videos/play/wwdc2026/262/ | Swift 6.3/6.4 compiler/language/performance 변화가 Swift-heavy 앱과 compiler-level transformation compatibility에 영향 가능. | Transcript first + selected compiler chapters | NOTE DRAFTED |
| Secure your apps with App Attest | https://developer.apple.com/videos/play/wwdc2026/201/ | modified/re-signed app, server-side validation, assertion counter, fraud metric이 app integrity/anti-tamper 보안/toolchain 맥락과 직접 연결됨. | Full video recommended | NOTE DRAFTED |
| Meet Trust Insights | https://developer.apple.com/videos/play/wwdc2026/379/ | iOS 27 social engineering/coercion risk signal. app tampering과 다른 fraud/risk layer 이해에 필요. | Transcript first | NOTE DRAFTED |
| Secure your app: mitigate risks to agentic features | https://developer.apple.com/videos/play/wwdc2026/347/ | Foundation Models/App Intents 기반 agentic feature의 indirect prompt injection, untrusted context, risky action mitigation 이해에 필요. | Transcript first + security chapters video | NOTE DRAFTED |

## Direct watch recommendations

직접 영상을 보는 목적은 도구 흐름과 위협 모델을 몸에 익히는 것이다. 단, 직접 보는 세션도 요약본은 유지한다.

| Watch recommendation | Session | 중점적으로 볼 것 | Summary note |
|---|---|---|---|
| Full video recommended | Secure your apps with App Attest | modified client → attestation → server validation → assertion → fraud metric flow. 특히 re-signing, Team Identifier, launch validation category, assertion counter. | `sessions/notes/secure-your-apps-with-app-attest.md` |
| Full video recommended | Xcode, agents, and you | agent transcript/artifacts UI, Apple Document Search, plan mode, build/preview/test validation, sub-agent orchestration. | `sessions/notes/xcode-agents-and-you.md` |
| Watch key chapters | What’s new in Xcode 27 | Coding Agents, Device Hub, Organizer metrics, Instruments Top Functions, Xcode Cloud setup. | `sessions/notes/whats-new-in-xcode-27.md` |
| Transcript first, selected video | What’s new in Swift | `@C`, `@inline(always)`, `@specialized`, ownership/noncopyable/borrow/mutate accessors. | `sessions/notes/whats-new-in-swift.md` |
| Transcript first | Meet Trust Insights | coercion/social engineering threat model, entitlement/API flow, feedback/privacy requirements. | `sessions/notes/meet-trust-insights.md` |
| Transcript first, selected video | Secure your app: mitigate risks to agentic features | indirect prompt injection, untrusted context, side-effect actions, confirmation/authentication checkpoints. | `sessions/notes/secure-your-app-mitigate-risks-to-agentic-features.md` |
| Selected video chapters | Profile, fix, and verify: Improve app responsiveness with Instruments | 보호 적용 후 CPU/hang/contention/performance regression을 어떻게 볼지. | TODO B note |
| Selected video chapters | Get the most out of Device Hub | simulator/physical device/app container/configuration 재현 workflow. | TODO B note |

## B — Review transcript / selected chapters

| Session | URL | Why for this study | Review mode | Status |
|---|---|---|---|---|
| Profile, fix, and verify: Improve app responsiveness with Instruments | https://developer.apple.com/videos/play/wwdc2026/268/ | 보호 적용 후 성능 저하·hang·contention 분석에 유용. | Transcript + Instruments chapters | TODO |
| Get the most out of Device Hub | https://developer.apple.com/videos/play/wwdc2026/260/ | 대상 환경 이슈 재현, simulator/device 설정, app container 확인 workflow 이해. | Selected video chapters | TODO |
| Build, deliver, and automate with Xcode Cloud | https://developer.apple.com/videos/play/wwdc2026/261/ | CI/CD, cloud build/test, signing/artifact handling compatibility 검토에 필요. | Transcript | TODO |
| Migrate to Swift Testing | https://developer.apple.com/videos/play/wwdc2026/267/ | 보호 로직 검증, crash/abort path 테스트 설계에 간접 관련. | Transcript | TODO |
| Debug and profile agentic app experiences with Instruments | https://developer.apple.com/videos/play/wwdc2026/243/ | agentic feature 보안 이슈 재현/관측에 보조적으로 유용. | Transcript + relevant chapters | TODO |
| Meet the new MetricKit | https://developer.apple.com/videos/play/wwdc2026/222/ | 보호 적용 후 real-world hang/performance/diagnostic signal 이해. | Transcript | TODO |
| What’s new in Foundation Models framework | https://developer.apple.com/videos/play/wwdc2026/241/ | agentic security 세션 보조 맥락. Foundation Models attack surface 이해에 필요한 부분만. | Security-relevant transcript sections | TODO |

## C — Skim only

| Session | URL | Why lower priority | Review mode | Status |
|---|---|---|---|---|
| What’s new in SwiftUI | https://developer.apple.com/videos/play/wwdc2026/269/ | UI framework 중심. compiler/runtime/security/build 영향이 보일 때만 확인. | Summary/chapter skim | TODO |
| Modernize your UIKit app | https://developer.apple.com/videos/play/wwdc2026/278/ | UIKit adaptivity/API 변화 중심. App Intents/View Annotations 보안 맥락이 필요할 때만 확인. | Summary skim | TODO |

## Suggested study order

1. **App integrity/security axis**: App Attest → Trust Insights → agentic risks.
2. **Toolchain/build axis**: Xcode 27 → Xcode agents → Swift.
3. **Compatibility/diagnostics axis**: Instruments responsiveness → Device Hub → Xcode Cloud → Swift Testing → MetricKit.
4. **Agentic context if needed**: Foundation Models framework → agentic Instruments.
5. **Skim only**: SwiftUI/UIKit when A/B notes require target-app context.

## Tooling-context questions to carry forward

- 실제 toolchain integration 지점이 Xcode build phase, Swift/Clang frontend, LLVM IR pass, linker, post-build binary rewriting 중 어디인지 **확인 필요**.
- Swift 코드 보호와 ObjC/C/C++ 코드 보호가 같은 pipeline을 타는지 **확인 필요**.
- App Attest server-side attestation/assertion/fraud metric을 보안 도구가 직접 제공하는지, 앱 backend integration guide 수준인지 **확인 필요**.
- Xcode 27 coding agents/tool workflow가 scan/protection/report workflow와 연결될 수 있는지 **확인 필요**.

## Source references

- Apple Developer WWDC26 session pages linked in the tables above.
