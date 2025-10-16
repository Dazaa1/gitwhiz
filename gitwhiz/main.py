from models.repository import Repository
from models.commit import Commit

def main():
    repo = Repository()
    commit = Commit()

    parsed = commit.parse_message("fix(program): a bug")
    print(parsed)
    

main()