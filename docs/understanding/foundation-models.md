# Foundation Models framework 이해하기

Source: https://developer.apple.com/videos/play/wwdc2026/241/

## 1. 한 문장으로 먼저 잡기

Foundation Models framework는 앱이 Apple platform 안에서 model 기반 기능을 만들 때 쓰는 기반 framework로 이해하면 된다.

이 문서에서 중요한 관점은 “어떤 API를 외우는가”가 아니라, **모델이 앱 context를 읽고 action 판단에 영향을 줄 때 보안 검토 범위가 어디까지 넓어지는가**다.

세부 API, 지원 model 종류, 실행 위치, entitlement, privacy boundary는 아직 이 repo에 transcript note가 없으므로 **확인 필요**다.

## 2. 왜 보안 스터디에서 보나

이 세션은 `outputs/watch-priority.md`에서 B priority로 분류되어 있다.

이유는 Foundation Models 자체가 app integrity나 compiler pass 세션은 아니지만, `Secure your app: mitigate risks to agentic features` 세션의 보조 맥락이기 때문이다. 이 repo 안에서는 [`agentic-security.md`](agentic-security.md)와 함께 읽으면 threat model 계층이 분리된다.

즉, Foundation Models를 먼저 이렇게 보면 된다.

```text
Foundation Models
  └─ 앱 내부 agentic feature의 기반이 될 수 있음
      └─ context를 읽음
      └─ model output으로 UI나 action 판단을 도움
      └─ App Intents / tool action과 결합될 수 있음
          └─ indirect prompt injection / risky action 검토가 필요해짐
```

여기서 보안 질문은 “모델이 똑똑한가?”가 아니라 “모델에게 무엇을 읽게 하고, 모델의 판단을 어디에 쓰는가?”다.

## 3. 먼저 나누어야 하는 세 가지 경계

### 3.1 Trusted instruction과 untrusted context

Agentic feature에서 가장 먼저 나눌 것은 instruction과 context다.

| 구분 | 예 | 보안 관점 |
|---|---|---|
| trusted instruction | 앱 개발자가 정한 system/developer policy | action 결정의 기준이 되어야 함 |
| user input | 사용자가 직접 입력한 요청 | 의도 확인이 필요할 수 있음 |
| untrusted context | 웹페이지, 이메일, 문서, tool result, 외부 데이터 | 의도하지 않은 instruction이 숨어 있을 수 있음 |

Foundation Models를 쓰는 앱은 model에 여러 context를 줄 수 있다. 이때 untrusted context 안의 문장을 instruction처럼 처리하면 indirect prompt injection 문제가 생길 수 있다.

### 3.2 Suggestion과 action

모델이 추천 문장을 보여주는 것과, 모델 판단으로 실제 action을 실행하는 것은 위험도가 다르다.

```text
낮은 위험:
모델이 텍스트 요약/추천을 생성

높은 위험:
모델 판단이 메시지 전송, 결제, 설정 변경, 데이터 삭제 같은 action으로 연결
```

따라서 Foundation Models 기반 기능을 검토할 때는 “model output이 어디로 흘러가는가?”를 봐야 한다.

### 3.3 Local app feature와 server/backend policy

Foundation Models가 앱 안에서 동작하더라도, 모든 보안 판단이 앱 안에서 끝난다고 보면 위험하다.

- 민감 action은 서버 정책과 함께 검토해야 하는가? **확인 필요**
- model output이 backend API 요청 내용에 영향을 주는가?
- App Attest 같은 app integrity signal과 별도 계층으로 다루어야 하는가?

App Attest는 서버가 앱/기기/key 신뢰를 판단하는 계층이고, Foundation Models risk는 agent가 context/action을 어떻게 다루는지의 계층이다. 둘은 같은 문제가 아니다.

## 4. Foundation Models에서 믿는 것과 믿지 않는 것

| 대상 | 바로 믿어도 되는가? | 이유 |
|---|---:|---|
| 앱 개발자가 작성한 고정 policy | 상대적으로 신뢰 | 코드/설계의 일부이지만 runtime 변조와 배포 상태는 별도 검토 필요 |
| 외부 문서/웹/email/tool result | 직접 믿지 않음 | instruction이 숨어 있을 수 있음 |
| model output | 직접 믿지 않음 | 입력 context와 policy 해석 결과이며, 사실/권한 판단의 최종 근거가 아님 |
| 사용자 확인 | 위험 action의 중요한 checkpoint | 단, UI가 무엇을 확인시키는지 명확해야 함 |
| 서버 정책 | 최종 policy 근거가 될 수 있음 | 민감 action은 backend authorization과 함께 봐야 함 |

