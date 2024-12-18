from collections import defaultdict
from lagoon import git
from lagoon.program import partial
import xml.dom.minidom as dom, os

class Files:

    @staticmethod
    def _findfiles(walkpath, suffixes, prefixes):
        def acceptname():
            for suffix in suffixes:
                if name.endswith(suffix):
                    return True
            for prefix in prefixes:
                if name.startswith(prefix):
                    return True
        prefixlen = len(walkpath + os.sep)
        for dirpath, dirnames, filenames in os.walk(walkpath):
            for name in sorted(filenames):
                if acceptname():
                    yield os.path.join(dirpath, name)[prefixlen:]
            dirnames.sort()

    @classmethod
    def relpaths(cls, root, suffixes, prefixes):
        paths = list(cls._findfiles(root, suffixes, prefixes))
        if os.path.exists(os.path.join(root, '.gitmodules')):
            for submoduleslash in (l.split(' ', 1)[1] + os.sep for l in git.config('--file', '.gitmodules', '--get-regexp', '^submodule[.].+[.]path$', cwd = root).splitlines()):
                paths = [p for p in paths if not p.startswith(submoduleslash)]
        if paths:
            with git.check_ignore[partial](*paths, check = False, cwd = root) as p:
                ignored = set(p.stdout.read().splitlines())
                assert p.wait() in [0, 1]
            for path in paths:
                if path not in ignored:
                    yield path

    def __init__(self, root):
        srcsuffixes = sum(([s, f"{s}.aridt"] for s in ['.py', '.py3', '.pyx', '.s', '.sh', '.h', '.cpp', '.cxx', '.arid', '.gradle', '.java', '.mk', '.md']), [])
        self.allsrcpaths = [os.path.join(root, p) for p in self.relpaths(root, srcsuffixes, ['Dockerfile', 'Makefile'])]
        self.docpaths = [p for p in self.allsrcpaths if p.endswith('.md')]
        self.pypaths = [p for p in self.allsrcpaths if p.endswith('.py')]
        self.root = root

    def testpaths(self, reportpath):
        paths = [p for p in self.pypaths if os.path.basename(p).startswith('test_')] + self.docpaths
        if os.path.exists(reportpath):
            with open(reportpath) as f:
                doc = dom.parse(f)
            nametopath = dict([p[len(self.root + os.sep):-len('.py')].replace(os.sep, '.'), p] for p in paths)
            pathtotime = defaultdict(int)
            for e in doc.getElementsByTagName('testcase'):
                name = e.getAttribute('classname')
                while True:
                    i = name.rfind('.')
                    if -1 == i:
                        break
                    name = name[:i]
                    if name in nametopath:
                        pathtotime[nametopath[name]] += float(e.getAttribute('time'))
                        break
            paths.sort(key = lambda p: pathtotime.get(p, float('inf')))
        return paths
