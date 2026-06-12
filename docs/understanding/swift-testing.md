# Swift Testing migration 이해하기

Source: https://developer.apple.com/videos/play/wwdc2026/267/

## 1. 한 문장으로 먼저 잡기

Swift Testing migration은 기존 XCTest를 한 번에 갈아엎는 작업이 아니라, 새 테스트는 Swift Testing으로 쓰고 기존 XCTest는 필요한 만큼 남겨 두면서 **두 test framework가 같은 프로젝트 안에서 안전하게 공존하도록 만드는 전환 전략**이다.

이 세션을 보안/toolchain 스터디에서 보는 이유는 “새 assertion 문법” 자체보다, 보호 로직·crash path·abort path·build validation을 어떻게 더 작고 명확한 테스트로 만들 수 있는가에 있다.

## 2. 왜 migration이 필요한가

기존 테스트가 이미 많다면 “모든 XCTest를 Swift Testing으로 변환”하는 접근은 위험하다.

1. 오래된 테스트 helper가 실제로는 여러 assertion API에 의존한다.
2. 테스트 target에는 XCTest와 Swift Testing이 같이 들어갈 수 있다.
3. 새 테스트를 추가하면서 기존 helper를 재사용하면 cross-framework issue가 생긴다.
4. Xcode 27의 interoperability mode가 그 issue를 warning, error, fatal error 중 어떤 강도로 다룰지 결정한다.

따라서 migration의 핵심 질문은 이것이다.

> 어떤 테스트는 그대로 두고, 어떤 새 검증만 Swift Testing으로 추가할 것인가?
> 기존 helper가 만든 실패를 새 framework에서도 같은 의미로 볼 수 있는가?
> warning으로 지나가면 안 되는 실패가 warning으로 약해지지는 않는가?

## 3. Swift Testing에서 먼저 이해할 세 가지

### 3.1 `@Test`와 `#expect`

Swift Testing의 기본 단위는 `@Test`로 표시한 함수와 `#expect` expectation이다.

처음에는 “XCTest class를 어떻게 옮기나”보다 더 단순하게 보면 된다.

```text
테스트 함수
  └─ 입력 준비
  └─ #expect로 기대값 표현
  └─ 실패 위치와 조건을 Xcode가 보여줌
```

보안 기능을 붙인 앱에서는 작은 expectation이 중요하다. 예를 들어 “정상 입력은 통과한다”, “변조된 입력은 거부된다”, “실패 시 사용자 영향이 제한된다” 같은 조건을 각각 분리해야 회귀를 찾기 쉽다. **추론**

### 3.2 Interoperability mode

Apple session 기준 Xcode 27은 XCTest와 Swift Testing 사이의 cross-framework issue를 다루는 interoperability를 제공한다.

이 mode는 migration 중에 특히 중요하다.

| Mode | 이해 방식 |
|---|---|
| limited | 일부 cross-framework issue가 warning으로 남을 수 있다. 기존 test plan에서 이어질 수 있다. |
| complete | cross-framework issue를 error로 유지해 놓치기 어렵게 한다. |
| strict | XCTest API가 Swift Testing test 안에서 문제를 만들면 더 강하게 멈춘다. |
| none | interoperability를 끄는 선택지다. 단, issue를 놓칠 수 있으므로 임시 예외로만 봐야 한다. |

보안 회귀 테스트 관점에서는 warning으로 지나간 실패가 실제 release gate를 통과하게 만들 수 있다. 그래서 “migration이 잘 된다”보다 “실패가 실패로 남는가”를 먼저 확인해야 한다. **추론 / 확인 필요**

### 3.3 Parameterized test

Parameterized test는 같은 검증을 여러 입력 조합으로 반복한다.

```text
검증할 규칙
  ├─ 입력 A
  ├─ 입력 B
  ├─ 입력 C
  └─ 각 조합을 독립 test case처럼 관찰
```

보안/toolchain 스터디에서는 이 기능을 다음처럼 이해하면 쉽다.

- 보호 전/후 build variant
- debug/release configuration
- 정상 payload/변조 payload/replay-like payload
- 지원 OS version과 Xcode toolchain 조합

이런 조합을 손으로 loop 안에 숨기면 어떤 입력이 실패했는지 보기 어렵다. Parameterized test는 실패 조합을 더 직접적으로 드러내는 도구로 볼 수 있다. **추론**

## 4. Exit test가 왜 눈에 띄는가

