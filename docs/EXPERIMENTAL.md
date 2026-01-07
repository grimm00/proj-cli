# Experimental Commands Guide

**Purpose:** Documentation for experimental/evolving commands in this template
**Last Updated:** 2025-12-12

---

## 📋 Overview

This template includes experimental commands that are not yet stable enough for the standard template. These commands provide early access to new features and are subject to change.

---

## 🟠 Evolving Commands

### `/status` - Project Status Tracking

**Status:** 🟠 Evolving
**Stability:** Experimental - may change without notice

**Purpose:** View, update, and sync project status tracking across features and phases.

**What it does:**
- Shows current progress at a glance
- Updates status documents consistently
- Syncs status with actual git history
- Validates status accuracy

**Known Limitations:**
- Command interface may change
- Some features may be incomplete
- Documentation may be updated frequently

**Feedback:** Please report issues or suggestions via GitHub Issues.

---

## 🔄 Graduation Process

Experimental commands graduate to the standard template when they meet the following criteria (from ADR-004):

- ✅ **Time in dev-infra:** ≥1 release cycle in dev-infra
- ✅ **Stability:** No major changes in 2+ weeks
- ✅ **Documentation:** 100% complete
- ✅ **Usage:** Demonstrated use in dev-infra
- ✅ **No critical bugs:** No open critical issues

When a command graduates, it will be:
1. Added to the standard template
2. Removed from experimental template (or marked as stable)
3. Announced in release notes

---

## 💬 Providing Feedback

Your feedback helps improve these commands! Please provide feedback via:

- **GitHub Issues:** Create an issue with the `experimental` label
- **Command-specific feedback:** See individual command documentation

**What to include:**
- What worked well
- What needs improvement
- Any bugs or issues encountered
- Suggestions for enhancements

---

## ⚠️ Important Notes

**Breaking Changes:**
- Experimental commands may change without notice
- Breaking changes will be documented in release notes when possible
- Always test experimental commands in non-production environments first

**Support:**
- Experimental commands receive best-effort support
- Critical bugs will be prioritized
- Feature requests are welcome but not guaranteed

**Stability Levels:**
- 🟢 **Stable** - Production-ready, included in standard template
- 🟠 **Experimental** - Under development, included in experimental template
- 🔴 **Deprecated** - Will be removed, migration path provided

---

## 🔗 Related Documentation

- [ADR-004: Graduation Process](../../admin/decisions/dev-infra-identity-and-focus/adr-004-graduation-process.md)
- [Command Tiers](../../admin/decisions/dev-infra-identity-and-focus/adr-003-command-strategy.md)
- [Main README](../README.md)

---

**Last Updated:** 2025-12-12

