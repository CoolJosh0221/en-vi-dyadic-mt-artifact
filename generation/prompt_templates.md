# Prompt templates

All 210 rendered requests are in `rendered_requests.jsonl`, verbatim as sent
(`request` holds the provider request body; credentials were never persisted).
The templates below are derived from those requests; `analysis/verify_aggregates.py`
checks that every rendered request matches its template exactly.

## Gemini (`v1beta generateContent`; no system message; `generationConfig`: temperature 0, maxOutputTokens 1024)

BASE, single user part:

```
Translate the following English sentence into Vietnamese. Output only the translation, nothing else.

{english_source}
```

DYAD and SWAPPED, single user part (SWAPPED exchanges the two profiles and reverses the relationship line):

```
Translate the following English sentence into Vietnamese.
Social context:
- Speaker profile: role=...; age=30; gender=woman; language=native Vietnamese speaker; employer=the same company; familiarity=...; setting=...; status=...; title=...; institutional role=...
- Addressee profile: role=...; age=30; gender=woman; language=native Vietnamese speaker; employer=the same company; familiarity=...; setting=...; status=...; title=...; institutional role=...
- Relationship (speaker -> addressee): {label}; {who is writing to whom}; {relative rank}
Output only the translation, nothing else.

{english_source}
```

## SEA-LION (Ollama `/api/chat`; `options`: temperature 0, num_predict 1024, num_ctx 4096, seed 42; stream false)

BASE: system message, then the English source as the user message.

```
You are a professional translator. Translate the user message from English to Vietnamese. Output only the Vietnamese translation, nothing else.
```

DYAD and SWAPPED: system message with the same social-context block as Gemini, then the English source as the user message.

```
You are a professional translator. Translate the user message from English to Vietnamese.
Social context:
- Speaker profile: ...
- Addressee profile: ...
- Relationship (speaker -> addressee): ...
Output only the Vietnamese translation, nothing else.
```

## Google Translate (`googletrans` 4.0.2)

BASE only: the byte-identical English source with `source_language=en`, `target_language=vi`. No social context.

The profile values are the released `sender_profile`, `recipient_profile`, and
`relationship` fields of `data/source_requests.jsonl` (intended direction), or the
same two profiles exchanged (SWAPPED). No prompt prescribed Vietnamese pronouns,
kin terms, particles, politeness levels, registers, or request forms.
