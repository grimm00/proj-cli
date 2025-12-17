# Cross-PR Fix Batches

**Purpose:** Fix batches created from fix-review reports across multiple PRs  
**Status:** ✅ Active  
**Last Updated:** 2025-12-17

---

## 📋 Quick Links

### Active Batches

- **[quick-wins-01.md](quick-wins-01.md)** - Quick Wins (🟡 MEDIUM/🟢 LOW, 🟢 LOW effort, 7 issues)

---

## 📊 Summary

**Total Batches:** 1  
**Total Issues:** 7  
**Source PRs:** #1, #2, #3

**Priority Breakdown:**
- 🟡 MEDIUM: 4 issues
- 🟢 LOW: 3 issues

**Effort Breakdown:**
- 🟢 LOW: 7 issues (all)

---

## 🟡 Active Batches

### Quick Wins Batch

- **Status:** 🔴 Not Started
- **Issues:** 7 issues (4 MEDIUM, 3 LOW priority, all LOW effort)
- **File:** [quick-wins-01.md](quick-wins-01.md)
- **Estimated:** ~1-1.5 hours
- **Source:** fix-review-report-2025-12-17.md

**Issues:**
1. PR1-#1: Add explicit encoding for config file
2. PR1-#3: Fix brittle return code test
3. PR1-#7: Add test for __version__ matching metadata
4. PR2-OC1: API URL validation in APIClient constructor
5. PR2-OC2: Format option validation with typer.Choice
6. PR3-#3: Defensive JSON parsing for inventory.json
7. PR3-Overall: Dedupe logic docs alignment

---

## 📝 Implementation Notes

**To implement a batch:**
```bash
/fix-implement quick-wins-01
```

**After implementation:**
```bash
/pr --fix quick-wins-01
```

---

**Last Updated:** 2025-12-17

