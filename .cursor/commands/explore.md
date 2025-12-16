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

**Key principle:** Start with exploration to identify research topics, then move to research phase.

**Workflow:**
```
/explore [topic]
  → Creates exploration document
  → Identifies research topics/questions
  → Outputs: research-topics.md (list of research questions)
```

---

## Usage

**Command:** `/explore [topic] [options]`

**Examples:**

- `/explore new-authentication-system` - Start exploration for new auth system
- `/explore "improve ci pipeline"` - Start exploration (topic sanitized to `improve-ci-pipeline`)
- `/explore --topic database-choice` - Specify topic explicitly
- `/explore --dry-run` - Show what would be created without creating files

**Options:**

- `--topic [name]` - Specify topic name (overrides prompt)
- `--dry-run` - Show what would be created without creating files

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

### 2. Create Exploration Document

**Location Detection:**

- **Dev-Infra:** `admin/explorations/[topic]/`
- **Template Structure:** `docs/maintainers/planning/explorations/[topic]/`
- **Project-Wide:** `docs/maintainers/planning/explorations/[topic]/`

**Auto-detection:**
- Check if `admin/explorations/` exists → use dev-infra structure
- Check if `docs/maintainers/planning/explorations/` exists → use template structure
- Otherwise → use project-wide structure

**Directory structure:**

```
explorations/[topic]/
├── README.md                    # Exploration hub
├── exploration.md                # Main exploration document
└── research-topics.md            # List of research topics/questions
```

**Create exploration hub:**

**File:** `docs/maintainers/planning/explorations/[topic]/README.md`

```markdown
# [Topic Name] - Exploration Hub

**Purpose:** Explore [topic description]  
**Status:** 🔴 Exploration  
**Created:** YYYY-MM-DD  
**Last Updated:** YYYY-MM-DD

---

## 📋 Quick Links

- **[Exploration Document](exploration.md)** - Main exploration document
- **[Research Topics](research-topics.md)** - Research questions to investigate

---

## 🎯 Overview

[Brief description of what we're exploring and why]

---

## 📊 Status

**Current Phase:** Exploration  
**Next Step:** Conduct research on topics identified in research-topics.md

---

**Last Updated:** YYYY-MM-DD
```

**Create exploration document:**

**File:** `docs/maintainers/planning/explorations/[topic]/exploration.md`

```markdown
# [Topic Name] - Exploration

**Status:** 🔴 Exploration  
**Created:** YYYY-MM-DD  
**Last Updated:** YYYY-MM-DD

---

## 🎯 What Are We Exploring?

[Clear description of the topic, idea, or proof of concept]

---

## 🤔 Why Explore This?

[Context: What problem does this solve? What opportunity does it present?]

---

## 💡 Initial Thoughts

[Any initial ideas, concepts, or approaches]

---

## 🔍 Key Questions

- [ ] Question 1: [What do we need to understand?]
- [ ] Question 2: [What are the options?]
- [ ] Question 3: [What are the trade-offs?]
- [ ] Question 4: [What are the risks?]

---

## 🚀 Next Steps

1. Review research topics in `research-topics.md`
2. Use `/research [topic] --from-explore [topic]` to conduct research
3. After research, use `/decision [topic] --from-research` to make decisions

---

## 📝 Notes

[Any initial thoughts, ideas, or concerns]

---

**Last Updated:** YYYY-MM-DD
```

**Create research topics document:**

**File:** `docs/maintainers/planning/explorations/[topic]/research-topics.md`

```markdown
# Research Topics - [Topic Name]

**Purpose:** List of research topics/questions to investigate  
**Status:** 🔴 Pending Research  
**Created:** YYYY-MM-DD  
**Last Updated:** YYYY-MM-DD

---

## 📋 Research Topics

This document lists research topics and questions that need investigation before making decisions.

### Research Topic 1: [Topic Name]

**Question:** [What specific question needs to be answered?]

**Why:** [Why is this research needed?]

**Priority:** [High | Medium | Low]

**Status:** 🔴 Not Started

---

### Research Topic 2: [Topic Name]

**Question:** [What specific question needs to be answered?]

**Why:** [Why is this research needed?]

**Priority:** [High | Medium | Low]

**Status:** 🔴 Not Started

---

## 🎯 Research Workflow

1. Use `/research [topic] --from-explore [topic]` to conduct research
2. Research will create documents in `docs/maintainers/research/[topic]/`
3. After research complete, use `/decision [topic] --from-research` to make decisions

---

**Last Updated:** YYYY-MM-DD
```

**Checklist:**

- [ ] Exploration directory created
- [ ] Exploration hub created
- [ ] Exploration document created
- [ ] Research topics document created

---

### 3. Update Explorations Hub

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

### Exploration → Research → Decision → Planning Flow

1. **`/explore [topic]`** - Start exploration
   - Creates exploration document
   - Identifies research topics/questions
   - Outputs: `research-topics.md`

2. **`/research [topic] --from-explore [topic]`** - Conduct research
   - Reads research topics from exploration
   - Creates research documents
   - Outputs: Research documents + `requirements.md`

3. **`/decision [topic] --from-research`** - Make decisions
   - Reads research documents
   - Creates ADR documents
   - Outputs: ADR documents

4. **`/transition-plan --from-adr`** - Transition to planning
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

## Tips

### When to Use

- **New ideas** - Start exploration before jumping to research
- **Proof of concepts** - Organize thoughts before research
- **Abstract concepts** - Structure thinking before investigation

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

- `/research` - Conduct research on topics identified in exploration
- `/decision` - Make decisions based on research
- `/transition-plan` - Transition to feature planning

---

**Last Updated:** 2025-12-07  
**Status:** ✅ Active  
**Next:** Use to initiate exploration cycles for new ideas or proof of concepts

