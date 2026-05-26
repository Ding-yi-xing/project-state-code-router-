#!/usr/bin/env node
// gc-lint.example.mjs
// MINIMAL REFERENCE IMPLEMENTATION — copy to your project and adapt.
//
// This is a *starting point* for adding doc-gardening (DOC.M.* invariants
// from references/gc-rules.md) to a project that uses the
// project-state-code-router skill. It does NOT cover code GC — that lives
// in your project's lint / architecture tests / custom analyzers.
//
// What this example checks (mirroring DOC.M.01-04 from gc-rules.md):
//   - manifest.yaml exists and parses
//   - every work_unit declared in manifest has a directory and manifest.md
//   - every directory under docs/units/ (except .template/) is in manifest
//   - every work unit contains the required minimum files
//
// Usage in your project:
//   1. Copy this file to scripts/gc-lint.mjs
//   2. Adjust DOCS_ROOT and REQUIRED_UNIT_FILES below
//   3. node scripts/gc-lint.mjs
//
// Zero dependencies (uses only Node.js stdlib + a tiny inline YAML parser
// for the manifest). Requires Node >= 16. Replace the YAML parser with
// `yaml` or `js-yaml` if your manifest is non-trivial.

import { readFileSync, readdirSync, existsSync, statSync } from 'node:fs';
import { join } from 'node:path';

// ---- Adapt these to your project ----
const DOCS_ROOT = 'docs';
const MANIFEST_PATH = join(DOCS_ROOT, '.project-docs-manifest.yaml');
const UNITS_DIR = join(DOCS_ROOT, 'units');
const REQUIRED_UNIT_FILES = [
    'manifest.md',
    'status.md',
    'requirements/index.md',
    'blockers/index.md',
    'issues/index.md',
    'sync/outward-needs.md',
    'archive/index.md',
];

// ---- Implementation ----
const violations = [];
function addViolation(id, where, msg) {
    violations.push(`[${id}] ${where} -- ${msg}`);
}

// Tiny manifest parser: just pulls out work_units list. Replace with a real
// YAML library if your manifest grows.
function parseWorkUnits(yamlText) {
    const units = [];
    const lines = yamlText.split(/\r?\n/);
    let inWorkUnits = false;
    for (const line of lines) {
        if (/^work_units\s*:/.test(line)) { inWorkUnits = true; continue; }
        if (inWorkUnits) {
            if (/^\S/.test(line)) break; // dedented, end of block
            const m = line.match(/^\s*-\s*(?:name\s*:\s*)?["']?([a-z0-9_-]+)["']?/i);
            if (m) units.push(m[1]);
        }
    }
    return units;
}

// ---- DOC.M.01: manifest exists ----
if (!existsSync(MANIFEST_PATH)) {
    addViolation('DOC.M.01', MANIFEST_PATH, 'manifest file missing');
} else {
    const manifestText = readFileSync(MANIFEST_PATH, 'utf8');
    const declaredUnits = parseWorkUnits(manifestText);

    // ---- DOC.M.02: every declared unit has a directory + manifest.md ----
    for (const unit of declaredUnits) {
        const unitDir = join(UNITS_DIR, unit);
        if (!existsSync(unitDir)) {
            addViolation('DOC.M.02', unitDir, `declared in manifest but directory missing`);
            continue;
        }
        if (!existsSync(join(unitDir, 'manifest.md'))) {
            addViolation('DOC.M.02', unitDir, `unit directory missing manifest.md`);
        }
    }

    // ---- DOC.M.03: every directory under units/ is declared ----
    if (existsSync(UNITS_DIR)) {
        for (const entry of readdirSync(UNITS_DIR)) {
            if (entry.startsWith('.')) continue; // skip .template/, etc.
            const entryPath = join(UNITS_DIR, entry);
            if (!statSync(entryPath).isDirectory()) continue;
            if (!declaredUnits.includes(entry)) {
                addViolation('DOC.M.03', entryPath, `directory exists but not declared in manifest work_units`);
            }
        }
    }

    // ---- DOC.M.04: required minimum files in each unit ----
    for (const unit of declaredUnits) {
        const unitDir = join(UNITS_DIR, unit);
        if (!existsSync(unitDir)) continue;
        for (const required of REQUIRED_UNIT_FILES) {
            const fullPath = join(unitDir, required);
            if (!existsSync(fullPath)) {
                addViolation('DOC.M.04', unitDir, `missing required file ${required}`);
            }
        }
    }
}

// ---- Report ----
if (violations.length === 0) {
    console.log('Doc GC: PASS (0 violations)');
    process.exit(0);
} else {
    console.log(`Doc GC: FAIL (${violations.length} violations)`);
    for (const v of violations) console.log(v);
    process.exit(1);
}

// ---- Where to take this further ----
//
// 1. Add DOC.M.05-07 (line caps for shared/current/, archive integrity, etc.)
// 2. Add DOC.S.* semantic checks via a Claude /loop prompt instead of script
// 3. Add CODE.M.* / CODE.S.* code GC by writing custom lint rules in your
//    language ecosystem (ESLint plugins, Pylint checkers, Go analyzers,
//    ArchUnit / ts-arch tests, etc.) — those don't belong in this script.
// 4. Hook this into pre-commit, GitHub Actions, or your IDE task runner.
//    skill does not prescribe which — pick what fits your team.
