from pathlib import Path
from importlib import import_module

DEBUG = 0

def load_all_plugins():
    for p in Path("plugins").iterdir():
        if p.stem.startswith(("_", ".")):
            continue
        name = ".".join(p.with_suffix("").parts)
        
        if DEBUG:
            import_module(name)
            
        else:
            try:
                import_module(name)
            except Exception as e:
                print(f"{name} 导入失败 X")
                print(e)
            else:
                print(f"{name} 导入成功")
