---
mode: "agent"
description: "Upgrade sample app dependencies and verify code compatibility across all levels"
---

# Sample App Upgrade

Check and upgrade dependencies for all workshop sample applications, verify
code compatibility, and ensure intentional bugs are preserved.

## Scope by Level

| Level | Language | Dependency Model | What to Check |
|-------|----------|-----------------|---------------|
| 1–6 | Python 3.8+ | stdlib only (zero deps) | Python version compatibility |
| 7 | TypeScript 5.x | npm (Express, Jest, Zod, etc.) | Package updates, breaking changes |
| 8 | JS + Python | Mixed / minimal | Dependency freshness, script compatibility |
| 9 | Mixed (JS/Config) | npm / config files | Extension scaffold, MCP config validity |

## Step 1: Python Sample Apps (Levels 1–6)

These apps use **stdlib only** — there are no packages to upgrade. Instead,
verify compatibility:

### 1.1 Check Python Version Compatibility

```bash
# Verify no Python 3.9+ syntax slipped in (walrus operator, etc.)
grep -rn ':=' workshop/level-{1,2,3,4,5,6}/sample-app/ --include="*.py"

# Check for match/case (Python 3.10+)
grep -rn '^\s*match\s\|^\s*case\s' workshop/level-{1,2,3,4,5,6}/sample-app/ --include="*.py"

# Check for type union syntax X | Y (Python 3.10+)
grep -rn ':\s*\w\+\s*|\s*\w\+' workshop/level-{1,2,3,4,5,6}/sample-app/ --include="*.py"
```

### 1.2 Verify No External Dependencies

```bash
# Check requirements.txt files — should be empty or comments only
for f in workshop/level-{1,2,3,4,5,6}/sample-app/requirements.txt; do
  echo "=== $f ==="
  grep -v '^\s*#\|^\s*$' "$f" 2>/dev/null || echo "(empty or not found)"
done
```

### 1.3 Run Tests (if available)

```bash
# Run each level's tests
for level in 1 2 3 4 5 6; do
  echo "=== Level $level ==="
  cd workshop/level-$level/sample-app
  python3 -m pytest tests/ 2>/dev/null || python3 -m unittest discover -s tests 2>/dev/null || echo "No test runner"
  cd ../../..
done
```

> ⚠️ Level 5 tests are **expected to fail** (6 intentional failures).
> Level 6 has incomplete test coverage by design. Do not fix these.

## Step 2: TypeScript Sample App (Level 7)

### 2.1 Check Current Dependencies

```bash
cd workshop/level-7/sample-app
cat package.json | python3 -c "import sys, json; d=json.load(sys.stdin); [print(f'{k}: {v}') for k,v in {**d.get('dependencies',{}), **d.get('devDependencies',{})}.items()]"
```

### 2.2 Check for Updates

```bash
cd workshop/level-7/sample-app
npm outdated 2>/dev/null || echo "Run npm install first"
```

### 2.3 Evaluate Updates

For each outdated package, evaluate:

| Package | Current | Latest | Breaking? | Action |
|---------|---------|--------|-----------|--------|
| express | X.Y.Z | A.B.C | Check changelog | Update/Skip |
| typescript | X.Y.Z | A.B.C | Check changelog | Update/Skip |
| jest | X.Y.Z | A.B.C | Check changelog | Update/Skip |
| zod | X.Y.Z | A.B.C | Check changelog | Update/Skip |

**Decision criteria:**
- **Minor/patch updates**: Generally safe — apply them
- **Major updates**: Check changelog for breaking changes; if Express 4→5
  or similar, assess impact on exercises that reference API patterns
- **TypeScript version**: Must maintain `strict: true` compatibility
- **Jest version**: Must maintain `describe`/`it`/`beforeEach` API

### 2.4 Apply Updates

If updates are appropriate:

```bash
cd workshop/level-7/sample-app

# Update package.json
npm update  # for minor/patch
# OR for major updates:
npm install package@latest

# Rebuild
npm run build

# Run tests
npm test
```

### 2.5 Verify After Update

- [ ] `npm run build` succeeds with no TypeScript errors
- [ ] `npm test` passes (all tests should pass for Level 7)
- [ ] No new lint warnings introduced
- [ ] `tsconfig.json` settings still valid for the new TypeScript version

