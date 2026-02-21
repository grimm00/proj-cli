# Discuss Command

Structured read-only conversation with context. Express thoughts, react to findings, and talk through ideas without the AI modifying any files. The AI reads relevant context for informed responses but produces no side effects until the user explicitly promotes discussion points.

---

## Why This Exists

With agentic coding, every command tends to produce artifacts. When you're reacting to research findings, questioning assumptions, or thinking through implications, the AI can misinterpret casual thoughts as directives to update requirements, amend explorations, or add findings. This creates premature formalization -- thoughts get committed to artifacts before they're ready.

`/discuss` fills the gap between casual chat and formal exploration. It's the "let me think about this" mode where:

- You can freely express reactions, concerns, and half-formed ideas
- The AI engages substantively with full project context
- No files are created, modified, or committed
- At the end, you decide what (if anything) gets promoted to formal artifacts

---

## Configuration

**Context Sources:**

The command loads relevant context based on the topic reference:

1. **Exploration context:** `admin/explorations/[topic]/exploration.md`, `research-topics.md`
2. **Research context:** `admin/research/[topic]/` -- hub, summary, topic documents, requirements
3. **Decision context:** `admin/decisions/[topic]/` -- ADRs
4. **Planning context:** `admin/planning/features/[feature]/` -- plans, status

**Path detection** follows the same patterns as `/explore` and `/research` (dev-infra, template structure, project-wide).

---

## Usage

**Command:** `/discuss [topic] [options]`

**Examples:**

- `/discuss workflow-simplification "Should we really put scripts in dev-infra?"` - Discuss with inline thought
- `/discuss workflow-simplification` - Open discussion referencing current exploration/research
- `/discuss --context research/topic-3` - Discuss with specific research topic loaded
- `/discuss` - Free-form discussion with no specific context

**Options:**

- `[topic]` - Topic name to load context from (exploration, research, decisions)
- `--context [path]` - Load specific file or directory as context
- `--summary` - At end of discussion, produce a structured summary of points raised

---

## Behavior Rules

**CRITICAL -- Read-Only Mode:**

When `/discuss` is invoked, the AI MUST follow these rules:

1. **DO NOT** create, modify, or delete any files
2. **DO NOT** update requirements, findings, recommendations, or status documents
3. **DO NOT** append themes to explorations or topics to research
4. **DO NOT** commit anything
5. **DO** read any files needed for informed responses
6. **DO** reference specific findings, requirements, or documents by name/number
7. **DO** challenge assumptions, identify gaps, and offer analysis
8. **DO** suggest what actions the user might take after the discussion

**The AI should treat every user message in a `/discuss` session as a thought to engage with, not a directive to implement.**

---

## Workflow

### Starting a Discussion

```
/discuss workflow-simplification "I'm not sure about the tiered approach"
```

The AI:
1. Loads relevant context (exploration, research, requirements for workflow-simplification)
2. Acknowledges the discussion mode (no artifacts will be modified)
3. Responds to the user's thought with analysis, drawing on loaded context
4. Continues the conversation as long as the user wants

### During the Discussion

The user can:
- React to research findings ("Finding 3 assumes too much about task count")
- Question recommendations ("Is the hybrid interface actually better?")
- Raise new concerns ("What about projects that don't use dev-toolkit?")
- Think through implications ("If we go with tiered, what does migration look like?")
- Compare options ("Walk me through the tradeoffs of specs-only vs scripts")

The AI should:
- Reference specific documents and findings when relevant
- Play devil's advocate when the user seems to be confirming their own bias
- Identify connections the user might not have seen
- Note when a thought seems significant enough to capture formally
- Keep track of key discussion points throughout the conversation

### Ending a Discussion

The user can end the discussion at any time. If `--summary` was specified (or the user asks for one), the AI produces a structured summary:

```markdown
## Discussion Summary: [Topic]

**Date:** YYYY-MM-DD
**Context:** [What was being discussed]

### Key Points Raised

1. [Point 1 -- brief description]
2. [Point 2 -- brief description]

### Questions Identified

1. [Question that emerged from discussion]
2. [Question that emerged from discussion]

### Suggested Actions

- [ ] `/explore [topic] --amend "..."` -- [if a new theme was identified]
- [ ] `/int-opp` -- [if an internal improvement was identified]
- [ ] `/research [topic] --add-topic N` -- [if a new research topic emerged]
- [ ] No action needed -- [if the discussion was purely clarifying]
```

**The summary is displayed in chat only.** It is NOT written to any file unless the user explicitly asks for it to be saved.

---

## Integration with Other Commands

