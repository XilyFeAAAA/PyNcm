from pathlib import Path

def path_to_module_name(path: Path) -> str:
    """转换路径为模块名"""
    return path.parts[-1]
