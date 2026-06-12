# MetricKit 이해하기

Source: https://developer.apple.com/videos/play/wwdc2026/222/

## 1. 한 문장으로 먼저 잡기

MetricKit은 “개발 중 trace가 아니라, **사용자 환경에서 앱이 실제로 겪은 성능·진단 신호를 모아 post-launch 품질을 보는 framework**”로 이해하면 된다.

보안/toolchain 관점에서는 이렇게 연결된다.

> 보호 적용 후 field에서 hang, crash, battery, disk write, launch time 같은 신호가 나빠졌는지 확인하고, local Instruments 재현으로 이어가는 관측 축이다.

## 2. 왜 필요한가: lab에서 못 본 문제가 field에서 보인다

Instruments와 Device Hub는 local 재현에 강하다. 하지만 실제 사용자는 더 다양한 조건을 가진다.

1. device model과 OS version이 다양하다.
2. app data와 cache가 오래 누적되어 있다.
3. network와 battery 상태가 다르다.
4. 특정 화면이나 feature 사용 패턴이 예측과 다르다.
5. crash가 아니어도 hang, disk write, battery drain, launch regression이 문제일 수 있다.

MetricKit은 이런 post-launch 신호를 앱 품질 지표로 보는 데 쓰인다.

## 3. MetricKit을 세 층으로 이해하기

### 3.1 Metrics: 사용자 경험을 숫자로 본다

MetricKit의 첫 층은 성능/자원 사용 지표다.

```text
field usage
  └─ MetricKit metrics
      ├─ launch / responsiveness 관련 신호
      ├─ CPU / memory / battery 관련 신호
      ├─ disk write / storage 관련 신호
      └─ app health trend
```

정확한 WWDC26 “new MetricKit” 항목별 변화는 세션 확인이 필요하다. **확인 필요**

### 3.2 Diagnostics: 문제가 있었던 순간을 설명한다

Metric은 “나빠졌다”를 알려주고, diagnostics는 “무슨 일이 있었는지”를 더 설명하는 층으로 이해하면 된다.

예를 들어 hang이나 crash 계열 신호는 local 재현 없이도 field issue의 우선순위를 정하는 데 도움이 된다. 단, 세부 payload schema와 iOS 27 변경점은 Apple 문서/세션으로 **확인 필요**.

### 3.3 Feedback loop: local 재현과 수정으로 돌아간다

MetricKit은 원인을 자동으로 고쳐 주지 않는다.

```text
MetricKit field signal
  └─ issue 우선순위 결정
      └─ Device Hub로 조건 재현
          └─ Instruments로 trace 분석
              └─ 수정 후 Xcode Cloud/test로 회귀 방지
```

따라서 MetricKit은 운영 신호이고, Instruments는 원인 분석 도구이며, Xcode Cloud는 반복 검증 gate로 보는 것이 이해하기 쉽다. **추론**

## 4. MetricKit에서 믿는 것과 조심할 것

| 대상 | 믿는가? | 이유 |
|---|---:|---|
| field aggregate trend | 중요한 근거 | 실제 사용자 환경에서 나온 신호다. |
| 단일 payload 또는 작은 표본 | 제한적으로 신뢰 | 표본 크기와 조건 편향을 확인해야 한다. |
| crash/hang diagnostics | 우선순위 근거 | 원인 후보를 좁히지만 local 재현이 필요할 수 있다. |
| local benchmark만 통과 | 불충분 | field regression을 놓칠 수 있다. |
| metric 변화의 즉시 원인 단정 | 위험 | release, device mix, feature usage 변화가 섞일 수 있다. |

## 5. 보안/toolchain 관점의 핵심 지표

### 5.1 Hang과 responsiveness

보호 적용 후 user-visible hang이 늘면 단순 CPU 비용보다 심각할 수 있다. hang은 main thread blocking, lock contention, synchronous IO, initialization path와 연결될 수 있다. **추론**

### 5.2 Battery와 CPU

runtime check, integrity validation, encryption/decryption, logging이 반복되면 CPU와 battery에 영향을 줄 수 있다. 실제 보호 방식은 **확인 필요**이므로, 문서에서는 가능한 관측 항목으로만 둔다.

### 5.3 Disk writes와 storage

Xcode 27 Organizer 노트 기준 storage, disk writes 같은 metric goal이 중요해졌다. MetricKit field signal과 Organizer 지표는 보호 적용 후 binary size, cache, report/log 생성 비용을 보는 데 연결될 수 있다. **추론 / 확인 필요**

### 5.4 Crash와 symbolication

MetricKit diagnostics를 해석하려면 symbolication이 중요하다. 보호 적용 후 symbol, dSYM, stack frame readability가 바뀐다면 crash 원인 분석 품질이 낮아질 수 있다. **추론 / 확인 필요**

## 6. MetricKit과 Organizer를 함께 보는 이유

Xcode 27 노트 기준 Organizer는 redesigned Overview, storage metric, broader animation hitches metric, Metric Goals, agent-powered recommendation을 제공한다.

MetricKit은 앱 안팎의 metric/diagnostic collection framework로 이해하고, Organizer는 그 신호를 개발자가 triage하는 Xcode UI 축으로 이해하면 된다. 둘의 정확한 데이터 경계와 WWDC26 변경점은 **확인 필요**.

중요한 것은 다음 흐름이다.

```text
post-launch signal
  ├─ MetricKit payload / diagnostics
  └─ Organizer metrics / goals
      └─ regression 후보 선정
          └─ local reproduction + trace
```

## 7. 실패와 예외를 어떻게 봐야 하나

MetricKit 신호는 강력하지만 해석에 주의가 필요하다.

1. release version별로 비교해야 한다.
2. device/OS mix 변화가 metric을 바꿀 수 있다.
3. 사용자 수나 표본이 작으면 trend가 흔들릴 수 있다.
4. 보호 기능 외의 feature change가 같은 release에 들어갔을 수 있다.
5. privacy와 aggregation 정책 때문에 모든 개별 사건을 볼 수 있는 것은 아니다. 정확한 정책은 **확인 필요**.

따라서 MetricKit은 “차단 버튼”이 아니라 “field에서 우선순위를 정하는 신호”로 보는 편이 안전하다.

## 8. 세션을 다시 볼 때 집중할 장면

- “new MetricKit”에서 추가/변경된 payload나 diagnostics가 무엇인지
- hang/responsiveness 관련 신호를 어떻게 설명하는지
- Organizer 또는 Metric Goals와 연결되는 부분
- privacy/aggregation/availability 조건
- local profiling로 돌아가는 troubleshooting 흐름

## 9. 내가 이해했는지 확인하는 질문

1. MetricKit은 Instruments와 어떤 점에서 다른가?
2. field metric이 나빠졌을 때 바로 보호 기능 때문이라고 단정하면 안 되는 이유는 무엇인가?
3. hang, CPU, battery, disk write는 각각 어떤 종류의 문제를 암시하는가?
4. symbolication이 MetricKit diagnostics 해석에 왜 중요한가?
5. MetricKit 신호를 Xcode Cloud와 Instruments 검증으로 어떻게 연결할 수 있는가?

## 10. 이 세션에서 외우지 않아도 되는 것

처음에는 MetricKit payload schema 전체를 외울 필요가 없다. 먼저 다음 구조만 잡으면 된다.

```text
metrics     = field에서 품질 변화를 본다
diagnostics = 문제가 있었던 사건을 설명한다
feedback    = local 재현/trace/CI 검증으로 돌아간다
```
