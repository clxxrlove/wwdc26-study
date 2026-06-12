# Xcode Cloud 이해하기

Source: https://developer.apple.com/videos/play/wwdc2026/261/

## 1. 한 문장으로 먼저 잡기

Xcode Cloud는 “내 Mac에서 한 번 성공한 build/test를 넘어서, **repository 기반으로 cloud에서 build, test, delivery를 반복 실행하는 Apple 개발 workflow**”로 이해하면 된다.

보안/toolchain 관점의 핵심 질문은 이것이다.

> 보호 도구나 build integration이 local Xcode뿐 아니라 cloud CI, signing, artifacts, test matrix, 배포 흐름에서도 깨지지 않는가?

## 2. 왜 필요한가: local 성공은 delivery 성공이 아니다

보안 기능이나 build-time 변환이 local 개발 환경에서 동작해도 CI/CD에서는 다른 문제가 생길 수 있다.

1. cloud runner에 필요한 tool이나 license가 없다.
2. custom build phase가 sandbox/network/secrets 정책과 충돌한다.
3. signing, provisioning, entitlement 설정이 local과 다르다.
4. protected artifact, dSYM, logs가 기대 위치에 남지 않는다.
5. unit/UI tests가 parallel device matrix에서만 실패한다.
6. TestFlight/App Store delivery 단계에서 artifact 처리 정책이 달라진다.

Xcode Cloud는 이런 차이를 “나중에 수동 확인”이 아니라 workflow 일부로 보게 만드는 도구다.

## 3. Xcode Cloud 흐름을 세 단계로 이해하기

### 3.1 Build: cloud에서 같은 산출물이 만들어지는가?

```text
Repository commit
  └─ Xcode Cloud workflow
      └─ clean/cloud build
          └─ app artifact 생성
```

보안/toolchain 관점에서는 local build와 cloud build가 같은 전제에서 동작하는지 봐야 한다. 특히 custom script, binary tool, Swift/Clang/LLVM integration, post-build processing 같은 지점은 실제 구조가 무엇인지 **확인 필요**다.

### 3.2 Test: 여러 조건에서 자동 검증되는가?

Xcode 27 노트 기준 Xcode Cloud는 unit/UI tests를 commit마다 cloud에서 병렬 실행하고 delivery와 연결하는 흐름으로 소개된다.

테스트는 단순히 pass/fail만 보는 것이 아니라 다음을 묻는다.

- 보호 적용 후 핵심 smoke test가 통과하는가?
- UI test가 protected build에서도 안정적인가?
- 특정 OS/device 조합에서만 실패하는가?
- App Attest, local storage, network mock 같은 환경 의존성이 CI에서 어떻게 처리되는가? **확인 필요**

### 3.3 Deliver: 산출물과 진단 파일이 안전하게 이어지는가?

delivery 단계에서는 app binary만 보면 부족하다.

```text
build artifact
  ├─ app / archive
  ├─ dSYM / symbolication material
  ├─ test logs
  ├─ protection logs or reports  추론 / 확인 필요
  └─ TestFlight/App Store delivery
```

보호 적용 후 crash/MetricKit/Organizer 분석을 하려면 symbolication과 artifact 보관이 중요하다. 어떤 파일을 생성하고 보관해야 하는지는 도구별로 **확인 필요**.

## 4. Xcode Cloud에서 믿는 것과 믿지 않는 것

| 대상 | 믿는가? | 이유 |
|---|---:|---|
| clean cloud build 통과 | 강한 호환성 근거 | local machine state에 덜 의존한다. |
| local-only build 통과 | 제한적 근거 | CI secrets/tool/version 차이를 못 본다. |
| unit/UI test matrix | 중요한 회귀 신호 | 여러 조건에서 반복 검증 가능하다. |
| build log | 진단 근거 | 단, 민감정보가 섞이지 않도록 관리 필요. |
| cloud 성공 한 번 | 불충분 | workflow trigger, branch, signing, delivery 조건별 확인 필요. |

