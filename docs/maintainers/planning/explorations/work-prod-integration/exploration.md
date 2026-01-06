# Work-Prod Integration - Exploration

**Status:** 🔴 Exploration  
**Created:** 2026-01-06  
**Last Updated:** 2026-01-06

---

## 🎯 What Are We Exploring?

How should `proj-cli` integrate with the `work-prod` backend API across all its commands and features?

**Scope includes:**
- Project creation (API-only, template-based, local-only)
- Project deletion (API + registry sync)
- Registry management (local tracking of work-prod projects)
- Offline/online mode handling
- Error handling and graceful degradation
- Configuration patterns (`api_enabled`, URLs, timeouts)

---

## 🤔 Why Explore This?

**Context:** During Phase 6 of template generation, we added API sync functionality. This surfaced several questions:

1. **Scope creep:** API sync was added to a "template generation" feature, but it's really a cross-cutting concern
2. **Incomplete patterns:** `proj delete` removes from API but not from registry
3. **Missing commands:** No `proj registry` commands for cleanup/management
4. **Unclear boundaries:** When should operations be API-first vs local-first?

**The problem:** Without a clear integration design, each feature will implement API integration differently, leading to inconsistent UX and maintenance burden.

---

## 💡 Initial Thoughts

### Current State

| Command | API Integration | Local Integration | Sync? |
|---------|-----------------|-------------------|-------|
| `proj create` (API mode) | ✅ Creates in API | ❌ No registry | N/A |
| `proj create` (template) | ✅ Optional sync | ✅ Registry | ✅ API→Registry |
| `proj delete` | ✅ Deletes from API | ❌ No registry cleanup | ❌ Gap |
| `proj list` | ✅ Lists from API | ❌ No registry list | N/A |
| `proj registry` | N/A | ❌ Doesn't exist | N/A |

### Potential Patterns

**Pattern A: API-First (current for most commands)**
- Operations go to API first
- Local registry is supplementary
- Pros: Single source of truth
- Cons: Requires API connectivity

**Pattern B: Local-First**
- Operations go to local registry first
- Sync to API when available
- Pros: Works offline
- Cons: Sync complexity

**Pattern C: Dual-Track**
- Some commands are API-first, some local-first
- Clear documentation on which is which
- Pros: Best of both worlds
- Cons: Complexity, user confusion

---

## 🔍 Key Questions

- [ ] **Q1:** Should the registry be the source of truth for template-created projects, with API as sync target?
- [ ] **Q2:** Should `proj delete` have `--from-api`, `--from-registry`, or `--all` flags?
- [ ] **Q3:** Should there be a `proj sync` command for explicit sync operations?
- [ ] **Q4:** How should offline mode work across all commands?
- [ ] **Q5:** Should registry-only projects (never synced) be visible in `proj list`?
- [ ] **Q6:** What's the relationship between inventory scanning and the registry?

---

## 🏗️ Components to Consider

### 1. Registry Management
- `proj registry list` - List local registry entries
- `proj registry remove <path>` - Remove entry from registry
- `proj registry sync` - Sync registry with API

### 2. Delete Enhancement
- `proj delete <id>` - Delete from API (current)
- `proj delete <id> --from-registry` - Also remove from registry
- `proj delete <path>` - Delete by path (local + API)

### 3. Sync Commands
- `proj sync` - Sync all registry entries to API
- `proj sync --status` - Show sync status (what's synced, what's pending)

### 4. Configuration
- `api_enabled` - Global enable/disable
- `offline_mode` - Force offline operation
- `sync_on_create` - Auto-sync new projects (current Phase 6 behavior)

---

## 🚀 Next Steps

1. Review research topics in `research-topics.md`
2. Use `/research work-prod-integration` to conduct research
3. After research, use `/decision` to make architectural decisions
4. Create feature plan for implementing chosen patterns

---

## 📝 Notes

**Lesson learned from Phase 6:**
> Template generation should focus on local workflow. API integration is a separate, cross-cutting concern that deserves dedicated design work.

**Principle to consider:**
> Each feature should work fully offline. API sync should be an enhancement, not a requirement.

---

**Last Updated:** 2026-01-06