## Step 3: Level 8 Sample App

### 3.1 Inventory Dependencies

```bash
# Check for package.json, requirements.txt, or other dep files
find workshop/level-8/sample-app -name "package.json" -o -name "requirements.txt" \
  -o -name "Pipfile" -o -name "go.mod" | while read f; do
  echo "=== $f ==="
  cat "$f"
done
```

### 3.2 Check Scripts

Level 8 includes bash scripts. Verify they use portable syntax:

```bash
# Check shebang lines
grep -rn '^#!' workshop/level-8/sample-app/ --include="*.sh"

# Verify set -euo pipefail is present
grep -rL 'set -euo pipefail' workshop/level-8/sample-app/*.sh 2>/dev/null
```

## Step 3.5: Level 9 Sample App (Project Scaffolder)

### 3.5.1 Verify Extension Scaffold

Level 9's sample app is a project scaffolder with intentionally incomplete components
for teaching exercises. Verify the scaffold is intact:

```bash
# Check that extension package.json exists and is valid JSON
cat workshop/level-9/sample-app/package.json 2>/dev/null | python3 -c "import sys,json; json.load(sys.stdin); print('Valid JSON')" 2>/dev/null || echo "Invalid or missing"

# Check MCP config exists
cat workshop/level-9/sample-app/.mcp.json 2>/dev/null || echo "No .mcp.json"

# Check CLAUDE.md exists
cat workshop/level-9/sample-app/CLAUDE.md 2>/dev/null || echo "No CLAUDE.md"
```

### 3.5.2 Verify Teaching Points Preserved

These are **intentionally incomplete** — do not fix them:

| Item | Expected State | Check |
|------|---------------|-------|
| Extension TODO placeholder tool | Contains TODO comment | `grep -r 'TODO' workshop/level-9/sample-app/` |
| CLAUDE.md | Intentionally minimal | Should be short/incomplete |
| `.mcp.json` placeholder server | Disabled/placeholder | Should have disabled entry |
| Skill description | Incomplete | Should lack full description |

## Step 4: Verify Intentional Bugs Preserved

After any dependency upgrade, verify intentional bugs are intact:

| Level | Check | Method |
|-------|-------|--------|
| 3/4 | 8 bugs in Quick Notes | Run `verify-bugs` prompt or manual check |
| 5 | 6 test failures | Run tests — expect exactly 6 failures |
| 5 | Lint issues | Run linter — expect unused imports, missing docstring |
| 6 | 5 issues | Check store.py, missing test_validator.py, etc. |
| 9 | 4 teaching points | Verify TODO placeholder, minimal CLAUDE.md, disabled MCP server, incomplete skill |

## Output

```markdown
## Sample App Upgrade Report

**Date:** YYYY-MM-DD

### Python Apps (Levels 1–6)
| Level | Python 3.8+ Compatible | No External Deps | Tests | Status |
|-------|----------------------|-------------------|-------|--------|
| 1 | ✅/❌ | ✅/❌ | ✅ Pass / ⚠️ Expected failures | OK |
...

### TypeScript App (Level 7)
| Package | Before | After | Breaking Changes | Tests |
|---------|--------|-------|-----------------|-------|
| express | X.Y.Z | A.B.C | None/Yes | ✅ Pass |
...

### Level 8
| Component | Status | Notes |
|-----------|--------|-------|
| Scripts | ✅ POSIX-compatible | ... |
| Dependencies | ✅ Current / ⚠️ Outdated | ... |

### Level 9
| Component | Status | Notes |
|-----------|--------|-------|
| Extension scaffold | ✅ Intact / ❌ Modified | ... |
| Teaching points | ✅ All preserved / ❌ N missing | ... |

### Bug Preservation
| Level | Expected Bugs | Verified | Status |
|-------|--------------|----------|--------|
| 3/4 | 8 | 8 | ✅ Intact |
| 5 | 6+lint | 6+lint | ✅ Intact |
| 6 | 5 | 5 | ✅ Intact |

### Actions Taken
1. Updated X in Level 7...
2. ...

### Next Steps
- [ ] If Level 7 API changed, run `workshop-refresh` for exercise updates
- [ ] Run `cross-reference-validate` to check sample-app README links
```
