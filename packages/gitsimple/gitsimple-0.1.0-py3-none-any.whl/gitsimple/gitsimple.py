import shutil
import subprocess
from pathlib import Path

"""
git config --global user.name <name>
git config --global user.email <email>
git config --global credential.helper store
"""


class GitSimple:
    def __init__(self, path: str | None = None, exist_ok: bool = True):
        """
        path: local target repository path
        """
        self.path = Path(path or ".").resolve()
        if exist_ok and not self.path.exists():
            self.path.mkdir(exist_ok=True, parents=True)

    def shell(
        self, opts: str | list[str], capture: bool = False, path: str = None, raise_err: bool = True
    ) -> subprocess.CompletedProcess | None:
        path = path or self.path

        error_, retcode = None, None
        try:
            retcode = subprocess.run(opts, text=True, check=True, cwd=path, capture_output=capture)
        except subprocess.CalledProcessError as e:
            error_ = (opts, e)

        if raise_err and error_:
            raise ValueError(f"{error_}")

        return retcode

    def exists(self, path: str = None) -> bool:
        path = path or self.path
        return (Path(path) / ".git").exists()

    def remove(self, path: str):
        shutil.rmtree(path)

    def clone(self, repo: str, branch: str | None = None, exists_ok: bool = False, path: str | None = None) -> bool:
        """
        git clone <repo>
        git clone <repo> -b <branch>
        """
        path = path or self.path
        cmd = f"git clone {repo} {path}"
        if branch is not None:
            cmd += f" -b {branch}"
        if exists_ok and self.exists(path=path):
            return False

        rtn = self.shell(cmd)

        return rtn is not None

    def status(self) -> list[tuple[str, str]]:
        """
        git status
        git status --porcelain
            XY <file>

            State Code            XY
            --------------        --
            ' ': Unchanged
            'M': Modified       # MM
            'A': Added          # A
            'D': Deleted        # DD
            'R': Renamed        # R
            'C': Copied         # C
            'U': Unmerged       # UU
            '?': Untracked      # ??
            '!': Ignored        # !!
        """
        cmd = r"git status --porcelain"

        content = self.shell(cmd, capture=True).stdout.strip()

        changes = []
        for line in content.split("\n"):
            if not line.strip():
                continue

            status_code, file = line[:2], line[3:]
            changes.append((status_code, file))

        return changes

    def branch(self, current: bool = False, remote: bool = False) -> str | list[str]:
        """
        git branch
        git branch --all
        git rev-parse --abbrev-ref HEAD
        """
        if current:
            return self.shell(r"git rev-parse --abbrev-ref HEAD", capture=True).stdout.strip()

        cmd = r"git branch"
        if remote:
            cmd += r" -a"  # --all
        content = self.shell(cmd, capture=True).stdout.strip()

        branches = []
        for line in content.split("\n"):
            line = line.strip()

            if line.startswith("*"):
                branches = [line[2:]] + branches
            else:
                if remote:
                    if "HEAD ->" in line:
                        continue
                    line = line.split(r"/", 1)[-1]
                branches.append(line)

        return branches

    def fetch(self, prune: bool = False, branch: str = None) -> str | None:
        """
        git fetch
        git fetch --all
        git fetch --tags
        git fetch --prune
        git fetch origin <branch>
        """
        cmd = "git fetch"
        if prune:
            cmd += " --prune"
        if branch:
            cmd += f" origin {branch}"

        content = self.shell(cmd, capture=True).stdout.strip()

        return content

    def switch(self, commit: str) -> str | None:
        """
        git switch <commit>
        """
        cmd = f"git switch {commit}"

        content = self.shell(cmd, capture=True).stdout.strip()

        return content

    def add(self, files: list[str] = None) -> bool:
        """
        git add .
        git add <file1> <file2>
        """
        files = " ".join(str(f) for f in files) if files else "."

        cmd = f"git add {files}"

        rtn = self.shell(cmd)

        return rtn is not None

    def commit(self, message: str, no_change_ok: bool = False) -> str | None:
        """
        git commit -m <message>
        """
        if no_change_ok and len(self.status()) == 0:
            return None

        cmd = f'git commit -m "{message}"'

        content = self.shell(cmd, capture=True).stdout.strip()

        return content

    def push(self, branch: str = None) -> str | None:
        """
        git push
        git push origin <branch>
        """
        cmd = r"git push"
        if branch:
            cmd += f" origin {branch}"

        content = self.shell(cmd, capture=True).stdout.strip()

        return content

    def reset(self, commit: str = None, mode: str = "hard") -> str | None:
        """
        git reset
        git reset --hard
        """
        cmd = f"git reset --{mode}"
        if commit:
            cmd += f" {commit}"

        content = self.shell(cmd, capture=True).stdout.strip()

        return content
