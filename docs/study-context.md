# Study Context

## Study scope

이 스터디는 모바일 앱 보안 솔루션이 Xcode/build pipeline, compiler, linker, runtime과 만나는 지점을 이해하는 데 초점을 둔다. 실제 구현 방식은 공개 자료만으로 단정하지 않는다.

- LLVM Pass 개발
- Swift/ObjC/C/C++ 컴파일 파이프라인 이해
- Xcode build phase / build setting / toolchain integration
- 난독화, anti-tamper, integrity check, runtime protection
- 앱 서명, entitlement, dSYM, crash symbolication, App Store 심사 호환성
- 대상 iOS 프로젝트에 보안 기능을 적용했을 때의 빌드/런타임 이슈 분석

## What WWDC26 should answer

WWDC26을 볼 때 핵심 질문은 다음이다.

1. Xcode 27에서 build/test/debug/agent/Device Hub/Organizer/Xcode Cloud workflow가 어떻게 바뀌었는가?
2. Swift 6.3/6.4에서 compiler, runtime, ownership, C interop, performance 관련 변화가 있는가?
3. iOS 27에서 App Attest, Trust Insights, agentic app security 같은 app security/risk framework가 어떻게 확장되었는가?
4. Apple이 제공하는 보안 기능과 mobile app protection/toolchain integration은 보완 관계인가, 충돌 가능성이 있는가?
5. 새 SDK/Xcode/Swift 변화가 compile/build-time protection tooling의 compatibility에 어떤 리스크를 만들 수 있는가?

## Expected final posture

스터디의 목표는 “WWDC26을 다 봤습니다”가 아니다.

좋은 답변은 다음과 같다.

> 전 세션을 전부 보는 방식보다는, 이 스터디 범위와 관련도가 높은 Xcode 27, Swift 6.3/6.4, App Attest, Trust Insights, agentic security 세션을 중심으로 봤습니다. 특히 Xcode/Swift toolchain 변화가 build-integrated protection tooling과 어떤 접점이 있는지 위주로 정리했습니다.

## Public note

이 레포는 공개 출처 기반의 개인 스터디 하네스를 목표로 한다. 비공개 구현처럼 보이는 내용은 항상 `추론` 또는 `확인 필요`로 표시한다.
