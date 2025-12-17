# Research Command

Conduct structured research following standardized workflow. Has two modes:
1. **Setup Mode** (default) - Creates research documents for each research topic/question
2. **Conduct Mode** (`--conduct`) - Actually performs research, fills in findings, and extracts requirements

---

## Configuration

**Path Detection:**

This command supports multiple project organization patterns:

1. **Template Structure (for generated projects):**
   - Research: `docs/maintainers/research/[topic]/`
   - Requirements: `docs/maintainers/research/[topic]/requirements.md`
   - Explorations: `docs/maintainers/exploration/[topic]/`

2. **Project-Wide Structure:**
   - Research: `docs/maintainers/research/[topic]/`
   - Requirements: `docs/maintainers/research/[topic]/requirements.md`
   - Explorations: `docs/maintainers/exploration/[topic]/`

**Topic Detection:**
- Use `--topic` option if provided
- Otherwise, auto-detect from input source
- Sanitize topic name (kebab-case, no spaces)

---

## Workflow Overview

**When to use:**

- After exploration identifies research topics
- When reflect artifacts identify opportunities needing research
- To conduct structured research on a specific topic

**Key principle:** Follow standardized research workflow, create documents for each research topic, extract requirements discovered during research.

**Two Modes:**

### Setup Mode (Default)
```
/research [topic] --from-explore [topic]
  → Reads research topics from exploration
  → Creates research hub
  → Creates research document for each topic (templates)
  → Creates requirements skeleton
  → Outputs: Research structure ready for conducting
```

### Conduct Mode (`--conduct`)
```
/research [topic] --conduct [--topic-num N]
  → Reads existing research document(s)
  → Uses web search to find information
  → Fills in findings with sources
  → Analyzes findings and draws insights
  → Makes recommendations
  → Extracts requirements
  → Updates summary and requirements docs
  → Commits changes
```

---

## Usage

**Command:** `/research [topic] [--from-explore|--from-reflect|--topic|--conduct] [options]`

**Setup Mode Examples:**

- `/research auth-system --from-explore new-authentication-system` - Create research structure from exploration
- `/research ci-optimization --from-reflect reflection-project-2025-12-07.md` - Create research structure from reflection
- `/research database-choice --topic "PostgreSQL vs MongoDB"` - Create research structure for direct topic
- `/research --dry-run` - Show what would be created without creating files

**Conduct Mode Examples:**

- `/research experimental-template --conduct` - Conduct ALL research topics for a topic
- `/research experimental-template --conduct --topic-num 1` - Conduct research for topic #1 only
- `/research experimental-template --conduct --topic-name user-demand` - Conduct specific topic by name

**Options:**

- `--from-explore [explore-topic]` - Read research topics from exploration document (Setup Mode)
- `--from-reflect [reflection-file]` - Read opportunities from reflection artifacts (Setup Mode)
- `--topic [topic]` - Direct topic specification (Setup Mode)
- `--conduct` - Actually perform research (Conduct Mode)
- `--topic-num [N]` - Research specific topic by number (with --conduct)
- `--topic-name [name]` - Research specific topic by name (with --conduct)
- `--dry-run` - Show what would be done without making changes

---

## Step-by-Step Process

### 1. Identify Research Source

**Determine input source:**

1. **From Exploration (`--from-explore`):**
   - Read `docs/maintainers/exploration/[explore-topic]/research-topics.md`
   - Extract research topics/questions
   - Use explore-topic as research topic name (or use --topic to override)

2. **From Reflection (`--from-reflect`):**
   - Read reflection document
   - Extract "Actionable Suggestions" or "Opportunities for Improvement"
   - Convert suggestions to research topics
   - Use topic from command or prompt user

3. **Direct Topic (`--topic` or no flag):**
   - Use provided topic
   - Prompt user for research questions if needed

**Checklist:**

- [ ] Research source identified
- [ ] Research topics extracted
- [ ] Topic name determined

---

