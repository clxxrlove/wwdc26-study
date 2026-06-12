# App Attest 이해하기

Source: https://developer.apple.com/videos/play/wwdc2026/201/

## 1. 한 문장으로 먼저 잡기

App Attest는 “이 요청이 내가 배포한 정상 앱이, 정상 Apple 기기에서, 변조되지 않은 상태로 만든 요청인가?”를 **서버가 판단할 수 있게 해주는 신뢰 증거 시스템**이다.

중요한 점은 “앱이 스스로 정상이라고 말한다”가 아니라 “서버가 Apple hardware와 Secure Enclave에 연결된 증거를 검증한다”는 점이다.

## 2. 왜 필요한가: 서버 입장에서 보는 문제

앱 보안을 처음 볼 때 흔히 이렇게 생각하기 쉽다.

> 앱에 anti-tamper 로직을 넣으면 변조된 앱은 막히겠지.

하지만 서버 입장에서는 더 단순하고 더 위험한 문제가 있다.

1. 공격자가 앱을 reverse engineering한다.
2. 앱 내부 로직이나 resource를 바꾼다.
3. 다른 provisioning profile로 re-sign한다.
4. 변조된 앱을 실제 기기에서 실행한다.
5. 서버에는 정상 앱처럼 보이는 request를 보낸다.

서버가 단순히 “API 형식이 맞는가”, “토큰이 있는가”만 본다면 변조된 앱의 요청도 정상처럼 보일 수 있다. App Attest는 이 지점에서 서버가 더 강한 질문을 하게 만든다.

> 이 요청을 만든 앱 인스턴스는 내가 기대한 app identity와 연결되어 있는가?
> 그 key는 genuine Apple hardware에서 생성되었는가?
> 이 요청은 이전에 검증한 key로 서명되었는가?
> replay나 broker device처럼 이상한 패턴은 없는가?

## 3. App Attest가 푸는 문제는 세 개다

### 3.1 Attestation: “이 key를 믿어도 되는가?”

Attestation은 초기 등록 절차에 가깝다.

앱이 Secure Enclave-bound key를 만들고, 서버는 그 key가 정상 Apple hardware와 정상 app identity에 연결되어 있는지 검증한다.

흐름은 이렇게 이해하면 된다.

```text
앱
  └─ App Attest로 key 생성
      └─ key ID를 Keychain에 저장

서버
  └─ challenge 발급

앱
  └─ key ID + challenge로 attestation 요청
      └─ Apple service가 device/app 관련 증거를 확인
      └─ attestation object 반환

서버
  └─ attestation object 검증
  └─ public key / receipt / 관련 상태 저장
```

여기서 핵심은 서버가 검증한다는 점이다. Apple session 기준으로 attestation은 app이 아니라 server에서 validate해야 한다. 변조된 앱은 자기 자신을 검증하는 주체가 될 수 없기 때문이다.

### 3.2 Assertion: “이 요청은 그 검증된 key로 만든 것인가?”

Attestation이 key 등록이라면, assertion은 이후 요청마다 “이 요청은 등록된 key가 만든 것”임을 증명하는 절차다.

```text
서버
  └─ challenge 발급

앱
  └─ payload + challenge를 준비
  └─ App Attest assertion 생성
  └─ payload와 assertion을 서버로 전송

서버
  └─ 저장해 둔 public key로 assertion 검증
  └─ counter가 증가했는지 확인
  └─ 요청 accept/reject 결정
```

Assertion이 필요한 이유는 attestation을 한 번 했다고 모든 미래 요청이 자동으로 안전해지는 것은 아니기 때문이다. 서버는 중요한 요청마다 “이 요청도 그 key가 만든 것인가?”를 확인해야 한다.

### 3.3 Fraud metric: “정상 attestation이 너무 많이 생기는 이상한 기기는 없는가?”

Fraud metric은 조금 다른 문제를 다룬다. 어떤 compromised device가 valid attestation을 만들어 주는 broker처럼 동작할 수 있다. 즉, 다른 변조 앱 인스턴스들을 위해 정상처럼 보이는 attestation을 계속 만들어 주는 상황이다.

Apple session 기준 fraud metric은 특정 device에서 최근 약 30일 동안 앱과 연결된 unique attested keys의 approximate count다.

이 값은 단독 차단 기준이 아니다. 이유는 정상적인 key rotation도 있기 때문이다.

- 앱 재설치
- device restore
- key invalidation
- 여러 기기 사용

따라서 fraud metric은 “차단 버튼”이 아니라 “조사 신호”로 이해해야 한다.

## 4. App Attest에서 믿는 것과 믿지 않는 것

| 대상 | 믿는가? | 이유 |
|---|---:|---|
| 앱 코드 자체 | 직접 믿지 않음 | 앱은 reverse engineering/patch/re-sign 대상이 될 수 있다. |
| 앱이 보내는 일반 request | 직접 믿지 않음 | 형식이 정상이어도 변조 앱이 만들 수 있다. |
| Secure Enclave-bound private key | 상대적으로 신뢰 | private key가 Secure Enclave에 묶여 있고 밖으로 나오지 않는 구조다. |
| Apple attestation evidence | 신뢰 근거 | genuine Apple hardware와 app identity 관련 증거를 제공한다. |
| 서버 검증 결과 | 최종 판단 근거 | 서버가 attestation/assertion/counter/risk를 종합해야 한다. |

이 구조 때문에 App Attest는 “앱 내부 보호 기능”이라기보다 “server-side trust protocol”에 가깝다.

## 5. Team Identifier, bundle identifier, relying party identifier

이 부분이 헷갈리기 쉽다.

