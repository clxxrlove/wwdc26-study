# Agentic app Instruments 이해하기

Source: https://developer.apple.com/videos/play/wwdc2026/243/

## 1. 한 문장으로 먼저 잡기

Agentic app Instruments는 agentic feature가 실제로 실행될 때의 흐름을 관찰하고, 지연·오류·tool/action 호출 같은 문제를 재현해서 이해하는 진단 축으로 보면 된다.

이 repo의 `outputs/watch-priority.md`는 이 세션을 “agentic feature 보안 이슈 재현/관측에 보조적으로 유용”한 B priority로 둔다.

세부 Instruments template 이름, trace event, UI 항목은 아직 transcript note가 없으므로 **확인 필요**다.

## 2. 왜 보안 스터디에서 보나

Agentic security는 설계 문서만으로 끝나지 않는다. 설계 계층은 [`agentic-security.md`](agentic-security.md), 기반 framework 맥락은 [`foundation-models.md`](foundation-models.md)에서 따로 본다.

```text
설계에서 기대한 흐름:
사용자 요청 → trusted instruction → context 분리 → 안전한 action 후보 → confirmation → 실행

실제 앱에서 확인할 흐름:
어떤 context가 들어갔는가?
어떤 tool/action이 호출되었는가?
어디서 지연이나 실패가 생겼는가?
confirmation이 정말 action 전에 있었는가?
```

Instruments는 이 두 흐름이 같은지 확인하는 관찰 도구로 이해하면 된다.

## 3. agentic feature에서 관찰해야 할 것

### 3.1 Context 흐름

Indirect prompt injection은 보통 “어떤 외부 content가 model context로 들어갔는가”에서 시작한다.

따라서 agentic app을 debug할 때는 다음을 확인해야 한다.

- model에 전달된 context의 출처
- trusted instruction과 untrusted context가 섞이는 지점
- tool result가 다시 model 입력으로 들어가는지
- 외부 content가 action decision에 영향을 주는지

구체적으로 Instruments가 이 항목들을 어떤 UI로 보여주는지는 **확인 필요**다.

### 3.2 Action/tool 호출 흐름

Agentic feature에서 action surface는 검토 표면가 될 수 있다.

```text
model 판단
  └─ action 후보 선택
      └─ user confirmation/authentication checkpoint
          └─ App Intent 또는 app 내부 action 실행
```

관찰해야 할 질문은 다음이다.

1. 어떤 action이 호출되었는가?
2. action 호출 전 확인 UI가 있었는가?
3. action 요청 내용에 untrusted context가 섞였는가?
4. 실패나 retry가 action을 중복 실행하지 않는가? **추론 / 확인 필요**

### 3.3 Latency와 responsiveness

Agentic feature는 model 호출, context 준비, tool call, UI update가 이어질 수 있다.

보안 도구 관점에서는 보호 적용 후 runtime overhead가 agentic flow의 지연을 키우는지 볼 수 있다. 이것은 세션 제목과 Instruments 역할에서 나온 **추론**이며, 실제 측정 항목은 **확인 필요**다.

## 4. Instruments를 보안 도구처럼 오해하지 않기

Instruments는 기본적으로 관찰/진단 도구다. 보안 정책을 대신 결정하는 도구로 보면 안 된다.

| 구분 | 역할 |
|---|---|
| Agentic security 설계 | untrusted context, risky action, confirmation 정책을 정함 |
| App/runtime code | 정책을 실제 흐름에 적용함 |
| Instruments | 실제 실행 흐름과 성능/오류를 관찰함 |
| 서버/backend | 민감 action의 authorization/risk policy를 적용할 수 있음 |

따라서 Instruments에서 이상 흐름을 봤다면, 수정은 policy, app code, App Intents 설계, backend policy 중 맞는 위치에서 해야 한다.

## 5. App Attest / anti-tamper와의 차이

App Attest는 서버가 “이 요청이 정상 앱/기기/key에서 왔는가”를 판단하는 계층이다.

Agentic Instruments는 “정상 앱 안에서 agentic flow가 어떻게 실행되었는가”를 관찰하는 계층에 가깝다.

```text
App Attest 질문:
이 앱 인스턴스와 요청을 믿을 수 있는가?

Agentic Instruments 질문:
이 앱 인스턴스 안에서 context/action 흐름이 기대대로 갔는가?
```

둘은 서로 대체하지 않는다.

## 6. 보안/toolchain 관점의 의미

이 세션은 compiler나 linker 기능 자체를 설명하는 세션은 아닐 가능성이 높다. **추론 / 확인 필요**

하지만 보호 도구 검증에는 다음 방식으로 연결될 수 있다.

- 보호 적용 전후 agentic flow latency 비교
- model/tool/action 호출 중 crash, hang, timeout 확인
- App Intents action이 보호 적용 후에도 호출되는지 확인
- confirmation/authentication checkpoint가 우회되거나 순서가 바뀌지 않는지 재현
- 로그/trace artifact에 민감 정보가 남는지 검토 **추론 / 확인 필요**

## 7. 세션을 다시 볼 때 집중할 장면

이 repo에는 아직 이 세션 transcript note가 없으므로 아래는 watch checklist다.

- Instruments가 agentic app experience를 어떤 단위로 보여주는지
- model request/response, tool call, App Intent, UI update가 trace에서 연결되는지
- 실패, retry, cancellation, timeout을 어떻게 확인하는지
- performance issue와 logical flow issue를 어떻게 구분하는지
- trace/export artifact에 민감 context가 포함될 수 있는지

## 8. 내가 이해했는지 확인하는 질문

1. agentic feature의 보안 설계가 맞는지 왜 실행 trace로 확인해야 하는가?
2. untrusted context가 action decision에 영향을 주었는지 어떤 흐름을 보면 알 수 있는가?
3. confirmation/authentication checkpoint는 trace에서 어느 위치에 있어야 하는가?
4. Instruments가 App Attest나 server-side validation을 대체할 수 없는 이유는 무엇인가?
5. 보호 적용 후 agentic feature regression을 볼 때 latency, crash, action ordering 중 무엇을 우선 확인해야 하는가?

## 9. 이 세션에서 외우지 않아도 되는 것

처음 볼 때는 Instruments UI의 모든 pane 이름을 외우기보다 다음 구조를 잡으면 된다.

```text
agentic trace
  = context 입력 + model 판단 + tool/action 호출 + UI/사용자 확인 + 결과

debug 목표
  = 설계한 security checkpoint가 실제 실행 순서에서도 유지되는지 확인

performance 목표
  = 보호 적용이나 agentic flow가 지연/hang/regression을 만들지 않는지 확인
```

구체 trace 항목과 template 이름은 Apple session 또는 docs로 **확인 필요**다.