### 2. Create Research Hub

**Location Detection:**

- **Template Structure:** `docs/maintainers/research/[topic]/`
- **Project-Wide:** `docs/maintainers/research/[topic]/`

**Auto-detection:**
- Check if `docs/maintainers/research/` exists → use template structure
- Otherwise → use project-wide structure

**Directory structure:**

```
research/[topic]/
├── README.md                    # Research hub
├── research-[question-1].md     # Research document for question 1
├── research-[question-2].md     # Research document for question 2
├── research-summary.md          # Summary of all research
└── requirements.md              # Requirements discovered during research
```

**Create research hub:**

**File:** `docs/maintainers/research/[topic]/README.md`

```markdown
# [Topic Name] - Research Hub

**Purpose:** Research for [topic description]  
**Status:** 🔴 Research  
**Created:** YYYY-MM-DD  
**Last Updated:** YYYY-MM-DD

---

## 📋 Quick Links

- **[Research Summary](research-summary.md)** - Summary of all research findings
- **[Requirements](requirements.md)** - Requirements discovered during research
- **[Research Documents](research-*.md)** - Individual research documents

### Research Documents

- **[Research: Question 1](research-[question-1].md)** - [Question description]
- **[Research: Question 2](research-[question-2].md)** - [Question description]

---

## 🎯 Research Overview

[Brief description of research goals]

**Research Topics:** [N] topics  
**Status:** 🔴 Research

---

## 📊 Research Status

| Research Topic | Status | Document |
|----------------|--------|----------|
| [Question 1] | 🔴 Not Started | [research-[question-1].md](research-[question-1].md) |
| [Question 2] | 🔴 Not Started | [research-[question-2].md](research-[question-2].md) |

---

## 🚀 Next Steps

1. Complete research documents for each topic
2. Review requirements in `requirements.md`
3. Use `/decision [topic] --from-research` to make decisions

---

**Last Updated:** YYYY-MM-DD
```

**Checklist:**

- [ ] Research directory created
- [ ] Research hub created
- [ ] Research topics listed in hub

---

### 3. Create Research Documents

**For each research topic/question:**

**File:** `docs/maintainers/research/[topic]/research-[question-name].md`

```markdown
# Research: [Question Name]

**Research Topic:** [Topic Name]  
**Question:** [Specific research question]  
**Status:** 🔴 Research  
**Created:** YYYY-MM-DD  
**Last Updated:** YYYY-MM-DD

---

## 🎯 Research Question

[What specific question is this research addressing?]

---

## 🔍 Research Goals

- [ ] Goal 1: [What do we need to understand?]
- [ ] Goal 2: [What information is needed?]
- [ ] Goal 3: [What comparisons are needed?]

---

## 📚 Research Methodology

[How will this research be conducted?]

**Note:** Web search is **allowed and encouraged** for research. Use web search tools to find current information, best practices, documentation, examples, and real-world implementations. This helps ensure research is based on up-to-date information and industry standards.

**Sources:**
- [ ] Source 1: [Description]
- [ ] Source 2: [Description]
- [ ] Source 3: [Description]
- [ ] Web search: [Use web search for current information, documentation, examples]

---

## 📊 Findings

### Finding 1: [Title]

[Description of finding]

**Source:** [Source reference]

**Relevance:** [Why this finding matters]

---

### Finding 2: [Title]

[Description of finding]

**Source:** [Source reference]

**Relevance:** [Why this finding matters]

---

## 🔍 Analysis

[Analysis of findings]

**Key Insights:**
- [ ] Insight 1: [Description]
- [ ] Insight 2: [Description]

---

## 💡 Recommendations

- [ ] Recommendation 1: [Description]
- [ ] Recommendation 2: [Description]

---

## 📋 Requirements Discovered

[Any requirements discovered during this research]

- [ ] Requirement 1: [Description]
- [ ] Requirement 2: [Description]

---

## 🚀 Next Steps

1. [Next action]
2. [Next action]

---

**Last Updated:** YYYY-MM-DD
```

