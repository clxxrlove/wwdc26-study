# Trust Insights 이해하기

Source: https://developer.apple.com/videos/play/wwdc2026/379/

## 1. App Attest와 다른 문제를 다룬다

Trust Insights는 app binary가 변조되었는지 확인하는 기능으로 이해하면 안 된다. 이 세션의 핵심은 다른 곳에 있다.

> 정상 앱, 정상 기기, 정상 로그인 사용자라도 social engineering이나 coercion 때문에 위험한 행동을 할 수 있다.

즉 App Attest가 “요청을 만든 앱/기기가 신뢰 가능한가?”에 가깝다면, Trust Insights는 “이 사용자가 지금 자유롭고 정상적인 의사결정을 하고 있는가?”에 가까운 risk signal이다.

## 2. 왜 mobile app security 관점에서 봐야 하나

앱 보안을 binary integrity만으로 보면 다음 위험을 놓친다.

- 사용자가 사기범의 지시에 따라 송금하는 상황
- 계정 복구나 인증 과정에서 누군가에게 조종되는 상황
- 정상 앱 기능이 사회공학 공격에 이용되는 상황

Trust Insights는 이런 risk를 앱이 고려할 수 있게 하는 별도 계층이다.

## 3. 이해 포인트

- entitlement/capability가 필요한 framework다.
- on-device processing, data minimization, user control 같은 privacy boundary가 중요하다.
- 결과값은 risk signal이지 단독 판정 근거가 아니다.
- operation category에 따라 어떤 행동의 risk를 평가하는지 달라진다.

## 4. App Attest와 비교

| 구분 | App Attest | Trust Insights |
|---|---|---|
| 주된 질문 | 이 요청은 정상 앱/기기에서 왔는가? | 사용자가 coercion/social engineering 상태일 가능성이 있는가? |
| 계층 | app/device/server trust | user risk/context signal |
| 대표 위험 | modified app, re-signing, replay | scam, coaching, coercion |
| 처리 방식 | server validation 중심 | privacy-preserving risk evaluation 중심 |

## 5. 이해 확인 질문

1. Trust Insights가 app tampering 방어가 아닌 이유는 무엇인가?
2. App Attest와 Trust Insights signal을 같은 risk score에 넣는다면 어떤 점을 구분해야 하는가?
3. unknown/medium/high 같은 risk 결과를 단독 차단 기준으로 쓰면 왜 위험할 수 있는가?
