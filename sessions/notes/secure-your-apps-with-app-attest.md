# Secure your apps with App Attest

- URL: https://developer.apple.com/videos/play/wwdc2026/201/
- Duration: 약 20분
- Category: iOS app security / App integrity / Server-side validation
- Priority: A
- Review mode: Full video recommended + transcript note
- Last updated: 2026-06-12

## Why this matters to this study

- Apple session 기준 App Attest는 modified client, re-signing, compromised copy가 서버에 valid-looking request를 보내는 위협을 직접 다룬다.
- 모바일 앱 보호 도구 관점에서 App Attest는 앱 내부 난독화/anti-tamper와 경쟁한다기보다, 서버가 앱/디바이스 신뢰 신호를 검증하는 보완 축으로 이해하는 것이 적절하다. **추론**.
- 특히 Team Identifier, bundle identifier, launch validation category, bundle version, assertion counter, fraud metric은 app integrity / replay / broker-device risk를 설명할 때 중요하다.
- 이 세션은 직접 영상 시청 권장이다. threat flow와 attestation/assertion sequence는 화면으로 보는 편이 이해가 빠르다.

## 5-line summary

1. Apple session 기준 App Attest는 modified/re-signed app이 서버에 정상처럼 보이는 요청을 보내는 상황을 방어하기 위한 framework다.
2. Attestation은 Secure Enclave-bound key와 Apple hardware 기반 신뢰 증거를 서버가 검증하도록 하고, app identity 관련 정보를 제공한다.
3. iOS 27에서는 launch validation category가 강조되고, authenticator data extensions가 attestation/assertion에 포함된다.
4. Assertion은 attested key로 payload를 보호하고, 서버는 assertion counter가 strictly increasing인지 확인해 replay/compromised-copy 신호를 본다.
5. Fraud metric은 약 30일 동안 특정 device에서 앱과 연결된 unique attested keys의 approximate count로, 차단 근거가 아니라 risk investigation signal로 사용해야 한다.

## New APIs / tools / frameworks

| Name | Type | Notes | Relevance |
|---|---|---|---|
| `DCAppAttestService.shared.generateKey()` | DeviceCheck API | Secure Enclave-bound key pair를 만들고 key ID를 반환. | App/device-bound 신뢰 anchor 생성. |
| `DCAppAttestService.shared.attestKey(...)` | DeviceCheck API | key ID와 server challenge로 attestation object 생성. | 서버 검증 기반 app integrity flow의 핵심. |
| `DCAppAttestService.shared.generateAssertion(...)` | DeviceCheck API | attested key로 assertion 생성. | payload integrity, anti-replay 설계에 중요. |
| `isSupported` | App Attest availability API | platform/app type 지원 여부 gate. Apple session 기준 unexpected unsupported response를 fraud signal로 볼 수 있음. | 대상 앱 호환성과 risk scoring에 필요. |
| Launch validation category | iOS 27 App Attest signal | App Store/TestFlight 등 launch validation category를 노출. | re-signing/비정상 배포 경로 탐지 맥락. |
| Authenticator data extensions | iOS 27 App Attest structure | attestation/assertion authenticator data 끝에 extension structure가 붙는다고 설명. | 서버 parser/validator 업데이트 필요 가능. |
| Fraud metric | App Attest server-side data flow | receipt 기반으로 App Attest data server에서 조회. | broker device / suspicious attestation activity signal. |

## Toolchain / compiler / build implications

- 직접적인 compiler/LLVM 변경 세션은 아니다.
- App Attest adoption은 “latest SDKs로 rebuild”가 next step으로 제시된다. SDK/Xcode 업데이트 시 서버 validator와 app-side DeviceCheck API usage가 함께 검증되어야 한다.
- re-signing, Team Identifier, bundle identifier, provisioning profile과 연결되므로 signing/distribution pipeline 이해가 필요하다.
- 보호 보안 도구가 bundle metadata, signing, embedded frameworks, resource bundle을 변경한다면 App Attest가 기대하는 app identity와 충돌하지 않는지 확인해야 한다. **추론 / 확인 필요**.

