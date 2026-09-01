# PDP-7 B characterization probes

These files are class **M** modern probes for the class **B** reconstructed
compiler and the surviving/restored PDP-7 runtime boundary. Each probe's
purpose, expected observation, and downstream decision are specified in
`docs/B-BASELINE.md`.

On the persistent host, use the installed sequence:

    b probe.b probe.s
    as op.s bl.s probe.s bi.s
    a.out

Synchronize each editor command and line with the prompt when entering source
through the console. Queuing a complete `ed` transcript can lose or merge
input; the retained corrupt captures demonstrate that failure mode. Do not
patch the compiler/runtime to make a probe pass.
