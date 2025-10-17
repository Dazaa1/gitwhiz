from models.repository import Repository
from models.commit import Commit
from models.branch import Branch
from core.template_engine import TemplateEngine

def main():
    repo = Repository()
    commit = Commit()
    branch = Branch()
    template_engine = TemplateEngine()

    is_merged = branch.is_merged("test")
    branch_age = branch.get_all_branches()

    load_docs = template_engine.load_template("feature")
    print(load_docs)
    
    print(branch_age)
    if is_merged == "test":
        print("Merged")

    else:
        print("Not merged")

main()