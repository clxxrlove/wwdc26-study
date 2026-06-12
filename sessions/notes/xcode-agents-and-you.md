# Xcode, agents, and you

- URL: https://developer.apple.com/videos/play/wwdc2026/259/
- Duration: 약 23분
- Category: Xcode / Coding agents / Developer workflow
- Priority: A
- Review mode: Full video recommended + transcript note
- Last updated: 2026-06-12

## Why this matters to this study

- Apple session 기준 Xcode 27은 coding agents interaction을 확장하고, project exploration, plan mode, build/preview/test validation, visual refinement, sub-agent orchestration을 보여준다.
- 보안 스터디 관점에서는 agent가 project context, build settings, source files, documentation, generated artifacts를 어떻게 다루는지 이해해야 한다.
- mobile app protection/toolchain integration가 CLI/report/config 기반으로 동작한다면, 향후 Xcode agent workflow와 연결될 수 있는지 탐색할 여지가 있다. 단, 이 세션에서 특정 외부 보안 도구 integration을 보장하지는 않는다. **확인 필요**.
- 직접 영상 시청 권장이다. agent transcript/artifacts, plan mode, tool calls, sub-agents UI는 화면 흐름을 봐야 실제 사용감을 이해하기 쉽다.

## 5-line summary

1. Apple session 기준 Xcode 27 agents는 새 프로젝트를 빠르게 이해하기 위해 codebase walkthrough, data model/view hierarchy 설명, reusable architecture documents 작성을 도와준다.
2. Apple Document Search를 사용해 최신 Apple framework knowledge를 agent conversation 안에서 활용할 수 있다.
3. Plan mode는 code 작성 전에 요구사항과 architecture approach를 정리하고, 사용자가 architect 역할로 방향을 조정하게 한다.
4. Xcode agents는 build, preview, test tools를 사용해 구현 중 validation을 수행하고 artifacts/changes/previews를 보여준다.
5. Orchestration 단계에서는 localization/accessibility 같은 high-level goal을 주면 Xcode가 tools와 sub-agents를 조합해 병렬 작업을 수행하는 흐름을 보여준다.

## New APIs / tools / frameworks

| Name | Type | Notes | Relevance |
|---|---|---|---|
| Xcode coding agents | Xcode feature | Xcode 26.3에 도입, Xcode 27에서 tools와 interaction이 확장되었다고 설명. | 대상 개발 workflow 변화 이해. |
| Agent transcript / artifacts | Xcode agent UI | transcript에는 progress/tool calls/sub-agents, artifacts에는 files/edits/previews가 표시. | 자동 변경 리뷰와 보안 설정 노출 검토에 중요. |
| Apple Document Search | Agent tool | agent가 최신 Apple documentation을 conversation 중 참조. | 최신 SDK/API 사용 시 hallucination 감소에 도움. |
| Plan mode | Agent workflow | code 작성 전 plan을 만들고 요구사항을 조정. | protection 적용 전 영향분석/적용계획 UX로 참고 가능. **추론**. |
| Inline annotations / image attachments | Agent input methods | source 위치 또는 design intent를 agent에 전달. | 대상 프로젝트 변경 지시 방식 이해. |
| Sub-agent orchestration | Agent workflow | high-level task를 여러 sub-agent/tool로 병렬 처리. | 대규모 프로젝트 분석/마이그레이션 자동화 가능성 검토. |

## Toolchain / compiler / build implications

- 이 세션은 compiler backend나 LLVM Pass 변경을 설명하지 않는다.
- 다만 Xcode agent가 build/preview/test tools를 사용해 validation하는 흐름은 build pipeline에 통합되는 도구의 UX에 영향을 줄 수 있다.
- 보안 도구가 build logs, generated files, config files를 남긴다면 agent artifacts/context에 노출될 수 있으므로 공개 가능한 로그와 민감한 로그를 분리할 필요가 있다. **추론**.
- Apple Document Search는 최신 SDK/API 확인에 유용하지만, 비공개 도구 동작이나 운영 정책을 대체하지는 못한다.

## Security / anti-tamper / integrity implications

- 직접적인 anti-tamper/App Attest 세션은 아니다.
- 보안 관점의 핵심은 agent가 코드/설정/문서/도구 호출을 다루면서 생기는 정보 경계다.
- protection config, license, signing material, project-specific scripts가 agent context에 들어갈 가능성이 있는지 확인해야 한다. **확인 필요**.
- agent-generated code가 보안 관련 build phase나 config를 바꿀 때 review gate가 필요한지도 확인해야 한다. **추론**.

## Security/toolchain impact hypothesis

> 추론: Xcode agents는 보안 도구 자체의 compiler/runtime 기능보다 “개발자 경험과 troubleshooting workflow”에 영향을 줄 가능성이 크다. 예를 들어 도입 환경에서 protection 적용 전 plan 생성, 설정 검토, build failure triage, Instruments/Organizer 진단 안내를 agent-friendly 문서/CLI output으로 제공하면 유용할 수 있다. 반대로 민감 정보가 agent context에 노출되지 않도록 log redaction과 config boundary가 필요하다.

## Risks / compatibility questions

- Xcode agent가 local scripts/CLI를 호출할 수 있는 공식 범위는 무엇인가? **확인 필요**.
- 보안 도구 config/log/artifact 중 agent에게 보여도 되는 것과 안 되는 것이 구분되어 있는가?
- agent가 build setting이나 script를 수정했을 때 보호 적용이 깨지는 위험을 어떻게 검증할 것인가?
- diagnostics/support 문서가 agent-friendly하게 구조화되어 있는가?

## Study questions from this session

1. 우리 보안 도구의 CLI/report/log는 Xcode agent가 읽어도 안전한 형태로 설계되어 있는가?
2. 대상 앱이 Xcode agent를 사용해 build setting이나 script를 수정할 때 보안 도구 적용이 깨질 수 있는 known issue가 있는가?
3. protection 적용 전 “plan/check” 단계가 있다면 agent workflow와 연결할 수 있는가?
4. build failure triage 문서를 Apple Document Search처럼 agent가 참고하기 쉬운 형태로 만들 계획이 있는가?
5. Xcode 27 agent 사용을 대상 환경 가이드에서 허용/주의/미지원 중 어떻게 안내할지 정해져 있는가?

## Must-watch chapters

- 7:38 — Explore: codebase walkthrough, architecture documents, Apple Document Search.
- 13:44 — Build: plan mode, queued messages, build/preview/test validation.
- 18:25 — Refine: image attachments, inline annotations, preview-driven iteration.
- 22:09 — Orchestrate: high-level goals, tools, sub-agents, parallel work.

## Source notes

- Apple Developer session page/transcript: https://developer.apple.com/videos/play/wwdc2026/259/
- Apple session 기준 확인한 항목: coding agents in Xcode, Apple Document Search, plan mode, transcript/artifacts, build/preview/test tools, sub-agent orchestration.
- 직접 시청 권장: agent UI와 artifacts flow는 transcript보다 영상으로 이해가 빠르다.
