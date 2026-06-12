# Secure your app: mitigate risks to agentic features

- URL: https://developer.apple.com/videos/play/wwdc2026/347/
- Duration: 약 22분
- Category: App security / Agentic features / Foundation Models / App Intents
- Priority: A
- Review mode: Transcript first + selected security chapters video
- Last updated: 2026-06-12

## Why this matters to this study

- Apple session 기준 agentic feature는 LLM이 context를 읽고 action/tool을 호출하는 구조이므로, 기존 앱 보안과 다른 risk가 생긴다.
- 보안 스터디 관점에서는 indirect prompt injection, untrusted context, risky actions, user confirmation, authenticated device state 같은 mitigation 개념을 이해해야 한다.
- 이 세션은 compiler/toolchain 직접 영향은 낮지만, 최신 iOS 앱 threat modeling을 이해하는 데 중요하다.

## 5-line summary

1. Apple session 기준 agentic feature는 Foundation Models framework로 직접 agent를 만들거나 App Intents로 Siri와 연동하는 방식으로 구현될 수 있다.
2. 핵심 신규 risk는 indirect prompt injection이다. 모델에 제공되는 추가 context나 tool result 안에 악의적 instruction이 포함되어 control flow를 바꿀 수 있다.
3. Threat modeling은 untrusted context source와 side-effect가 있는 action/tool을 식별하는 것에서 시작한다.
4. Mitigation은 context handling, instruction hierarchy/spotlighting, risky action에 대한 user confirmation, device unlock/authentication 요구 등을 포함한다.
5. App Intents / Foundation Models 사용 시 agent execution 안에 security checkpoint를 넣는 설계가 필요하다.

## New APIs / tools / frameworks

| Name | Type | Notes | Relevance |
|---|---|---|---|
| Foundation Models framework | App framework | app이 자체 agentic experience를 만들 수 있는 경로로 설명. | 대상 앱의 AI attack surface 이해. |
| App Intents | App framework | Siri와 app action 연동. | action permission/side effect threat model. |
| Indirect prompt injection | Threat pattern | context/tool result에 instruction을 숨겨 model control flow를 바꾸는 공격. | agentic app security 핵심. |
| User confirmation checkpoints | Mitigation pattern | side effect가 큰 action 전 human confirmation. | 고위험 action 방어. |
| Device authentication/unlock gating | Mitigation pattern | lock screen 등에서 위험 action 제한. | user presence/authentication 요구. |

## Toolchain / compiler / build implications

- 직접적인 compiler/build/linker 영향은 없다.
- App Intents metadata, Foundation Models integration, app action surface가 늘어나면 security review 대상이 source/binary protection만이 아니라 “agent가 호출 가능한 action 목록”까지 확장된다. **추론**.
- protection tooling이 static analysis/report를 제공한다면 App Intents/action capability inventory를 함께 표시할 수 있는지 검토할 수 있다. **추론 / 확인 필요**.

## Security / anti-tamper / integrity implications

- 이 세션은 app tampering보다 agentic behavior risk를 다룬다.
- 중요한 관점은 “정상 앱, 정상 모델, 정상 API”라도 untrusted context가 action을 오도할 수 있다는 점이다.
- side-effect action은 confirmation, authenticated state, limited capability, context trust boundary로 보호해야 한다.
- App Attest/anti-tamper와 달리 agentic risk는 서버/app integrity만으로 해결되지 않는다.

## Security/toolchain impact hypothesis

> 추론: 모바일 앱 보호 보안 도구의 핵심이 난독화/무결성이라도, 대상 앱이 Foundation Models/App Intents를 도입하면 threat model 상담 범위가 넓어진다. 보안 도구가 직접 agentic mitigation을 제공하지 않더라도, “우리 보호 기능이 막는 것”과 “agentic feature 설계에서 별도로 막아야 하는 것”을 구분해 설명할 수 있어야 한다.

## Risks / compatibility questions

- 대상 앱의 App Intents/action surface를 보호 적용 전후에 inventory할 수 있는가? **확인 필요**.
- agentic feature가 민감 API나 결제/계정 action을 호출할 때 user confirmation policy가 있는가?
- untrusted context source를 식별하는 정적/동적 분석 지원이 가능한가? **추론 / 확인 필요**.
- lock screen에서 reachable한 agent action과 authenticated device state 요구사항을 어떻게 테스트하는가?

## Study questions from this session

1. 우리 보안 도구의 threat model 문서에 LLM/agentic feature risk가 포함되어 있는가?
2. App Intents나 Foundation Models를 쓰는 대상 앱에서 보호 적용 시 추가로 봐야 할 action surface가 있는가?
3. indirect prompt injection처럼 앱 무결성과 다른 계층의 위험은 도입 환경에서 어떻게 안내하는가?
4. side-effect action에 대한 user confirmation/authentication checkpoint를 보안 가이드에 포함하는가?

## Must-watch chapters

- 6:32 — Threat modeling: untrusted context와 risky actions 식별.
- 11:56 — Implementing mitigations: context/action mitigation 구조.
- 12:03 — Foundation Models: agentic app을 안전하게 만드는 concrete tools.
- 17:55 — App Intents: security checkpoints와 App Intents 연결.
- 전체 영상 필수는 아니지만 threat model diagram과 mitigation chapter는 직접 시청 권장.

## Source notes

- Apple Developer session page/transcript: https://developer.apple.com/videos/play/wwdc2026/347/
- Apple session 기준 확인한 항목: Foundation Models, App Intents, indirect prompt injection, untrusted context, action side effects, user confirmation, device authentication/unlock gating, security checkpoints.
