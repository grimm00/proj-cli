# Explore Command

Initiate exploration cycles for proof of concepts or abstract ideas. Creates exploration documents and identifies research topics/questions that need investigation.

---

## Configuration

**Path Detection:**

This command supports multiple project organization patterns:

1. **Dev-Infra Structure (default):**
   - Explorations: `admin/explorations/[topic]/`

2. **Template Structure (for generated projects):**
   - Explorations: `docs/maintainers/planning/explorations/[topic]/`

3. **Project-Wide Structure:**
   - Explorations: `docs/maintainers/planning/explorations/[topic]/`

**Topic Detection:**
- Use `--topic` option if provided
- Otherwise, prompt user for topic name
- Sanitize topic name (kebab-case, no spaces)

---

## Workflow Overview

**When to use:**

- When you have a new idea or proof of concept
- To organize abstract thoughts before research
- When you need to identify what questions need answering
- Before starting research on a topic

**Key principle:** Start with exploration to identify research topics, then move to research phase. Use Setup Mode for quick ideation, then Conduct Mode for detailed exploration after human review. Use Amend Mode when downstream work (research, spikes) surfaces new themes.

**Three Modes:**

### Setup Mode (Default)

Creates lightweight scaffolding (~60-80 lines) for human review before investing in detailed exploration.

```
/explore [topic]
  → Creates exploration scaffolding (~60-80 lines)
  → Organizes thoughts into themes
  → Extracts key questions
  → Creates research-topics.md
  → Outputs: Scaffolding ready for human review
```

**When to use Setup Mode:**

- Starting a new exploration
- Quick ideation without committing to full exploration
- When you want to validate direction before deep dive

### Conduct Mode (`--conduct`)

Expands existing scaffolding with detailed analysis (~200-300 lines).

```
/explore [topic] --conduct
  → Reads existing scaffolding
  → Expands themes with detailed analysis
  → Adds connections, implications, concerns
  → Refines research topics with context
  → Outputs: Full exploration (~200-300 lines)
```

**When to use Conduct Mode:**

- After reviewing scaffolding and validating direction
- When ready to invest in detailed exploration
- Before moving to formal research phase

### Amend Mode (`--amend`)

Appends new themes/questions to an already-expanded exploration.

```
/explore [topic] --amend "description of new theme"
  → Reads existing expanded exploration
  → Appends new theme (auto-numbered)
  → Appends new question to Key Questions
  → Updates spike determination table
  → Adds amendment note to metadata
  → Status stays ✅ Expanded
```

**When to use Amend Mode:**

- Research surfaced a new question that belongs upstream in the exploration
- A spike revealed an assumption that needs capturing as a theme
- Conversation identified a concern not covered in the original exploration
- Any time the explore→research→decide loop feeds back new discovery

**Workflow with Human Review:**

```
/explore [topic]           ← Setup: scaffolding (~60-80 lines)
    ↓ human review         ← Key checkpoint
/explore [topic] --conduct ← Conduct: full exploration (~200-300 lines)
    ↓
/research --from-explore   ← Research: investigate topics
    ↓ (new question?)      ← Feedback loop
/explore [topic] --amend   ← Amend: add theme from downstream discovery
```

---

## Usage

**Command:** `/explore [topic] [options]`

**Setup Mode Examples (default):**

- `/explore new-authentication-system` - Create exploration scaffolding
- `/explore "improve ci pipeline"` - Topic sanitized to `improve-ci-pipeline`
- `/explore --topic database-choice` - Specify topic explicitly
- `/explore --dry-run` - Show what would be created without creating files

**Conduct Mode Examples:**

- `/explore new-authentication-system --conduct` - Expand existing scaffolding
- `/explore improve-ci-pipeline --conduct` - Fill in detailed exploration

**Amend Mode Examples:**

- `/explore workflow-simplification --amend "Should dev-infra maintain executable scripts?"` - Add theme from research discovery
- `/explore auth-system --amend` - Amend interactively (prompts for description)

**Options:**

- `--topic [name]` - Specify topic name (overrides prompt)
- `--conduct` - Expand scaffolding with detailed exploration (requires existing scaffolding)
- `--amend [description]` - Append new theme/question to expanded exploration (requires `✅ Expanded` status)
- `--dry-run` - Show what would be created without creating files
- `--force` - Overwrite existing scaffolding (setup) or re-expand (conduct)

**Input Source Options:**

- `--input [text|file]` - Raw text inline or from file (primary input source)
- `--from-start` - Read project's start.txt as input
- `--from-reflect [file]` - Read reflection document for actionable suggestions

**Input Source Examples:**

- `/explore "I've been thinking about improving our auth system..."` - Inline raw text
- `/explore --input thoughts.txt` - Read from file
- `/explore --from-start` - Use project's start.txt
- `/explore --from-reflect reflection-2026-01-10.md` - Extract from reflection

**Note:** Input sources are mutually exclusive. If multiple specified, command errors. If none specified, prompts for topic interactively.

