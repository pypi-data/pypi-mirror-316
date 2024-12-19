import importlib.util
import os


def load_models(directory):
    """
    动态导入指定目录及其子目录中所有的models.py文件中的类。

    Args:
        directory (str): 要搜索的目录路径。

    """

    # 使用os.walk()递归遍历目录结构
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith("models.py") and file != "__init__.py":
                module_name = file[:-3]  # 移除 .py 扩展名
                module_path = os.path.join(root, file)

                spec = importlib.util.spec_from_file_location(module_name, module_path)
                if spec:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    # 导入模块中的所有类
                    globals().update(vars(module))
