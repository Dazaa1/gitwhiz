from models.repository import Repository
from models.commit import Commit
from models.branch import Branch

def main():
    repo = Repository()
    commit = Commit()
    branch = Branch()

    is_merged = branch.is_merged("test")
    branch_age = branch.get_all_branches()
    
    print(branch_age)
    if is_merged == "test":
        print("Merged")

    else:
        print("Not merged")

main()