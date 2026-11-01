import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

path=Path(__file__).resolve().parents[1]/'scripts/install_codex.py'
spec=importlib.util.spec_from_file_location('installer',path)
installer=importlib.util.module_from_spec(spec);spec.loader.exec_module(installer)

class InstallationTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name)
        self.source=self.root/'source';self.source.mkdir()
        (self.source/'SKILL.md').write_text('original',encoding='utf-8')
        (self.source/'EDITION.json').write_text(json.dumps({'version':'1.0.0','files':{'SKILL.md':hashlib.sha256(b'original').hexdigest()}}),encoding='utf-8')
    def tearDown(self):self.tmp.cleanup()
    def test_first_install(self):
        result=installer.install(self.root/'dest',source=self.source)
        self.assertEqual(result['status'],'installed_and_verified')
        self.assertEqual((self.root/'dest/stl-houjie/SKILL.md').read_text(),'original')
    def test_existing_requires_explicit_upgrade(self):
        installer.install(self.root/'dest',source=self.source)
        with self.assertRaisesRegex(ValueError,'already installed'):
            installer.install(self.root/'dest',source=self.source)
    def test_upgrade_preserves_backup_and_removes_stale_files(self):
        installer.install(self.root/'dest',source=self.source)
        old=self.root/'dest/stl-houjie';(old/'local-note.md').write_text('preserve me')
        result=installer.install(self.root/'dest',True,self.source)
        self.assertEqual((Path(result['backup'])/'local-note.md').read_text(),'preserve me')
        self.assertFalse((old/'local-note.md').exists())
    def test_tamper_rejected_before_mutation(self):
        (self.source/'SKILL.md').write_text('tampered')
        with self.assertRaisesRegex(ValueError,'integrity'):
            installer.install(self.root/'dest',source=self.source)
        self.assertFalse((self.root/'dest').exists())
    def test_extra_file_rejected(self):
        (self.source/'untracked').write_text('x')
        with self.assertRaisesRegex(ValueError,'file set'):
            installer.verify(self.source)
    def test_parent_path_manifest_rejected(self):
        (self.root/'escape').write_text('secret')
        manifest={'version':'1.0.0','files':{'../escape':hashlib.sha256(b'secret').hexdigest()}}
        (self.source/'EDITION.json').write_text(json.dumps(manifest))
        with self.assertRaises(ValueError):installer.verify(self.source)

if __name__=='__main__':unittest.main()
