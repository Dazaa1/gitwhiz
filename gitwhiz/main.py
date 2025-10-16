from models.repository import Repository

def main():
    repo = Repository()
    changes_files = repo.get_status()
    branch_name = repo.get_current_branch()

    print(f"branch name: {branch_name}")


main()