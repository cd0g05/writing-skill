---
summary: "Writing Skill should feel like a careful writing coach and librarian: it guides the user through creating local style profiles, keeps privacy boundaries explicit, uses neutral calibration prompts by default, and makes every saved style inspectable before reuse. The experience is conversational rather than visual-app-driven, with local files as the durable interface and clear confirmations around sanitization, profile inheritance, settings changes, and profile readiness."
phase: "ux"
when_to_load:
  - "When designing or reviewing Writing Skill journeys, flows, states, copy, and interaction constraints."
  - "When implementation questions depend on the profile creation, calibration, privacy, or local-file experience."
depends_on:
  - "prd.md"
modules:
  - "LLM skill workflow"
  - "Local profile files"
  - "Settings/config interaction"
  - "Calibration and feedback loop"
index:
  design_goals: "## Design Goals & Constraints"
  journeys: "## User Journeys & Touchpoints"
  information_architecture: "## Information Architecture"
  key_flows: "## Key User Flows"
  ui_states: "## UI States"
  copy_tone: "## Copy & Tone"
  visual_design: "## Visual Design Direction"
  consistency: "## UX Consistency Patterns"
  accessibility: "## Responsive & Accessibility"
next_section: "Tech Design"
---

# UX Design: Writing Skill

## Progress

- [x] Design Goals & Constraints
- [x] User Journeys & Touchpoints
- [x] Information Architecture
- [x] Key User Flows
- [x] UI States
- [x] Copy & Tone
- [x] Visual Design Direction
- [x] UX Consistency Patterns
- [x] Responsive & Accessibility

---

## Design Goals & Constraints

**Primary goal:** The experience should make the user feel that they are teaching a patient, privacy-conscious writing coach how to write like them. The skill should reduce the blank-page burden of prompt engineering while preserving user control over what gets saved.

**Design constraints:**
- The primary surface is an agent conversation, not a graphical app.
- The durable product surface is local files: profile files, config/settings, and later eval artifacts.
- The skill must work for one user first, but should not hard-code Carter-only assumptions into the interaction model.
- The skill must distinguish style from content at every important point.
- The skill must default to sanitization, neutral prompts, and explicit confirmation for risky overrides.
- The skill should not require a complete set of examples; it can fall back to targeted questions and neutral calibration.

**Experience principles:**
- **Ask just enough:** Prefer a short focused question over a long intake form.
- **Show the working model:** The user should see the inferred style hypothesis before it becomes a saved profile.
- **Make risk visible:** Privacy-affecting choices should be named plainly and confirmed.
- **Treat files as product UI:** Saved profiles should be readable, organized, and useful without hidden state.
- **Calibrate through contrast:** Show outputs, ask what feels right/wrong, then summarize what changed.

---

## User Journeys & Touchpoints

### Carter — Building a Personal Email Style

**Entry point:** Carter invokes the skill to create a new style, e.g. "create a writing style called `email-professional`."
**First touchpoint:** The skill confirms the profile name, explains that examples will be used for style rather than facts, and asks Carter to paste examples or continue with questions.
**Key moment:** Carter sees the first style hypothesis and thinks, "Yes, that is close to how I write, and it did not copy work details."
**Exit state:** A local `email-professional` profile exists, marked ready or experimental, with usage instructions for future writing and rewriting.
**Pain points to design around:** Anxiety about private content, uncertainty about how many examples are needed, fatigue from grading too many samples, and distrust if the model overgeneralizes from one example.

---

### Carter — Forking a Style for a New Context

**Entry point:** Carter asks to create `email-neutral` from `email-professional`.
**First touchpoint:** The skill loads the source profile, summarizes it, and asks what should change in the new profile.
**Key moment:** Carter sees a before/after comparison that clarifies the difference between the source and forked style.
**Exit state:** A separate local file exists for the new style, with a source-profile reference and a concise explanation of what changed.
**Pain points to design around:** Accidentally modifying the source profile, creating a fork with no meaningful distinction, and losing track of profile relationships.

---

### Future User — Creating a Presentation Style

**Entry point:** A user invokes the skill after installation and asks to create a `presentation` style.
**First touchpoint:** The skill explains profile creation in plain language and offers examples, questions, or both.
**Key moment:** Even with few source examples, the user gets useful neutral calibration prompts and can shape the style through feedback.
**Exit state:** A reusable profile captures how presentations should sound and be structured, without containing presentation topics unless explicitly approved.
**Pain points to design around:** Confusion about what a "style profile" is, uncertainty over writing versus rewriting, and wanting advanced options without being forced through them up front.

---

## Information Architecture

### Local Artifact Map

```text
writing-skill/
├── config.json
├── profiles/
│   ├── email-professional.md
│   ├── email-neutral.md
│   └── presentation.md
├── prompts/
│   └── neutral-calibration-prompts.md
└── evals/
    ├── eval-spec.md
    └── cases/
```

### Profile File Structure

