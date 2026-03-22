from datetime import datetime
import logging
from utils.path_tool import get_abs_path
import os
# 目录报错根目录
LOG_ROOT = get_abs_path("logs")

#确保目录存在
os.makedirs(LOG_ROOT,exist_ok=True)

#日志的格式配置 error info debug
DEFAULT_LOG_FORMAT=logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s -%(filename)s:%(lineno)d- %(message)s'
    #日志输出时间---名字----级别-error-info-debug-废话-文件名字以及哪一行-日志正文
)


def get_logger(    #
        name: str = "agent",#区分不同模块
        console_level: int = logging.INFO,#默认级别,控制只有大于info级别的日志才会输出
        file_level: int = logging.DEBUG, #啰嗦模式
        log_file = None, #
) -> logging.Logger:#logging模块的类对象
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)#设置级别

    # 避免重复添加Handler
    if logger.handlers: #确保后面代码只执行一次
        return logger

    # 控制台Handler-
    console_handler = logging.StreamHandler()#流式
    console_handler.setLevel(console_level)
    console_handler.setFormatter(DEFAULT_LOG_FORMAT)#格式-传默认的格式

    logger.addHandler(console_handler)#添加

    # 文件Handler
    if not log_file:        # 日志文件的存放路径
        log_file = os.path.join(LOG_ROOT, f"{name}_{datetime.now().strftime('%Y%m%d')}.log")

    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(file_level)
    file_handler.setFormatter(DEFAULT_LOG_FORMAT)

    logger.addHandler(file_handler)

    return logger

#快捷获取日志器
logger = get_logger()#from文件 import logger变量

if __name__ == '__main__':
    logger.info("信息日志")
    logger.error("错误日志")
    logger.warning("警告日志")
    logger.debug("调试日志")
