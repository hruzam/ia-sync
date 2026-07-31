# Sonnet Reading Order & Task Handoff

**Purpose:** Navigation guide for Sonnet (office machine agent)  
**How to use:** Sonnet reads this document, follows the reading order, then executes tasks  
**Authority:** @majkee  
**Principle:** No duplication — reference actual source files; this is navigation only  

---

## 🎯 BEFORE YOU START

**Check which machine you're on:**
```bash
hostname -s          # Should show: office
echo $MACHINE_NAME   # Should show: office (if zsh sourced)
```

If either returns something other than "office", STOP. You're on the wrong machine.

---

## 📖 READING ORDER (Follow in sequence)

### STAGE 1: UNDERSTAND THE SYSTEM (10 min)

**Read these files in order:**

1. **`~/ia-sync/README.md`** (5 min)
   - What: Overview of ia-sync as a multi-machine system
   - Why: Understand project structure and purpose
   - Key takeaways: What's in the repo, what gets deployed

2. **`~/ia-sync/journal.host-cleanup.md`** (3 min)
   - What: Bi-directional audit trail (HOME and OFFICE sections)
   - Why: See what home machine is running, what office should have
   - Focus: OFFICE section (2026-06-29) for your machine context
   - Focus: HOME section to understand differences

3. **`~/ia-sync/zsh/config.office.zsh`** (2 min)
   - What: Your actual machine configuration (office-specific)
   - Why: Know your paths, constants, services
   - Key: MACHINE_NAME="office", OFFICE_PROJECT_PATH="/media/data/projects"

---

### STAGE 2: UNDERSTAND DEPLOYMENT (5 min)

**Read these files:**

4. **`~/ia-sync/OFFICE_DEPLOYMENT_EXECUTION.md`** (5 min)
   - What: Detailed execution guide with 6 phases + bash scripts
   - Why: Know exactly what will happen at each step
   - Read: All 6 phases carefully
   - Read: Agent safeguard section (backup/restore procedures)

---

### STAGE 3: EXECUTE DEPLOYMENT (1 min setup + 5-10 min execution)

**Follow the script:**

5. **`~/ia-sync/deploy-office.sh`** (run it)
   - What: Production-ready deployment script
   - Why: Automates all 6 phases with safeguards
   - How: `bash ~/ia-sync/deploy-office.sh`
   - Expected: Colored output, auto-generated OFFICE_AUDIT_<timestamp>.md

---

### STAGE 4: VERIFY & DOCUMENT (5 min)

**After deployment runs:**

6. **`~/ia-sync/journal.host-cleanup.md`** (append entry)
   - What: Update the journal with deployment results
   - Why: Keep bi-directional audit trail current
   - Format: `## OFFICE — 2026-06-29 (deployment)` section with findings

---

## 🔍 REFERENCE MATERIALS (Read as needed)

**For machine profile after deployment:**
- `~/.config/zsh/guides/office.md` — Auto-generated during deploy
  - Contains: Office hardware specs, services, differences from home

**For infrastructure comparison:**
- `~/ia-sync/guides/README.md` — Guide navigation matrix
  - Shows: Which guides apply to home vs office vs both

**For team context:**
- `~/ia-sync/claude/agents/houston.md` — Understand orchestration
- `~/ia-sync/guides/cross-machine/` — Tool references (apply to both)

**For troubleshooting:**
- `~/ia-sync/OFFICE_MACHINE_SETUP.md` — High-level phases (if you need to understand "why")

---

## ✅ YOUR TASKS

### Task 1: Verify Prerequisites
```bash
hostname -s              # office
git --version            # 2.x+
ssh -T git@github.com    # successful auth
pacman --version         # Arch/Manjaro available
php --version            # PHP installed
valet --version          # Valet installed
```

### Task 2: Follow Reading Order
1. Read `~/ia-sync/README.md` (5 min)
2. Read `~/ia-sync/journal.host-cleanup.md` (3 min) — focus OFFICE and HOME sections
3. Read `~/ia-sync/zsh/config.office.zsh` (2 min)
4. Read `~/ia-sync/OFFICE_DEPLOYMENT_EXECUTION.md` (5 min)

### Task 3: Run Deployment
```bash
bash ~/ia-sync/deploy-office.sh
```
Expected: All 6 phases complete, colored output, OFFICE_AUDIT_<timestamp>.md generated

### Task 4: Test
```bash
source ~/.zshrc
archx-services
archx-monitor system
ls -la /media/data/projects/
```

### Task 5: Update Journal
Append to `~/ia-sync/journal.host-cleanup.md`:
```markdown
## OFFICE — 2026-06-29 (deployment)

**Agent:** Sonnet (office machine)
**Session:** Deployment via deploy-office.sh

### Completed
- [X] Prerequisites verified
- [X] Reading order followed
- [X] Deployment script executed
- [X] All 6 phases completed
- [X] Services verified
- [X] Projects accessible

### System Specs
[Output from deployment script]

### Issues/Observations
[Any findings during deployment]
```

---

## 🎯 SUCCESS CRITERIA

After completing all tasks, you should have:

- ✅ MACHINE_NAME=office verified (hostname -s + echo $MACHINE_NAME)
- ✅ deploy-office.sh completed without critical errors
- ✅ Agent count = 26 (or more if office-custom agents preserved)
- ✅ archx-services works
- ✅ archx-monitor system works
- ✅ archx-help works
- ✅ /media/data/projects/ accessible
- ✅ OFFICE_AUDIT_<timestamp>.md generated
- ✅ Journal updated with findings

---

## 📌 CRITICAL POINTS

**Machine Identity:**
- You are on the OFFICE machine
- Verify with: `hostname -s` and `echo $MACHINE_NAME`
- Paths: /media/data/projects/ (not ~/www/)

**Deployment:**
- One command: `bash ~/ia-sync/deploy-office.sh`
- All 6 phases automated
- Agent backup automatic (can restore if needed)

**Reference:**
- Don't duplicate information — all details in actual files
- This document is navigation only
- Read source files for complete understanding

**Cooperation:**
- Home and office machines sync via ia-sync
- Each machine runs independently but shares infrastructure
- Journal tracks findings from both machines
- Handoffs between agents via reading order + tasks

---

**Generated:** 2026-06-29  
**For:** Sonnet (office machine agent)  
**Authority:** @majkee  
**Pattern:** Read → Execute → Document → Handoff to next task

