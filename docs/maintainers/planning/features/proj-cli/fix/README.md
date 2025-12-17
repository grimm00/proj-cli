# proj-cli - Fix Tracking Hub

**Purpose:** Track and document fixes for the proj-cli feature  
**Status:** ✅ Active  
**Last Updated:** 2025-12-17

---

## 📋 Quick Links

### By PR

- **[PR #1](pr1/README.md)** - Phase 1: Repository Setup (6 deferred issues)
- **[PR #2](pr2/README.md)** - Phase 2: Migrate Project Commands (4 deferred issues)
- **[PR #3](pr3/README.md)** - Phase 3: Add Inventory Commands (7 deferred + 3 enhancements)

### Cross-PR Batches

None yet.

---

## 📁 Directory Structure

```
fix/
├── README.md                    # This hub file
├── pr1/                         # PR #1 fixes
│   └── README.md                # PR #1 hub
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
| Total Issues | 24 |
| Resolved | 10 |
| Pending | 0 |
| Deferred | 14 |
| Enhancements | 3 |

---

**Last Updated:** 2025-12-17

