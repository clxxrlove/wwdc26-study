# Prompt 02 — Summarize Single Session

아래 WWDC26 세션 transcript 또는 Apple Developer 세션 페이지 내용을 바탕으로 세션 노트를 작성해라.

대상 파일:

- `docs/note-template.md`
- 출력 위치: `sessions/notes/{session_id_or_slug}.md`

관점:

이 세션은 모바일 앱 보안 솔루션 / Xcode build pipeline / Swift Compiler / LLVM Pass 관점에서 검토한다.

반드시 포함할 것:

1. 이 세션이 스터디 범위와 관련 있는지 A/B/C/Skip으로 판단
2. 관련 있다면 왜 관련 있는지
3. 핵심 내용 5줄
4. 새 API / framework / tool / Xcode 기능
5. compiler / build / linker / signing / entitlement / runtime 관련 영향
6. app security / anti-tamper / integrity / obfuscation과 연결되는 내용
7. 기술 영향 추론
8. 후속 질문 3개 이상
9. 영상 전체를 볼 필요가 있는지, transcript만으로 충분한지

작성 규칙:

- 한국어로 작성하되 API와 기술 용어는 영어 유지
- 과장하지 말 것
- transcript에 없는 내용은 “추론” 또는 “확인 필요”로 표시
- Apple이 말한 내용과 내 추론을 분리
- 중요하지 않은 UI 데모 내용은 제외
