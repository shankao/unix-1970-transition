import importlib.util
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).parents[1]; TOOLS=ROOT/"tools"; sys.path.insert(0,str(TOOLS))
SPEC=importlib.util.spec_from_file_location("build_stage3b",TOOLS/"build_stage3b.py")
s3b=importlib.util.module_from_spec(SPEC); assert SPEC.loader is not None
sys.modules[SPEC.name]=s3b; SPEC.loader.exec_module(s3b)
import pdp11_oracle as oracle


class Stage3BBuildTests(unittest.TestCase):
    def setUp(self): self.images=s3b.build_images()

    def test_nine_images_and_expected_results(self):
        self.assertEqual(set("efghijklm"),set(self.images))
        self.assertEqual({"e":"E","f":"F","g":"123","h":"H","i":"A","j":"B","k":"C","l":"D","m":"V"},{n:i.expected for n,i in self.images.items()})

    def test_every_instruction_decodes_and_is_ka11(self):
        for image in self.images.values():
            placed={w.address:w for w in image.words}
            for word in image.words:
                if word.kind!="instruction": continue
                seq=[word.word]; address=word.address+2
                while address in placed and placed[address].kind=="extension" and placed[address].text==word.text:
                    seq.append(placed[address].word); address+=2
                decoded=oracle.decode_one(seq,word.address)
                self.assertEqual(tuple(seq),decoded.words)
                self.assertNotIn(decoded.mnemonic,oracle.UNSUPPORTED)

    def test_control_targets_are_threaded_addresses(self):
        e={w.address:w.word for w in self.images["e"].words}
        self.assertEqual(0o002222,e[0o002206])
        self.assertEqual(0o002230,e[0o002220])
        f={w.address:w.word for w in self.images["f"].words}
        self.assertEqual(0o002260,f[0o002246])
        g={w.address:w.word for w in self.images["g"].words}
        self.assertEqual(0o002300,g[0o002336])

    def test_call_stream_order_matches_stage1_contract(self):
        j={w.address:w.word for w in self.images["j"].words}
        expected=[s3b.L["c"],s3b.L["fn_addtwo"],s3b.L["mark"],s3b.L["c"],0o100,s3b.L["c"],2,s3b.L["call"]]
        self.assertEqual(expected,[j[s3b.L["stream_j"]+2*i] for i in range(len(expected))])

    def test_argument_and_frame_layout_model(self):
        frame=s3b.L["stack"]
        self.assertEqual(frame,0o005000)
        self.assertEqual(frame+0,0o005000)  # previous R4
        self.assertEqual(frame+2,0o005002)  # saved R3, later return value
        self.assertEqual(frame+4,0o005004)  # argument/automatic slot 2
        self.assertEqual(frame+6,0o005006)  # argument/automatic slot 3
        self.assertEqual(frame+6,0o005006)  # nested inner frame after outer set 3

    def test_n11_words_materially_match_documented_sequence(self):
        words={w.address:w.word for w in self.images["h"].words}
        decoded=[]; pc=s3b.L["n11"]
        for _ in range(4):
            ins=oracle.decode_one([words[pc]],pc); decoded.append((ins.mnemonic,ins.operands)); pc+=2
        self.assertEqual(["MOV","MOV","MOV","JMP"],[x[0] for x in decoded])
        self.assertEqual(("R4","R5"),decoded[0][1])
        self.assertEqual(("(R5)+","R4"),decoded[1][1])
        self.assertEqual(("(R5)","R3"),decoded[2][1])
        self.assertEqual(("@(R3)+",),decoded[3][1])

    def test_layout_bounds_and_bootstrap_exclusion(self):
        for image in self.images.values():
            addresses=[w.address for w in image.words]
            self.assertEqual(len(addresses),len(set(addresses)))
            for address in addresses:
                self.assertEqual(0,address&1); self.assertLess(address,s3b.s3a.MEMORY_BYTES)
                self.assertFalse(s3b.s3a.BOOTSTRAP_FIRST<=address<=s3b.s3a.BOOTSTRAP_LAST)

    def test_generated_files_are_deterministic(self):
        again=s3b.build_images()
        self.assertEqual(s3b.manifest(self.images),s3b.manifest(again))
        self.assertEqual(s3b.manifest(self.images),(s3b.OUT/"manifest.txt").read_text(encoding="ascii"))
        for name,image in self.images.items():
            script=s3b.simh_script(image)
            self.assertEqual(script,s3b.simh_script(again[name]))
            self.assertEqual(script,(s3b.OUT/f"test-{name}.simh").read_text(encoding="ascii"))
            commands=[line.strip().lower() for line in script.splitlines() if not line.lstrip().startswith(";")]
            self.assertFalse(any(line.startswith("attach ") for line in commands))

    def test_observed_bare_machine_transcripts(self):
        for name,image in self.images.items():
            text=(s3b.OUT/f"test-{name}.transcript.txt").read_text(encoding="utf-8")
            self.assertIn("        24KB",text); self.assertIn("KE      disabled",text)
            self.assertIn("RK      disabled",text); self.assertIn("TM      disabled",text)
            self.assertIn("        not attached",text)
            self.assertIn(f"EXPECT={image.expected}\n{image.expected}\nHALT instruction",text)
        self.assertIn("3000:\t000064",(s3b.OUT/"test-g.transcript.txt").read_text(encoding="utf-8"))
        self.assertIn("5004:\t000101",(s3b.OUT/"test-i.transcript.txt").read_text(encoding="utf-8"))
        j=(s3b.OUT/"test-j.transcript.txt").read_text(encoding="utf-8")
        self.assertIn("5002:\t000102",j); self.assertIn("5004:\t000100",j); self.assertIn("5006:\t000002",j)
        nested=(s3b.OUT/"test-l.transcript.txt").read_text(encoding="utf-8")
        self.assertIn("5000:\t004000",nested); self.assertIn("5006:\t005000",nested)
        self.assertIn("5010:\t000104",nested); self.assertIn("5012:\t000001",nested)


if __name__=="__main__": unittest.main()
