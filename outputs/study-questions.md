# Study Questions

> 목적: WWDC26 학습 내용을 mobile app security / toolchain 관점의 후속 질문으로 정리한다.

## 1. Integration context

1. 보안 도구는 대상 Xcode 프로젝트의 어느 단계에 통합되는지 먼저 이해하고 싶습니다. Build Phase, custom toolchain, compiler/LLVM 단계, linker 이후 단계 중 어떤 구조에 가까운가요?
   - 왜 묻는가: WWDC26 Xcode/Swift 변화가 실제로 어느 지점에 영향을 주는지 판단하려면 통합 지점을 알아야 합니다.

2. 난독화, 위변조 탐지, anti-tamper, runtime protection은 하나의 pipeline으로 적용되나요, 아니면 기능별로 적용 단계가 나뉘나요?
   - 왜 묻는가: 기능별 적용 단계가 다르면 Xcode/Swift/LLVM 변화에 대한 compatibility risk도 달라집니다.

3. 대상 앱이 보안 도구를 적용할 때 가장 자주 겪는 실패 유형은 build 실패, signing 문제, runtime crash, 성능 저하 중 무엇인가요?
   - 왜 묻는가: 어떤 troubleshooting 역량을 우선 학습해야 하는지 정하기 위해서입니다.

## 2. Xcode / Build pipeline

1. Xcode 27 대응에서 현재 가장 주의 깊게 보는 변화가 있나요? Xcode Cloud, Organizer diagnostics, Device Hub, coding agents 중 영향이 큰 부분이 있는지 궁금합니다.
   - 왜 묻는가: WWDC26 기준 Xcode 27은 build/test/diagnostics/agent workflow가 함께 바뀌고 있습니다.

2. 보안 도구 적용 과정이 Xcode Cloud 같은 cloud CI에서도 공식 지원되는지, 또는 local build 중심인지 알고 싶습니다.
   - 왜 묻는가: cloud CI에서는 license, signing, artifact, network, cache 처리가 달라질 수 있습니다.

3. 대상 프로젝트가 Tuist, XcodeGen, Swift Package Manager, CocoaPods, custom scripts를 사용할 때 지원 범위가 어떻게 달라지나요?
   - 왜 묻는가: 실제 대상 build graph가 Xcode 기본 구조와 다를 수 있기 때문입니다.

## 3. Swift / LLVM / Compiler

1. Swift 코드 보호와 ObjC/C/C++ 코드 보호는 같은 LLVM 기반 pipeline을 사용하나요, 아니면 언어별로 다른 접근을 하나요?
   - 왜 묻는가: Swift compiler output과 Clang 기반 output의 처리 방식이 다르면 학습해야 할 영역이 달라집니다.

2. LLVM Pass를 사용한다면 pass ordering, optimization level, debug info 보존 문제는 어떻게 관리하나요?
   - 왜 묻는가: 난독화/보안 변환은 최적화 pass와 상호작용하면서 성능·정확성·symbolication에 영향을 줄 수 있습니다.

3. Swift 6.3/6.4의 `@C`, `@inline(always)`, `@specialized`, ownership/noncopyable 기능을 포함한 regression test가 있나요?
   - 왜 묻는가: WWDC26 Swift 세션 기준 compiler/language 변화가 compatibility test corpus에 들어가야 할 수 있습니다.

4. Swift-C interop boundary나 exported symbol은 보호/난독화 정책에서 어떻게 다루나요?
   - 왜 묻는가: `@C` 같은 기능이 늘어나면 Swift와 C boundary가 toolchain behavior에 영향을 줄 수 있습니다.

## 4. iOS app security

1. 보안 도구가 우선적으로 방어하려는 threat model은 re-signing, static reverse engineering, dynamic instrumentation, jailbreak/rootless jailbreak, runtime tampering 중 어디에 가장 가깝나요?
   - 왜 묻는가: 같은 “앱 보호”라도 threat model에 따라 구현과 검증 방법이 달라집니다.

2. anti-tamper나 integrity check가 실패했을 때 대상 앱에서 어떤 정책을 권장하나요? 차단, degrade, server-side risk scoring 등 패턴이 있는지 궁금합니다.
   - 왜 묻는가: 보안 기능은 false positive와 사용자 경험도 함께 고려해야 합니다.

3. 보호 적용 후 dSYM, crash report, symbolication, App Store 심사 호환성은 어떤 방식으로 검증하나요?
   - 왜 묻는가: 운영 단계에서 보안 기능과 진단 가능성이 충돌하면 진단 비용이 커질 수 있습니다.

## 5. App Attest / Apple security frameworks