서버는 “내 앱”을 구분해야 한다. App Attest에서 app identity는 Team Identifier와 bundle identifier를 연결한 relying party identifier로 이해하면 된다.

```text
Team Identifier
  + bundle identifier
  = relying party identifier
```

공격자가 앱을 수정하고 다른 provisioning profile로 re-sign하면 Team Identifier가 기대값과 달라질 수 있다. App Attest는 이런 app identity 정보를 서버가 확인할 수 있게 한다.

### 왜 보안/toolchain 관점에서 중요한가

보안 도구가 build/signing/resource/bundle metadata에 영향을 준다면, App Attest 서버 검증이 기대하는 값과 충돌할 가능성을 확인해야 한다. 이것은 확정된 문제가 아니라 compatibility checklist로 봐야 한다. **추론 / 확인 필요**

## 6. iOS 27에서 특히 봐야 할 신호

Apple session 기준 iOS 27에서는 authenticator data extensions에 다음 성격의 정보가 추가된다.

- launch validation category
- bundle version

### launch validation category

앱이 어떤 launch validation category로 실행되고 있는지 알려주는 신호다. 예를 들어 기대한 배포 경로와 다른 category가 보이면 risk signal로 볼 수 있다.

### bundle version

서버가 알고 있는 배포 version과 device에서 관측된 version이 맞는지 볼 수 있다. 공격자가 bundle version을 임의로 바꿔 re-sign한 경우 탐지 단서가 될 수 있다.

중요한 점은 이 값들도 단독 판정 기준이 아니라 risk assessment의 일부로 봐야 한다는 것이다.

## 7. Assertion counter가 왜 중요한가

Assertion에는 counter가 들어 있고, 서버는 이 값이 strictly increasing인지 확인해야 한다.

왜 counter가 필요한가?

```text
정상 흐름:
요청 1 counter = 1
요청 2 counter = 2
요청 3 counter = 3
```

서버가 이미 counter 3을 봤는데, 이후 counter 2나 3이 다시 오면 이상하다. 이것은 replay이거나, 서버가 알고 있는 최신 상태를 모르는 compromised copy일 수 있다.

```text
의심 흐름:
서버가 저장한 최신 counter = 10
새 요청 counter = 7
=> replay 또는 compromised copy 가능성
```

## 8. App Attest와 앱 내부 anti-tamper는 같은 것이 아니다

둘은 해결하는 위치가 다르다.

| 구분 | 앱 내부 anti-tamper | App Attest |
|---|---|---|
| 주된 위치 | 앱 runtime 내부 | 앱 + Apple service + 서버 |
| 주요 목적 | 변조 비용 증가, runtime tampering 탐지 | 서버가 요청의 신뢰도를 판단 |
| 최종 판단 | 앱 내부 정책일 수 있음 | 서버 검증과 risk policy |
| 약점 | 앱 자체가 공격 대상 | backend integration이 필요함 |

따라서 App Attest를 이해할 때 “이걸 쓰면 anti-tamper가 필요 없어지는가?”라고 묻기보다 이렇게 묻는 편이 낫다.

> 앱 내부 보호가 뚫리거나 우회되어도, 서버가 변조 앱의 요청을 구분할 수 있는가?

## 9. 실패와 예외를 어떻게 봐야 하나

App Attest는 실패하면 무조건 사용자 차단을 하라는 기능이 아니다. Apple session 기준 graceful degradation과 risk assessment가 중요하다.

예외 상황은 정상적으로도 생길 수 있다.

- App Attest 미지원 app type/platform
- 네트워크 실패
- attestation retry 필요
- 앱 재설치로 key rotation
- device restore
- 기존 사용자의 새 key 생성

따라서 운영 관점에서는 다음 결정을 해야 한다.

1. 어떤 기능은 App Attest 실패 시 제한할 것인가?
2. 어떤 기능은 monitoring만 강화할 것인가?
3. 어떤 threshold에서 추가 인증이나 재시도를 요구할 것인가?
4. 어떤 조합의 signal이 모였을 때만 차단할 것인가?

## 10. 세션을 다시 볼 때 집중할 장면

- modified/re-signed app이 valid-looking request를 보내는 부분
- key generation → attestation → server validation 흐름
- attestation과 assertion이 분리되는 이유
- assertion counter 설명
- fraud metric을 단독 차단 기준으로 쓰지 말라는 부분

## 11. 내가 이해했는지 확인하는 질문

1. 왜 App Attest validation은 앱이 아니라 서버에서 해야 하는가?
2. attestation은 언제 하고, assertion은 언제 하는가?
3. Secure Enclave-bound key가 있으면 replay 공격이 자동으로 막히는가? 아니라면 counter는 왜 필요한가?
4. re-signing이 Team Identifier / relying party identifier와 어떻게 연결되는가?
5. fraud metric이 높으면 무조건 차단하면 안 되는 이유는 무엇인가?
6. App Attest와 앱 내부 anti-tamper는 어떤 점에서 보완 관계인가?

## 12. 이 세션에서 외우지 않아도 되는 것

처음 볼 때는 attestation object의 세부 binary structure, certificate chain parsing 세부 구현, receipt field 전체를 외울 필요는 없다. 먼저 다음 구조만 잡으면 된다.

```text
attestation = key와 app/device identity를 서버가 신뢰할 수 있게 등록하는 절차
assertion   = 이후 요청이 그 key로 만들어졌음을 서버가 확인하는 절차
counter     = replay/compromised copy를 의심하기 위한 증가 값
fraud metric = device 단위의 수상한 attestation activity를 보는 조사 신호
```
