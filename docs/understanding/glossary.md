# Glossary

## App Attest

Apple DeviceCheck framework의 기능. 앱이 생성한 Secure Enclave-bound key와 app/device identity 관련 증거를 서버가 검증할 수 있게 한다.

## Attestation

초기 신뢰 등록 절차. 서버가 “이 key와 앱/기기 상태를 신뢰할 수 있는가?”를 확인한다.

## Assertion

이후 요청 검증 절차. 서버가 “이 payload가 이전에 attested된 key로 만들어졌는가?”를 확인한다.

## Assertion counter

Assertion에 포함되는 증가 값. 서버는 counter가 strictly increasing인지 확인해 replay나 compromised copy 가능성을 본다.

## Relying party identifier

App Attest에서 app identity를 식별하는 값. Apple session 기준 Team Identifier와 bundle identifier의 연결로 이해하면 된다.

## Team Identifier

Apple Developer provisioning profile과 연결되는 team 식별자. Re-signing이나 provisioning 변경과 관련된 app identity 검증에서 중요하다.

## Launch validation category

iOS 27 App Attest signal. 앱이 어떤 launch validation category로 실행되는지 알려주며, 기대하지 않은 실행/배포 상태를 risk signal로 볼 수 있다.

## Fraud metric

App Attest data server에서 조회하는 risk signal. 특정 device에서 최근 약 30일 동안 앱과 연결된 unique attested keys의 approximate count로 이해하면 된다. 단독 차단 기준이 아니라 investigation signal이다.

## Secure Enclave-bound key

Secure Enclave에 묶인 key. private key가 일반 앱 코드 밖으로 노출되지 않는 신뢰 anchor 역할을 한다.

## Re-signing

앱을 수정한 뒤 다른 provisioning profile/certificate로 다시 서명하는 행위. App Attest에서는 Team Identifier나 app identity mismatch와 연결될 수 있다.

## LLVM Pass

LLVM IR을 분석하거나 변환하는 compiler pass. 난독화, instrumentation, optimization과 연결될 수 있지만, 실제 통합 단계는 도구마다 다르다.

## Swift-C interop

Swift code와 C ABI/interface가 만나는 지점. `@C` 같은 기능은 Swift function export, symbol, ABI boundary 관점에서 중요할 수 있다.

## Indirect prompt injection

사용자가 직접 입력하지 않은 외부 content나 tool result 안에 악의적 instruction이 들어 있고, agent가 이를 따라 action을 수행하는 공격 패턴.
