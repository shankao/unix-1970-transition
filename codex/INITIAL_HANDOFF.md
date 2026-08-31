# Initial Codex Handoff

You are helping initialize and develop the `unix-1970-transition` repository.

First read:

- `README.md`
- `AGENTS.md`
- `docs/METHOD.md`
- `docs/PLAN.md`
- `docs/STATE.md`
- `docs/SOURCES.md`
- `docs/DECISIONS.md`

## Initial setup task

Do **not** begin implementing the cross-assembler yet.

1. Inspect the local PDP-7 and PDP-11 project directories without modifying their working state.
2. Capture exact reproducibility metadata required by Stage 0:
   - Open SIMH versions/commits;
   - startup/configuration files;
   - relevant disk/filesystem image paths and SHA-256 hashes;
   - current upstream commits/dirty state for the PDP-7 UNIX restoration and B reconstruction;
   - PDP-7 PTP/PTR current state if it can be queried non-destructively;
   - PDP-11 enabled/disabled device state and the memory contents at 057744-057776.
3. Add this information to `docs/STATE.md` or machine-specific files under `evidence/`, keeping local/private machine paths out of public docs where they are not useful.
4. Add scripts under `tools/` only if they make Stage-0 capture reproducible and are non-destructive.
5. Do not attach tapes, run the deposited PDP-11 bootstrap, modify the PDP-7 filesystem, enable devices, or change either machine configuration.
6. Report any mismatch between observed state and `docs/STATE.md` before changing anything.

Once Stage 0 is reproducible, stop. The next planned work is Stage 1 characterization of the existing PDP-7 B environment.
