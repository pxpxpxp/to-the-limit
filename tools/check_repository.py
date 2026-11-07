#!/usr/bin/env python3
"""Read-only checks for site links, download pairs, hashes and source ZIPs.

Run from anywhere: python3 /path/to/repo/tools/check_repository.py
An optional repository path is useful for tests. External URLs are never fetched.
Markdown checks cover inline links/images and reference definitions, not code
examples or generated Markdown heading anchors. ZIPs are read, never extracted.
"""

import argparse
import hashlib
from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit
import zipfile


CSS_URL = re.compile(r'url\(\s*(?:"([^"]*)"|\'([^\']*)\'|([^)]*?))\s*\)', re.I)


def css_urls(text):
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.S)
    return [next(value for value in match.groups() if value is not None)
            for match in CSS_URL.finditer(text)]


class HTMLLinks(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.ids = set()
        self.in_style = False
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'):
            self.ids.add(attrs['id'])
        if tag == 'a' and attrs.get('name'):
            self.ids.add(attrs['name'])
        for name in ('href', 'src', 'poster') + (('data',) if tag == 'object' else ()):
            if attrs.get(name):
                self.links.append(attrs[name])
        if attrs.get('style'):
            self.links.extend(css_urls(attrs['style']))
        self.in_style = tag == 'style'

    def handle_endtag(self, tag):
        if tag == 'style':
            self.in_style = False

    def handle_data(self, data):
        if self.in_style:
            self.links.extend(css_urls(data))


def markdown_urls(text):
    """Extract ordinary file links, ignoring fenced/indented/inline code."""
    lines = []
    fence = None
    for line in text.splitlines():
        marker = re.match(r'^ {0,3}(`{3,}|~{3,})', line)
        if fence:
            if re.match(r'^ {0,3}' + re.escape(fence[0]) +
                        '{' + str(len(fence)) + r',}\s*$', line):
                fence = None
            continue
        if marker:
            fence = marker.group(1)
            continue
        if line.startswith(('    ', '\t')):
            continue
        lines.append(line)
    text = re.sub(r'(`+).*?\1', '', '\n'.join(lines), flags=re.S)
    text = re.sub(r'<!--.*?-->', '', text, flags=re.S)
    # Support angle-bracket destinations and one level of parentheses in paths.
    destination = r'(<[^>\n]+>|(?:[^\s()]+|\([^\s()]*\))+)'
    inline = re.findall(r'!?\[[^\]\n]*\]\(\s*' + destination +
                        r'(?:\s+["\'][^\n]*?["\'])?\s*\)', text)
    references = re.findall(r'^ {0,3}\[[^\]\n]+\]:\s*' + destination,
                            text, flags=re.M)
    return [value.strip('<>') for value in inline + references]


def check_repository(root):
    """Return all detected errors; never change files or access the network."""
    root = Path(root).resolve()
    site = root / 'docs'
    errors = []
    files = sorted(path for path in root.rglob('*')
                   if path.is_file() and not path.is_symlink()
                   and not any(part.startswith('.') or part == '__pycache__'
                               for part in path.relative_to(root).parts))
    html = {path: HTMLLinks(path.read_text(encoding='utf-8'))
            for path in files if path.suffix.lower() in ('.html', '.htm')}

    def label(path):
        return str(path.relative_to(root))

    def local_target(source, url):
        parsed = urlsplit(url.strip())
        if parsed.scheme or parsed.netloc:
            return None
        name = unquote(parsed.path)
        base = site if source.is_relative_to(site) else root
        target = ((base / name.lstrip('/')) if name.startswith('/')
                  else (source.parent / name if name else source)).resolve()
        if not target.is_relative_to(root):
            errors.append(f'{label(source)}: link escapes repository: {url}')
            return None
        return target, unquote(parsed.fragment)

    def check_link(source, url):
        result = local_target(source, url)
        if result is None:
            return
        target, fragment = result
        if not target.exists():
            errors.append(f'{label(source)}: missing link target: {url}')
            return
        if target.is_dir() and (target / 'index.html').is_file():
            target /= 'index.html'
        if fragment and target in html and fragment not in html[target].ids:
            errors.append(f'{label(source)}: missing fragment: {url}')

    for path in files:
        suffix = path.suffix.lower()
        if path in html:
            urls = html[path].links
        elif suffix == '.css':
            urls = css_urls(path.read_text(encoding='utf-8'))
        elif suffix == '.md':
            urls = markdown_urls(path.read_text(encoding='utf-8'))
        else:
            urls = []
        for url in sorted(set(urls)):
            check_link(path, url)

        if suffix == '.sha256':
            entries = 0
            for number, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
                if not line.strip() or line.lstrip().startswith('#'):
                    continue
                match = re.fullmatch(r'([0-9a-fA-F]{64}) [ *](.+)', line)
                if not match:
                    errors.append(f'{label(path)}:{number}: malformed SHA-256 entry')
                    continue
                entries += 1
                digest, name = match.groups()
                target = (path.parent / name).resolve()
                if not target.is_relative_to(root) or not target.is_file():
                    errors.append(f'{label(path)}:{number}: missing/unsafe checksum target: {name}')
                    continue
                hasher = hashlib.sha256()
                with target.open('rb') as stream:
                    for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                        hasher.update(chunk)
                if hasher.hexdigest() != digest.lower():
                    errors.append(f'{label(path)}:{number}: SHA-256 mismatch: {name}')
            if not entries:
                errors.append(f'{label(path)}: no SHA-256 entries')

        if path.name.endswith('_source.zip'):
            try:
                with zipfile.ZipFile(path) as archive:
                    bad = archive.testzip()
                    if bad:
                        errors.append(f'{label(path)}: ZIP CRC failure: {bad}')
            except (OSError, ValueError, RuntimeError, zipfile.BadZipFile, NotImplementedError) as exc:
                errors.append(f'{label(path)}: invalid source ZIP: {exc}')

    index = site / 'index.html'
    if index not in html:
        errors.append('docs/index.html: missing download page')
    else:
        linked = set()
        for url in html[index].links:
            result = local_target(index, url)
            if result is not None and result[0].suffix.lower() == '.rbf':
                linked.add(result[0])
        for rbf in sorted(linked):
            source = rbf.with_name(rbf.stem + '_source.zip')
            if not source.is_file():
                errors.append(f'{label(rbf)}: missing matching source ZIP: {source.name}')
        for rbf in sorted((site / 'downloads').glob('*.rbf')):
            if rbf.resolve() not in linked:
                errors.append(f'{label(rbf)}: orphan RBF not linked by docs/index.html')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('repository', nargs='?', type=Path,
                        default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        errors = check_repository(args.repository)
    except (OSError, UnicodeError, ValueError) as exc:
        errors = [f'Unable to complete repository checks: {exc}']
    if errors:
        for error in errors:
            print(f'ERROR: {error}')
        print(f'Repository checks failed ({len(errors)} errors).')
        return 1
    print('Repository checks passed: links, fragments, SHA-256, source ZIPs and RBF pairs.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
