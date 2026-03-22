#路径工具-为整个工程提供统一的绝对路径
import os
def get_project_root()->str:
    '''
    #获取工程所在的根目录
    return:字符串根目录
    '''
    #当前文件的根目录
    curr_file=os.path.abspath(__file__)
    #往上跳两级，获取工程根目录
    #先获取文件所在文件夹绝对路径
    curr_dir=os.path.dirname(curr_file)
    #在获取工程根目录
    project_root=os.path.dirname(curr_dir)

    return project_root

def get_abs_path(relative_path:str) ->str:
    '''
    你给我相对路径，我返回绝对路径
    :param relative_path:
    :return:绝对路径
    '''
    project_root=get_project_root()
    return os.path.join(project_root,relative_path)


if __name__=="__main__":
    print(get_abs_path("config/config.txt"))
