import os
import logging
from datetime import datetime
from typing import Optional
from utils.path_tool import get_abs_path

# 1. 定义颜色代码 (ANSI Escape Sequences)
BLUE = "\033[34m"
RESET = "\033[0m"

# 目录配置
LOG_ROOT = get_abs_path("logs")
os.makedirs(LOG_ROOT, exist_ok=True)

# 2. 定义两种格式化器
# 文件格式：标准纯文本
FILE_FORMAT = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
)

# 控制台格式：加入蓝色转义字符
# 我们只让 %(message)s 变蓝，这样看起来更清晰
CONSOLE_FORMAT = logging.Formatter(
    f'%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - {BLUE}%(message)s{RESET}'
)


def get_logger(
        name: str = "agent",
        console_level: int = logging.INFO,
        file_level: int = logging.DEBUG,
        log_file: Optional[str] = None,
) -> logging.Logger:
    logger = logging.getLogger(name)

    # 关键：如果已经有 Handler 了，直接返回，防止重复打印日志
    if logger.handlers:
        return logger

    # 必须设置 Logger 的总门槛为最低级别，否则 Handler 的低级别设置会失效
    logger.setLevel(logging.DEBUG)

    # --- 控制台 Handler (带颜色) ---
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(CONSOLE_FORMAT)  # 使用带颜色的格式
    logger.addHandler(console_handler)

    # --- 文件 Handler (纯文本) ---
    if not log_file:
        log_file = os.path.join(LOG_ROOT, f"{name}_{datetime.now().strftime('%Y%m%d')}.log")

    # 指定 encoding='utf-8' 非常正确，防止 Windows 上乱码
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(file_level)
    file_handler.setFormatter(FILE_FORMAT)  # 使用不带颜色的格式
    logger.addHandler(file_handler)

    # 阻止日志向上传递到 root logger，避免在某些环境下产生双重输出
    logger.propagate = False

    return logger


# 快捷获取默认日志器
logger = get_logger()

if __name__ == '__main__':
    logger.info("这是一条蓝色的信息日志")
    logger.error("这是一条带蓝色正文的错误日志")
    logger.debug("这条调试日志在控制台看不见，但在文件里能看见")