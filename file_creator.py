"""
QuickFileCreator - 文件创建模块

本模块负责：
1. 判断输入名称是文件还是文件夹
2. 验证文件名合法性
3. 执行文件或文件夹的创建操作

工作原理：
- 通过检查名称是否包含扩展名来判断类型
- 使用 pathlib 库处理路径，确保跨平台兼容性
- 返回操作结果和消息供 UI 显示
"""

import os
from pathlib import Path


def has_extension(name):
    """
    判断名称是否包含文件扩展名
    
    判断逻辑：
    - 名称中包含点号（.）
    - 点号不在末尾（排除 "filename." 情况）
    - 点号不在开头（排除 ".gitignore" 情况，隐藏文件视为无扩展名）
    
    Args:
        name: 文件名或文件夹名
        
    Returns:
        bool: True 表示是文件名（有扩展名），False 表示是文件夹名
    
    Examples:
        >>> has_extension("test.txt")
        True
        >>> has_extension("folder")
        False
        >>> has_extension(".gitignore")
        False  # 隐藏文件，视为无扩展名
        >>> has_extension("file.")
        False  # 点号在末尾，视为无扩展名
    """
    return '.' in name and not name.endswith('.') and not name.startswith('.')


def create_item(base_path, name):
    """
    在指定路径创建文件或文件夹
    
    根据名称是否包含扩展名决定创建类型：
    - 有扩展名：创建空文件
    - 无扩展名：创建文件夹
    
    Args:
        base_path: 基础路径（资源管理器当前路径）
        name: 要创建的文件名或文件夹名
        
    Returns:
        tuple: (成功标志, 消息)
            - (True, "文件 'xxx' 创建成功")
            - (False, "错误原因")
    
    工作流程：
        1. 验证名称非空
        2. 构建完整路径
        3. 检查是否已存在
        4. 根据类型创建文件或文件夹
        5. 处理可能的异常
    """
    # 验证名称非空
    if not name or not name.strip():
        return False, "名称不能为空"
    
    # 去除首尾空白
    name = name.strip()
    
    # 使用 pathlib 构建完整路径（自动处理路径分隔符）
    full_path = Path(base_path) / name
    
    # 检查是否已存在同名文件或文件夹
    if full_path.exists():
        return False, f"'{name}' 已存在"
    
    try:
        if has_extension(name):
            # 创建文件
            # parent.mkdir 确保父目录存在
            # touch 创建空文件
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.touch()
            return True, f"文件 '{name}' 创建成功"
        else:
            # 创建文件夹
            # parents=True 自动创建父目录
            # exist_ok=True 如果目录已存在不报错（但前面已检查）
            full_path.mkdir(parents=True, exist_ok=True)
            return True, f"文件夹 '{name}' 创建成功"
            
    except PermissionError:
        # 权限不足
        return False, f"没有权限在当前位置创建"
        
    except Exception as e:
        # 其他异常（如路径无效、磁盘空间不足等）
        return False, f"创建失败: {str(e)}"


def is_valid_name(name):
    """
    验证文件名是否合法
    
    Windows 文件名不能包含以下字符：
    < > : " / \\ | ? *
    
    其中：
    - < > : " | ? * 是 Windows 保留字符
    - / \\ 是路径分隔符
    - : 还用于驱动器号
    
    Args:
        name: 要验证的文件名
        
    Returns:
        tuple: (是否合法, 错误消息)
            - (True, None) 表示合法
            - (False, "名称包含非法字符: x") 表示非法
    
    Note:
        此函数只检查基本合法性，不检查：
        - 保留名称（如 CON, PRN, AUX 等）
        - 路径长度限制
        - 文件名长度限制
    """
    # Windows 文件名非法字符
    invalid_chars = '<>:"/\\|?*'
    
    # 遍历检查每个非法字符
    for char in invalid_chars:
        if char in name:
            return False, f"名称包含非法字符: {char}"
    
    return True, None
