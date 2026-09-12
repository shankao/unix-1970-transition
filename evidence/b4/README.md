# B4 paper-tape transport evidence

The physical PDP-7-to-PDP-11 tape workflow is historically attested. This
working DEC loader path is class C, a contemporary substitute, because Bell
Labs' exact 1970 receiving loader and tape format remain unknown.

`DEC-11-L2PC-PO.json` is PCjs's lossless word packing of the DEC Absolute
Loader bootstrap-format tape, archived from
<https://www.pcjs.org/software/dec/pdp11/tapes/absloader/DEC-11-L2PC-PO.json>.
Its SHA-256 is
`a9fba85bab5249eaffd689b69d3bfc8b9455b9457fc8bf0db84ed49c4c47e1fc`.
It is historical DEC material and is not relicensed as project GPL code. The
fourteen-word 24 KB bootstrap and procedure come from DEC's handbook cited in
`docs/SOURCES.md`.

The accepted U1 traces matched the resident PDP-7 files. A project-original B
formatter built under `shankao` emitted DEC records through real PTP. Because
`pptout` is a privileged special file in `dd/system`, temporary native links
exposed the formatter and inputs there and the restored `system` super-user did
only the punch operation. The links were removed afterward.

- Interrupt article: 131 words, 132 records including transfer, 1,226 bytes,
  SHA-256 `35bb32f5fafc256791c9354300ae26758ba83fb68aeee23b07ddc5f398d41791`.
- RAM article: 211 words, 212 records including transfer, 1,946 bytes, SHA-256
  `fc1e86d1c90749af7dfeda67244028a95edcb671c02b0569f91e3aec958411b7`.
- Every checksum and all 342 native-word comparisons passed.
- PDP-11 SIMH executed the front-panel bootstrap, read the Absolute Loader and
  payload through PTR, halted for comparison, and reproduced the established
  interrupt/TRAP `AB` and RAM results.

The transcripts retain both machine paths. Python verified records and
automated operator actions; it did not produce either acceptance tape or
deposit payload words.

After the bounded regressions, cleanup of two ordinary-file discovery
artifacts, and restoration of the interrupted `u1ram.s` source transfer, the
authoritative PDP-7 image SHA-256 is
`0a7a3589b13a4b4732b20cfa5c1afe5ed14474e2a62670add1e29016b8525dba`.
Read-only `fsck7` exits 0 with only the established inode-38/block-2987
self-revisit. The authentic `dd/system/pptout` special inode remains unchanged;
no device entry or additional privilege was installed for `shankao`.