```text
Profile: {profile-name}
├── Metadata
│   ├── status
│   ├── source profile
│   ├── created/updated dates
│   └── privacy mode
├── Purpose and Use Cases
├── Style Traits
├── Structure and Formatting
├── Do / Do Not Rules
├── Privacy and Content Boundaries
├── Calibration Summary
├── Invocation Examples
└── Change Notes
```

### Navigation Model

**Primary nav:** Conversational commands and local filenames.
**Secondary nav:** The skill should offer numbered choices for multi-path decisions.
**Key entry points:**
- Create a new profile.
- Create a profile from an existing profile.
- Update/recalibrate a profile.
- Use a profile for a writing or rewriting task.
- Change settings/config.

The user should never need to memorize the folder structure during normal use; the skill should surface profile names and file paths when relevant.

---

## Key User Flows

### Flow 1: Create a Profile From Examples

1. User asks to create a profile, optionally naming it.
2. Skill confirms the profile name and profile type if ambiguous.
3. Skill states the default privacy behavior: examples are used for style, not facts.
4. User provides examples, skips examples, or asks what examples are useful.
5. Skill runs a sanitization/style extraction pass.
6. Skill presents a style hypothesis with sections for tone, structure, rhythm, vocabulary, formatting, and exclusions.
7. User approves or edits the hypothesis.
8. Skill generates one or more neutral calibration samples.
9. User gives freeform feedback and optional score.
10. Skill updates the profile draft and summarizes what changed.
11. Steps 8-10 repeat until the readiness rule is met or the user saves as experimental.
12. Skill writes the local profile file and shows invocation examples.

**Alternate path A:** If the user has no examples, the skill asks targeted style questions and proceeds to neutral calibration.
**Alternate path B:** If the user wants to use custom prompts, the skill asks whether those prompts are one-time calibration prompts or should influence future defaults.
**Alternate path C:** If the user asks to retain a source-specific term, the skill explains the privacy tradeoff and asks for confirmation.

---

### Flow 2: Fork a Profile

1. User asks to create a new profile from an existing profile.
2. Skill lists matching source profiles if needed.
3. User selects the source profile and new profile name.
4. Skill summarizes the source profile and asks what should change.
5. User gives directional feedback, such as "less formal" or "more concise."
6. Skill creates a proposed style diff.
7. Skill generates comparison samples using the source style and new style.
8. User gives feedback.
9. Skill saves the new profile as a separate file with source-profile metadata.

**Alternate path A:** If the new profile is too similar, the skill asks whether to keep it as a distinct style or update the source profile instead.
**Alternate path B:** If the user tries to overwrite the source profile, the skill asks for explicit confirmation.

---

### Flow 3: Use a Saved Profile

1. User asks to write or rewrite using a profile.
2. Skill loads the named profile or asks the user to choose from available profiles.
3. Skill asks for the actual writing task content if missing.
4. Skill applies the profile as "how to write" instructions while treating the user's request as "what to write."
5. Skill produces the requested output.
6. Skill asks whether the output should update the profile, be ignored, or be treated as one-time feedback.

**Alternate path A:** If the profile is experimental, the skill warns that the style is not fully calibrated.
**Alternate path B:** If the task asks for facts not provided, the skill asks for the missing content rather than inventing.

---

### Flow 4: Change Settings

1. User asks to change a default setting.
2. Skill explains the current value and the proposed new value.
3. If the setting affects privacy, retention, or confirmation behavior, the skill explains the risk plainly.
4. User confirms.
5. Skill updates `config.json` and summarizes the effect.

**Alternate path A:** If the user requests a risky change casually, the skill should ask a second confirmation question.
**Alternate path B:** If the setting name is ambiguous, the skill should list relevant configurable defaults.

---

## UI States

### Profile Creation Conversation

| State | Trigger | What the User Sees |
|-------|---------|--------------------|
| **Empty** | No profile name or examples yet | A short explanation of profile creation and a prompt for profile name/examples |
| **Collecting** | User is providing examples or answers | Clear next question, with optional examples of useful input |
| **Analyzing** | Skill extracts style traits | A brief progress note: "I am separating style signals from source-specific content." |
| **Hypothesis Ready** | Initial analysis complete | A structured style hypothesis and a request for approval/correction |
| **Calibrating** | Generated sample needs feedback | The sample, feedback options, and optional score prompt |
| **Success** | Profile saved | File path, status, invocation examples, and next available actions |
| **Error** | Missing examples, bad profile name, file write issue | Plain-language error and recovery action |

### Profile File

| State | Trigger | What the User Sees |
|-------|---------|--------------------|
| **Draft** | Calibration in progress | Status marked `draft`, incomplete readiness notes |
| **Experimental** | User saves early | Status marked `experimental`, with remaining calibration suggestions |
| **Ready** | Readiness criteria met | Status marked `ready`, invocation examples included |
| **Forked** | Created from another profile | Source profile metadata and difference summary |
| **Stale** | Config or template version changes later | Notice that profile may need migration or review |

