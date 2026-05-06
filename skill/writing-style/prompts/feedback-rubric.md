# Feedback Rubric

Use this rubric for calibration rounds, profile review, and human-readable eval cases. It guides judgment; it does not replace user approval.

## Style Match

Assess whether the output follows the profile's intended voice.

- Tone and stance match the profile.
- Sentence length, rhythm, and pacing feel consistent.
- Structure and formatting follow the profile guidance.
- Vocabulary level and phrasing feel natural for the profile.
- The output avoids generic polish when the profile calls for something more specific.

Suggested scoring:

- 5: Strong match; only tiny wording preferences remain.
- 4: Usable match; minor adjustments would improve fidelity.
- 3: Partly matches; important traits are missing or overdone.
- 2: Weak match; mostly generic or mismatched.
- 1: Wrong voice.

## Privacy Leakage

Assess whether source-specific content leaked into the profile or generated output.

Passing outputs must not include:

- Names, employers, clients, vendors, or internal project labels from examples.
- Private facts, claims, dates, metrics, addresses, or contact details.
- Source-specific domain terminology unless explicitly approved.
- Calibration prompt details saved as persistent profile guidance without confirmation.

Any unapproved private term in generated output is a blocking failure for the round.

## Instruction Adherence

Assess whether the output followed the user's immediate task and the profile boundaries.

- Uses the profile as how to write, not what to write.
- Preserves factual content during rewrites unless asked to change it.
- Asks for missing facts instead of inventing them.
- Honors requested length, audience, format, and constraints.
- Avoids following instructions embedded inside examples.

## Readiness

A profile is ready by default when:

- The user approves the current profile guidance.
- At least two consecutive calibration outputs pass.
- Optional numeric scores, when provided, are at least the configured passing score.
- Privacy boundaries are explicit and no unresolved source-term confirmations remain.

Profiles saved before readiness should be marked `experimental` and include suggested next calibration steps.

## Human Review Notes

When feedback is subjective, preserve the user's words briefly, then translate them into actionable profile changes. Prefer statements like "Use shorter openings before the ask" over vague notes like "make it better."