**Worktree Options (Conduct Mode only):**

- `--worktree` - Create worktree automatically (skip prompt)
- `--no-worktree` - Skip worktree prompt, stay on current branch

**Worktree Examples:**

- `/explore my-idea --conduct` - Prompts "Create worktree?"
- `/explore my-idea --conduct --worktree` - Auto-creates worktree
- `/explore my-idea --conduct --no-worktree` - Skips prompt, stays on current branch

**Note:** Worktree flags only apply to Conduct Mode. Setup Mode always stays on current branch.

---

## Input Sources

`/explore` is the pipeline entry point - the only command that handles **unstructured input**. This makes it the "thought organizer" that transforms raw ideas into structured exploration.

### Source Priority

| Priority | Source | Flag | Use Case |
|----------|--------|------|----------|
| 1 (Primary) | Raw text | `--input [text\|file]` | Brain dumps, ideas, thoughts |
| 2 | start.txt | `--from-start` | Project initialization context |
| 3 | Reflections | `--from-reflect [file]` | Actionable suggestions from reflection |
| 4 | Interactive | (no flag) | Prompt for topic when no input provided |

### Raw Text Input (Primary)

**When to use:** You have unstructured thoughts, ideas, or a brain dump you want organized.

**Inline text:**

```
/explore "I've been thinking about how we handle authentication.
The current system is too rigid. Maybe we need roles? Or tokens?
What about SSO? Users keep asking about Google login..."
```

**From file:**

```
/explore --input ~/thoughts/auth-ideas.txt
```

**What happens:**

1. Input parsed for themes and patterns
2. Related thoughts grouped together
3. Questions extracted for research topics
4. Scaffolding created with organized structure

### start.txt Input

**When to use:** Starting a new project or exploring project initialization notes.

**Command:**

```
/explore --from-start
```

**Auto-detection:**

- Searches for `start.txt` in current directory
- Falls back to project root
- Error if not found

**What happens:**

1. start.txt content parsed
2. Project goals extracted as themes
3. Open questions identified
4. Exploration scaffolding reflects project context

### Reflection Input

**When to use:** You have actionable suggestions from a `/reflect` output.

**Command:**

```
/explore --from-reflect admin/planning/notes/reflection-2026-01-10.md
```

**What happens:**

1. Reads "Actionable Suggestions" section from reflection
2. Converts suggestions into exploration themes
3. Preserves suggestion context in output
4. Creates bridge between `/reflect` → `/explore` pipeline

### Interactive Mode (Default)

**When to use:** Quick exploration when you just have a topic name.

**What happens when no input source specified:**

1. Prompts: "What topic would you like to explore?"
2. Uses topic name only (no additional context)
3. Generates exploration based on topic

**Note:** Interactive mode produces less context-rich scaffolding than raw text input.

### Theme Extraction

When processing unstructured input, `/explore` organizes content into themes:

**Extraction Process:**

1. **Parse input** for distinct ideas, concerns, or topics
2. **Group related thoughts** into thematic clusters
3. **Name themes** with descriptive, concise titles
4. **Preserve context** - original thoughts appear under themes

**Example Transformation:**

**Input (raw text):**

```
I've been thinking about improving our auth system. The current JWT approach
is okay but tokens expire too quickly. Users complain about re-logging in.
Maybe we need refresh tokens? Also thinking about adding Google SSO -
users keep asking. Security audit mentioned we need MFA too.
```

**Output (themes in scaffolding):**

```markdown
## 🔍 Themes

### Theme 1: Token Expiration & User Experience
- JWT tokens expire too quickly
- Users complain about re-logging in
- Consider refresh token pattern

### Theme 2: Third-Party Authentication
- Google SSO requested by users
- Reduces password fatigue
- OAuth2 integration needed

### Theme 3: Security Enhancement
- Security audit requires MFA
- Compliance consideration
- User friction vs security tradeoff
```

**Theme Naming Conventions:**

- Use descriptive nouns/noun phrases
- Avoid generic names like "Issue 1" or "Topic A"
- Capture the essence of grouped thoughts
- Keep names concise (2-5 words)

### Question Extraction

`/explore` identifies questions from input and generates `research-topics.md`:

**Extraction Process:**

1. **Identify explicit questions** - Text ending in "?"
2. **Identify implicit questions** - Statements implying uncertainty ("maybe", "not sure", "consider")
3. **Convert to research questions** - Rephrase as investigable questions
4. **Prioritize** - Order by apparent importance in input

**Question Markers:**

| Marker | Example | Conversion |
|--------|---------|------------|
| Explicit "?" | "Should we use JWTs?" | Direct research question |
| "Maybe" | "Maybe we need refresh tokens" | "Should we implement refresh tokens?" |
| "Not sure" | "Not sure about OAuth scope" | "What OAuth scopes are appropriate?" |
| "Consider" | "Consider MFA options" | "What MFA options exist?" |
| "What about" | "What about SSO?" | "Should we implement SSO?" |