## 5. 보안/toolchain checklist

### 5.1 Build integration 위치

보호 도구가 어디에 붙는지 알아야 Xcode Cloud 대응도 가능하다.

- Xcode build phase인가?
- Swift/Clang frontend 단계인가?
- LLVM IR/pass 단계인가?
- linker 이후 post-build 단계인가?
- 별도 archive/export 단계인가?

현재 repo 자료만으로 실제 integration 지점은 **확인 필요**다. 따라서 문서에서는 가능성으로만 다루고 단정하지 않아야 한다.

### 5.2 Secrets와 license

cloud build에서 필요한 token, license, signing material, private endpoint가 있다면 노출 경계를 정해야 한다. Apple 세션 링크만으로 구체 정책은 알 수 없으므로 **확인 필요**.

중요한 원칙은 build log와 agent-readable artifact에 민감한 값이 남지 않도록 하는 것이다. **추론**

### 5.3 Artifacts와 symbolication

보호 적용이 dSYM, symbol map, crash report symbolication, MetricKit payload 해석에 영향을 줄 수 있다. **추론 / 확인 필요**

따라서 Xcode Cloud workflow에는 다음 확인이 필요하다.

1. protected build의 dSYM이 보존되는가?
2. crash/diagnostic system이 symbolicated 결과를 만들 수 있는가?
3. protection report가 있다면 공개 가능한 정보만 포함하는가?
4. TestFlight/App Store delivery artifact와 local archive가 같은 기준으로 추적되는가?

## 6. Device Hub / Instruments / MetricKit와 이어지는 흐름

```text
Xcode Cloud
  └─ commit마다 build/test/delivery 검증
      ├─ 실패 조건은 Device Hub로 local 재현
      ├─ performance 문제는 Instruments로 trace 확인
      └─ field signal은 MetricKit/Organizer와 비교
```

Xcode Cloud는 “모든 원인을 알려주는 도구”가 아니라 반복 가능한 검증 gate다. 실패가 나오면 local 재현과 trace 분석으로 내려가야 한다.

## 7. 실패와 예외를 어떻게 봐야 하나

Xcode Cloud 실패를 바로 code defect로 단정하면 안 된다.

- cloud image의 Xcode/SDK version 차이
- signing/provisioning 설정 차이
- environment variable/secrets 누락
- network 접근 정책
- test flakiness
- simulator/device availability 차이
- custom tool 설치 여부

이 항목은 각각 확인 절차가 필요하다. 특히 보안 도구가 외부 service나 local binary에 의존한다면 cloud 지원 정책은 **확인 필요**다.

## 8. 세션을 다시 볼 때 집중할 장면

- repository 연결과 workflow 설정 흐름
- commit마다 unit/UI tests를 cloud에서 실행하는 흐름
- Xcode/OS/device matrix를 다루는 부분
- TestFlight/App Store delivery와 연결되는 부분
- logs/artifacts/reports를 어디서 확인하는지

## 9. 내가 이해했는지 확인하는 질문

1. local Xcode build 성공과 Xcode Cloud build 성공은 왜 다른 의미인가?
2. 보호 도구의 build integration 위치를 모르면 CI 설계를 왜 구체화하기 어려운가?
3. cloud build logs에 남으면 안 되는 정보는 무엇인가?
4. protected build에서 dSYM과 symbolication을 확인해야 하는 이유는 무엇인가?
5. Xcode Cloud 실패를 Device Hub/Instruments로 어떻게 좁힐 수 있는가?

## 10. 이 세션에서 외우지 않아도 되는 것

처음에는 Xcode Cloud UI의 모든 설정 이름을 외울 필요가 없다. 먼저 다음 구조만 잡으면 된다.

```text
build   = cloud에서 산출물이 만들어지는가
test    = matrix에서 반복 검증되는가
deliver = artifact/signing/symbolication이 이어지는가
```
