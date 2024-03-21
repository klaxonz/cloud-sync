import os
import logging
from alipcs_py.alipcs import AliPCSApi
from alipcs_py.commands.upload import upload, from_tos, UploadType
from alipcs_py.common.io import EncryptType
from datetime import datetime


def get_files_in_directory(directory):
    """
    获取指定目录中的所有文件路径列表。
    
    参数:
    directory (str): 需要扫描文件的目录路径。
    
    返回:
    list: 包含目录中所有文件路径的列表。
    """
    files = []
    # 使用os.scandir()高效遍历目录
    with os.scandir(directory) as entries:
        for entry in entries:
            # 筛选出文件并加入列表
            if entry.is_file():
                files.append(entry.path)
    return files


def upload_to_aliyun(local_path, remote_path, refresh_token, encrypt_password):
    """
    上传本地文件到阿里云存储。
    
    参数:
    local_path: str - 本地文件路径。
    remote_path: str - 阿里云存储的远程路径。
    refresh_token: str - 刷新令牌，用于获取访问令牌以进行API调用。
    encrypt_password: str - 文件加密密码，用于在上传时加密文件。

    返回值:
    无。函数执行成功会打印上传成功的消息，失败则抛出异常。
    """
    # 获取当前日期，用于创建日期目录
    current_date = datetime.now().date()
    formatted_date = str(current_date).replace('-', '')
    # 拼接远程路径和日期，作为文件上传的目标目录
    target_dir = os.path.join(remote_path, formatted_date)

    # 初始化阿里云API客户端
    api = AliPCSApi(refresh_token)
    # 检查目标目录是否存在
    paths = api.paths(target_dir)

    if paths and paths[0] is None:
        try:
            # 如果目标目录不存在，则尝试创建目录
            api.makedir_path(target_dir)
        except Exception as e:
            logging.error(f'Failed to create directory {target_dir}: {e}')
            raise

    # 准备上传文件列表
    _to_list = from_tos([local_path], target_dir)

    try:
        # 执行文件上传
        upload(api=api,
               from_to_list=_to_list,
               upload_type=UploadType.One,
               check_name_mode='refuse',
               encrypt_password=encrypt_password,
               encrypt_type=EncryptType.AES256CBC)
        logging.info(f'Successfully uploaded files to {target_dir}')
    except Exception as e:
        logging.error(f'Failed to upload files: {e}')
        raise