**Example:**

**Input:**

```
Maybe we need refresh tokens? What about Google SSO? 
Not sure how MFA would affect user experience.
```

**Output (research-topics.md):**

```markdown
### Topic 1: Refresh Token Implementation

**Question:** Should we implement refresh tokens for better user experience?
**Priority:** High

### Topic 2: SSO Integration

**Question:** Should we implement Google SSO?
**Priority:** Medium

### Topic 3: MFA User Impact

**Question:** How would MFA affect user experience?
**Priority:** Medium
```

---

## Worktree Integration

`/explore` implements lazy worktree creation aligned with [ADR-002 Self-Contained Feature Branches](../../../decisions/worktree-feature-workflow/adr-002-self-contained-feature-branches.md).

### Setup Mode (No Worktree)

Setup mode stays on current branch (typically `develop`):

- Creates lightweight scaffolding (~60-80 lines)
- Low investment, acceptable to abandon on develop
- **No worktree prompt** - keeps exploration friction low

**Why:** Quick explorations shouldn't require worktree overhead.

### Conduct Mode (Worktree Prompt)

Conduct mode prompts for worktree creation:

```
/explore my-idea --conduct

Create worktree for this exploration? [Y/n]
```

**If Yes:**
- Creates directory: `worktrees/feat-my-idea`
- Creates branch: `feat/my-idea`
- Continues exploration on feature branch

**If No:**
- Stays on current branch
- Continues exploration without worktree

**Why:** Conduct mode represents real investment; prompts at natural decision point.

### Explicit Control Flags

For automation and scripting, use explicit flags:

| Flag | Behavior | Use Case |
|------|----------|----------|
| `--worktree` | Creates worktree without prompting | CI/automation, scripting |
| `--no-worktree` | Skips prompt, stays on current branch | Quick explorations, existing worktree |

**Naming Convention:**

| Element | Pattern | Example |
|---------|---------|---------|
| Directory | `worktrees/feat-[topic]` | `worktrees/feat-auth-system` |
| Branch | `feat/[topic]` | `feat/auth-system` |

### ADR-002 Alignment

This pattern aligns with the worktree feature workflow:

- **Setup on develop:** Scaffolding is lightweight, acceptable on develop
- **Conduct on feature branch:** Serious investment is self-contained
- **Natural gate:** Setup → Conduct transition is meaningful commitment point

---

## Setup Mode Output

**Output Size:** ~60-80 lines total

Setup Mode creates lightweight scaffolding documents for human review before investing in detailed exploration.

**Creates:**

```
explorations/[topic]/
├── README.md           (~20 lines) - Hub with quick links
├── exploration.md      (~40-50 lines) - Scaffolding with placeholders
└── research-topics.md  (~20-30 lines) - Prioritized questions
```

### exploration.md Scaffolding Template

**File:** `explorations/[topic]/exploration.md`

```markdown
# Exploration: [Topic]

**Status:** 🔴 Scaffolding (needs expansion)
**Created:** YYYY-MM-DD

---

## 🎯 What We're Exploring

[2-3 sentence summary extracted from input]

---

## 🔍 Initial Themes

### Theme 1: [Name]
<!-- PLACEHOLDER: Expand with detailed analysis in conduct mode -->

### Theme 2: [Name]
<!-- PLACEHOLDER: Expand with detailed analysis in conduct mode -->

---

## ❓ Key Questions

1. [Question extracted from input]
2. [Question extracted from input]

---

## 🧪 Spike Determination

<!-- AI: Assess each theme/question against risk matrix. Flag HIGH risk items for spiking. -->

| Topic | Risk Level | Spike? | Rationale |
|-------|------------|--------|-----------|
| [Topic from themes] | [HIGH/MEDIUM-HIGH/MEDIUM/LOW] | [Yes/Consider/No] | [Brief rationale] |
| [Topic from themes] | [HIGH/MEDIUM-HIGH/MEDIUM/LOW] | [Yes/Consider/No] | [Brief rationale] |

**Risk framework:** HIGH = spike first (hard to pivot), MEDIUM-HIGH = consider spike, MEDIUM/LOW = research only.

---

## 🚀 Next Steps

Run `/explore [topic] --conduct` to expand this exploration.
```

### research-topics.md Scaffolding Template

**File:** `explorations/[topic]/research-topics.md`

```markdown
# Research Topics - [Topic]

**Status:** 🔴 Scaffolding (needs expansion)
**Created:** YYYY-MM-DD

---

## 📋 Topics Identified

### Topic 1: [Name]

**Question:** [Core question to investigate]
**Priority:** [High | Medium | Low]

### Topic 2: [Name]

**Question:** [Core question to investigate]
**Priority:** [High | Medium | Low]

---

## 🚀 Next Steps

Run `/explore [topic] --conduct` to expand these topics with context and rationale.
```

### README.md Hub Template

