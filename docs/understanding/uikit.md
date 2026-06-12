# UIKit modernization 이해하기

Source: https://developer.apple.com/videos/play/wwdc2026/278/

## 1. 한 문장으로 먼저 잡기

Modernize your UIKit app은 “UIKit 앱을 새 UI 모양으로 꾸미는 세션”이라기보다, iOS 27/macOS 27 환경에서 iPhone app이 더 자주 resize되고 iPad/Mac 환경에 노출되면서 **scene, screen, idiom, orientation 가정을 최신 방식으로 바꾸는 세션**이다.

보안/toolchain 스터디에서는 이 세션을 “대상 앱이 오래된 UIKit 가정에 묶여 있을 때 보호 적용 후 재현·진단이 어려워지는 지점을 찾는 자료”로 본다.

## 2. UIKit modernization의 핵심 문제

Apple session 기준 iPhone Mirroring on Mac과 iPad에서 iPhone-only app 실행 환경은 더 dynamic해진다. 따라서 앱은 runtime에 주어진 scene size와 environment에 맞춰 조정되어야 한다.

문제는 오래된 UIKit 코드가 다음처럼 고정 가정을 하기 쉽다는 점이다.

1. 앱은 하나의 main screen에서 돈다.
2. orientation은 기기 방향과 거의 같다.
3. user interface idiom으로 layout을 크게 나눌 수 있다.
4. app lifecycle이면 충분하다.
5. full-screen 크기는 launch 이후 크게 변하지 않는다.

새 환경에서는 이런 가정이 틀릴 수 있다. 그래서 modernization은 “새 API를 쓰자”보다 “환경을 고정값으로 보지 말자”에 가깝다.

## 3. 특히 봐야 할 변화

### 3.1 Scene lifecycle

Apple session 기준 최신 SDK로 build할 때 scene lifecycle은 adaptive app의 기반이다. 기존 app lifecycle에 남아 있다면 launch 자체가 영향을 받을 수 있다.

보안/toolchain 관점에서는 launch-time protection, initialization hook, logging, crash handling이 app lifecycle delegate에 강하게 묶여 있는지 확인해야 한다. Scene lifecycle로 이동하면 초기화 위치와 timing이 달라질 수 있다. **추론 / 확인 필요**

### 3.2 Main screen reference 제거

iPhone Mirroring이나 external display 상황에서는 scene이 연결된 screen이 바뀔 수 있다. Apple session은 main screen 대신 window scene에서 동적으로 screen을 얻거나, 가능하면 screen reference 자체를 줄이라고 설명한다.

이것은 layout만의 문제가 아니다.

```text
잘못된 가정
  └─ UIScreen.main 기준으로 scale/bounds 판단

더 나은 질문
  └─ 이 window/scene이 실제로 어느 environment에서 보이는가?
  └─ traitCollection/displayScale/scene bounds로 충분한가?
```

보호 도구가 overlay, watermark, debug view, runtime warning UI를 표시한다면 main screen 가정은 특히 위험할 수 있다. **추론 / 확인 필요**

### 3.3 Idiom과 orientation 가정 줄이기

Apple session은 user interface idiom, interface orientation 같은 legacy 판단을 size class나 trait 기반 판단으로 바꾸는 방향을 제시한다.

보안 스터디에서는 다음 질문으로 바꿔 보면 된다.

> 이 UI가 “iPhone이니까 작다”라고 판단하는가?
> 아니면 “현재 scene의 실제 크기와 trait가 이렇다”라고 판단하는가?

Runtime protection UI, error recovery UI, consent/confirmation UI가 있다면 orientation 변화와 size class 변화에서 가려지거나 잘못 배치되지 않는지 확인해야 한다. **추론 / 확인 필요**

### 3.4 Tab bar, navigation bar, menu 변화

세션은 tab bar, navigation bar, menu 관련 새 API도 다룬다. 이 부분은 보안/toolchain과 직접 관련도는 낮지만, 중요한 action을 어디에 노출할지와 연결될 수 있다.

특히 menu에는 Apple Intelligence와 Siri entry point가 연결될 수 있다. Apple session 기준 관련 content가 있을 때 Ask Siri button이 표시될 수 있고, 앱은 View Annotations API로 app-specific context를 제공할 수 있다.

이것은 agentic feature security와 만나는 지점이다. 어떤 view/context를 Siri나 App Intents에 노출하는지, drag handler가 어떤 resource를 제공하는지, user gesture 없이 drag session callback이 시작될 수 있는지 확인해야 한다. **추론 / 확인 필요**

