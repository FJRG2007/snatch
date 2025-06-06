from pathlib import Path
from filecmp import dircmp
import os, git, shutil, tempfile
from gitignore_parser import parse_gitignore

GITHUB_REPO_URL = "https://github.com/FJRG2007/snatch.git"
LOCAL_DIR = "" # Coming Soon.

def clone_repo(temp_dir):
    # Clones the GitHub repository to a temporary directory.
    git.Repo.clone_from(GITHUB_REPO_URL, temp_dir)

def load_gitignore(local_dir):
    # Loads and parses the .gitignore file.
    gitignore_file = Path(local_dir) / ".gitignore"
    if not gitignore_file.exists(): return None
    with open(gitignore_file) as f:
        return parse_gitignore(f.read())

def compare_directories(repo_dir, local_dir, gitignore_rule):
    # Compares files in two directories, applying the .gitignore rules.
    differences = []
    dcmp = dircmp(repo_dir, local_dir)
    def check_diffs(dcmp):
        for name in dcmp.left_only:
            if not gitignore_rule or not gitignore_rule(os.path.join(dcmp.left, name)): differences.append(os.path.join(dcmp.left, name))
        for name in dcmp.right_only:
            if not gitignore_rule or not gitignore_rule(os.path.join(dcmp.right, name)): differences.append(os.path.join(dcmp.right, name))
        for name in dcmp.diff_files:
            if not gitignore_rule or not gitignore_rule(os.path.join(dcmp.left, name)): differences.append(os.path.join(dcmp.left, name))
        for sub_dcmp in dcmp.subdirs.values():
            check_diffs(sub_dcmp)
    check_diffs(dcmp)
    return differences

def update_files(differences, repo_dir, local_dir):
    # Updates the local files with those in the repository.
    for diff in differences:
        rel_path = os.path.relpath(diff, repo_dir)
        src = os.path.join(repo_dir, rel_path)
        dst = os.path.join(local_dir, rel_path)
        if os.path.isdir(src): shutil.copytree(src, dst, dirs_exist_ok=True)
        else: shutil.copy2(src, dst)

def verifySnatch():
    with tempfile.TemporaryDirectory() as temp_dir:
        clone_repo(temp_dir)
        differences = compare_directories(temp_dir, LOCAL_DIR, load_gitignore(LOCAL_DIR))
        if differences:
            print(f"Differences found: {differences}")
            update_files(differences, temp_dir, LOCAL_DIR)
            print("Files updated.")
        else: print("No differences found.")