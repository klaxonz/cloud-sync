import logging
import sys
import configparser
from alipcs_py import AliPCSApi
from alipcs_py.commands.download import download


def download_from_aliyun(remote_path, local_download_path, refresh_token, encrypt_password):
    """
    从阿里云下载文件或目录。
    
    参数:
    - remote_path: 远程路径，指定要下载的文件或目录在阿里云上的路径。
    - local_download_path: 本地下载路径，指定文件或目录下载到本地的路径。
    - refresh_token: 刷新令牌，用于授权访问阿里云资源。
    - encrypt_password: 加密密码，用于解密下载的文件（如果文件被加密）。
    
    返回值:
    无。函数执行成功则不返回任何内容，若执行失败则抛出异常并退出程序。
    """
    api = AliPCSApi(refresh_token)  # 初始化阿里云API对象

    try:
        # 检查远程路径是否存在
        remote_path_info = api.path(remote_path)

        if remote_path_info is None:
            raise ValueError(f"Remote path '{remote_path}' does not exist.")  # 如果远程路径不存在，则抛出异常

        # 开始下载远程路径指定的文件或目录
        download(api=api, remotepaths=[remote_path], localdir=local_download_path, file_ids=[], recursive=True, encrypt_password=encrypt_password)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        sys.exit(1) 