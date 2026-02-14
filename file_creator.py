import os
from pathlib import Path


def has_extension(name):
    return '.' in name and not name.endswith('.') and not name.startswith('.')


def create_item(base_path, name):
    if not name or not name.strip():
        return False, "名称不能为空"
    
    name = name.strip()
    full_path = Path(base_path) / name
    
    if full_path.exists():
        return False, f"'{name}' 已存在"
    
    try:
        if has_extension(name):
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.touch()
            return True, f"文件 '{name}' 创建成功"
        else:
            full_path.mkdir(parents=True, exist_ok=True)
            return True, f"文件夹 '{name}' 创建成功"
    except PermissionError:
        return False, f"没有权限在当前位置创建"
    except Exception as e:
        return False, f"创建失败: {str(e)}"


def is_valid_name(name):
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        if char in name:
            return False, f"名称包含非法字符: {char}"
    return True, None