**Checklist:**

- [ ] Research document created for each topic
- [ ] Research documents linked in hub
- [ ] Status tracking initialized

---

### 4. Create Research Summary

**File:** `docs/maintainers/research/[topic]/research-summary.md`

```markdown
# Research Summary - [Topic Name]

**Purpose:** Summary of all research findings  
**Status:** 🔴 Research  
**Created:** YYYY-MM-DD  
**Last Updated:** YYYY-MM-DD

---

## 📋 Research Overview

[Brief summary of research conducted]

**Research Topics:** [N] topics  
**Research Documents:** [N] documents  
**Status:** 🔴 Research

---

## 🔍 Key Findings

### Finding 1: [Title]

[Summary of finding]

**Source:** [research-[question].md](research-[question].md)

---

### Finding 2: [Title]

[Summary of finding]

**Source:** [research-[question].md](research-[question].md)

---

## 💡 Key Insights

- [ ] Insight 1: [Description]
- [ ] Insight 2: [Description]

---

## 📋 Requirements Summary

[Summary of requirements discovered]

**See:** [requirements.md](requirements.md) for complete requirements document

---

## 🎯 Recommendations

- [ ] Recommendation 1: [Description]
- [ ] Recommendation 2: [Description]

---

## 🚀 Next Steps

1. Review requirements in `requirements.md`
2. Use `/decision [topic] --from-research` to make decisions
3. Decisions will create ADR documents

---

**Last Updated:** YYYY-MM-DD
```

**Checklist:**

- [ ] Research summary created
- [ ] Key findings documented
- [ ] Requirements referenced

---

### 5. Create Requirements Document

**File:** `docs/maintainers/research/[topic]/requirements.md`

```markdown
# Requirements - [Topic Name]

**Source:** Research on [topic]  
**Status:** [Draft | Final]  
**Created:** YYYY-MM-DD  
**Last Updated:** YYYY-MM-DD

---

## 📋 Overview

This document captures requirements discovered during research on [topic].

**Research Source:** [research-summary.md](research-summary.md)

---

## ✅ Functional Requirements

### FR-1: [Requirement Name]

**Description:** [Requirement description]

**Source:** [research-[question].md](research-[question].md)

**Priority:** [High | Medium | Low]

**Status:** 🔴 Pending

---

### FR-2: [Requirement Name]

**Description:** [Requirement description]

**Source:** [research-[question].md](research-[question].md)

**Priority:** [High | Medium | Low]

**Status:** 🔴 Pending

---

## 🎯 Non-Functional Requirements

### NFR-1: [Requirement Name]

**Description:** [Requirement description]

**Source:** [research-[question].md](research-[question].md)

**Priority:** [High | Medium | Low]

**Status:** 🔴 Pending

---

### NFR-2: [Requirement Name]

**Description:** [Requirement description]

**Source:** [research-[question].md](research-[question].md)

**Priority:** [High | Medium | Low]

**Status:** 🔴 Pending

---

## ⚠️ Constraints

### C-1: [Constraint Name]

**Description:** [Constraint description]

**Source:** [research-[question].md](research-[question].md)

---

## 💭 Assumptions

### A-1: [Assumption Name]

**Description:** [Assumption description]

**Source:** [research-[question].md](research-[question].md)

---

## 🔗 Related Documents

- [Research Summary](research-summary.md)
- [Research Documents](README.md)

---

## 🚀 Next Steps

1. Review and refine requirements
2. Use `/decision [topic] --from-research` to make decisions
3. Decisions may refine requirements

---

**Last Updated:** YYYY-MM-DD
```

**Checklist:**

- [ ] Requirements document created
- [ ] Requirements extracted from research documents
- [ ] Requirements categorized (functional, non-functional, constraints, assumptions)

---

### 6. Update Research Hub

**Update research hub:**