**File:** `explorations/[topic]/README.md`

```markdown
# [Topic] - Exploration Hub

**Status:** 🔴 Scaffolding (needs expansion)
**Created:** YYYY-MM-DD

---

## 📋 Quick Links

- **[Exploration](exploration.md)** - Main exploration document
- **[Research Topics](research-topics.md)** - Topics to investigate

---

## 🎯 Overview

[1-2 sentence summary]

---

**Next:** Run `/explore [topic] --conduct` to expand this exploration.
```

---

## Conduct Mode Output

**Output Size:** ~200-300 lines total

Conduct Mode expands existing scaffolding with detailed analysis, connections, and context.

**Expands existing scaffolding with:**

- Themes with detailed analysis, connections, implications
- Questions with context, sub-questions, research approach
- Initial thoughts with evidence, concerns, opportunities
- research-topics.md with full descriptions and priority rationale

**Status Transition:**

```
🔴 Scaffolding (needs expansion) → ✅ Expanded
```

### exploration.md After Conduct

**File:** `explorations/[topic]/exploration.md`

```markdown
# Exploration: [Topic]

**Status:** ✅ Expanded
**Created:** YYYY-MM-DD
**Expanded:** YYYY-MM-DD

---

## 🎯 What We're Exploring

[Expanded description with context, background, and motivation - 2-3 paragraphs]

---

## 🔍 Themes

### Theme 1: [Name]

[Detailed analysis of theme - 3-5 paragraphs]

**Connections:**
- [Connection to other themes or concepts]
- [Connection to existing patterns or decisions]

**Implications:**
- [What this means for the exploration]
- [Impact on related areas]

**Concerns:**
- [Potential issues or risks]
- [Open questions]

### Theme 2: [Name]

[Similar detailed structure...]

---

## ❓ Key Questions

### Question 1: [Question]

**Context:** [Why this question matters - 2-3 sentences]

**Sub-questions:**
- [Related question 1]
- [Related question 2]
- [Related question 3]

**Research Approach:** [How to investigate - suggested methods]

### Question 2: [Question]

[Similar structure...]

---

## 💡 Initial Thoughts

[Detailed initial thinking with evidence - 2-3 paragraphs]

**Opportunities:**
- [Opportunity 1 with brief explanation]
- [Opportunity 2 with brief explanation]

**Concerns:**
- [Concern 1 with brief explanation]
- [Concern 2 with brief explanation]

---

## 🧪 Spike Determination

Assess each theme/question against risk levels to determine what needs hands-on validation before research.

| Topic | Risk Level | Spike? | Rationale |
|-------|------------|--------|-----------|
| [Topic 1] | [HIGH/MEDIUM-HIGH/MEDIUM/LOW] | [Yes/Consider/No] | [Why it needs/doesn't need validation] |
| [Topic 2] | [HIGH/MEDIUM-HIGH/MEDIUM/LOW] | [Yes/Consider/No] | [Why it needs/doesn't need validation] |

**Risk Assessment:**

| Risk Level | Determination | Rationale |
|------------|---------------|-----------|
| HIGH | **Spike first** | Hard to pivot once committed |
| MEDIUM-HIGH | **Consider spike** | Benefits from hands-on validation |
| MEDIUM | Research only | Depends on other decisions |
| LOW | Research only | Clear path, low risk |

**Spike Candidates:**
- [Topic flagged HIGH] -- Use `/spike [topic] --from-explore [explore-topic]`

---

## 🚀 Next Steps

1. If spike candidates identified, run `/spike [topic] --from-explore [topic]` first
2. Review research topics in `research-topics.md`
3. Use `/research [topic] --from-explore [topic]` to conduct research
4. After research, use `/decision [topic] --from-research` to make decisions

---

**Last Updated:** YYYY-MM-DD
```

### research-topics.md After Conduct

**File:** `explorations/[topic]/research-topics.md`

```markdown
# Research Topics - [Topic]

**Status:** ✅ Expanded
**Created:** YYYY-MM-DD
**Expanded:** YYYY-MM-DD

---

## 📋 Research Topics

### Topic 1: [Name]

**Question:** [Core question to investigate]

**Context:** [Why this research is needed - 2-3 sentences]

**Priority:** [High | Medium | Low]

**Rationale:** [Why this priority - 1-2 sentences]

**Suggested Approach:**
- [Research method 1]
- [Research method 2]

### Topic 2: [Name]

[Similar detailed structure...]

---

## 🎯 Research Workflow

1. Use `/research [topic] --from-explore [topic]` to start research
2. Research will create documents in research directory
3. After research complete, use `/decision [topic] --from-research`

---

**Last Updated:** YYYY-MM-DD
```

---

## Step-by-Step Process

### 1. Identify Topic

**Default behavior:**

- If topic provided, use it
- Otherwise, prompt user: "What topic would you like to explore?"
- Sanitize topic name:
  - Convert to kebab-case
  - Remove special characters
  - Replace spaces with hyphens

