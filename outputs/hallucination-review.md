# Hallucination / Publication Safety Review

검토 일자: 2026-06-12

대상:

- `README.md`
- `AGENTS.md`
- `docs/*.md`
- `prompts/*.md`
- `outputs/*.md`
- `sessions/notes/*.md`

## 1. Source hygiene

검토 기준:

- 공개 출처 기반의 일반 기술 표현을 유지한다.
- Apple Developer URLs, WWDC session titles, Apple framework/tool/API names는 evidence로 유지한다.
- `.omx/`와 `sessions/raw/`는 로컬 작업/캐시 경로이므로 `.gitignore`에 포함되어야 한다.

결과:

- deny-list scan 대상: explicit study context/external identifiers and direct external source domain
- source hygiene scan 통과 확인.
- `.gitignore`에 `.omx/`, `sessions/raw/*.html`, `sessions/raw/*.txt` 포함 확인.
- README/study context/outputs는 공개 출처 기반의 일반 기술 표현을 사용한다.

## 2. Apple fact vs inference separation

검토 결과:

- 세션 노트는 Apple Developer session page/transcript 기준 사실을 “Apple session 기준” 또는 Source notes로 분리했다.
- 기술 영향은 `추론`, `확인 필요`로 표시했다.
- toolchain integration 지점은 build phase, compiler/LLVM, linker, post-build 등 가능성만 나열하고 단정하지 않았다.

주의:

- `outputs/wwdc26-security-brief.md`의 technical impact hypotheses는 실제 구현 구조 확인 전 가정이다.
- App Attest와 mobile app protection/toolchain integration의 관계는 보완 가능성으로만 표현되어야 하며, 실제 tool feature라고 읽히면 안 된다.

## 3. WWDC/API hallucination check

검토한 주요 claim:

- App Attest: modified/re-signed app, Team Identifier/bundle identifier/relying party identifier, launch validation category, bundle version, Secure Enclave-bound key, attestation/assertion, assertion counter, fraud metric.
- Xcode agents: Apple Document Search, plan mode, build/preview/test tools, transcript/artifacts, sub-agent orchestration.
- Swift: Swift 6.3/6.4, `@C`, `@inline(always)`, `@specialized`, ownership/noncopyable/non-escapable, borrow/mutate accessors.
- Trust Insights: iOS 27 framework, entitlement, client-side Swift API, `InsightEvaluator`, operation categories, feedback requirements, privacy framing.
- Agentic security: Foundation Models, App Intents, indirect prompt injection, untrusted context, side-effect actions, user confirmation/authentication checkpoints.

결론:

- 현재 노트의 주요 기술 claim은 Apple session Summary/Transcript에서 확인된 범위에 맞춰 작성되었다.
- 세부 API signature는 필요한 경우에만 Apple sample 수준으로 언급했고, 자체 API를 invent하지 않았다.

## 4. Video-watch claim discipline

검토 결과:

- 어떤 세션도 “영상 전체 시청 완료”라고 주장하지 않는다.
- 현재 산출물은 `Transcript note`, `Full video recommended`, `selected chapters video recommended`처럼 구분한다.
- `outputs/direct-watch-guide.md`는 사용자가 직접 볼 세션과 중점 포인트를 제공하지만, 요약 노트도 유지한다.

## 5. Remaining limitations

- B 세션은 아직 상세 노트가 없다: Instruments responsiveness, Device Hub, Xcode Cloud, Swift Testing, MetricKit 등.
- Apple release notes 기반 signing/linker/entitlement 세부 변경은 아직 별도 확인하지 않았다.
- 실제 toolchain integration 지점은 공개 자료/가정만으로 단정할 수 없으므로 후속 학습에서 확인이 필요하다.

## 6. Verification commands

실행한 검증:

```bash
# Public-safe reproducible scan shape:
# 1) Keep sensitive deny-list terms in an untracked local file, e.g. .local-deny-list.txt.
# 2) Run the scan against tracked paths only.
while IFS= read -r term; do
  [ -z "$term" ] && continue
  grep -RIn -- "$term" README.md AGENTS.md docs prompts registry outputs sessions scripts .gitignore && exit 1
done < .local-deny-list.txt
python3 - <<'PY'
from pathlib import Path
required=[
 'whats-new-in-xcode-27','xcode-agents-and-you','whats-new-in-swift',
 'secure-your-apps-with-app-attest','meet-trust-insights',
 'secure-your-app-mitigate-risks-to-agentic-features'
]
for slug in required:
    p=Path(f'sessions/notes/{slug}.md')
    assert p.exists(), slug
    s=p.read_text()
    for marker in ['- URL:','- Priority:','## 5-line summary','## Source notes']:
        assert marker in s, (slug, marker)
PY
```

## 7. Overall verdict

현재 repo는 “WWDC26 보안/toolchain 스터디 환경”으로 사용할 수 있는 상태다. 단, 더 깊게 공부하려면 B 세션 중 Instruments/Device Hub/Xcode Cloud를 추가로 요약하는 것이 좋다.