### Position in Workflow

```
/explore [topic]                    <- Organize thoughts into themes
    |
/discuss [topic] "reaction..."     <- Think through ideas (no side effects)
    |                                  Can happen at ANY point in the workflow
    ├── Result: nothing             <- Just needed to talk it through
    ├── /explore --amend            <- Thought was significant, add to exploration
    ├── /int-opp                    <- Identified an internal improvement
    └── /research --add-topic       <- New research question emerged
```

`/discuss` is not a pipeline step -- it's a **lateral tool** that can be invoked at any point during exploration, research, decision-making, or implementation. It doesn't feed into or block any other command.

### When to Use `/discuss` vs Other Commands

| Situation | Command | Why |
|-----------|---------|-----|
| Organizing unstructured thoughts into themes | `/explore` | Creates formal exploration artifacts |
| Reacting to a research finding | `/discuss` | No artifacts needed yet; thinking out loud |
| Questioning a recommendation | `/discuss` | Want to challenge before deciding |
| Identifying a new improvement | `/int-opp` | Ready to capture formally |
| Adding a theme after research | `/explore --amend` | Ready to formalize the thought |
| Half-formed concern, not sure if it matters | `/discuss` | Talk it through first |
| Comparing tradeoffs before deciding | `/discuss` | Need analysis, not artifacts |

---

## Common Scenarios

### Scenario 1: Reacting to Research Findings

**Situation:** You're reading Topic 3 findings and disagree with the single-file recommendation.

```
/discuss workflow-simplification "Have we really weighed the pros and cons 
of squashing everything into one file? What about AI context waste?"
```

**AI behavior:** Reads Topic 3 findings, analyzes the concern, presents tradeoffs. Does NOT update Topic 3 or add requirements.

**After discussion:** User decides to `/explore workflow-simplification --amend` to add the concern as a formal theme.

---

### Scenario 2: Questioning a Design Decision

**Situation:** You're not sure whether dev-infra should maintain scripts.

```
/discuss workflow-simplification "Should this repo be maintaining any code 
outside of CI? Won't scripts just get deprecated when dev-toolkit implements them?"
```

**AI behavior:** Reads current exploration themes, research requirements, dev-toolkit patterns. Engages with the question. Does NOT add themes, requirements, or findings.

**After discussion:** User decides the concern is significant enough for `/explore --amend`.

---

### Scenario 3: Just Thinking Out Loud

**Situation:** You had a related thought but aren't sure it's relevant.

```
/discuss "I wonder if the tiered approach is overengineering this. 
Most features are probably simple or medium."
```

**AI behavior:** Analyzes the distribution of feature sizes across existing projects. Responds with data. Does NOT create any artifacts.

**After discussion:** User decides no action needed -- the thought was clarifying, not actionable.

---

### Scenario 4: Comparing Options

**Situation:** You want to think through the tradeoffs of two approaches before committing.

```
/discuss workflow-simplification --context admin/research/workflow-simplification/topic-3-transition-plan-output-format.md "Walk me through specs-only vs scripts vs hybrid for the tier logic"
```

**AI behavior:** Reads the specific document, analyzes each approach, presents structured comparison. Does NOT update any documents.

**After discussion:** User has clarity and proceeds to the decision phase.

---

## Tips

### When to Use

- **Reacting** -- You're reading findings and have a gut reaction
- **Questioning** -- Something doesn't feel right but you can't articulate why
- **Comparing** -- You want to think through options before committing
- **Clarifying** -- You need to talk through something to understand it
- **Challenging** -- You want the AI to push back on your assumptions

### When NOT to Use

- You already know the thought should be captured -- use `/explore --amend` or `/int-opp` directly
- You want to create a new exploration -- use `/explore`
- You want to make a decision -- use `/decision`
- You need to conduct research -- use `/research --conduct`

### Best Practices

- **Be honest about uncertainty** -- "I'm not sure about..." is a perfect `/discuss` input
- **Don't feel pressure to act** -- Not every discussion needs a follow-up command
- **Ask for a summary** when the discussion was substantive and you want to preserve key points
- **Use `--context`** to load specific documents when your thought is about something specific

---

## Reference

**Related Commands:**

- `/explore` - Organize thoughts into formal themes (creates artifacts)
- `/explore --amend` - Add thought to existing exploration (modifies artifacts)
- `/int-opp` - Capture internal improvement (creates artifacts)
- `/research` - Conduct structured research (creates artifacts)
- `/reflect` - Project reflection and suggestions (creates artifacts)

---

**Last Updated:** 2026-02-13
**Status:** ✅ Active