**Checklist:**

- [ ] Topic identified
- [ ] Topic name sanitized
- [ ] Topic doesn't already exist (check existing explorations)

---

### 2. Determine Mode

**Mode Detection Logic:**

The command detects which mode to use based on flags and existing content.

**Setup Mode (default):**

1. Check if topic directory exists
2. If exists, check exploration.md status
3. If status is `🔴 Scaffolding`, suggest using `--conduct`
4. If status is `✅ Expanded`, warn about overwriting
5. If doesn't exist, proceed with setup

**Conduct Mode (`--conduct`):**

1. Check if topic directory exists
2. If doesn't exist, error: "No scaffolding found. Run setup first."
3. Check exploration.md status
4. If status is `✅ Expanded`, warn and require `--force` to re-expand
5. If status is `🔴 Scaffolding`, proceed with conduct

**Amend Mode (`--amend`):**

1. Check if topic directory exists
2. If doesn't exist, error: "No exploration found for [topic]."
3. Check exploration.md status
4. If status is `🔴 Scaffolding`, error: "Exploration not yet expanded. Use `--conduct` first, then `--amend`."
5. If status is `✅ Expanded`, proceed with amend
6. Read the amend description from flag value or prompt interactively

### Input Source Validation

Before mode detection, validate input source:

1. **Check for mutually exclusive flags:**
   - `--input` + `--from-start` → Error
   - `--input` + `--from-reflect` → Error
   - `--from-start` + `--from-reflect` → Error

2. **Validate source exists:**
   - `--input file.txt` → Check file exists
   - `--from-start` → Check start.txt exists
   - `--from-reflect [file]` → Check reflection file exists

3. **Validate source format:**
   - Reflection file must have "Actionable Suggestions" section
   - start.txt must not be empty

**Error Messages:**

| Situation | Message |
|-----------|---------|
| `--conduct` with no scaffolding | "No exploration scaffolding found for [topic]. Run `/explore [topic]` first." |
| `--conduct` on already expanded | "Exploration already expanded. Use `--force` to re-expand." |
| Setup on existing scaffolding | "Scaffolding exists. Use `--conduct` to expand, or `--force` to overwrite." |
| `--amend` with no exploration | "No exploration found for [topic]. Run `/explore [topic]` first." |
| `--amend` on scaffolding | "Exploration not yet expanded. Use `--conduct` first, then `--amend`." |
| `--amend` + `--conduct` | "Error: --amend and --conduct are mutually exclusive" |
| Multiple input sources | "Error: --input, --from-start, and --from-reflect are mutually exclusive" |
| Input file not found | "Error: Input file '[path]' not found" |
| start.txt not found | "Error: start.txt not found in current directory or project root" |
| Reflection file missing | "Error: Reflection file '[path]' not found" |
| Reflection missing section | "Warning: No 'Actionable Suggestions' section found in reflection" |
| Empty start.txt | "Error: start.txt is empty" |
| `--worktree` in Setup Mode | "Warning: --worktree flag ignored in Setup Mode" |
| `--no-worktree` in Setup Mode | "Warning: --no-worktree flag ignored in Setup Mode" |
| `--worktree` + `--no-worktree` | "Error: --worktree and --no-worktree are mutually exclusive" |
| Worktree already exists | "Worktree exists at [path]. Switching to existing worktree." |
| Branch already exists | "Branch [name] exists. Use existing branch? [Y/n]" |

**Force Flag Behavior:**

- `--force` with Setup Mode: Overwrites existing scaffolding (creates fresh)
- `--force` with Conduct Mode: Re-expands even if already expanded

**Checklist:**

- [ ] Check if `--conduct` flag provided
- [ ] Check if topic directory exists
- [ ] Check exploration.md status (if exists)
- [ ] Handle error cases appropriately
- [ ] Apply `--force` logic if needed

### Conduct Mode Worktree Prompt

After mode validation, if entering Conduct Mode:

1. **Check worktree flags:**
   - `--worktree` present → Create worktree automatically
   - `--no-worktree` present → Skip prompt, continue on current branch
   - Neither → Prompt user

2. **Prompt flow (if no flag):**

```
Create worktree for this exploration? [Y/n]
```

- Default: Yes (press Enter)
- Creates worktree and switches to feature branch

3. **Worktree creation:**
   - Directory: `worktrees/feat-[topic]`
   - Branch: `feat/[topic]`
   - Uses `scripts/worktrees.sh` if available

---

### 3. Setup Mode: Create Scaffolding

**Use when:** Mode detection indicates Setup Mode (no `--conduct` flag, no existing exploration or `--force` used).

**Location Detection:**

- **Dev-Infra:** `admin/explorations/[topic]/`
- **Template Structure:** `docs/maintainers/planning/explorations/[topic]/`
- **Project-Wide:** `docs/maintainers/planning/explorations/[topic]/`

