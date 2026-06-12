# SwiftUI 2027 변화 이해하기

Source: https://developer.apple.com/videos/play/wwdc2026/269/

## 1. 한 문장으로 먼저 잡기

What’s new in SwiftUI는 UI framework 신기능 목록이지만, 이 스터디에서는 “앱이 더 많이 resize되고, 더 많은 document/data flow를 framework에 맡기며, performance 기본값이 바뀔 때 보안/toolchain 검증에서 무엇을 봐야 하는가”를 이해하는 세션으로 본다.

즉, 핵심은 예쁜 UI가 아니라 **layout, document I/O, data flow, caching 변화가 기존 앱 동작과 검증 방식에 미치는 영향**이다.

## 2. 이 세션을 낮은 우선순위로 보되 버리면 안 되는 이유

`outputs/watch-priority.md`는 SwiftUI를 “UI framework 중심”이라서 skim 대상으로 분류한다. 그래도 완전히 제외하지 않는 이유가 있다.

1. SwiftUI 앱은 새 OS appearance와 resizable behavior를 자동으로 얻을 수 있다.
2. Document 기반 앱은 disk access와 snapshot/diffing 모델을 쓴다.
3. AsyncImage caching과 `@State` lazy initialization처럼 성능·lifetime 기본값이 달라진다.
4. UIKit과 섞인 앱은 geometry, size class, orientation 처리에서 추가 검토가 필요하다.

보안/toolchain 관점에서는 “SwiftUI API를 자세히 배우기”보다 “대상 앱이 이 변화 때문에 테스트해야 할 표면이 늘어나는가”를 보는 것이 맞다.

## 3. 특히 봐야 할 변화

### 3.1 Resizable app과 Live Preview

Apple session 기준 SwiftUI 앱은 새 platform release에서 resizable 환경과 refreshed look을 많이 자동으로 얻는다. Xcode 27 Live Previews에는 resize handle이 있어 iPhone Mirroring이나 iPad에서 iPhone app이 resize되는 상황을 미리 볼 수 있다.

이것은 보안 기능 자체와 직접 연결되지는 않는다. 다만 보호 SDK나 runtime check가 view lifecycle, scene size, preview/build configuration에 영향을 준다면 resize 상황에서 side effect가 드러날 수 있다. **추론 / 확인 필요**

### 3.2 Document protocol

세션은 새 Document protocol을 direct disk access와 snapshot 기반 diffing 관점에서 소개한다.

이 흐름은 다음처럼 이해하면 된다.

```text
앱 상태
  └─ snapshot으로 문서 상태 표현
      └─ diff/write/read 흐름을 framework가 다룸
```

보안/toolchain 관점에서는 document 저장 경로, temporary file, package format, snapshot serialization이 중요해질 수 있다. 예를 들어 보호 도구가 resource나 file coordination에 영향을 준다면 document save/load 회귀를 확인해야 한다. **추론 / 확인 필요**

### 3.3 Reordering, presentation, interaction

Apple summary 기준 SwiftUI에는 list, grid, section 등에서 content reordering을 지원하는 API와, 특정 view에 더 넓게 적용되는 swipe action/presentation API가 추가된다.

이 변화는 보안 기능보다 사용자 interaction surface에 가깝다. 하지만 권한 있는 action, destructive action, agentic feature entry point가 UI interaction과 연결되어 있다면 “사용자가 의도한 action인지”를 다시 확인해야 한다. **추론**

### 3.4 AsyncImage caching

Apple session 기준 AsyncImage는 standard HTTP caching을 기본 지원하고, 앱은 URLRequest나 URLSession 설정으로 다운로드 방식을 조정할 수 있다.

이것을 보안 스터디에서 볼 때는 두 가지를 분리해야 한다.

- 성능 관점: 스크롤 중 이미지 재다운로드가 줄어들 수 있다.
- 데이터 관점: cache header, URLRequest policy, URLCache capacity가 앱의 resource lifecycle에 영향을 준다.