Apple session은 exit test를 “프로세스가 종료되는 코드 경로를 child process에서 실행하고 exit condition을 확인하는 방식”으로 설명한다.

이것은 일반 unit test와 성격이 다르다.

```text
일반 테스트
  └─ 같은 test process 안에서 함수 호출

exit test
  └─ child process에서 crash/precondition failure/exit path 실행
  └─ parent test가 종료 상태를 확인
```

보안 로직에는 “절대 계속 실행하면 안 되는 상태”가 있을 수 있다. 예를 들어 tamper 감지 후 fail-closed path, precondition failure, process abort 같은 경로는 일반 테스트 안에서 그대로 실행하기 어렵다. Exit test는 이런 경로를 관찰할 가능성을 준다. **추론 / 확인 필요**

단, Apple session 기준 exit test 지원 platform은 제한되어 있다. iOS 앱 자체의 device-side 동작을 그대로 검증하는 기능이라고 단정하면 안 된다. 지원 platform과 CI 환경은 별도로 확인해야 한다. **확인 필요**

## 5. 이 세션에서 믿는 것과 믿지 않는 것

| 대상 | 믿는가? | 이유 |
|---|---:|---|
| Swift Testing이 XCTest와 공존 가능하다는 점 | 신뢰 | Apple session의 migration 전략과 interoperability 설명에 포함된다. |
| Interoperability mode가 release gate 품질에 영향을 줄 수 있다는 점 | 추론 | warning/error/fatal 차이가 CI 판단과 연결될 수 있다. |
| Parameterized test가 보안 입력 matrix에 유용하다는 점 | 추론 | 세션의 입력 조합 테스트 개념을 보안 검증에 적용한 것이다. |
| Exit test가 모든 iOS crash path를 커버한다는 주장 | 믿지 않음 | platform 지원과 실행 환경 제한이 있으므로 확인 필요다. |
| Coding Assistant가 migration을 완전히 안전하게 끝낸다는 주장 | 믿지 않음 | 자동화 결과는 test failure semantics와 diff review가 필요하다. |

## 6. 보안/toolchain 관점의 체크리스트

1. 기존 XCTest target에 Swift Testing test를 추가할 수 있는가?
2. test plan의 interoperability mode는 무엇인가?
3. 기존 helper가 `XCTFail` 같은 XCTest issue API를 감싸고 있는가?
4. migration 후 실패가 warning으로 약해지지 않는가?
5. 보호 로직의 입력 조합을 parameterized test로 표현할 수 있는가?
6. crash/abort/precondition failure 경로는 exit test로 검증 가능한 platform인가? **확인 필요**
7. `swift test`와 Xcode test plan에서 mode가 다르게 적용되지는 않는가? **확인 필요**

## 7. 세션을 다시 볼 때 집중할 장면

- XCTest를 그대로 두고 Swift Testing을 추가하는 migration strategy
- cross-framework issue가 limited/complete/strict mode에서 어떻게 달라지는지
- helper의 `XCTFail`을 `Issue.record`로 바꾸는 흐름
- parameterized test가 실패 입력을 드러내는 장면
- exit test가 child process에서 실패 경로를 검증하는 장면

## 8. 내가 이해했는지 확인하는 질문

1. XCTest를 모두 삭제하지 않아도 Swift Testing migration을 시작할 수 있는 이유는 무엇인가?
2. limited mode에서 warning으로 남는 실패가 왜 위험할 수 있는가?
3. complete mode와 strict mode는 각각 어떤 migration 단계에 더 어울리는가?
4. Parameterized test는 loop 기반 테스트보다 어떤 정보를 더 잘 보여주는가?
5. Exit test를 iOS device test의 만능 대체재로 보면 안 되는 이유는 무엇인가?
6. 보안 보호 로직 테스트에서 “실패가 실패로 남는가”를 어떻게 확인할 것인가?

## 9. 이 세션에서 외우지 않아도 되는 것

처음 볼 때는 모든 macro syntax와 환경 변수 이름을 외우기보다 다음 구조만 잡으면 된다.

```text
migration = 기존 XCTest를 유지하면서 새 Swift Testing을 점진적으로 추가
interoperability = 두 framework 사이 issue의 의미를 보존하기 위한 장치
mode = warning/error/fatal처럼 실패 강도를 정하는 release gate 변수
parameterized test = 입력 matrix를 테스트 결과에 드러내는 방식
exit test = 종료/abort 경로를 격리 process에서 확인하는 방식
```
