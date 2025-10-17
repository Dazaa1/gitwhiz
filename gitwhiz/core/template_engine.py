from .constants import TEMPLATES, BASE_DIR

class TemplateEngine:
    def __init__(self):
        pass

    def load_template(self, template_type):
        if template_type in TEMPLATES:
            path = f"{BASE_DIR}/templates/{template_type}.txt"
            with open(path, "r") as f:
                value = f.read()

            return value
        
        else:
            print("Not a template type")