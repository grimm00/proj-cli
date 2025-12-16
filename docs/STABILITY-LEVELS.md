# Stability Levels

**Purpose:** Communicate the maturity of features and commands  
**Last Updated:** 2025-12-15

---

## Overview

This project uses stability levels to communicate the maturity of features and commands. This helps you make informed decisions about adoption and understand what to expect from different features.

---

## Stability Indicators

| Indicator | Level        | Meaning          |
| --------- | ------------ | ---------------- |
| 🟢        | Stable       | Production-ready |
| 🟠        | Experimental | May change       |
| 🔴        | Deprecated   | Being removed    |

---

## Stable (🟢)

Features marked as **Stable**:

- Have been tested in production
- Have complete documentation
- Follow semantic versioning for changes
- Are included in the standard template
- Have backward compatibility guarantees

**What this means for you:**

- Safe to use in production
- Breaking changes follow deprecation process
- API/behavior is well-documented
- Updates are incremental and predictable

---

## Experimental (🟠)

Features marked as **Experimental**:

- Are under active development
- May change without notice
- May have incomplete documentation
- Are included only in the experimental template
- Welcome feedback and bug reports

**What this means for you:**

- Use with caution in production
- Check release notes before updating
- Provide feedback to help shape the feature
- Be prepared to adapt to changes

**How to provide feedback:**

- Create an issue using the [Experimental Feature Feedback](../.github/ISSUE_TEMPLATE/experimental-feedback.yml) template
- Include which command/feature you're providing feedback on
- Describe what worked well and what could be improved

---

## Deprecated (🔴)

Features marked as **Deprecated**:

- Will be removed in a future release
- Have migration guides available
- Should be replaced with alternatives
- Are still functional but not recommended

**What this means for you:**

- Plan migration to alternatives
- Check migration guides for replacement options
- Timeline for removal is documented in release notes
- Existing functionality continues to work until removal

---

## Graduation Process

Experimental features graduate to Stable when they meet the [graduation criteria](GRADUATION-CHECKLIST.md).

### Required Criteria (ALL must be met)

- ≥1 release cycle in dev-infra
- No major changes in 2+ weeks
- Documentation 100% complete
- Demonstrated use in dev-infra
- No open critical issues

### Graduation Timeline

1. **Experimental Phase:** Active development, frequent changes
2. **Stabilization:** Feature freeze, documentation complete
3. **Review Period:** 1 week minimum, final testing
4. **Graduation:** Move to standard template, update indicators

---

## Identifying Stability Levels

### In Command Documentation

Commands display their stability level in the header:

```markdown
# Command Name

**Status:** 🟠 Experimental  
**Stability:** Evolving - may change without notice  
**Feedback:** [Create issue](link)

> ⚠️ **Experimental Command**: This command is under active development...
```

### In README Files

The main README lists commands with their stability indicators:

```markdown
## Available Commands

| Command | Status | Description |
|---------|--------|-------------|
| `/example` | 🟠 Experimental | Does something useful |
```

---

## Questions?

If you're unsure about a feature's stability level or have questions about adoption:

1. Check the feature's documentation header
2. Look for stability indicators in the README
3. Create an issue for clarification

---

## Related Documents

- **[Graduation Checklist](GRADUATION-CHECKLIST.md)** - Criteria for graduating commands
- **[Experimental Features](EXPERIMENTAL.md)** - Overview of experimental template
- **[Feedback Template](../.github/ISSUE_TEMPLATE/experimental-feedback.yml)** - Report feedback

---

**Last Updated:** 2025-12-15