### Settings Interaction

| State | Trigger | What the User Sees |
|-------|---------|--------------------|
| **Default** | No config exists yet | Skill creates or proposes conservative defaults |
| **Populated** | Config exists | Current settings summarized before changes |
| **Warning** | Risky setting change requested | Risk explanation and confirmation prompt |
| **Success** | Config updated | Setting diff and reminder of future behavior |
| **Error** | Config cannot be read/written | File path, likely cause, and safe fallback |

---

## Copy & Tone

**Voice:** Warm, precise, privacy-conscious, and lightly coaching. The skill should sound like a thoughtful editor who respects the user's voice, not a branding consultant forcing polish onto everything.

**Key principles:**
- Make privacy boundaries explicit without sounding alarmist.
- Use direct questions and numbered choices when the user must decide.
- Avoid vague praise; describe concrete style traits and concrete changes.
- Prefer "style" language over "training" language when discussing examples.
- Ask before retaining anything that looks like content, identity, workplace detail, or domain knowledge.

**Critical copy samples:**

| Context | Copy |
|---------|------|
| Profile creation intro | `Let's build a local style profile for {profile}. I will use your examples to infer how the writing should sound, not what private facts it should remember.` |
| Example request | `Paste any examples you have. A few short samples are enough to start; I can ask follow-up questions where the examples are thin.` |
| Sanitization notice | `Default privacy mode is on: I will extract tone, structure, rhythm, and preferences, while leaving out names, facts, internal terms, and source-specific claims unless you explicitly approve them.` |
| Style hypothesis prompt | `Here is my current read on the style. Correct anything that feels off before we calibrate against sample outputs.` |
| Feedback prompt | `What feels right or wrong? You can answer freely, add a 1-5 score, or say pass/fail.` |
| Risk confirmation | `This would allow source-specific content into future profile guidance. Confirm only if that term should be part of the reusable style, not just this example.` |
| Save confirmation | `Saved {profile} locally at {path}. It is marked {status}. You can now ask to write or rewrite using this profile.` |
| Missing content prompt | `I have the style, but I still need the substance. What should this piece actually say?` |

---

## Visual Design Direction

**Style:** Conversational, file-native, and structured. The "visual design" is mostly Markdown structure, command output, and local artifact readability.
**Color palette:** Not applicable for the MVP unless a future UI is added. If rendered in a UI later, use restrained semantic colors for status: neutral for draft, green for ready, amber for experimental/risky settings, red for privacy or write errors.
**Typography:** Markdown-first. Use headings, tables, short lists, and monospace for profile names, file paths, and commands.
**Spacing & density:** Comfortable but efficient. Avoid walls of prose during interactive prompts; profile files can be more detailed.
**Existing design system:** None. Establish a minimal Markdown artifact system.
**Mood reference:** A careful editor's notebook plus a local configuration file: calm, inspectable, and direct.

---

## UX Consistency Patterns

### Choice Patterns
- Use numbered choices for discrete decisions, especially profile source, feedback mode, and settings changes.
- Always include a plain-language default recommendation when a user may not know enough to choose.
- For risky choices, use confirmation rather than burying the risk in the option text.

### Feedback Patterns
- **Success:** Show the saved file path, status, and one next action.
- **Error:** Explain what failed and how the user can recover.
- **Warning:** Use a short risk statement before privacy-affecting actions.
- **Info:** Use brief inline explanations, especially for "style vs content."

### Form/Input Patterns
- Profile names should be lowercase kebab-case by recommendation, but the skill can offer to normalize names.
- Freeform user feedback is always accepted.
- Optional numeric ratings should use a simple 1-5 scale.
- Missing information should trigger one focused question at a time.

### Confirmation Patterns
- Required before disabling sanitization.
- Required before retaining source-derived terms or facts.
- Required before overwriting an existing profile.
- Required before changing config defaults that reduce privacy protections.

### File Output Patterns
- Every saved profile should begin with metadata and status.
- Every saved profile should include usage examples.
- Every generated or revised profile should be summarized before writing.
- The skill should avoid hidden state; if something matters later, it belongs in a local artifact.

---

## Responsive & Accessibility

**Breakpoints:**

| Breakpoint | Width | Layout |
|------------|-------|--------|
| Mobile | N/A | The MVP has no custom visual UI; host app handles layout |
| Tablet | N/A | The MVP has no custom visual UI; host app handles layout |
| Desktop | N/A | The MVP has no custom visual UI; host app handles layout |

**Accessibility standards:** The MVP should be accessible through plain text interaction and readable Markdown artifacts.

**Key requirements:**
- Prompts should not rely on color, layout, or visual-only cues.
- Numbered options should be readable by screen readers.
- Saved Markdown files should use semantic headings and tables sparingly.
- Error and warning copy should state the concrete action needed.
- Future UI implementations should target WCAG 2.1 AA minimum.
