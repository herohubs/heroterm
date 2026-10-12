# -*- coding: utf-8 -*-
# pylint: disable=redefined-outer-name
import os

from guake.utils import FileManager
from guake.utils import get_git_branch
from guake.utils import get_process_name


def test_file_manager(fs):
    fs.create_file("/foo/bar", contents="test")
    fm = FileManager()
    assert fm.read("/foo/bar") == "test"


def test_file_manager_hit(fs):
    f = fs.create_file("/foo/bar", contents="test")

    fm = FileManager(delta=9999)
    assert fm.read("/foo/bar") == "test"
    f.set_contents("changed")
    assert fm.read("/foo/bar") == "test"


def test_file_manager_miss(fs):
    f = fs.create_file("/foo/bar", contents="test")

    fm = FileManager(delta=0.0)
    assert fm.read("/foo/bar") == "test"
    f.set_contents("changed")
    assert fm.read("/foo/bar") == "changed"


def test_file_manager_clear(fs):
    f = fs.create_file("/foo/bar", contents="test")

    fm = FileManager(delta=9999)
    assert fm.read("/foo/bar") == "test"
    f.set_contents("changed")
    assert fm.read("/foo/bar") == "test"
    fm.clear()
    assert fm.read("/foo/bar") == "changed"


def test_process_name():
    assert get_process_name(os.getpid())


def test_get_git_branch_on_branch(tmp_path):
    (tmp_path / ".git").mkdir()
    (tmp_path / ".git" / "HEAD").write_text("ref: refs/heads/feature/foo\n")
    sub = tmp_path / "a" / "b"
    sub.mkdir(parents=True)
    assert get_git_branch(str(sub)) == "feature/foo"


def test_get_git_branch_detached(tmp_path):
    (tmp_path / ".git").mkdir()
    (tmp_path / ".git" / "HEAD").write_text("0123456789abcdef0123456789abcdef01234567\n")
    assert get_git_branch(str(tmp_path)) == "0123456"


def test_get_git_branch_worktree(tmp_path):
    git_dir = tmp_path / "main" / ".git" / "worktrees" / "wt"
    git_dir.mkdir(parents=True)
    (git_dir / "HEAD").write_text("ref: refs/heads/wt-branch\n")
    worktree = tmp_path / "wt"
    worktree.mkdir()
    (worktree / ".git").write_text(f"gitdir: {git_dir}\n")
    assert get_git_branch(str(worktree)) == "wt-branch"


def test_get_git_branch_outside_repo(tmp_path):
    assert get_git_branch(str(tmp_path)) is None
