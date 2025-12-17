# proj-cli - Fix Tracking Hub

**Purpose:** Track and document fixes for the proj-cli feature  
**Status:** ✅ Active  
**Last Updated:** 2025-12-16

---

## 📋 Quick Links

### By PR

No PRs yet - Phase 1 PR pending.

### Cross-PR Batches

None yet.

---

## 📁 Directory Structure

```
fix/
├── README.md                    # This hub file
├── pr##/                        # PR-specific fixes
│   ├── README.md                # PR hub
│   └── issue-N-description.md   # Individual issue
├── cross-pr/                    # Cross-PR batches
│   └── batch-name.md            # Batch fix plans
└── archived/                    # Completed fix PRs
    └── README.md                # Archive hub
```

---

## 🔄 Fix Workflow

1. **After PR Review:** Run `/fix-plan` to create fix plans from Sourcery feedback
2. **Batch Issues:** Group by priority/effort for efficient fixing
3. **Implement Fixes:** Use `/fix-implement` with TDD workflow
4. **Create Fix PR:** Use `/pr --fix [batch-name]`
5. **Post-Merge:** Use `/post-pr` to update tracking and clean up

---

## 📊 Fix Statistics

| Category | Count |
|----------|-------|
| Total Issues | 0 |
| Resolved | 0 |
| Pending | 0 |
| Deferred | 0 |

---

**Last Updated:** 2025-12-16

