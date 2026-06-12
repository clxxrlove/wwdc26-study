# Instruments Responsiveness 이해하기

Source: https://developer.apple.com/videos/play/wwdc2026/268/

## 1. 한 문장으로 먼저 잡기

Instruments responsiveness 학습의 핵심은 “앱이 느리다”를 감으로 말하지 않고, **어느 시점의 어떤 code path, hang, contention, main-thread work가 사용자 경험을 막았는지 증거로 좁히는 방법**을 익히는 것이다.

보안/toolchain 관점에서는 더 구체적으로 이렇게 잡으면 된다.

> 보호 적용 전후에 앱이 멈추거나 느려졌다면, Instruments로 원인 구간을 재현하고 측정해 compatibility regression인지 판단한다.

## 2. 왜 필요한가: 보호 기능은 성능 질문을 만든다

앱 보호나 build-time 변환을 다룰 때 처음에는 “기능이 정상 동작하는가”에 집중하기 쉽다. 하지만 실제 도입 검증에서는 다음 질문이 곧 따라온다.

1. 앱 launch나 특정 화면 진입이 느려졌는가?
2. CPU 사용량이 특정 helper나 변환된 함수에 몰리는가?
3. main thread에서 긴 작업이 생겼는가?
4. lock, queue, actor, thread contention 때문에 응답성이 떨어지는가?
5. 재현 가능한 특정 device/OS/app state에서만 문제가 생기는가?

Instruments는 이 질문을 “느낌”이 아니라 trace와 time range로 좁히는 도구다.

## 3. 이 세션에서 먼저 이해할 세 가지

### 3.1 Profile: 문제가 생긴 순간을 기록한다

Profile은 앱 실행 중 실제 비용을 관찰하는 단계다.

```text
앱 실행
  └─ 사용자 흐름 재현
      └─ Instruments trace 기록
          └─ time range 선택
              └─ 비싼 함수 / hang / contention 후보 확인
```

여기서 중요한 점은 “전체 앱이 느리다”가 아니라 “어느 구간에서 느린가”를 먼저 고르는 것이다. 같은 앱이라도 launch, 로그인, 목록 스크롤, 암호화된 resource 로딩, network callback 이후 화면 갱신은 원인이 다를 수 있다.

### 3.2 Fix: 원인 후보를 code path와 연결한다

Profile 결과는 수정 방향을 바로 보장하지 않는다. CPU sample, hang, thread state, call tree를 보고 “어떤 코드가 사용자의 기다림으로 연결되는가”를 해석해야 한다.

보안/toolchain 관점의 예시는 다음처럼 볼 수 있다. **추론**

| 관찰 | 가능한 해석 | 바로 단정하면 안 되는 것 |
|---|---|---|
| 보호 runtime helper가 hot path에 자주 보임 | 반복 호출 비용 증가 가능성 | helper가 문제의 유일한 원인 |
| main thread에서 긴 초기화 | launch 또는 첫 화면 비용 증가 가능성 | 모든 device에서 동일한 문제 |
| lock/contention 증가 | 보호 로직과 앱 동시성 구조 충돌 가능성 | 특정 lock만 문제라고 보기 어려움 |
| symbolication이 부정확함 | dSYM/artifact 처리 확인 필요 | 앱 코드가 손상됨 |

### 3.3 Verify: 수정 후 같은 조건에서 다시 측정한다

Instruments의 강점은 수정 전후를 비교할 수 있다는 점이다.

```text
Baseline trace
  └─ 보호 적용 trace
      └─ 수정/설정 변경 trace
          └─ 같은 user flow와 같은 metric으로 비교
```

이때 “한 번 빨라졌다”보다 중요한 것은 재현 조건이다. device, OS, build configuration, input data, network state, app container state가 다르면 비교가 흐려질 수 있다.

## 4. Instruments에서 믿는 것과 조심할 것

| 대상 | 믿는가? | 이유 |
|---|---:|---|
| 같은 조건에서 얻은 trace | 강한 근거 | 실제 실행 비용과 대기 구간을 보여준다. |
| 단일 trace의 한 번 관찰 | 제한적으로 신뢰 | cold start, cache, device state 영향이 있을 수 있다. |
| symbolicated call tree | 유용한 근거 | 함수 단위 원인 후보를 좁힌다. 단, symbol 처리 상태 확인 필요. |
| “느려 보인다”는 수동 체감 | 출발점 | 측정 없이 regression 판단 근거로 쓰기 어렵다. |
| Instruments 결과의 자동 해석 | 참고 | 최종 판단은 재현 조건과 code context를 함께 봐야 한다. |

