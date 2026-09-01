import importlib.util
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))
SPEC = importlib.util.spec_from_file_location("build_stage3a", TOOLS / "build_stage3a.py")
stage3a = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = stage3a
SPEC.loader.exec_module(stage3a)
import pdp11_oracle as oracle


class Stage3ABuildTests(unittest.TestCase):
    def setUp(self): self.images = stage3a.build_images()

    def test_four_fixed_images(self):
        self.assertEqual({"a", "b", "c", "d"}, set(self.images))
        self.assertEqual("ABCD", "".join(image.expected for image in self.images.values()))

    def test_instruction_words_decode_and_avoid_eis(self):
        for image in self.images.values():
            words = {item.address: item for item in image.words}
            for item in image.words:
                if item.kind != "instruction": continue
                following, address = [item.word], item.address + 2
                while address in words and words[address].kind == "extension" and words[address].text == item.text:
                    following.append(words[address].word); address += 2
                decoded = oracle.decode_one(following, item.address)
                self.assertEqual(tuple(following), decoded.words)
                self.assertNotIn(decoded.mnemonic, oracle.UNSUPPORTED)

    def test_layout_inside_24k_and_clear_of_bootstrap(self):
        for image in self.images.values():
            for item in image.words:
                self.assertLess(item.address, stage3a.MEMORY_BYTES)
                self.assertEqual(0, item.address & 1)
                self.assertFalse(stage3a.BOOTSTRAP_FIRST <= item.address <= stage3a.BOOTSTRAP_LAST)

    def test_threaded_stream_words(self):
        L = stage3a.LABELS
        expected = {
            "a": [L["c"], 0o100, L["c"], 1, L["b12"], L["emit"], L["stop"]],
            "b": [L["x"], L["external"], L["emit"], L["stop"]],
            "c": [L["c"], 0o1401, L["c"], 0o103, L["b1"], L["emit"], L["stop"]],
            "d": [L["va"], 4, L["c"], 0o104, L["b1"], L["emit"], L["stop"]],
        }
        for name, values in expected.items():
            placed = {item.address: item.word for item in self.images[name].words}
            actual = [placed[self.images[name].stream + 2 * i] for i in range(len(values))]
            self.assertEqual(values, actual)

    def test_b_word_address_scaling(self):
        self.assertEqual(0o1401, stage3a.LABELS["target"] // 2)
        self.assertEqual(stage3a.LABELS["target"], 0o1401 * 2)
        self.assertEqual((stage3a.LABELS["frame"] + 4) // 2, 0o2002)

    def test_emit_uses_kl11_addresses(self):
        words = self.images["a"].words
        emit_words = [item.word for item in words if stage3a.LABELS["emit"] <= item.address < stage3a.LABELS["stop"]]
        self.assertIn(0o177564, emit_words)
        self.assertIn(0o177566, emit_words)

    def test_generated_deposits_are_deterministic(self):
        first, second = stage3a.build_images(), stage3a.build_images()
        self.assertEqual(stage3a.manifest(first), stage3a.manifest(second))
        for name in first:
            self.assertEqual(stage3a.simh_script(first[name]), stage3a.simh_script(second[name]))
            commands = [line.strip().lower() for line in stage3a.simh_script(first[name]).splitlines() if not line.lstrip().startswith(";")]
            self.assertFalse(any(line.startswith("attach ") for line in commands))

    def test_generated_files_match_builder(self):
        self.assertEqual(stage3a.manifest(self.images), (stage3a.OUT / "manifest.txt").read_text(encoding="ascii"))
        for name, image in self.images.items():
            self.assertEqual(stage3a.simh_script(image), (stage3a.OUT / f"test-{name}.simh").read_text(encoding="ascii"))

    def test_observed_bare_machine_transcripts(self):
        for name, image in self.images.items():
            text = (stage3a.OUT / f"test-{name}.transcript.txt").read_text(encoding="utf-8")
            self.assertIn("        24KB", text)
            self.assertIn("KE      disabled", text)
            self.assertIn("RK      disabled", text)
            self.assertIn("RP      disabled", text)
            self.assertIn("TM      disabled", text)
            self.assertIn("        not attached", text)
            self.assertIn(f"STAGE3A-{name.upper()} START=001000 EXPECT={image.expected}\n{image.expected}\nHALT instruction", text)
        self.assertIn("3002:\t000103", (stage3a.OUT / "test-c.transcript.txt").read_text(encoding="utf-8"))
        self.assertIn("4004:\t000104", (stage3a.OUT / "test-d.transcript.txt").read_text(encoding="utf-8"))


if __name__ == "__main__": unittest.main()