1. App Attest 같은 Apple framework와 app integrity/anti-tamper 기능은 보완 관계로 안내하나요, 아니면 사용 시 주의할 점이 있나요?
   - 왜 묻는가: App Attest는 서버 검증 기반 신뢰 신호이고, 앱 내부 보호 기능과 역할이 다를 수 있습니다.

2. 대상 앱에서 App Attest를 이미 사용 중인 경우, 보호 적용 후 attestation/assertion flow에 영향이 있는지 확인하는 checklist가 있나요?
   - 왜 묻는가: Team Identifier, bundle identifier, bundle version, launch validation category, assertion counter와 관련될 수 있습니다.

3. App Attest fraud metric은 도입 환경에서 어떤 수준으로 설명하나요? 단독 차단 기준이 아니라 investigation signal로 안내하나요?
   - 왜 묻는가: Apple session 기준 fraud metric은 baseline/spike/risk investigation signal로 다뤄야 합니다.

4. Trust Insights 같은 iOS 27 risk signal framework는 도구 가이드나 대상 threat modeling에서 고려 대상인가요?
   - 왜 묻는가: social engineering/coercion risk는 app tampering과 다른 계층의 보안 문제입니다.

## 6. Agentic app security

1. Foundation Models나 App Intents를 쓰는 대상 앱에서 agentic feature risk를 별도로 검토하나요?
   - 왜 묻는가: WWDC26 보안 세션은 indirect prompt injection, untrusted context, risky action mitigation을 강조합니다.

2. App Intents/action surface inventory를 보호 적용 전후에 확인하는 절차가 있나요?
   - 왜 묻는가: agent가 호출 가능한 action이 늘어나면 기존 binary protection과 다른 review 대상이 생깁니다.

3. indirect prompt injection처럼 앱 무결성과 다른 계층의 위험은 도입 환경에서 어떻게 설명하나요?
   - 왜 묻는가: 보안 도구가 막는 위험과 앱 설계에서 별도로 막아야 하는 위험을 구분해야 합니다.

## 7. Target-app compatibility

1. 보호 적용 전후 binary size, launch time, hot path overhead를 측정하는 표준 benchmark가 있나요?
   - 왜 묻는가: Xcode 27 Organizer storage metric과 Instruments Top Functions를 검증에 활용할 수 있을지 알고 싶습니다.

2. 대상 앱에서 성능 문제가 보고되면 Instruments, MetricKit, Organizer 중 어떤 도구를 우선 사용하나요?
   - 왜 묻는가: WWDC26에서 Apple이 performance/diagnostics workflow를 강화했습니다.

3. 보호 적용 후 문제가 생겼을 때 최소 재현 프로젝트나 sample app을 만드는 기준이 있나요?
   - 왜 묻는가: troubleshooting 역량을 빠르게 키우기 위해 필요합니다.

## 8. Testing / diagnostics / CI

1. Xcode Cloud, GitHub Actions, Jenkins 같은 CI에서 보안 도구 적용을 검증하는 공식 sample이나 guide가 있나요?
   - 왜 묻는가: 도입 CI 환경에서 signing, license, artifact, cache 처리가 문제될 수 있습니다.

2. Device Hub나 `devicectl`을 대상 환경 이슈 재현에 활용하는 계획이 있나요?
   - 왜 묻는가: Xcode 27의 Device Hub는 simulator/physical device/app container 상태 확인에 유용해 보입니다.

3. 보호 runtime/helper가 hot path에 들어가는지 확인하는 Instruments 기반 절차가 있나요?
   - 왜 묻는가: Top Functions 같은 기능으로 protection overhead를 구체적으로 확인할 수 있습니다.

## 9. Study plan

1. 후속 학습에서 우선 읽거나 실습할 공개 문서·샘플 코드는 무엇인가요?
   - 왜 묻는가: 도구 통합 지점과 도입 환경 진단 흐름을 빠르게 파악하기 위해서입니다.

2. LLVM/Swift/iOS 보안 중 어느 축을 먼저 깊게 파는 것이 학습에 가장 도움이 될까요?
   - 왜 묻는가: 역할 범위가 넓어 보이므로 초반 학습 우선순위를 맞추고 싶습니다.

3. 과거 Xcode major update 때 가장 문제가 되었던 compatibility issue 사례를 볼 수 있을까요?
   - 왜 묻는가: Xcode 27 대응에서도 비슷한 리스크가 반복될 수 있기 때문입니다.

4. 첫 달에 직접 재현해보면 좋은 end-to-end 시나리오가 있을까요? 예: sample app 보호 적용, archive/export, TestFlight 배포, crash symbolication 확인 등.
   - 왜 묻는가: 문서만 읽기보다 실제 pipeline을 한 번 통과해보는 것이 빠른 학습에 도움이 됩니다.