## 5. Xcode 27의 Top Functions와 연결해서 보기

`outputs/watch-priority.md`와 Xcode 27 노트 기준, Xcode 27의 Instruments에는 CPU profile/time range에서 expensive code path를 빠르게 찾는 Top Functions 흐름이 소개된다.

Top Functions는 처음 볼 때 이렇게 이해하면 된다.

```text
선택한 time range 안에서
  └─ 반복적으로 비용이 큰 함수 후보를 위로 올려
      └─ 어디부터 봐야 하는지 알려주는 triage入口
```

즉 Top Functions는 원인 판정 장치라기보다 “분석을 어디서 시작할지” 정하는 도구다. 보호 적용 후 특정 helper, wrapper, generated thunk, bridged function이 반복적으로 보인다면 그 지점을 benchmark 후보로 삼을 수 있다. **추론**

## 6. 보안/toolchain 검증에서 특히 봐야 할 신호

### 6.1 Launch와 first-use 비용

보호 로직이 앱 시작 시 초기화되거나 첫 사용 시 key/resource/table을 준비한다면 launch time 또는 첫 화면 latency에 보일 수 있다. 실제 적용 지점은 repo 자료만으로 단정할 수 없으므로 **확인 필요**.

### 6.2 Hot path에 들어간 보호 코드

성능 비용은 “비싼 작업”보다 “자주 반복되는 작업”에서 커질 수 있다. 예를 들어 아주 작은 check라도 scroll cell rendering, tight loop, serialization path에 들어가면 사용자 경험에 보일 수 있다. **추론**

### 6.3 Contention과 thread hop

보호 코드가 shared state, lock, queue, actor boundary를 사용한다면 contention이나 thread hop이 늘 수 있다. 어떤 동시성 모델을 쓰는지는 대상 도구/앱별로 **확인 필요**.

### 6.4 Symbolication과 artifact 경계

보호 적용 후 dSYM, symbol map, build artifact가 바뀌면 Instruments/Organizer/MetricKit에서 원인 분석이 어려워질 수 있다. 이것은 성능 문제가 아니라 관측 가능성 문제일 수 있다. **추론 / 확인 필요**

## 7. 실패와 예외를 어떻게 봐야 하나

Instruments 결과가 바로 “보호 기능 문제”를 뜻하지는 않는다. 다음을 분리해야 한다.

1. baseline 앱에도 있던 기존 병목인가?
2. 보호 적용 후 새로 생긴 병목인가?
3. 특정 build configuration에서만 생기는가?
4. simulator와 physical device 결과가 다른가?
5. trace가 충분히 symbolicated되었는가?
6. 재현 flow가 실제 사용자 flow를 대표하는가?

성능 regression은 단정하기 전에 최소한 baseline과 같은 조건의 비교 trace가 필요하다.

## 8. 세션을 다시 볼 때 집중할 장면

- responsiveness 문제를 재현 가능한 user flow로 만드는 부분
- trace에서 time range를 좁히는 부분
- expensive function 또는 hang 원인 후보를 찾는 부분
- 수정 후 같은 조건에서 verify하는 부분
- CPU, hang, contention을 서로 다른 증거로 구분하는 부분

## 9. 내가 이해했는지 확인하는 질문

1. “앱이 느리다”를 Instruments에서 어떤 time range와 metric으로 바꿀 수 있는가?
2. Top Functions는 원인 판정 도구인가, triage 도구인가?
3. 보호 적용 전후 성능 비교에서 device/app state를 맞춰야 하는 이유는 무엇인가?
4. symbolication 문제가 있으면 성능 분석에 어떤 영향을 주는가?
5. CPU hot path와 hang은 같은 문제인가, 다른 증거인가?

## 10. 이 세션에서 외우지 않아도 되는 것

처음에는 Instruments의 모든 template과 세부 column을 외울 필요가 없다. 먼저 다음 구조만 잡으면 된다.

```text
profile = 문제 구간을 기록한다
fix     = trace를 code path와 연결해 원인 후보를 줄인다
verify  = 같은 조건에서 수정 전후를 비교한다
```