**File location (auto-detected):**
- **Template Structure:** `docs/maintainers/research/README.md`
- **Project-Wide:** `docs/maintainers/research/README.md`

```markdown
# Research Hub

**Purpose:** Research documents and analysis  
**Status:** ✅ Active  
**Last Updated:** YYYY-MM-DD

---

## 📋 Quick Links

### Active Research

- **[Topic 1]([topic-1]/README.md)** - [Description] (🔴 Research)
- **[Topic 2]([topic-2]/README.md)** - [Description] (🟡 Analysis)

---

## 🎯 Overview

This directory contains research documents supporting exploration and decision-making.

**Workflow:**
1. `/explore [topic]` - Start exploration
2. `/research [topic] --from-explore [topic]` - Conduct research
3. `/decision [topic] --from-research` - Make decisions
4. `/transition-plan --from-adr` - Transition to planning

---

**Last Updated:** YYYY-MM-DD
```

**Checklist:**

- [ ] Research hub created/updated
- [ ] New research added to quick links

---

### 7. Commit and Push Changes

**IMPORTANT:** Always commit work before completing command.

**Since research is documentation-only, use docs-only workflow:**

**Branch naming:**

- Format: `docs/research-[topic]` (e.g., `docs/research-template-generation-testing-automation`)

**Steps:**

1. **Check current branch:**

   ```bash
   git branch --show-current
   ```

2. **Create docs branch (if not already on one):**

   ```bash
   git checkout -b docs/research-[topic]
   ```

3. **Stage all changes:**

   ```bash
   git add docs/maintainers/research/[topic]/
   ```

4. **Commit with proper message:**

   ```bash
   git commit -m "docs(research): add [topic] research

   Created research documents:
   - Research hub with [N] research topics
   - [Research document 1]
   - [Research document 2]
   - Requirements document ([N] FRs, [N] NFRs)

   Related: [Context]"
   ```

5. **Push branch:**

   ```bash
   git push origin docs/research-[topic]
   ```

6. **Merge directly to develop (docs-only, no PR needed):**

   ```bash
   git checkout develop
   git pull origin develop
   git merge docs/research-[topic] --no-edit
   git push origin develop
   ```

7. **Clean up branch:**
   ```bash
   git branch -d docs/research-[topic]
   git push origin --delete docs/research-[topic]
   ```

8. **Verify no uncommitted changes:**
   ```bash
   git status --short
   ```

---

## Conduct Mode Workflow (`--conduct`)

**When to use:** After research structure has been created (Setup Mode), use Conduct Mode to actually perform the research.

### 1. Identify Research to Conduct

**Determine scope:**

1. **All Topics** (`/research [topic] --conduct`):
   - Process all research documents in the topic directory
   - Research high-priority topics first

2. **Specific Topic** (`--topic-num N` or `--topic-name [name]`):
   - Research only the specified topic
   - Useful for incremental progress

**Read the research document:**

```bash
# Example: Read research-user-demand.md
# Extract: Question, Goals, Methodology, Sources to investigate
```

**Checklist:**

- [ ] Research document(s) identified
- [ ] Research question understood
- [ ] Goals clear
- [ ] Sources to investigate listed

---

### 2. Conduct Web Research

**IMPORTANT:** Web search is **required** for Conduct Mode.

**For each research topic:**

1. **Formulate search queries** based on:
   - The research question
   - Sub-questions listed
   - Sources mentioned in methodology

2. **Execute web searches:**
   - Use `web_search` tool for current information
   - Search for industry patterns, best practices
   - Look for real-world examples and implementations
   - Find documentation, tutorials, case studies

3. **Document findings:**
   - Record each finding with source
   - Note relevance to research question
   - Capture quotes or key data points

**Example searches for "User Demand" research:**
```
- "experimental features adoption rate software"
- "beta feature user preferences developer tools"
- "feature flags user opt-in patterns"
- "early adopter vs mainstream user preferences"
```

**Checklist:**

