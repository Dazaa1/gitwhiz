from .constants import TEMPLATES, BASE_DIR
import subprocess

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


    def get_available_templates(self):
        return TEMPLATES
    

    def prompt_user_for_values(self):
        title = input("Title: ")
        description = input("Description: ")

        return {
            "Title": title,
            "Description": description
        }
    
    
    def render_template(self, template, values):
        if not template:
            return ""

        rendered = template
        for key, val in (values or {}).items():
            rendered = rendered.replace(f"{{{{{key}}}}}", str(val))
            rendered = rendered.replace(f"{{{key}}}", str(val))

        return rendered