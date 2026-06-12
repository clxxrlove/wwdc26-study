# Priority Rubric

## A — Must review

A 세션은 영상 또는 transcript 전체를 보고 세션 노트를 작성한다.

조건:

- Xcode, Swift Compiler, build system, toolchain, agent/plugin integration과 직접 관련
- iOS security, app integrity, anti-tamper, App Attest, Trust Insights와 직접 관련
- LLVM Pass 기반 보안 도구의 호환성/전략에 영향을 줄 수 있음

예상 예시:

- What’s new in Xcode 27
- Xcode, agents, and you
- What’s new in Swift
- Secure your apps with App Attest
- Meet Trust Insights
- Secure your app: mitigate risks to agentic features

## B — Review transcript

B 세션은 transcript 기반으로 훑고, 필요할 때만 영상 일부를 본다.

조건:

- 개발자 workflow, diagnostics, testing, profiling과 관련
- 대상 앱이 새 도구를 사용하는 방식 이해에 도움
- 보안 보안 도구의 직접 구현과는 거리가 있지만 맥락상 유용

예상 예시:

- Profile, fix, and verify: Improve app responsiveness with Instruments
- Get the most out of Device Hub
- Build, deliver, and automate with Xcode Cloud
- Migrate to Swift Testing
- Debug and profile agentic app experiences with Instruments

## C — Skim only

C 세션은 목록/summary만 보고 필요 시 제외한다.

조건:

- 일반 iOS 앱 개발자로서는 유용하지만 보안 솔루션/컴파일러 관점 관련도 낮음
- SwiftUI, UIKit, AppKit 등 일반 UI 업데이트 중심

## Skip

제외한다.

조건:

- 디자인/마케팅/visionOS/game 중심이며 현재 스터디 범위와 접점이 거의 없음
- 최종 학습 노트에 넣어도 보안/toolchain 이해에 직접 기여하지 않음