- [ ] Search queries formulated
- [ ] Web searches executed
- [ ] Findings documented with sources
- [ ] Relevance noted for each finding

---

### 3. Fill In Research Document

**Update the research document with actual findings:**

```markdown
## 📊 Findings

### Finding 1: Industry Adoption Patterns

Early adopter segments typically represent 10-15% of user base for developer tools.
Studies show beta/experimental feature opt-in rates vary from 5-25% depending on
how features are communicated and the perceived value.

**Source:** [Web search: "beta feature adoption rates developer tools"]

**Relevance:** Helps set expectations for experimental template adoption.

---

### Finding 2: Communication is Key

Projects with clear stability communication (like Rust editions, Node.js LTS)
see higher adoption of experimental features because users understand the risk.

**Source:** [Rust Edition Guide, Node.js Release Schedule documentation]

**Relevance:** Supports need for clear stability communication in our approach.
```

**Analysis section:**

```markdown
## 🔍 Analysis

Based on the findings, we can expect:
- 5-15% of users would likely opt-in to experimental features
- Clear communication significantly increases adoption confidence
- Low-friction opt-in (flag vs separate template) affects adoption

**Key Insights:**
- [x] Insight 1: Early adopter segment exists and wants experimental features
- [x] Insight 2: Communication quality directly impacts adoption rates
```

**Recommendations section:**

```markdown
## 💡 Recommendations

- [x] Recommendation 1: Implement experimental template with clear stability indicators
- [x] Recommendation 2: Provide easy upgrade path when features graduate
```

**Requirements discovered:**

```markdown
## 📋 Requirements Discovered

- [x] REQ-1: Stability levels must be clearly visible in template documentation
- [x] REQ-2: Users should be able to identify which commands are experimental
```

**Checklist:**

- [ ] Findings filled in with sources
- [ ] Analysis completed
- [ ] Key insights documented
- [ ] Recommendations made
- [ ] Requirements extracted

---

### 4. Update Research Status

**Update the research document status:**

```markdown
**Status:** ✅ Complete
**Completed:** YYYY-MM-DD
```

**Update research goals:**

```markdown
## 🔍 Research Goals

- [x] Goal 1: Understand what percentage of users would opt-in
- [x] Goal 2: Identify which experimental features would be most valuable
- [x] Goal 3: Assess user comfort level with instability
```

**Update methodology sources:**

```markdown
**Sources:**
- [x] Web search: Industry adoption patterns
- [x] Web search: Beta feature communication
- [x] Case studies: Rust, Node.js, VS Code
```

---

### 5. Update Summary and Requirements

**Update `research-summary.md`:**

```markdown
## 🔍 Key Findings

### Finding 1: User Demand Exists

Research confirms 5-15% early adopter segment for developer tools.
Communication quality significantly impacts adoption rates.

**Source:** [research-user-demand.md](research-user-demand.md)
```

**Update `requirements.md`:**

Add any new requirements discovered during research:

```markdown
### FR-5: Stability Indicators

**Description:** Each command must display its stability level (Stable/Experimental)

**Source:** [research-user-demand.md](research-user-demand.md)

**Priority:** High

**Status:** 🔴 Pending
```

---

### 6. Update Hub Status

**Update the research hub status table:**

```markdown
## 📊 Research Status

| Research Topic | Priority | Status | Document |
|----------------|----------|--------|----------|
| User Demand | 🔴 High | ✅ Complete | [research-user-demand.md](research-user-demand.md) |
| Implementation Approach | 🔴 High | 🔴 Not Started | [research-implementation-approach.md](research-implementation-approach.md) |
```

---

### 7. Commit Research Results

**Commit with clear message:**

```bash
git add docs/maintainers/research/[topic]/
git commit -m "docs(research): conduct [topic-name] research

Completed research for [topic]:
- [N] findings documented with sources
- [N] key insights identified
- [N] recommendations made
- [N] requirements discovered

Sources: [List key sources]"
```

**Push changes:**

