# Template Generation Extension - Feature Hub

**Feature:** Extend proj create with template generation from dev-infra  
**Status:** 🔴 Not Started  
**Created:** 2025-01-05  
**ADR:** [ADR-0008](../../decisions/ADR-0008-template-generation-extension.md)  
**Extends:** [proj-cli feature](../proj-cli/README.md)

---

## 📋 Quick Links

### Phase Documents

| Phase | Name | Status | Effort |
|-------|------|--------|--------|
| [Phase 1](phase-1.md) | Config Extension | ✅ Complete | ~2 hrs |
| [Phase 2](phase-2.md) | Local Registry | ✅ Expanded | ~2 hrs |
| [Phase 3](phase-3.md) | Template Copying | 🔴 Scaffolding | ~3 hrs |
| [Phase 4](phase-4.md) | Create Command Extension | 🔴 Scaffolding | ~3 hrs |
| [Phase 5](phase-5.md) | Testing & Polish | 🔴 Scaffolding | ~2 hrs |

### Supporting Documents

- **[Feature Plan](feature-plan.md)** - Requirements and success criteria
- **[Transition Plan](transition-plan.md)** - Phase breakdown and implementation strategy
- **[Status & Next Steps](status-and-next-steps.md)** - Current progress tracking

### Source Documents

- **[ADR-0008](../../decisions/ADR-0008-template-generation-extension.md)** - Architecture decision
- **[Requirements](../../research/proj-cli-architecture/requirements.md)** - Full requirements list
- **[Research Hub](../../research/proj-cli-architecture/README.md)** - Research findings
- **[Exploration](../../explorations/proj-cli-architecture/README.md)** - Initial exploration

---

## 🎯 Overview

Extend the existing `proj create` command with template generation capabilities from dev-infra. This provides:

1. **Interactive mode (default):** Prompts for project name, template, description
2. **Template mode (`--template`):** Creates project from dev-infra template  
3. **API-only mode (`--api-only`):** Preserves current behavior (API record only)
4. **Local-only mode (`--local-only`):** Works without API connectivity

### Key Benefits

- **Unified Workflow:** Single command for all project creation scenarios
- **Interactive-First:** Matches familiar `new-project.sh` UX
- **Backward Compatible:** Existing `proj create` usage unchanged
- **Offline Support:** Works without API when configured
- **Local Tracking:** Registry enables future sync feature

---

## 📊 Progress Summary

| Phase | Focus | Effort | Status | Completion |
|-------|-------|--------|--------|------------|
| 1 | Config Extension | ~2 hrs | ✅ Complete | 100% |
| 2 | Local Registry | ~2 hrs | ✅ Expanded | 0% impl |
| 3 | Template Copying | ~3 hrs | 🔴 Scaffolding | 0% |
| 4 | Create Command Extension | ~3 hrs | 🔴 Scaffolding | 0% |
| 5 | Testing & Polish | ~2 hrs | 🔴 Scaffolding | 0% |
| **Total** | | **~12 hrs** | | **0%** |

---

## 🚀 Next Steps

1. **Implement Phase 2** - Use `/task-phase 2 1` to begin Task 1
2. **Create PR** - Use `/pr --phase 2` after implementation
3. **Expand Phase 3** - Run `/transition-plan template-generation --expand --phase 3` when ready

---

## 📚 Related Documents

### Planning

- [Features Hub](../README.md) - All features overview
- [Planning Hub](../../README.md) - Overall planning

### External

- [proj-cli README](../../../../../README.md) - Project documentation
- [dev-infra new-project.sh](https://github.com/grimm00/dev-infra/blob/develop/scripts/new-project.sh) - Source script

---

**Last Updated:** 2025-01-05  
**Status:** ✅ Phase 2 Expanded  
**Next:** Begin implementation with `/task-phase 2 1`


