# Agentic feature security 이해하기

Source: https://developer.apple.com/videos/play/wwdc2026/347/

## 1. 한 문장으로 먼저 잡기

Agentic feature security는 “앱이 모델이나 agent를 통해 context를 읽고 action을 수행할 때, 믿으면 안 되는 입력이 위험한 행동으로 이어지지 않게 하는 설계”다.

중요한 점은 이 문제가 app binary 변조와 다른 계층이라는 것이다. 앱이 정상이고 서명도 정상이어도, agent가 untrusted content 안의 instruction을 믿으면 문제가 생길 수 있다.

## 2. 기존 앱 보안과 무엇이 다른가

전통적인 mobile app security는 주로 다음을 본다.

- binary 변조
- runtime tampering
- reverse engineering
- API abuse
- signing/entitlement 문제

Agentic feature에서는 여기에 다른 질문이 추가된다.

> 앱이 LLM/agent를 통해 외부 context를 읽고, tool/action을 호출하고, 사용자를 대신해 side effect가 있는 행동을 할 수 있는가?

이때 문제 상황에서는 앱 binary를 바꾸지 않고도 외부 content에 의도하지 않은 instruction을 숨길 수 있다.

```text
정상 앱
  └─ 외부 context 읽기
      └─ context 안의 숨은 instruction
          └─ agent가 이를 instruction처럼 처리
              └─ risky action 수행 가능
```

## 3. 핵심 문제: indirect prompt injection

직접 prompt injection은 사용자가 의도하지 않은 명령을 직접 입력하는 경우다.

Indirect prompt injection은 앱이나 agent가 읽는 외부 content 안에 의도하지 않은 instruction이 들어 있는 경우다.

```text
웹페이지 / 이메일 / 문서 / tool result
  └─ 숨겨진 instruction 포함
      └─ agent가 이를 신뢰하고 action 수행
```

이 문제는 anti-tamper만으로 해결되지 않는다. 앱은 정상이고 binary도 변조되지 않았지만, agent가 신뢰하면 안 되는 context를 신뢰했기 때문이다.

## 4. 먼저 inventory해야 하는 것

### 4.1 Untrusted context source

agent가 읽는 context 중 외부 출처를 분리해야 한다.

- 웹페이지
- 이메일
- 문서
- tool result
- 외부 API 응답
- 사용자가 붙여 넣은 content

이 목록은 “모델이 읽는 데이터 목록”이 아니라 “instruction처럼 오해되면 안 되는 데이터 목록”이다.

### 4.2 Risky action

Agentic app에서는 “무슨 action을 할 수 있는가”가 검토 표면가 된다.

예:

- 돈 이동
- 메시지 전송
- 파일 삭제
- 설정 변경
- 민감 데이터 조회
- 외부 서버로 데이터 전송

따라서 App Intents나 tool action을 설계할 때 side effect와 권한 수준을 분류해야 한다.

## 5. Mitigation을 이해하는 방식

| mitigation | 의미 | 확인 질문 |
|---|---|---|
| untrusted context boundary | agent가 읽는 정보 중 믿으면 안 되는 출처를 표시 | 외부 content가 instruction으로 취급되지 않는가? |
| instruction hierarchy | 더 높은 우선순위의 app/developer policy가 유지됨 | 외부 content가 policy를 덮어쓰지 못하는가? |
| user confirmation | side effect가 큰 action 전에 사용자가 명시적으로 확인 | 사용자가 무엇을 승인하는지 볼 수 있는가? |
| authentication/device unlock | 민감 action 전에 기기 인증 상태 확인 | lock 상태나 user presence를 확인하는가? |
| least privilege | action이 필요한 최소 권한만 갖도록 설계 | action scope가 과도하지 않은가? |
| logging/review | agent action을 사후 검토 가능하게 남김 | 민감 정보 노출 없이 흐름을 재현할 수 있는가? **확인 필요** |

여기서 confirmation은 단순히 “확인 버튼 하나”가 아니다. 사용자가 어떤 action과 어떤 요청 내용을 승인하는지 이해할 수 있어야 한다.

## 6. Foundation Models / App Intents와 연결하기

Apple 세션 기준 agentic feature는 Foundation Models framework나 App Intents와 연결될 수 있다.

```text
Foundation Models
  └─ 앱 안의 model 기반 경험

App Intents
  └─ 앱 action을 system/Siri/agentic flow에 노출하는 경로

Agentic security
  └─ context boundary와 action checkpoint를 설계하는 계층
```