```bash
git push origin develop
```

---

### Conduct Mode Output

**After conducting research, you should have:**

1. ✅ Filled research document(s) with actual findings
2. ✅ Sources documented for each finding
3. ✅ Analysis and insights completed
4. ✅ Recommendations made
5. ✅ Requirements extracted
6. ✅ Summary updated
7. ✅ Hub status updated
8. ✅ Changes committed

**Next step:** Use `/decision [topic] --from-research` when all research is complete.

---

## Integration with Other Commands

### Research → Decision → Planning Flow

1. **`/research [topic] --from-explore [topic]`** - Conduct research
   - Reads research topics from exploration
   - Creates research documents
   - Outputs: Research documents + `requirements.md`

2. **`/research [topic] --from-reflect [reflection-file]`** - Research from reflection
   - Reads opportunities from reflection
   - Creates research documents
   - Outputs: Research documents + `requirements.md`

3. **`/decision [topic] --from-research`** - Make decisions
   - Reads research documents
   - Reads requirements document
   - Creates ADR documents
   - Outputs: ADR documents

4. **`/transition-plan --from-adr`** - Transition to planning
   - Reads ADR documents
   - Automatically reads requirements if they exist
   - Creates feature plan and phase documents
   - Outputs: Transition plan + Feature plan + Phase documents

---

## Common Scenarios

### Scenario 1: Setup from Exploration

**Situation:** Exploration identified research topics, need to create structure

**Action:**
```bash
/research auth-system --from-explore new-authentication-system
```

**Output:**
- Research hub created
- Research documents created (templates)
- Requirements skeleton created
- Ready for Conduct Mode

---

### Scenario 2: Setup from Reflection

**Situation:** Reflection identified opportunities needing research

**Action:**
```bash
/research ci-optimization --from-reflect reflection-project-2025-12-07.md
```

**Output:**
- Research hub created
- Research documents created (templates)
- Requirements skeleton created
- Ready for Conduct Mode

---

### Scenario 3: Conduct All Research

**Situation:** Research structure exists, ready to actually research

**Action:**
```bash
/research experimental-template --conduct
```

**Output:**
- All research documents filled in with findings
- Web searches conducted for each topic
- Analysis and recommendations completed
- Requirements extracted
- Summary updated
- Ready for decision phase

---

### Scenario 4: Conduct Single Topic

**Situation:** Want to research incrementally, one topic at a time

**Action:**
```bash
/research experimental-template --conduct --topic-num 1
# or
/research experimental-template --conduct --topic-name user-demand
```

**Output:**
- Single research document filled in
- Web searches conducted for that topic
- Findings, analysis, recommendations for that topic
- Hub status updated for that topic
- Continue with next topic when ready

---

## Tips

### When to Use Each Mode

**Setup Mode:**
- After exploration identifies research topics
- After reflection identifies opportunities
- When you need research structure but not ready to research yet

**Conduct Mode:**
- When research structure already exists
- When ready to actually investigate topics
- When you have time for web searches and analysis

### Best Practices

- **Setup first, conduct later** - Create structure when planning, conduct when ready
- **Document sources** - Every finding needs a source reference
- **Use web search** - Required for Conduct Mode, ensures current information
- **Extract requirements** - Capture requirements as you research
- **Update summary** - Keep research summary current after each topic
- **Incremental progress** - Use `--topic-num` to research one topic at a time

---

## Reference

**Research Structure:**

- **Template Structure:** `docs/maintainers/research/[topic]/`
- **Project-Wide:** `docs/maintainers/research/[topic]/`
- Requirements: `[research-path]/[topic]/requirements.md`

**Related Commands:**

- `/explore` - Start exploration and identify research topics
- `/decision` - Make decisions based on research
- `/transition-plan` - Transition to feature planning

---

**Last Updated:** 2025-12-16  
**Status:** ✅ Active  
**Next:** Use Setup Mode to create structure, Conduct Mode to actually research