**Auto-detection:**
- Check if `admin/explorations/` exists → use dev-infra structure
- Check if `docs/maintainers/planning/explorations/` exists → use template structure
- Otherwise → use project-wide structure

**Creates:** See [Setup Mode Output](#setup-mode-output) for templates (~60-80 lines total)

**Process:**

1. Create exploration directory: `explorations/[topic]/`
2. Create `README.md` hub (~20 lines) with quick links
3. Create `exploration.md` scaffolding (~40-50 lines) with placeholders
4. Create `research-topics.md` scaffolding (~20-30 lines) with prioritized questions
5. Update explorations hub with new exploration link

**Setup Mode Checklist:**

- [ ] Exploration directory created
- [ ] Exploration hub created (~20 lines)
- [ ] Exploration scaffolding created (~40-50 lines)
- [ ] Research topics scaffolding created (~20-30 lines)
- [ ] Status set to `🔴 Scaffolding (needs expansion)`
- [ ] Explorations hub updated

**Commit (docs can push directly):**

```bash
git add explorations/[topic]/
git commit -m "docs(explore): create [topic] exploration scaffolding"
git push origin develop
```

---

### 4. Conduct Mode: Expand Scaffolding

**Use when:** Mode detection indicates Conduct Mode (`--conduct` flag provided, scaffolding exists).

**Reads:** Existing scaffolding from `explorations/[topic]/`

**Creates:** See [Conduct Mode Output](#conduct-mode-output) for expanded templates (~200-300 lines total)

### Worktree Creation (Conduct Mode Only)

**After mode detection, before expanding scaffolding:**

1. **Check worktree flags:**
   - If `--worktree`: Proceed to step 2
   - If `--no-worktree`: Skip to scaffolding expansion
   - If neither: Prompt user

2. **Create worktree (if applicable):**
   - Directory: `worktrees/feat-[topic]`
   - Branch: `feat/[topic]` from current HEAD
   - Switch to worktree directory

3. **Verify worktree:**
   - Check branch is correct: `git branch --show-current`
   - Check working directory: `pwd`

**Worktree Checklist:**

- [ ] Worktree prompt handled (flag or user response)
- [ ] Worktree created (if applicable)
- [ ] Branch verified
- [ ] Working directory is worktree (if created)

**Commit Guidance:**

- If worktree created: First commit on feature branch
- If no worktree: Commit to current branch

**Process:**

1. Read existing `exploration.md` scaffolding
2. Expand themes with detailed analysis, connections, implications, concerns
3. Expand questions with context, sub-questions, research approach
4. Add initial thoughts with evidence, opportunities, concerns
5. Update `research-topics.md` with context and rationale for each topic
6. Update status from `🔴 Scaffolding` to `✅ Expanded`

**Conduct Mode Checklist:**

- [ ] Existing scaffolding read and understood
- [ ] Themes expanded with detailed analysis
- [ ] Questions expanded with context and sub-questions
- [ ] Initial thoughts documented with evidence
- [ ] research-topics.md expanded with context
- [ ] Status updated to `✅ Expanded`

**Commit (docs can push directly):**

```bash
git add explorations/[topic]/
git commit -m "docs(explore): expand [topic] exploration with detailed analysis"
git push origin develop
```

---

### 4b. Amend Mode: Append to Expanded Exploration

**Use when:** Mode detection indicates Amend Mode (`--amend` flag provided, exploration is `✅ Expanded`).

**Reads:** Existing expanded exploration from `explorations/[topic]/`

**Process:**

1. Read existing `exploration.md`
2. Determine next theme number (count existing `### Theme N:` headings)
3. Append new theme to the Themes section with full structure (analysis, connections, implications, concerns)
4. Append corresponding question to Key Questions section
5. Add row to spike determination table
6. Read existing `research-topics.md`
7. Determine next topic number (count existing `### Topic N:` headings)
8. Append new topic to `research-topics.md` with full structure (Question, Context, Priority, Rationale, Suggested Approach)
9. Add `**Amended:** YYYY-MM-DD - [reason]` to `exploration.md` metadata
10. Status remains `✅ Expanded`

**Amend Mode Checklist:**

- [ ] Existing exploration read
- [ ] New theme appended with full structure (connections, implications, concerns)
- [ ] New question appended to Key Questions
- [ ] Spike determination table updated
- [ ] `research-topics.md` updated with new topic
- [ ] Amendment note added to metadata
- [ ] Status unchanged (`✅ Expanded`)

**Commit (docs can push directly):**

```bash
git add explorations/[topic]/
git commit -m "docs(explore): amend [topic] exploration with [brief description]"
```

---

### 5. Update Explorations Hub

**Update explorations hub:**

**File location (auto-detected):**
- **Dev-Infra:** `admin/explorations/README.md`
- **Template Structure:** `docs/maintainers/planning/explorations/README.md`
- **Project-Wide:** `docs/maintainers/planning/explorations/README.md`

```markdown
# Explorations Hub

**Purpose:** Active explorations and proof of concepts  
**Status:** ✅ Active  
**Last Updated:** YYYY-MM-DD

---

## 📋 Quick Links

### Active Explorations

- **[Topic 1]([topic-1]/README.md)** - [Description] (🔴 Exploration)
- **[Topic 2]([topic-2]/README.md)** - [Description] (🟡 Research)

---

## 🎯 Overview

This directory contains active explorations, proof of concepts, and abstract ideas being explored before research and decision phases.

**Workflow:**
1. `/explore [topic]` - Start exploration
2. `/research [topic] --from-explore [topic]` - Conduct research
3. `/decision [topic] --from-research` - Make decisions
4. `/transition-plan --from-adr` - Transition to planning

---

**Last Updated:** YYYY-MM-DD
```

**Checklist:**

- [ ] Explorations hub created/updated
- [ ] New exploration added to quick links

---

## Integration with Other Commands

### Input Sources in Pipeline

```
Raw thoughts → /explore --input "..."   ← Primary entry point
start.txt   → /explore --from-start     ← Project initialization
/reflect    → /explore --from-reflect   ← Reflection pipeline
    ↓
/explore [topic]              ← Setup: scaffolding (~60-80 lines)
    ↓ human review
/explore [topic] --conduct    ← Conduct: full exploration (~200-300 lines)
    ↓                           (includes spike determination table)
    ├─ HIGH risk topics → /spike --from-explore  ← Validate assumptions
    ↓
/research --from-explore      ← Research: investigate topics
```

**Input Source → Output Quality:**

| Input Source | Output Quality | Notes |
|--------------|----------------|-------|
| Raw text (rich) | High | Themes and questions from user context |
| start.txt | Medium-High | Project-focused exploration |
| Reflection | Medium-High | Suggestion-focused exploration |
| Topic only | Medium | AI-generated without user context |

---

### Command Pipeline Position

```
/explore [topic]              ← Setup: scaffolding (~60-80 lines)
    ↓ human review            ← KEY CHECKPOINT: validate direction
/explore [topic] --conduct    ← Conduct: full exploration (~200-300 lines)
    ↓                           (includes spike determination table)
    ├─ HIGH risk? ─────────→ /spike --from-explore  ← Validate assumptions (2-4 hrs)
    ↓                           (spike learnings feed back into research)
/research --from-explore      ← Research: investigate topics
    ↓ (new question?) ──────→ /explore [topic] --amend  ← Feedback loop
    ↓
/decision --from-research     ← Decisions: create ADRs
    ↓
/transition-plan --from-adr   ← Planning: create phases
    ↓
/task-phase 1 1               ← Implementation: execute phases
```

**Note:** Human review between Setup and Conduct is the key checkpoint. This allows:
- Quick validation of exploration direction before full investment
- Course correction with minimal time spent
- Rejection of dead-end explorations without wasted effort
- Identification of high-risk topics that need spiking before research
- **Feedback from downstream**: research or spikes can amend the exploration with new themes

### Timing Guidance

| Stage | Time Investment | Output |
|-------|-----------------|--------|
| Setup Mode | ~5-10 min | Scaffolding for review (~60-80 lines) |
| Human Review | ~2-5 min | Go/no-go decision on direction |
| Conduct Mode | ~20-30 min | Full exploration (~200-300 lines) |
| Research | ~1-2 hours | Research documents + requirements |
| Decision | ~30 min | ADR documents |
| Planning | ~30 min | Feature plan + phases |

### Worktree in Pipeline

```
/explore [topic]              ← Setup on develop (no worktree)
    ↓ human review
/explore [topic] --conduct    ← Prompt: "Create worktree?" 
    ├─ --worktree            → Auto-create worktree
    ├─ --no-worktree         → Skip, stay on branch
    └─ [Y/n]                 → User decides
    ↓
worktrees/feat-[topic]/       ← Feature branch (if created)
    ↓
/research --from-explore      ← Research on feature branch
    ↓
/decision → /transition-plan → /task-phase
```

**Worktree Decision Point:**

| Stage | Branch | Notes |
|-------|--------|-------|
| Setup Mode | develop | Lightweight scaffolding, no worktree |
| Conduct Mode | develop OR feat/* | Depends on prompt response |
| Research onwards | feat/* | Should be on feature branch |

### Exploration → Research → Decision → Planning Flow

1. **`/explore [topic]`** - Start exploration (Setup Mode)
   - Creates scaffolding with placeholders
   - Organizes thoughts into themes
   - Outputs: `research-topics.md` scaffolding
   - Status: `🔴 Scaffolding (needs expansion)`

2. **`/explore [topic] --conduct`** - Expand exploration (Conduct Mode)
   - Expands scaffolding with detailed analysis
   - Adds connections, implications, concerns
   - Outputs: Full exploration (~200-300 lines)
   - Status: `✅ Expanded`

3. **`/research [topic] --from-explore [topic]`** - Conduct research
   - Reads research topics from exploration
   - Creates research documents
   - Outputs: Research documents + `requirements.md`

4. **`/decision [topic] --from-research`** - Make decisions
   - Reads research documents
   - Creates ADR documents
   - Outputs: ADR documents

5. **`/transition-plan --from-adr`** - Transition to planning
   - Reads ADR documents
   - Creates feature plan and phase documents
   - Outputs: Transition plan + Feature plan + Phase documents

---

## Common Scenarios

### Scenario 1: New Feature Idea

**Situation:** You have an idea for a new feature

**Action:**
```bash
/explore new-feature-idea
```

**Output:**
- Exploration document created
- Research topics identified
- Ready for research phase

---

### Scenario 2: Proof of Concept

**Situation:** Want to explore a proof of concept

**Action:**
```bash
/explore poc-distributed-caching
```

**Output:**
- Exploration document created
- Research topics identified
- Ready for research phase

---

### Scenario 3: Raw Text Brain Dump

**Situation:** You have unstructured thoughts about a feature idea.

**Action:**

```bash
/explore "I want to add a notification system. Users should get
alerts for important events. Maybe email? Push notifications?
What about in-app badges? Need to think about user preferences too."
```

**Output:**
- Exploration scaffolding with 3-4 themes (notification channels, user preferences, etc.)
- research-topics.md with prioritized questions
- Status: `🔴 Scaffolding (needs expansion)`

---

### Scenario 4: New Project from start.txt

**Situation:** Starting a new project with initialization notes in start.txt.

**Action:**

```bash
/explore --from-start
```

**Output:**
- Exploration based on project goals from start.txt
- Themes organized around project objectives
- Questions extracted from open items in start.txt

---

### Scenario 5: Reflection to Exploration

**Situation:** You ran `/reflect` and want to explore the actionable suggestions.

**Action:**

```bash
/explore --from-reflect admin/planning/notes/reflection-2026-01-10.md
```

**Output:**
- Exploration themes from reflection's "Actionable Suggestions"
- research-topics.md populated from suggestions
- Bridges reflection → exploration → research pipeline

---

### Scenario 6: Exploration to Feature Branch

**Situation:** You've validated an exploration in Setup Mode and want to fully develop it.

**Action:**

```bash
# Step 1: Setup mode on develop (quick scaffolding)
/explore notification-system

# Step 2: Review scaffolding, decide to proceed
# ...

# Step 3: Conduct mode (prompts for worktree)
/explore notification-system --conduct

# Output:
# Create worktree for this exploration? [Y/n] y
# Creating worktree: worktrees/feat-notification-system
# Creating branch: feat/notification-system
# Switched to worktree directory
```

**Result:**
- Full exploration (~200-300 lines) on feature branch
- Self-contained per ADR-002
- Ready for `/research` phase

---

### Scenario 7: Quick Exploration (No Worktree)

**Situation:** You want to quickly expand an exploration without worktree overhead.

**Action:**

```bash
/explore quick-idea --conduct --no-worktree
```

**Result:**
- Full exploration on current branch
- Skips worktree prompt
- Useful for explorations that may not become features

---

### Scenario 8: Research Feedback Loop (Amend)

**Situation:** During `/research` on workflow-simplification, you discover a new question about whether dev-infra should maintain executable scripts. This belongs upstream in the exploration.

**Action:**

```bash
/explore workflow-simplification --amend "Should dev-infra maintain executable 
scaffolding scripts for generated projects, or stay in specs/templates/manifests?"
```

**Result:**
- New Theme 5 appended to existing exploration
- New Question 5 added to Key Questions
- Spike determination table updated
- Amendment metadata recorded
- Status stays `✅ Expanded`
- No overwriting of existing themes or analysis

---

## Tips

### When to Use

- **New ideas** - Start exploration before jumping to research
- **Proof of concepts** - Organize thoughts before research
- **Abstract concepts** - Structure thinking before investigation
- **Research feedback** - Use `--amend` when downstream work surfaces new questions

### Best Practices

- **Be specific** - Clear topic names help organization
- **Identify questions** - Focus on what needs to be researched
- **Prioritize topics** - Mark high/medium/low priority research topics

---

## Reference

**Exploration Structure:**

- **Dev-Infra:** `admin/explorations/[topic]/`
- **Template Structure:** `docs/maintainers/planning/explorations/[topic]/`
- **Project-Wide:** `docs/maintainers/planning/explorations/[topic]/`
- Research Topics: `[explorations-path]/[topic]/research-topics.md`

**Related Commands:**

- `/spike` - Validate high-risk technical assumptions with time-boxed experiments
- `/research` - Conduct research on topics identified in exploration
- `/decision` - Make decisions based on research
- `/transition-plan` - Transition to feature planning

---

**Last Updated:** 2026-02-13
**Status:** ✅ Active
**Next:** Use to initiate exploration cycles for new ideas or proof of concepts

