# Meet Trust Insights

- URL: https://developer.apple.com/videos/play/wwdc2026/379/
- Duration: 약 13분
- Category: iOS security / Trust and Safety / Fraud risk signal
- Priority: A
- Review mode: Transcript first; video if user-flow UX matters
- Last updated: 2026-06-12

## Why this matters to this study

- Apple session 기준 Trust Insights는 iOS 27 framework로, coercion과 social engineering 상황을 앱이 감지하고 대응하도록 돕는다.
- 기술적 app tampering과는 다른 축이지만, 금융/계정/고가치 transaction을 다루는 앱의 risk logic과 연결될 수 있다.
- 모바일 앱 보호 도구 관점에서는 “기기/앱 무결성” 외에도 “사용자가 자유로운 의사로 행동하는가”라는 신호가 보안 설계에 들어온다는 점이 중요하다.

## 5-line summary

1. Trust Insights는 social engineering/coercion threat를 다루며, 사용자가 실제로는 압박을 받는 상황에서도 앱 action은 정상 사용자 action처럼 보인다는 문제를 출발점으로 한다.
2. Apple session 기준 integration은 client-side Swift API로 이루어지며 entitlement 선언, parameter pack 구성, `InsightEvaluator` 사용이 필요하다.
3. Operation category는 payment, account, resourceUse, communication 등 사용자 action 유형에 맞는 model logic을 선택하는 역할을 한다.
4. `IsLikelyBeingCoachedInsight` 결과는 unknown/medium/high 같은 risk-oriented value로 설명된다.
5. Trust Insights는 mandatory real-time consumption feedback과 offline fraud feedback을 요구하며, privacy architecture는 data minimization/on-device processing/user control을 강조한다.

## New APIs / tools / frameworks

| Name | Type | Notes | Relevance |
|---|---|---|---|
| Trust Insights | iOS 27 framework | coercion/social engineering detection 지원. | app fraud/risk signal 이해. |
| Entitlement / capability | App capability | Xcode app target에 capability 선언 필요. | entitlement/signing compatibility 확인 필요. |
| `InsightEvaluator` | Swift API | requested insights와 operation category를 평가. | transaction/action risk evaluation. |
| `IsLikelyBeingCoachedInsight` | Insight | coaching risk를 unknown/medium/high로 제공한다고 설명. | social-engineering risk scoring. |
| Consumption feedback | Required feedback | app이 insight에 어떻게 반응했는지 real-time feedback. | 모델 정확도/운영 요구사항. |
| Offline fraud feedback | Required feedback | 나중에 fraud로 판명된 transaction feedback. | risk pipeline 운영. |

## Toolchain / compiler / build implications

- 직접 compiler/LLVM 영향은 없다.
- entitlement/capability가 필요하므로 signing, provisioning profile, App Store capability configuration과 연결된다.
- 보호 보안 도구가 entitlement, signing, provisioning profile, build settings를 다룬다면 Trust Insights capability와 충돌하지 않는지 확인해야 한다. **추론 / 확인 필요**.

## Security / anti-tamper / integrity implications

- Trust Insights는 app binary integrity를 직접 보장하지 않는다.
- 보안 관점의 핵심은 “정상 앱 + 정상 인증 사용자”라도 coercion/social engineering으로 위험 행동을 할 수 있다는 threat model 확장이다.
- Apple session 기준 unknown은 low risk를 의미하지 않으며, medium/high는 additional verification, friction, risk scoring 조정, 사용자 고지 등으로 대응해야 한다.
- 기존 risk logic과 결합하는 방식이 중요하며 단독 차단 signal로 과신하면 안 된다. **추론**.

## Security/toolchain impact hypothesis

> 추론: 모바일 앱 보호 보안 도구가 앱 무결성/anti-tamper 중심이라면 Trust Insights는 직접 경쟁 기능이 아니라 대상 앱의 fraud/risk pipeline에 들어가는 별도 Apple signal이다. 금융/계정/결제 앱 운영 측과 대화할 때 “앱 변조 방어”와 “사용자 coercion risk”를 구분해 설명할 수 있어야 한다.

## Risks / compatibility questions

- Trust Insights entitlement가 필요한 앱에서 보호 도구가 signing/capability 설정을 건드리지 않는가? **확인 필요**.
- 앱 risk engine이 Trust Insights feedback requirement를 운영할 수 있는가?
- unknown/medium/high 결과를 user blocking으로 바로 쓰지 않도록 tool guidance가 있는가?
- privacy/user control 요구사항이 사용자 UX와 충돌하지 않는가?

## Study questions from this session

1. 우리 스터디 범위의 threat model은 app tampering 중심인지, fraud/risk signal integration까지 포함하는지 알고 싶다.
2. entitlement/capability가 필요한 Apple security framework와 보호 도구가 충돌한 사례가 있는가?
3. 대상 앱이 Trust Insights 같은 Apple risk signal을 쓰는 경우 보안 도구 적용 전후 signing/provisioning 검증 checklist가 있는가?
4. app integrity signal과 social engineering risk signal을 도입 환경에서 어떻게 구분해서 설명하는가?

## Must-watch chapters

- 2:35 — Generating insights: Trust Insights가 해결하려는 coercion/social engineering 문제.
- 6:50 — Feedback requirements: entitlement, parameter pack, `InsightEvaluator`, operation category.
- 9:25 — Privacy: required feedback과 privacy architecture.
- 영상 전체 필수는 아니며 transcript 우선. 사용자 고지/UX 흐름이 중요하면 해당 구간 영상 확인.

## Source notes

- Apple Developer session page/transcript: https://developer.apple.com/videos/play/wwdc2026/379/
- Apple session 기준 확인한 항목: Trust Insights iOS 27 framework, entitlement, client-side Swift API, `InsightEvaluator`, operation categories, `IsLikelyBeingCoachedInsight`, feedback requirements, privacy framing.
