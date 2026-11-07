"""Run with: python3 -m unittest discover -s tools -p 'test_check_repository.py'."""

import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

from check_repository import check_repository


class RepositoryChecks(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.write('docs/index.html', '<main id="main"><a href="#main">Main</a>'
                   '<a href="downloads/release.rbf">Core</a>'
                   '<a href="other.html#target">Other</a>'
                   '<link href="style.css?v=1" rel="stylesheet"></main>')
        self.write('docs/other.html', '<h1 id="target">Target</h1>')
        self.write('docs/style.css', 'body { background: url("assets/pixel.svg?v=1"); }')
        self.write('docs/assets/pixel.svg', '<svg/>')
        self.write('docs/downloads/release.rbf', 'test binary')
        self.write('README.md', '[Website](docs/index.html#main)\n'
                   '[Download][core]\n[core]: docs/downloads/release.rbf\n')
        with zipfile.ZipFile(self.root / 'docs/downloads/release_source.zip', 'w') as archive:
            archive.writestr('source.txt', 'source fixture')
        self.update_manifest()

    def write(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')

    def update_manifest(self):
        lines = []
        for name in ('release.rbf', 'release_source.zip'):
            path = self.root / 'docs/downloads' / name
            lines.append(hashlib.sha256(path.read_bytes()).hexdigest() + '  ' + name)
        self.write('docs/downloads/release.sha256', '\n'.join(lines) + '\n')

    def assert_failure(self, message):
        errors = check_repository(self.root)
        self.assertTrue(any(message in error for error in errors), errors)

    def test_healthy_repository(self):
        self.assertEqual(check_repository(self.root), [])

    def test_missing_html_link(self):
        (self.root / 'docs/other.html').unlink()
        self.assert_failure('missing link target: other.html#target')

    def test_missing_fragment(self):
        self.write('docs/other.html', '<h1 id="different">Target</h1>')
        self.assert_failure('missing fragment: other.html#target')

    def test_missing_css_asset(self):
        (self.root / 'docs/assets/pixel.svg').unlink()
        self.assert_failure('missing link target: assets/pixel.svg?v=1')

    def test_missing_markdown_link(self):
        self.write('README.md', '[Absent](missing.md)\n')
        self.assert_failure('missing link target: missing.md')

    def test_missing_markdown_reference(self):
        self.write('README.md', '[Absent][ref]\n[ref]: missing.md "Title"\n')
        self.assert_failure('missing link target: missing.md')

    def test_documentation_code_examples_are_ignored(self):
        self.write('README.md', '`[inline](missing.md)`\n'
                   '```markdown\n[fenced](missing.md)\n```\n'
                   '~~~\n[fenced](missing.md)\n~~~\n'
                   '    [indented](missing.md)\n'
                   '<!-- [comment](missing.md) -->\n')
        self.assertEqual(check_repository(self.root), [])

    def test_bad_checksum(self):
        self.write('docs/downloads/release.rbf', 'changed')
        self.assert_failure('SHA-256 mismatch: release.rbf')

    def test_bad_manifest(self):
        self.write('docs/downloads/release.sha256', 'not a checksum\n')
        self.assert_failure('malformed SHA-256 entry')

    def test_orphan_rbf(self):
        self.write('docs/downloads/stale.rbf', 'old binary')
        self.assert_failure('orphan RBF')

    def test_missing_source(self):
        (self.root / 'docs/downloads/release_source.zip').unlink()
        self.assert_failure('missing matching source ZIP')

    def test_invalid_source_zip(self):
        self.write('docs/downloads/release_source.zip', 'not a zip')
        self.update_manifest()
        self.assert_failure('invalid source ZIP')

    def test_corrupt_zip_member_crc(self):
        path = self.root / 'docs/downloads/release_source.zip'
        path.write_bytes(path.read_bytes().replace(b'source fixture', b'broken fixture'))
        self.update_manifest()
        self.assert_failure('ZIP CRC failure')

    def test_external_links_are_ignored(self):
        self.write('README.md', '[Web](https://example.invalid/absent)\n'
                   '[Web](//example.invalid/absent)\n[Email](mailto:a@example.invalid)')
        self.assertEqual(check_repository(self.root), [])

    def test_root_relative_and_encoded_links(self):
        self.write('docs/other.html', '<h1 id="target">Target</h1>'
                   '<img src="/assets/my%20pixel.svg"><a href="/index.html#main">Home</a>')
        self.write('docs/assets/my pixel.svg', '<svg/>')
        self.assertEqual(check_repository(self.root), [])

    def test_cli_from_other_directory(self):
        script = Path(__file__).resolve().with_name('check_repository.py')
        result = subprocess.run([sys.executable, str(script), str(self.root)],
                                cwd=self.root / 'docs', capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('Repository checks passed', result.stdout)
        self.write('docs/downloads/orphan.rbf', 'old')
        result = subprocess.run([sys.executable, str(script), str(self.root)],
                                cwd=self.root / 'docs', capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn('orphan RBF', result.stdout)


if __name__ == '__main__':
    unittest.main()
