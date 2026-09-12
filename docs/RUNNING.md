# Explore the reconstructed eras

The eras are current runnable hypotheses about capability states in the
PDP-7-to-PDP-11 transition, not snapshots of this project's implementation
sequence. Their boundaries are analytical and chronology remains uncertain.
Project checkpoint machines are retained separately under `snapshots/`.

## 1. Late PDP-7 Unix

This is the usable PDP-7 Unix baseline before reconstructed PDP-11 tooling
dominates the experience. See [`ERA.md`](../eras/pdp7-unix/ERA.md).

```sh
cd eras/pdp7-unix
pdp7 pdp7.simh
```

Log in as `shankao` / `shankao` and try `ls`.

## 2. PDP-7 cross-development

This slice contains the reconstructed native B-hosted `as11` and the
PDP-7-side paper-tape formatter. See
[`ERA.md`](../eras/pdp7-crossdev/ERA.md).

```sh
cd eras/pdp7-crossdev
pdp7 pdp7.simh
```

Log in as `shankao` / `shankao`, then try `cat readme` and `stat abspun.b`.

## 3. Diskless PDP-11 cross-development

This slice consumes committed PDP-7-produced paper tapes through real PTR,
the contemporary DEC bootstrap, and the DEC Absolute Loader. First prepare the
archival loader media, then enter the era:

```sh
python3 tools/materialize_dec_loader.py
cd eras/pdp11-crossdev
pdp11 interrupt-trap.simh
```

Type `AB` at the prompt. For the noninteractive RAM diagnostic, run `pdp11
ram-substrate.simh`. See [`ERA.md`](../eras/pdp11-crossdev/ERA.md).

The core-only PDP-11 Unix and RF11-backed Unix eras do not exist yet.
