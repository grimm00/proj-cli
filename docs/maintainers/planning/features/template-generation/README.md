# Template Generation Extension - Feature Hub

**Feature:** Extend proj create with template generation from dev-infra  
**Status:** 🟠 Phase 6 Ready  
**Created:** 2025-01-05  
**ADR:** [ADR-0008](../../decisions/ADR-0008-template-generation-extension.md)  
**Extends:** [proj-cli feature](../proj-cli/README.md)

---

## 📋 Quick Links

### Phase Documents

| Phase | Name | Status | Effort |
|-------|------|--------|--------|
| [Phase 1](phase-1.md) | Config Extension | ✅ Complete | ~2 hrs |
| [Phase 2](phase-2.md) | Local Registry | ✅ Complete | ~2 hrs |
| [Phase 3](phase-3.md) | Template Copying | ✅ Complete | ~3 hrs |
| [Phase 4](phase-4.md) | Create Command Extension | ✅ Complete | ~3 hrs |
| [Phase 5](phase-5.md) | Testing & Polish | 🟡 Paused | ~2 hrs |
| [Phase 6](phase-6.md) | API Sync Enhancement | 🔴 Not Started | ~2-3 hrs |

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
| 2 | Local Registry | ~2 hrs | ✅ Complete | 100% |
| 3 | Template Copying | ~3 hrs | ✅ Complete | 100% |
| 4 | Create Command Extension | ~3 hrs | ✅ Complete | 100% |
| 5 | Testing & Polish | ~2 hrs | 🟡 Paused (4/6 tasks) | 67% |
| 6 | API Sync Enhancement | ~2-3 hrs | 🔴 Not Started | 0% |
| **Total** | | **~14-15 hrs** | | **70%** |

---

## 🚀 Next Steps

1. **Expand Phase 6** - Use `/transition-plan --expand --phase 6` to detail API sync tasks
2. **Implement Phase 6** - Use `/task-phase 6 1` to begin implementation
3. **Resume Phase 5** - Complete manual testing after Phase 6
4. **Feature Complete** - Ready for production use after Phase 5 resumes

---

## 📚 Related Documents

### Planning

- [Features Hub](../README.md) - All features overview
- [Planning Hub](../../README.md) - Overall planning

### External

- [proj-cli README](../../../../../README.md) - Project documentation
- [dev-infra new-project.sh](https://github.com/grimm00/dev-infra/blob/develop/scripts/new-project.sh) - Source script

---

**Last Updated:** 2026-01-06  
**Status:** 🟠 Phase 6 Ready  
**Next:** Expand Phase 6 with `/transition-plan --expand --phase 6`


