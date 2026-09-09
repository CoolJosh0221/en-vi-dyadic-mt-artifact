# Prompt and message structure

This file records the execution structure supported by preserved records and
the manuscript. It does **not** reconstruct unavailable verbatim wording.

| System | BASE | DYAD | SWAPPED |
|---|---|---|---|
| Gemini | Translation-only user instruction plus the English source; no system message | The same user-message structure plus complete speaker, addressee, and directed-relationship profiles | The DYAD structure with speaker and addressee profiles exchanged |
| SEA-LION | Professional-translator system message; English source in the user message | Complete social context added to the system message; English source in the user message | The DYAD structure with speaker and addressee profiles exchanged |
| Google Translate | Byte-identical English source with `en`/`vi` language codes | Not run | Not run |

The contextual prompts supplied factual participant profiles and directed
relationships. They did not prescribe particular Vietnamese pronouns, kin
terms, particles, politeness levels, registers, or request forms.

The separately preserved private generation packet was previously verified to
contain exact templates and rendered request JSON, but those files were not
present in the workspace used to build this artifact. They are therefore not
included here and must not be backfilled from this structural summary.
