"""Check that 0.2 preserves the exact upstream shader cache version inputs."""
import hashlib
from pathlib import Path
import re
import subprocess
import unittest
ROOT = Path(__file__).resolve().parents[2]
class CacheContract(unittest.TestCase):
    def test_cache_inputs_unchanged(self):
        cmake = (ROOT/'CMakeModules/GenerateSCMRev.cmake').read_text()
        paths = re.findall(r'"\$\{VIDEO_CORE\}/([^"\n]+)"', cmake)
        self.assertGreater(len(paths), 20)
        old, new = bytearray(), bytearray()
        for relative in paths:
            path = 'src/video_core/' + relative
            old.extend(subprocess.check_output(['git','show','8fb0faab5ae73c0034ffcf6dcfaa9f70c9ead5e5:'+path], cwd=ROOT))
            new.extend((ROOT/path).read_bytes())
        self.assertEqual(hashlib.md5(old).hexdigest(), hashlib.md5(new).hexdigest())
        print('shader cache version unchanged:', hashlib.md5(new).hexdigest())
