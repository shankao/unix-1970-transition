#!/usr/bin/env python3
"""Build fixed Stage 3B deposits; class-M instrumentation, not an assembler."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import build_stage3a as s3a
from pdp11_oracle import Operand


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence" / "stage3b"
L = dict(s3a.LABELS)
L.update({
    "f": 0o001320, "tra": 0o001360, "b4": 0o001400,
    "mark": 0o001440, "call": 0o001500, "set": 0o001540,
    "a": 0o001560, "n11": 0o001600, "retv": 0o001620,
    "stream_e": 0o002200, "stream_f": 0o002240,
    "stream_g": 0o002300, "stream_h": 0o002340,
    "stream_i": 0o002400, "stream_j": 0o002440,
    "stream_k": 0o002500, "stream_l": 0o002540,
    "stream_m": 0o002600,
    "counter": 0o003000,
    "fn_identity": 0o003100, "fn_addtwo": 0o003140,
    "fn_constc": 0o003200, "fn_outer": 0o003240,
    "fn_inner": 0o003300, "fn_void": 0o003340,
    "synthetic": 0o006000, "synthetic_caller": 0o006040,
})


@dataclass(frozen=True)
class Image:
    name: str
    expected: str
    stream: int
    words: tuple[s3a.PlacedWord, ...]
    examines: tuple[tuple[int, int], ...]


def _new_ops() -> list[s3a.PlacedWord]:
    b = s3a.FixedBuilder()
    pc = L["f"]
    pc = b.instruction(pc, "tst -(r5)", "TST", Operand(4, 5))
    bne = pc
    pc = b.instruction(pc, "bne f.nonzero", "BNE", address=pc, target=0o001330)
    pc = b.instruction(pc, "mov (r3),r3", "MOV", Operand(1, 3), Operand(0, 3))
    pc = b.instruction(pc, "jmp @(r3)+", "JMP", Operand(3, 3))
    if pc != 0o001330 or bne != 0o001322: raise AssertionError("f layout changed")
    pc = b.instruction(pc, "add #2,r3", "ADD", Operand(2, 7, 2), Operand(0, 3))
    b.instruction(pc, "jmp @(r3)+", "JMP", Operand(3, 3))

    pc = L["tra"]
    pc = b.instruction(pc, "mov (r3),r3", "MOV", Operand(1, 3), Operand(0, 3))
    b.instruction(pc, "jmp @(r3)+", "JMP", Operand(3, 3))

    pc = L["b4"]
    pc = b.instruction(pc, "mov -(r5),r0", "MOV", Operand(4, 5), Operand(0, 0))
    pc = b.instruction(pc, "cmp -(r5),r0", "CMP", Operand(4, 5), Operand(0, 0))
    pc = b.instruction(pc, "bne b4.ne", "BNE", address=pc, target=0o001414)
    pc = b.instruction(pc, "mov #1,r0", "MOV", Operand(2, 7, 1), Operand(0, 0))
    pc = b.instruction(pc, "br b4.store", "BR", address=pc, target=0o001416)
    pc = b.instruction(pc, "clr r0", "CLR", Operand(0, 0))
    pc = b.instruction(pc, "mov r0,(r5)+", "MOV", Operand(0, 0), Operand(2, 5))
    b.instruction(pc, "jmp @(r3)+", "JMP", Operand(3, 3))

    pc = L["mark"]
    pc = b.instruction(pc, "mov -(r5),r0", "MOV", Operand(4, 5), Operand(0, 0))
    pc = b.instruction(pc, "mov r5,r2", "MOV", Operand(0, 5), Operand(0, 2))
    pc = b.instruction(pc, "mov r4,(r5)+", "MOV", Operand(0, 4), Operand(2, 5))
    pc = b.instruction(pc, "mov r0,(r5)+", "MOV", Operand(0, 0), Operand(2, 5))
    b.instruction(pc, "jmp @(r3)+", "JMP", Operand(3, 3))

    pc = L["call"]
    pc = b.instruction(pc, "mov 2(r2),r0", "MOV", Operand(6, 2, 2), Operand(0, 0))
    pc = b.instruction(pc, "mov r3,2(r2)", "MOV", Operand(0, 3), Operand(6, 2, 2))
    pc = b.instruction(pc, "mov r2,r4", "MOV", Operand(0, 2), Operand(0, 4))
    pc = b.instruction(pc, "mov r0,r3", "MOV", Operand(0, 0), Operand(0, 3))
    b.instruction(pc, "jmp @(r3)+", "JMP", Operand(3, 3))

    pc = L["set"]
    pc = b.instruction(pc, "mov (r3)+,r0", "MOV", Operand(2, 3), Operand(0, 0))
    pc = b.instruction(pc, "asl r0", "ASL", Operand(0, 0))
    pc = b.instruction(pc, "add r4,r0", "ADD", Operand(0, 4), Operand(0, 0))
    pc = b.instruction(pc, "mov r0,r5", "MOV", Operand(0, 0), Operand(0, 5))
    b.instruction(pc, "jmp @(r3)+", "JMP", Operand(3, 3))

    pc = L["a"]
    pc = b.instruction(pc, "mov (r3)+,r0", "MOV", Operand(2, 3), Operand(0, 0))
    pc = b.instruction(pc, "add r4,r0", "ADD", Operand(0, 4), Operand(0, 0))
    pc = b.instruction(pc, "mov (r0),(r5)+", "MOV", Operand(1, 0), Operand(2, 5))
    b.instruction(pc, "jmp @(r3)+", "JMP", Operand(3, 3))

    pc = L["n11"]
    pc = b.instruction(pc, "mov r4,r5", "MOV", Operand(0, 4), Operand(0, 5))
    pc = b.instruction(pc, "mov (r5)+,r4", "MOV", Operand(2, 5), Operand(0, 4))
    pc = b.instruction(pc, "mov (r5),r3", "MOV", Operand(1, 5), Operand(0, 3))
    b.instruction(pc, "jmp @(r3)+", "JMP", Operand(3, 3))

    pc = L["retv"]
    pc = b.instruction(pc, "mov -(r5),r0", "MOV", Operand(4, 5), Operand(0, 0))
    pc = b.instruction(pc, "mov r4,r5", "MOV", Operand(0, 4), Operand(0, 5))
    pc = b.instruction(pc, "mov (r5)+,r4", "MOV", Operand(2, 5), Operand(0, 4))
    pc = b.instruction(pc, "mov (r5),r3", "MOV", Operand(1, 5), Operand(0, 3))
    pc = b.instruction(pc, "mov r0,(r5)+", "MOV", Operand(0, 0), Operand(2, 5))
    b.instruction(pc, "jmp @(r3)+", "JMP", Operand(3, 3))
    return b.words


def _stream_data(name: str) -> tuple[int, list[int], list[tuple[int, list[int], str]], tuple[tuple[int, int], ...], str]:
    c, emit, stop = L["c"], L["emit"], L["stop"]
    if name == "e":
        base=L["stream_e"]; fail=base+0o22; end=base+0o30
        return base,[c,1,L["f"],fail,c,0o105,emit,L["tra"],end,c,0o130,emit,stop],[],(),"E"
    if name == "f":
        base=L["stream_f"]; false=base+0o20
        return base,[c,0,L["f"],false,c,0o130,emit,stop,c,0o106,emit,stop],[],(),"F"
    if name == "g":
        base=L["stream_g"]; loop=base; counter_word=L["counter"]//2
        words=[L["x"],L["counter"],emit,c,counter_word,L["x"],L["counter"],c,1,L["b12"],L["b1"],c,0o64,L["b4"],L["f"],loop,stop]
        return base,words,[(L["counter"],[0o61],"loop counter")],((L["counter"],L["counter"]),),"123"
    if name == "h":
        base=L["stream_h"]
        caller=[c,0o110,emit,stop]
        frame=[L["frame"],L["synthetic_caller"]]
        return base,[L["n11"]],[(L["synthetic"],frame,"synthetic return frame"),(L["synthetic_caller"],caller,"synthetic caller")],((L["synthetic"],L["synthetic"]+2),),"H"
    funcs={
        "i":(L["stream_i"],L["fn_identity"],[L["set"],3,L["a"],4,L["retv"]],[0o101],"A"),
        "j":(L["stream_j"],L["fn_addtwo"],[L["set"],4,L["a"],4,L["a"],6,L["b12"],L["retv"]],[0o100,2],"B"),
        "k":(L["stream_k"],L["fn_constc"],[L["set"],3,c,0o103,L["retv"]],[0],"C"),
        "m":(L["stream_m"],L["fn_void"],[L["set"],3,L["n11"]],[0],"V"),
    }
    if name in funcs:
        base,fn,body,args,expected=funcs[name]
        caller=[c,fn,L["mark"]]
        for arg in args: caller += [c,arg]
        caller += [L["call"]]
        if name=="m": caller += [c,0o126]
        caller += [emit,stop]
        return base,caller,[(fn,body,f"function {name}")],((L["stack"],L["stack"]+2+2*len(args)),),expected
    if name == "l":
        base=L["stream_l"]
        caller=[c,L["fn_outer"],L["mark"],c,0o103,L["call"],emit,stop]
        outer=[L["set"],3,c,L["fn_inner"],L["mark"],L["a"],4,L["call"],c,1,L["b12"],L["retv"]]
        inner=[L["set"],3,L["a"],4,L["retv"]]
        extra=[(L["fn_outer"],outer,"outer function"),(L["fn_inner"],inner,"inner function")]
        return base,caller,extra,((L["stack"],L["stack"]+0o12),),"D"
    raise KeyError(name)


def build_images() -> dict[str, Image]:
    images={}
    for name in "efghijklm":
        stream,stream_words,extra,examines,expected=_stream_data(name)
        common=s3a.build_common(stream)+_new_ops()
        data=s3a.FixedBuilder(); data.data(stream,stream_words,f"threaded stream {name.upper()}")
        for address,words,text in extra: data.data(address,words,text)
        words=tuple(sorted(common+data.words,key=lambda w:w.address))
        s3a._validate_layout(words)
        images[name]=Image(name,expected,stream,words,examines)
    return images


def manifest(images:dict[str,Image])->str:
    lines=["Stage 3B deterministic word manifest (M / modern instrumentation)","All numbers are octal PDP-11 byte addresses/16-bit words.",""]
    for name,image in images.items():
        lines.append(f"TEST {name.upper()} expected={image.expected} start={L['start']:06o} stream={image.stream:06o}")
        lines.extend(f"{w.address:06o}\t{w.word:06o}\t{w.kind}\t{w.text}" for w in image.words); lines.append("")
    return "\n".join(lines)


def simh_script(image:Image)->str:
    lines=["; Stage 3B M-class deterministic deposit/run harness.","; Baseline only: no disk/tape attachment, UNIX, KE11, or EIS.",f"set log -n evidence/stage3b/test-{image.name}.transcript.txt","do machines/pdp11/late-summer-1970.simh"]
    lines.extend(f"dep {w.address:06o} {w.word:06o}" for w in image.words)
    if image.name=="h":
        lines.extend((f"dep r3 {image.stream:06o}",f"dep r4 {L['synthetic']:06o}",f"dep r5 {L['synthetic']+4:06o}"))
    start=L["start"] if image.name!="h" else L["n11"]
    lines.extend((f"echo STAGE3B-{image.name.upper()} START={start:06o} EXPECT={image.expected}",f"go {start:06o}","echo",f"echo STAGE3B-{image.name.upper()} HALTED","examine pc,r2,r3,r4,r5"))
    for first,last in image.examines: lines.append(f"examine {first:06o}-{last:06o}")
    lines.extend(("show cpu","show dev","show ptr","quit","")); return "\n".join(lines)


def write_outputs()->None:
    images=build_images(); OUT.mkdir(parents=True,exist_ok=True)
    (OUT/"manifest.txt").write_text(manifest(images),encoding="ascii")
    for name,image in images.items(): (OUT/f"test-{name}.simh").write_text(simh_script(image),encoding="ascii")


if __name__=="__main__": write_outputs()