핵심은 model output을 “권위 있는 판단”으로 보지 않는 것이다. model은 reasoning helper일 수 있지만, 권한과 side effect는 앱/서버 policy가 통제해야 한다.

## 5. 보안/toolchain 관점의 의미

Foundation Models 세션은 LLVM pass, linker, build phase와 직접 연결되는 세션은 아니다. **확인 필요**

하지만 보안 도구나 toolchain 검토에서는 다음 질문이 추가된다.

1. 대상 앱이 Foundation Models를 도입하면 새로운 action surface가 생기는가?
2. model에게 제공되는 context 중 외부 출처가 있는가?
3. model output이 보안 판단, 권한 판단, 결제/계정/삭제 action에 영향을 주는가?
4. 보호 적용 후에도 App Intents metadata, action routing, entitlement, privacy prompt가 정상 동작하는가? **추론 / 확인 필요**
5. 정적 report가 있다면 agentic feature inventory를 포함할 수 있는가? **추론 / 확인 필요**

여기서 “보호 기능이 Foundation Models를 막는다”가 아니라, “대상 앱의 threat model이 넓어진다”로 이해해야 한다.

## 6. Secure agentic features 세션과 연결하기

[`agentic-security.md`](agentic-security.md)는 Foundation Models/App Intents 기반 feature의 security checkpoint를 직접 다룬다. 실행 흐름을 관찰하는 관점은 [`agentic-instruments.md`](agentic-instruments.md)에서 따로 본다.

Foundation Models 문서를 읽을 때는 다음 연결을 기억하면 된다.

```text
Foundation Models = agentic 기능을 만들 수 있는 기반
Agentic security = 그 기능이 untrusted context와 risky action을 다룰 때 필요한 방어 설계
```

따라서 Foundation Models 자체를 학습할 때도 API 사용법보다 먼저 다음을 묻는 편이 좋다.

- model이 어떤 context를 받는가?
- 그 context는 trusted인가, untrusted인가?
- output은 단순 표시인가, action 실행으로 이어지는가?
- action 전에 user confirmation/authentication이 필요한가?
- 로그나 review trail이 남는가? **확인 필요**

## 7. 세션을 다시 볼 때 집중할 장면

이 repo에는 아직 이 세션 transcript note가 없으므로 아래는 watch checklist다.

- Foundation Models가 앱 코드 안에서 어떤 구성 요소로 소개되는지
- model에게 context를 전달하는 방식
- tool/action/App Intents와 연결되는 장면이 있는지
- privacy, on-device/server execution, entitlement, data handling 설명
- error/fallback/availability 처리
- 보안 세션에서 말한 indirect prompt injection mitigation과 연결되는 API가 있는지

## 8. 내가 이해했는지 확인하는 질문

1. Foundation Models 기반 기능에서 untrusted context는 어디서 들어오는가?
2. model output이 사용자에게 보여지는 것과 action 실행에 쓰이는 것은 왜 위험도가 다른가?
3. App Attest가 해결하는 app integrity 문제와 Foundation Models의 agentic risk는 어떤 계층이 다른가?
4. side-effect action 앞에 user confirmation이나 authentication이 필요한 기준은 무엇인가?
5. 대상 앱 보호 도구가 Foundation Models 자체를 몰라도, 왜 action surface inventory는 필요할 수 있는가? **추론**

## 9. 이 세션에서 외우지 않아도 되는 것

처음 볼 때는 class/function 이름 전체를 외우는 것보다 다음 구조를 잡는 편이 중요하다.

```text
model framework
  = 앱 기능을 만드는 기반

untrusted context
  = 모델 판단을 오도할 수 있는 입력

model output
  = 권한 판단의 최종 근거가 아니라 검토 대상

risky action
  = confirmation/authentication/policy checkpoint가 필요한 지점
```

세부 API, platform availability, entitlement, privacy boundary는 세션 transcript나 Apple documentation으로 **확인 필요**다.
