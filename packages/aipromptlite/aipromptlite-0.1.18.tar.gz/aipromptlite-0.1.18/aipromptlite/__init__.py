
from pathlib import Path
import importlib

# Dynamically import all modules from subdirectories
__package_dir = Path(__file__).parent
__module_dirs = [d for d in __package_dir.iterdir() if d.is_dir() and not d.name.startswith('__')]

for __module_dir in __module_dirs:
    if (__module_dir / '__init__.py').exists():
        __module_name = __module_dir.name
        globals()[__module_name] = importlib.import_module(f'.{__module_name}', package=__package__)
        if hasattr(globals()[__module_name], '__all__'):
            globals().update({__name: getattr(globals()[__module_name], __name) 
                            for __name in globals()[__module_name].__all__})
                            
__all__ = ["CODE_GENERATION_PROMPT","CODE_EXPLANATION_CLAUDE_PROMPT","TECHNICAL_EXPLANATIONS","PYTHON_CODER_PROMPT","EXPERT_TECHNICAL_WRITER","PREVIEW_SYS_PROMPT","CLAUDE_SYS_PROMPT","PREDICTIVE_QUESTION_REASONING_PROMPT","BRAINSTROM_BUDDY_PROMPT","AI_TECH_LEAD_PROMPT"]