민감한 이미지를 다룬다는 식의 단정은 하지 않는다. 다만 앱이 remote image를 인증 상태나 사용자 context와 연결해 보여준다면 cache 정책은 별도 확인 대상이다. **추론 / 확인 필요**

### 3.5 `@State` lazy initialization

Apple session은 `@State`가 macro로 변환되어 Observable class 초기화가 lazy해지고 불필요한 allocation을 줄일 수 있다고 설명한다.

이 변화는 앱 code가 더 적게 실행되는 방향일 수도 있고, 초기화 시점이 달라지는 방향일 수도 있다. 따라서 side effect가 있는 initializer에 의존하는 앱이라면 lifecycle 가정을 점검해야 한다. **추론 / 확인 필요**

## 4. SwiftUI에서 믿는 것과 믿지 않는 것

| 대상 | 믿는가? | 이유 |
|---|---:|---|
| Document protocol, reordering API, toolbar/presentation/API 변화 | 신뢰 | Apple session summary와 chapters에 포함된다. |
| AsyncImage 기본 HTTP caching | 신뢰 | Apple transcript/summary가 설명한다. |
| `@State` lazy initialization이 모든 앱 성능을 개선한다는 주장 | 믿지 않음 | 앱의 initializer side effect와 data flow에 따라 다르다. |
| SwiftUI 변화가 보안 도구와 직접 충돌한다는 주장 | 믿지 않음 | 현재는 compatibility checklist 수준의 추론이다. |
| UI 변화가 보안 검증과 무관하다는 주장 | 믿지 않음 | action, document, cache, lifecycle 표면은 간접적으로 영향을 줄 수 있다. |

## 5. 보안/toolchain 관점의 체크리스트

1. 대상 앱이 SwiftUI document-based app인가?
2. Document snapshot/save/load 경로가 보호 적용 전후에 동일하게 동작하는가? **확인 필요**
3. Remote image cache 정책이 앱의 privacy/security expectation과 충돌하지 않는가? **추론 / 확인 필요**
4. Observable object initializer에 side effect가 있는가?
5. `@State` lazy initialization 때문에 side effect timing이 달라질 수 있는가? **확인 필요**
6. Resize/preview/iPhone Mirroring 상황에서 scene geometry 가정이 깨지지 않는가?
7. SwiftUI와 UIKit을 섞은 앱에서 size class와 orientation 처리 방식이 최신 권장 흐름과 맞는가?

## 6. 세션을 다시 볼 때 집중할 장면

- Xcode 27 Live Preview resize handle로 resizable behavior를 확인하는 부분
- Document protocol과 snapshot/diffing 설명
- list/grid/section reordering과 swipe action/presentation 변화
- AsyncImage HTTP caching과 custom URLRequest/URLSession 설정
- `@State` macro/lazy initialization 설명
- UIKit 혼합 앱은 별도 고려가 필요하다고 연결되는 부분

## 7. 내가 이해했는지 확인하는 질문

1. SwiftUI 변화가 직접 보안 기능은 아니어도 compatibility checklist에 들어가는 이유는 무엇인가?
2. Document snapshot model은 기존 file save/load 테스트와 어떤 점이 다른가?
3. AsyncImage caching은 성능 개선 외에 어떤 검토 질문을 만들 수 있는가?
4. `@State` lazy initialization은 side effect가 있는 initializer에 어떤 질문을 던지는가?
5. Resizable app 검증은 왜 단순 screenshot 확인으로 끝나지 않는가?
6. SwiftUI/UIKit 혼합 앱에서 geometry 판단을 어떤 기준으로 다시 봐야 하는가?

## 8. 이 세션에서 외우지 않아도 되는 것

처음 볼 때는 모든 modifier 이름보다 다음 구조를 잡으면 된다.

```text
SwiftUI 2027 변화
  = 자동 appearance/resizability
  + document snapshot/diffing
  + interaction/reordering 확장
  + AsyncImage cache 기본값
  + @State lazy initialization

스터디 관점
  = 직접 보안 기능이 아니라 앱 동작/검증 표면을 넓히는 compatibility signal
```
