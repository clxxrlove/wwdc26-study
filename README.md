# WWDC26 Security Study Harness

WWDC26 내용을 무작정 전부 훑기보다, **모바일 앱 보안 솔루션 / Xcode Toolchain / Swift Compiler / LLVM Pass** 관점에서 선별·요약·질문으로 정리하는 개인 스터디 레포입니다.

이 레포는 WWDC26을 보안 및 toolchain 관점에서 공부하기 위한 개인 스터디 노트입니다.

## Goal

최종 산출물은 다음입니다.

1. `outputs/learning-guide.md`
   이해 중심 메인 학습 지도
2. `outputs/understanding-index.md`
   세션별로 어떤 이해 문서를 읽을지 정리한 인덱스
3. `docs/understanding/README.md`와 `docs/understanding/*.md`
   App Attest, Xcode, Swift, diagnostics, agentic security 등을 개념 단위로 설명하는 문서
4. `outputs/direct-watch-guide.md`
   직접 영상을 볼 세션과 중점 체크리스트
5. `outputs/wwdc26-security-brief.md`
   전체 관점을 다시 압축한 학습 브리프
6. `outputs/study-questions.md`
   후속 학습 질문 목록
7. `outputs/watch-priority.md`
   어떤 세션을 영상으로 보고, 어떤 세션은 transcript/selected chapter로 볼지 정리한 우선순위표
8. `sessions/notes/*.md`
   Apple Developer Summary/Transcript 기반 세션별 노트

## Study focus

- Xcode 27 / Xcode agents / Device Hub / Xcode Cloud
- Swift 6.3·6.4 / Swift Compiler / Swift-C interop / optimizer control
- App Attest / Trust Insights / app integrity / fraud signals
- LLVM Pass, build pipeline, signing, diagnostics, runtime compatibility 관점의 질문 정리

## Current highest-priority sessions

- What’s new in Xcode 27
- Xcode, agents, and you
- What’s new in Swift
- Secure your apps with App Attest
- Meet Trust Insights
- Secure your app: mitigate risks to agentic features

## Start here

처음 열었을 때는 아래 순서만 따르면 됩니다.

1. [`outputs/learning-guide.md`](outputs/learning-guide.md) — 전체 학습 순서와 “이해했다”의 기준을 봅니다.
2. [`outputs/understanding-index.md`](outputs/understanding-index.md) — 세션별로 어떤 deep-dive 문서를 읽을지 고릅니다.
3. [`outputs/direct-watch-guide.md`](outputs/direct-watch-guide.md) — 영상은 여기 있는 chapter만 가볍게 봅니다.
4. [`docs/understanding/README.md`](docs/understanding/README.md) — 이해 문서를 문제 축별로 읽습니다.
5. [`outputs/wwdc26-security-brief.md`](outputs/wwdc26-security-brief.md) — 마지막에 전체 관점을 다시 압축합니다.
6. [`outputs/study-questions.md`](outputs/study-questions.md) — 후속 학습 질문을 정리합니다.

## How to study

- 영상은 “화면 흐름 확인”용입니다.
- 이해는 `docs/understanding/*.md`에서 합니다.
- 세션 노트는 Apple session 기준 근거를 확인할 때만 봅니다.
- 모르는 용어는 `docs/understanding/glossary.md`로 돌아갑니다.

## Evidence rule

- Apple 발표 사실은 Apple Developer session page의 Summary/Transcript 기준으로 작성합니다.
- 기술 영향은 `추론`으로 표시합니다.
- 확실하지 않은 구현 구조는 `확인 필요`로 표시합니다.
- 직접 영상을 보지 않은 경우 “영상 전체 시청 완료”라고 쓰지 않습니다.

## Repository structure

```text
wwdc26-security-harness/
  AGENTS.md
  README.md
  docs/
    study-context.md
    priority-rubric.md
    note-template.md
    final-brief-template.md
    understanding/
      README.md
      app-attest.md
      trust-insights.md
      agentic-security.md
      xcode-27-toolchain.md
      xcode-agents.md
      swift-compiler.md
      xcode-cloud.md
      instruments-responsiveness.md
      device-hub.md
      swift-testing.md
      metrickit.md
      foundation-models.md
      agentic-instruments.md
      swiftui.md
      uikit.md
      glossary.md
  registry/
    seed_sessions.csv
  sessions/
    raw/        # ignored; local Apple page/transcript cache only
    notes/      # concise notes
  outputs/
    learning-guide.md
    understanding-index.md
    wwdc26-security-brief.md
    direct-watch-guide.md
    study-questions.md
    watch-priority.md
    hallucination-review.md
  prompts/
  scripts/
```

## Important rule

목적은 “WWDC26 전체를 다 봤다”고 말하는 것이 아닙니다.
목적은 **보안/toolchain 관점에서 WWDC26 내용을 이해하고, 왜 알아야 하는지와 후속 학습 질문으로 정리하는 것**입니다.