### 3.5 Agentic coding skill

Apple session은 Xcode 27의 app modernization skill이 main screen call 변환, orientation check 교체, scene lifecycle migration 같은 작업을 도울 수 있다고 설명한다.

이것은 “agent에게 맡기면 끝”이라는 뜻이 아니다. 자동화는 migration 후보를 만들 수 있지만, 실제 앱의 launch flow, analytics, security initialization, UI policy는 사람이 diff와 테스트로 확인해야 한다. **추론**

## 4. UIKit modernization에서 믿는 것과 믿지 않는 것

| 대상 | 믿는가? | 이유 |
|---|---:|---|
| iOS/macOS 27에서 iPhone app resize/adaptivity 요구가 커졌다는 점 | 신뢰 | Apple session summary/transcript에 포함된다. |
| Scene lifecycle, main screen reference, idiom/orientation migration이 중요하다는 점 | 신뢰 | 세션 chapters와 transcript의 핵심 흐름이다. |
| Apple Intelligence entry point와 View Annotations가 UIKit context와 연결된다는 점 | 신뢰 | 세션에서 menu/Siri context 흐름으로 설명된다. |
| 자동 modernization skill이 모든 앱을 안전하게 고친다는 주장 | 믿지 않음 | project-specific side effect와 policy 검토가 필요하다. |
| UIKit 변화가 보안 기능과 직접 충돌한다는 주장 | 믿지 않음 | 현재는 대상 앱별 compatibility checklist로 봐야 한다. |

## 5. 보안/toolchain 관점의 체크리스트

1. 앱이 scene lifecycle을 사용하고 있는가?
2. launch-time security initialization이 scene lifecycle 전환 후에도 같은 조건에서 실행되는가? **확인 필요**
3. `UIScreen.main` 또는 main screen bounds/scale 가정이 남아 있는가?
4. orientation/idiom 기반 조건문을 size class, trait, scene size로 바꿔야 하는가?
5. 보호 관련 overlay, warning, confirmation UI가 resize/iPhone Mirroring/iPad 실행에서 깨지지 않는가? **확인 필요**
6. Menu의 Ask Siri entry point나 View Annotations가 어떤 app context를 노출하는가? **확인 필요**
7. Drag handler가 Siri/Apple Intelligence 호출에서 resource를 제공할 때 user gesture 가정을 하지 않는가? **확인 필요**
8. Agentic modernization 결과를 적용한다면 diff review와 regression test가 있는가?

## 6. 세션을 다시 볼 때 집중할 장면

- iPhone Mirroring on Mac과 iPad에서 iPhone app이 fully resizable해지는 설명
- app lifecycle에서 scene lifecycle로 옮겨야 하는 이유
- main screen reference 대신 scene/window/trait를 쓰는 흐름
- idiom/orientation check를 size class 중심으로 바꾸는 부분
- Device Hub와 resizable simulator로 테스트하는 부분
- Ask Siri button, View Annotations, drag handler 주의점
- Xcode 27 app modernization skill이 자동화할 수 있는 범위와 한계

## 7. 내가 이해했는지 확인하는 질문

1. `UIScreen.main`은 왜 iPhone Mirroring이나 external display 환경에서 위험한 가정이 될 수 있는가?
2. Scene lifecycle migration은 단순 UI 문제가 아니라 launch/security initialization에도 영향을 줄 수 있는가?
3. Idiom과 orientation 대신 size class와 trait를 보라는 이유는 무엇인가?
4. 보호 관련 UI가 resize 환경에서 깨지면 어떤 운영 문제가 생길 수 있는가?
5. Ask Siri/View Annotations/drag handler는 agentic security와 어떤 접점이 있는가?
6. Agentic modernization skill의 결과를 그대로 믿지 않고 검증해야 하는 이유는 무엇인가?

## 8. 이 세션에서 외우지 않아도 되는 것

처음 볼 때는 모든 UIKit API 이름보다 다음 구조를 잡으면 된다.

```text
modern UIKit app
  = scene lifecycle
  + dynamic scene/window/screen 판단
  + trait/size class 기반 layout
  + resize/iPhone Mirroring/iPad 실행 검증
  + Apple Intelligence context 노출 점검

스터디 관점
  = 오래된 UI 환경 가정이 보호 로직·진단·agentic context와 충돌하지 않는지 보는 checklist
```