세부 API 이름, entitlement, platform availability는 이 understanding 문서의 범위를 넘으므로 session transcript/API docs로 **확인 필요**다. Foundation Models 자체의 학습 관점은 [`foundation-models.md`](foundation-models.md), 실행 관찰 관점은 [`agentic-instruments.md`](agentic-instruments.md)에서 분리해 둔다.

## 7. App Attest와 같은 문제가 아니다

App Attest는 서버가 앱 인스턴스와 요청의 신뢰도를 판단하도록 돕는다.

Agentic security는 정상 앱 내부에서 model/context/action 흐름이 안전한지 보는 문제다.

| 구분 | App Attest | Agentic feature security |
|---|---|---|
| 주된 질문 | 이 요청이 정상 앱/기기/key에서 왔는가? | agent가 믿으면 안 되는 context를 믿고 action하지 않는가? |
| 주요 위치 | 앱 + Apple service + 서버 | 앱 설계 + model context + App Intents/action + 사용자 확인 |
| 문제/오류 계층 | 변조 앱, replay, re-signing 등 | indirect prompt injection, risky action, context 혼동 |
| 최종 판단 | 서버 검증과 risk policy | action policy, confirmation/authentication, context handling |

따라서 둘은 보완 관계다. App Attest가 있더라도 agentic action 설계는 별도로 검토해야 한다.

## 8. 보안/toolchain 관점의 의미

이 세션은 LLVM Pass나 Xcode build와 직접 연결되는 세션은 아니다.

하지만 modern app threat model이 넓어지고 있음을 보여준다.

보안 도구가 app integrity를 다룬다고 해도, 대상 앱이 Foundation Models/App Intents 기반 feature를 도입하면 다음 질문이 생긴다.

- 어떤 action surface가 생기는가?
- action이 side effect를 갖는가?
- untrusted context를 action decision에 쓰는가?
- user confirmation이 필요한 지점은 어디인가?
- 보호 적용 후 App Intents metadata나 action routing이 바뀌지 않는가? **추론 / 확인 필요**
- report나 checklist가 agentic feature risk를 별도 계층으로 설명해야 하는가? **추론**

## 9. 실패와 예외를 어떻게 봐야 하나

Agentic mitigation은 사용성을 해칠 수 있으므로 모든 action을 같은 방식으로 막는 접근은 좋지 않다.

먼저 action risk를 나누어야 한다.

```text
낮은 위험:
요약, 분류, 초안 생성, 추천 표시

중간 위험:
사용자 데이터 조회, 외부 데이터와 결합, 저장 전 제안

높은 위험:
전송, 결제, 삭제, 권한 변경, 민감 정보 공유
```

높은 위험 action일수록 confirmation, authentication, server-side authorization, audit trail을 조합해야 한다. 구체 threshold는 앱 정책과 Apple guidance로 **확인 필요**다.

## 10. 세션을 다시 볼 때 집중할 장면

- indirect prompt injection threat model
- untrusted context와 trusted instruction을 구분하는 설명
- risky action inventory를 만드는 방식
- Foundation Models 기반 feature에서 mitigation을 적용하는 부분
- App Intents action과 security checkpoint를 연결하는 부분
- user confirmation / authenticated device state가 필요한 예시

## 11. 내가 이해했는지 확인하는 질문

1. indirect prompt injection은 왜 binary tampering 없이도 발생하는가?
2. App Intents action surface는 왜 보안 review 대상이 되는가?
3. user confirmation은 어떤 action에서 필요한가?
4. agentic security와 App Attest는 서로 어떤 계층이 다른가?
5. untrusted context boundary가 없으면 model output과 action decision 사이에서 어떤 문제가 생기는가?
6. 보호 도구의 threat model 문서에는 agentic feature risk를 어디까지 포함해야 하는가? **추론 / 확인 필요**

## 12. 이 세션에서 외우지 않아도 되는 것

처음 볼 때는 Foundation Models/App Intents API 전체를 외울 필요가 없다. 먼저 다음 구조만 잡으면 된다.

```text
untrusted context
  = instruction처럼 취급되면 안 되는 외부 입력

risky action
  = side effect가 있어 confirmation/authentication이 필요한 행동

agentic mitigation
  = context boundary + instruction hierarchy + user checkpoint + least privilege

app integrity와의 관계
  = 정상 앱에서도 agentic risk는 별도로 생길 수 있음
```
