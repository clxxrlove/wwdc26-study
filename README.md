# WWDC26 Security Study Harness

WWDC26 내용을 무작정 전부 훑기보다, **모바일 앱 보안 솔루션 / Xcode Toolchain / Swift Compiler / LLVM Pass** 관점에서 선별·요약·질문으로 정리하는 개인 스터디 레포입니다.

이 레포는 WWDC26을 보안 및 toolchain 관점에서 공부하기 위한 개인 스터디 노트입니다.

## Goal

최종 산출물은 다음입니다.

1. `outputs/wwdc26-security-brief.md`
   핵심 학습 브리프
2. `outputs/direct-watch-guide.md`
   직접 영상을 볼 세션과 중점 체크리스트
3. `outputs/study-questions.md`
   후속 학습 질문 목록
4. `outputs/watch-priority.md`
   어떤 세션을 영상으로 보고, 어떤 세션은 transcript/selected chapter로 볼지 정리한 우선순위표
5. `sessions/notes/*.md`
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

## How to study

1. `outputs/watch-priority.md`로 전체 우선순위를 확인합니다.
2. `outputs/direct-watch-guide.md`를 열고 직접 볼 세션과 chapter를 표시합니다.
3. 직접 보기 전후로 `sessions/notes/*.md`를 읽습니다.
4. `outputs/wwdc26-security-brief.md`에서 주제별로 다시 정리합니다.
5. `outputs/study-questions.md`를 참고해 toolchain integration, compatibility matrix, diagnostics를 후속 학습 주제로 정리합니다.

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
  registry/
    seed_sessions.csv
  sessions/
    raw/        # ignored; local Apple page/transcript cache only
    notes/      # concise notes
  outputs/
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
목적은 **보안/toolchain 관점에서 WWDC26 내용을 이해하고, 후속 학습 질문으로 정리하는 것**입니다.
