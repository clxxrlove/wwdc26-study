# What’s new in Swift

- URL: https://developer.apple.com/videos/play/wwdc2026/262/
- Duration: 약 32분
- Category: Swift / Compiler / Language / Runtime-adjacent performance
- Priority: A
- Review mode: Transcript first + selected video for compiler/performance chapters
- Last updated: 2026-06-12

## Why this matters to this study

- Apple session 기준 Swift 6.3/6.4는 language improvements, library updates, cross-platform support, performance tuning을 다룬다.
- LLVM Pass 또는 compile-time protection 관점에서는 `@C`, optimizer control, ownership/noncopyable/borrow/mutate, Embedded Swift/DWARF 개선이 특히 중요하다.
- 이 세션은 iOS app security 자체보다 Swift compiler/language evolution이 대상 앱과 보호 도구 호환성에 미칠 수 있는 영향을 파악하기 위한 A 세션이다.

## 5-line summary

1. Swift 6.4는 optional `some/any` parentheses 완화, concurrency task error warning, `weak let`, `~Sendable`, memberwise initializer 등 everyday language 개선을 제공한다.
2. `anyAppleOS` availability와 `@diagnose`, module selector `::`는 multi-platform code와 warning control/name conflict 해결을 돕는다.
3. Swift 6.4의 `@C` attribute는 Swift function을 C에 노출해 C codebase의 incremental migration을 돕는다.
4. Swift 6.4의 `@inline(always)`와 Swift 6.3의 `@specialized`는 optimizer decision을 개발자가 직접 제어하는 고급 performance tuning 기능이다.
5. Ownership system은 noncopyable/non-escapable types, borrow/mutate accessors, UniqueBox/UniqueArray/Ref 계열을 통해 unnecessary copy를 줄이는 방향으로 확장된다.

## New APIs / tools / frameworks

| Name | Type | Notes | Relevance |
|---|---|---|---|
| `anyAppleOS` availability | Language availability | 여러 Apple OS availability 조건을 하나로 줄임. | multi-platform SDK 코드 boilerplate 감소. |
| `@diagnose` | Diagnostic attribute | 특정 declaration 안에서 warning suppress/enable/promote 가능. | warning/error policy와 migration 관리에 유용. |
| Module selector `::` | Language syntax | name conflict 시 특정 module type/member를 명시. | 대형 대상 앱 name collision 대응. |
| `@C` | Swift-C interop | Swift function을 C-compatible interface로 export. | Swift/C 혼합 코드와 protection boundary 이해에 중요. |
| `@inline(always)` | Optimizer control | optimizer가 망설이는 경우에도 inlining 강제. | 보호 runtime/helper hot path 최적화 검토에 관련. |
| `@specialized` | Optimizer control | generic function 특정 type constraint specialization 생성. | generic-heavy 보호 코드 성능 튜닝에 관련. |
| Ownership/noncopyable expansion | Language/performance | noncopyable/non-escapable types와 protocols, borrow/mutate accessors 확장. | copy 비용과 memory safety 이해에 중요. |
| Embedded Swift DWARF improvements | Tooling/debug info | constrained hardware coredump debugging 관련 개선 언급. | debug info 보존 관점에서 참고. |

## Toolchain / compiler / build implications

- `@inline(always)`와 `@specialized`는 compiler optimizer decision에 직접 개입한다. 보호 코드가 hot path에 들어가면 이런 attribute 사용 여부가 성능/size tradeoff에 영향을 줄 수 있다. **추론**.
- `@C`는 Swift와 C boundary를 넓힌다. Swift 보호 로직과 C/ObjC/C++ 보호 로직이 서로 다른 단계에서 적용된다면 symbol/export boundary 검토가 필요하다. **확인 필요**.
- Ownership/noncopyable/borrow/mutate 기능 확장은 Swift codegen과 copy semantics 이해를 요구한다. 난독화나 IR transformation이 ownership assumptions를 깨지 않는지 검증해야 한다. **추론 / 확인 필요**.
- `@diagnose`와 module selector는 대상 코드 migration/compatibility 이슈를 줄이는 도구로 볼 수 있다.

## Security / anti-tamper / integrity implications

- 세션은 보안 framework를 직접 다루지 않는다.
- 보안 도구 관점에서는 Swift compiler/language 변화가 보호 변환의 안정성, debug symbol, performance overhead, C interop boundary에 주는 영향을 봐야 한다.
- optimizer control attribute는 보호 코드가 inlined/specialized되며 binary size와 reverse engineering surface에 영향을 줄 수 있다. **추론**.

## Security/toolchain impact hypothesis

> 추론: Swift 6.3/6.4는 앱 보안 기능 자체보다 보호 도구의 compatibility matrix와 성능 tuning 관점에서 중요하다. 특히 Swift-C interop, optimizer control, ownership/noncopyable 확장은 Swift-heavy 대상 앱에서 compiler-level transformation을 수행할 때 test corpus에 포함해야 할 변화다.

## Risks / compatibility questions

- 보안 도구가 Swift SIL/LLVM IR/binary 중 어느 단계에서 Swift 코드를 다루는가? **확인 필요**.
- `@C`로 export된 Swift function이나 C-compatible boundary를 보호 도구가 어떻게 인식하는가?
- `@inline(always)`/`@specialized`가 적용된 함수에 obfuscation/instrumentation을 넣을 때 code size/performance가 어떻게 변하는가?
- noncopyable/borrow/mutate semantics를 포함한 Swift 6.3/6.4 sample에 대한 regression test가 있는가?
- debug info/dSYM/symbolication 보존 정책이 최신 Swift compiler output과 호환되는가?

## Study questions from this session

1. Swift 코드 보호는 Swift compiler output의 어느 단계에서 적용되는가? SIL, LLVM IR, Mach-O/binary 중 어디에 가까운가?
2. Swift 6.3/6.4 language feature를 포함한 compatibility test app이 있는가?
3. optimizer control attribute가 붙은 hot path 함수에 보호 코드를 넣을 때 성능/size 기준은 어떻게 잡는가?
4. Swift-C interop boundary(`@C`, C headers, exported symbols)는 보호/난독화 정책에서 어떻게 다루는가?
5. noncopyable/ownership 관련 feature가 보호 변환의 correctness에 영향을 준 사례가 있는가?

## Must-watch chapters

- 12:35 — Swift–C Interoperability (`@C attribute`): Swift/C boundary 확인.
- 21:29 — Performance Tuning: optimizer control과 ownership system 개요.
- 24:29 — `@inline(always)` / `@specialized`: compiler optimization control.
- 26:18 이후 — ownership/noncopyable/borrow/mutate accessors.
- 전체 영상은 필수는 아니며 transcript로 키워드 확인 후 위 chapter 시청 권장.

## Source notes

- Apple Developer session page/transcript: https://developer.apple.com/videos/play/wwdc2026/262/
- Apple session 기준 확인한 항목: Swift 6.3/6.4, `@C`, `@inline(always)`, `@specialized`, ownership/noncopyable/non-escapable, borrow/mutate accessors, module selector, `@diagnose`, `anyAppleOS`.
