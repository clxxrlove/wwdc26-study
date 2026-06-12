# Xcode agents 이해하기

Source: https://developer.apple.com/videos/play/wwdc2026/259/

## 1. 핵심 질문

Xcode agents를 “코드를 대신 써주는 기능”으로만 보면 부족하다. 보안/toolchain 관점에서는 이렇게 봐야 한다.

> agent가 project context를 읽고, build/test를 실행하고, artifact를 해석하고, 설정을 바꿀 수 있다면 어떤 자동화 기회와 어떤 정보 노출 경계가 생기는가?

## 2. agent가 바꾸는 workflow

전통적인 workflow:

```text
개발자 → 문서 검색 → 코드 수정 → build → error 확인 → 다시 수정
```

agent workflow:

```text
개발자 → 목표 설명
agent → project 탐색
agent → Apple documentation 검색
agent → plan 작성
agent → 코드/설정 수정
agent → build/preview/test 실행
개발자 → artifact와 diff 검토
```

이 변화는 보안 도구 자체를 자동으로 이해한다는 뜻은 아니다. 하지만 도구가 남기는 log, report, config가 agent가 읽기 쉬운 형태인지가 중요해질 수 있다. **추론**

## 3. 보안 관점에서 보는 두 얼굴

### 기회

- build failure triage 자동화
- 설정 누락 탐지
- diagnostics report 요약
- Apple documentation 기반 migration 도움
- 반복적인 test/build 확인 자동화

### 리스크

- config, token, license-like string, signing-related path가 agent context에 들어갈 수 있음
- build log에 민감한 값이 그대로 남을 수 있음
- agent가 build setting이나 script를 바꾸면서 toolchain integration을 깨뜨릴 수 있음
- 생성된 patch를 사람이 충분히 검토하지 않으면 보안 설정이 약해질 수 있음

## 4. 이 세션에서 외울 것보다 봐야 할 것

- Plan mode가 code 작성 전에 어떤 정보를 수집하는지
- Apple Document Search가 어떤 식으로 최신 API 지식을 보완하는지
- build/preview/test validation이 agent loop 안에 어떻게 들어가는지
- artifacts와 transcript가 사람이 review할 수 있는 형태인지
- sub-agent orchestration이 큰 작업을 어떻게 나누는지

## 5. 이해 확인 질문

1. Xcode agent가 읽는 project context에는 어떤 민감 정보가 들어갈 수 있는가?
2. 보안 도구의 CLI output은 사람뿐 아니라 agent가 읽기에도 구조화되어야 하는가?
3. agent가 build setting을 바꾸는 경우 어떤 regression test가 필요할까?
4. Apple Document Search가 비공개 구현 지식을 대체할 수 없는 이유는 무엇인가?
