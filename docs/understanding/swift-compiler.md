# Swift 6.3/6.4를 compiler compatibility 관점에서 이해하기

Source: https://developer.apple.com/videos/play/wwdc2026/262/

## 1. 이 세션을 보는 관점

`What’s new in Swift`는 language feature가 많다. 하지만 보안/toolchain 관점에서는 “새 문법을 외우기”보다 다음 질문이 중요하다.

> Swift compiler가 만들어내는 symbol, ABI boundary, optimization 결과, ownership model이 바뀌면 protection/obfuscation/debugging은 어떤 영향을 받을 수 있는가?

## 2. 특히 봐야 할 변화

### `@C`

Swift function을 C-compatible interface로 export하는 기능이다.

왜 중요한가?

- Swift code가 C/ObjC/C++ boundary로 노출될 수 있다.
- exported symbol 정책과 난독화 정책이 달라질 수 있다.
- Swift-only라고 생각한 코드가 C ABI 관점에서 관측될 수 있다.

이것은 “무조건 위험하다”가 아니라 compatibility test에 넣어야 할 feature로 보는 것이 적절하다. **추론**

### `@inline(always)` / `@specialized`

optimizer control에 가깝다.

왜 중요한가?

- helper/runtime code가 inline되면 binary size와 hot path가 달라질 수 있다.
- specialization은 generic code의 code generation 양상을 바꿀 수 있다.
- obfuscation이나 instrumentation이 optimization과 충돌할 가능성을 확인해야 한다.

### ownership / noncopyable / borrow / mutate

Swift가 memory safety와 performance를 위해 ownership model을 더 명시적으로 다루는 흐름이다.

왜 중요한가?

- compiler transformation이 value lifetime과 ownership assumption을 깨면 안 된다.
- copy elision, borrow semantics, noncopyable type은 단순한 source rewrite나 IR transform에서 edge case가 될 수 있다.
- performance regression을 볼 때 불필요한 copy가 줄어드는 코드와 보호 삽입 코드가 어떻게 상호작용하는지 봐야 한다.

## 3. Swift 변화가 보안 도구와 만나는 지점

```text
Swift source
  ↓
Swift compiler frontend
  ↓
SIL / optimization
  ↓
LLVM IR
  ↓
Mach-O binary
  ↓
runtime behavior
```

보안 도구가 어느 단계에 붙는지에 따라 신경 써야 할 Swift 변화가 달라진다.

- source-level이면 새 syntax 대응이 중요하다.
- SIL/LLVM IR 단계이면 optimizer와 ownership lowering 결과가 중요하다.
- binary 단계이면 symbol, section, debug info, Swift metadata가 중요하다.
- runtime 단계이면 Swift concurrency/ownership/runtime behavior가 중요할 수 있다.

실제 통합 단계는 공개 자료만으로 단정하지 않는다. **확인 필요**

## 4. 이해 확인 질문

1. `@C`가 늘어나면 exported symbol과 obfuscation 정책에 어떤 질문이 생기는가?
2. `@inline(always)`가 protection runtime/helper code size에 영향을 줄 수 있는 이유는 무엇인가?
3. noncopyable/borrow feature는 왜 transformation correctness test에 들어가야 할 수 있는가?
4. Swift source, SIL, LLVM IR, Mach-O 중 어느 단계에서 도구가 동작하는지에 따라 필요한 test가 어떻게 달라지는가?