## Security / anti-tamper / integrity implications

- App Attest는 modified copy가 서버에 보내는 요청을 서버 측에서 거절할 수 있게 돕는다.
- Apple session 기준 app identity는 Team Identifier + bundle identifier 기반 relying party identifier와 연결된다.
- iOS 27 launch validation category와 bundle version signal은 unauthorized modification/re-signing 판단에 도움이 될 수 있다.
- Assertion counter는 steady/decreasing value가 compromised copy나 replay 관련 신호일 수 있다고 설명된다.
- Fraud metric은 outright block이 아니라 monitoring, baseline, spike detection에 쓰라고 안내된다.

## Security/toolchain impact hypothesis

> 추론: 모바일 앱 보호 보안 도구는 앱 내부 변조 비용을 올리고, App Attest는 서버가 “이 요청을 신뢰할 수 있는 앱/디바이스에서 온 것으로 볼 수 있는가”를 판단하게 한다. 따라서 스터디 관점에서는 App Attest를 대체재가 아니라 backend risk pipeline과 결합되는 신뢰 신호로 이해해야 한다. 보안 도구가 signing/resource/bundle metadata를 건드린다면 App Attest validator와의 compatibility checklist가 필요할 수 있다.

## Risks / compatibility questions

- 보호 적용 후 Team Identifier, bundle identifier, bundle version, launch validation category가 서버 기대값과 일치하는가? **확인 필요**.
- 앱 backend가 attestation certificate chain, receipt, authenticator data extensions, assertion counter를 검증할 준비가 되어 있는가? **확인 필요**.
- App reinstall/device restore/key rotation을 fraud로 오탐하지 않도록 risk policy가 설계되어 있는가?
- Fraud metric을 user blocking 기준으로 쓰지 않고 investigation signal로 다루는 가이드가 있는가?
- App Attest unsupported response를 tampering signal로 볼 때 false positive 처리 기준이 있는가?

## Study questions from this session

1. 우리 맥락의 mobile app protection/toolchain integration은 App Attest와 어떤 관계로 설명되는가? 보완 기능인가, 앱 backend integration guide만 제공하는가?
2. 보호 적용 후 App Attest attestation/assertion flow가 깨지지 않는지 검증하는 sample app이나 checklist가 있는가?
3. re-signing이나 bundle/resource 변경을 수행하는 보호 기능이 있다면 App Attest relying party identifier, bundle version, launch validation category와 충돌하지 않는가?
4. 대상 앱에서 App Attest fraud metric을 사용할 때 false positive와 graceful degradation 가이드를 제공하는가?
5. App Attest 관련 서버 검증 코드를 도구 범위에 포함하는지, 아니면 대상 환경 책임 영역인지 확인하고 싶다.

## Must-watch chapters

- 1:35 — Protections: modified copy, re-signing, valid-looking request 위협 모델.
- 4:04 — Availability: supported platform/app type과 `isSupported` risk signal.
- 6:12 — Attestation: Secure Enclave key, server challenge, server-side validation.
- 12:10 — Assertion: payload protection, CPU impact, assertion counter.
- 16:27 — Fraud metric: broker device risk, receipt flow, risk signal로 쓰는 방식.

## Source notes

- Apple Developer session page/transcript: https://developer.apple.com/videos/play/wwdc2026/201/
- Apple session 기준 확인한 항목: modified/re-signed app threat, Team Identifier/bundle identifier/relying party identifier, launch validation category, bundle version, `isSupported`, Secure Enclave-bound key, attestation/assertion, assertion counter, fraud metric, graceful degradation guidance.
- 직접 시청 권장: 전체 flow diagram과 attestation/assertion/fraud metric sequence는 영상으로 확인하는 편이 좋다.
