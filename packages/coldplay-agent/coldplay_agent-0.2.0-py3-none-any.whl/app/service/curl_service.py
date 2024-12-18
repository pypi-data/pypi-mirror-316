import os
import requests

from app.service.util_service import UtilService
 
class CurlService:
    def get_token():
        coldplay_config = UtilService.load_coldplay_config()  # 加载Coldplay的配置文件
        apiserver_host = coldplay_config['DEFAULT'].get('apiserver_host')  # 从配置文件中获取API服务器的主机地址
        apiserver_user = coldplay_config['DEFAULT'].get('apiserver_user')  # 从配置文件中获取API用户名
        apiserver_pwd = coldplay_config['DEFAULT'].get('apiserver_pwd')  # 从配置文件中获取API密码
        # 登陆API URL
        url = f"{apiserver_host}/api/login"
        # 设置请求头
        headers = {
            "Content-Type": "application/json"  # 可选：如果你发送JSON数据
        }

        # 要发送的数据
        payload = {
            "username": apiserver_user,
            "password": apiserver_pwd
        }
        try:
            # 发送POST请求
            response = requests.post(url, headers=headers, json=payload)
            # 检查请求是否成功
            if response.status_code == 200:
                data = response.json()  # 解析JSON响应
                if data['code'] == 200:
                    token  = data['token']
                    return token
                else:
                    print(f"请求失败：{data['msg']}")
            else:
                print(f"请求失败，状态码：{response.status_code}, 响应内容：{response.text}")
        except requests.exceptions.RequestException as e:
            print(f"请求出现错误：{e}")
        return None
    
    def update_task_status(task_id: str, task_status: str):
        coldplay_config = UtilService.load_coldplay_config()  # 加载Coldplay的配置文件
        apiserver_host = coldplay_config['DEFAULT'].get('apiserver_host')  # 从配置文件中获取API服务器的主机地址
        # 修改状态API接口
        url = f"{apiserver_host}/api/task/update/status"
        token = CurlService.get_token()
        if token == None:
            print(f"获取token失败")
        else:
            # 设置请求头
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"  # 可选：如果你发送JSON数据
            }
            # 要发送的数据
            payload = {
                "taskId": task_id,
                "taskStatus": task_status
            }
            try:
                # 发送POST请求
                response = requests.post(url, headers=headers, json=payload)
                # 检查请求是否成功
                if response.status_code == 200:
                    data = response.json()  # 解析JSON响应
                    return data
                else:
                    print(f"请求失败，状态码：{response.status_code}, 响应内容：{response.text}")
            except requests.exceptions.RequestException as e:
                print(f"请求出现错误：{e}")
        return None
    
    def add_user_queue(queue_name: str):
        coldplay_config = UtilService.load_coldplay_config()  # 加载Coldplay的配置文件
        apiserver_host = coldplay_config['DEFAULT'].get('apiserver_host')  # 从配置文件中获取API服务器的主机地址
        # 修改状态API接口
        url = f"{apiserver_host}/api/task/queue/create"
        token = CurlService.get_token()
        if token == None:
            print(f"获取token失败")
        else:
            # 设置请求头
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"  # 可选：如果你发送JSON数据
            }
            # 要发送的数据
            payload = {
                "queueName": queue_name
            }
            try:
                # 发送POST请求
                response = requests.post(url, headers=headers, json=payload)
                # 检查请求是否成功
                if response.status_code == 200:
                    data = response.json()  # 解析JSON响应
                    return data
                else:
                    print(f"请求失败，状态码：{response.status_code}, 响应内容：{response.text}")
            except requests.exceptions.RequestException as e:
                print(f"请求出现错误：{e}")
        return None
    
    def upload_file(file_path: str):
        """
        上传本地文件到服务器
        :param file_path: 本地文件路径
        :return: 包含文件上传结果的字典或 None
        """
        coldplay_config = UtilService.load_coldplay_config()  # 加载Coldplay的配置文件
        apiserver_host = coldplay_config['DEFAULT'].get('apiserver_host')  # 从配置文件中获取API服务器的主机地址
        # 上传文件API接口
        url = f"{apiserver_host}/api/common/upload"
        token = CurlService.get_token()
        if token is None:
            print("获取token失败")
            return None

        # 设置请求头
        headers = {
            "Authorization": f"Bearer {token}"
        }

        # 检查文件是否存在
        try:
            with open(file_path, 'rb') as file:
                # 使用 requests 提供的文件上传方式
                files = {
                    "file": file
                }
                try:
                    # 发送POST请求
                    response = requests.post(url, headers=headers, files=files)
                    # 检查请求是否成功
                    if response.status_code == 200:
                        data = response.json()  # 解析JSON响应
                        if data.get("code") == 200 and data.get("success"):
                            print(f"文件上传成功: {data['url']}")
                            return data
                        else:
                            print(f"上传失败: {data.get('msg')}")
                    else:
                        print(f"请求失败，状态码：{response.status_code}, 响应内容：{response.text}")
                except requests.exceptions.RequestException as e:
                    print(f"请求出现错误：{e}")
        except FileNotFoundError:
            print(f"文件未找到：{file_path}")
        return None
    
    def upload_urdf(task_id: str, urdf_file_uri: str, file_path: str):
        """
        上传文件并请求 /api/task/urdf/up 接口，添加URDF文件信息
        :param task_id: 任务ID
        :param file_path: 本地文件路径
        :return: 包含接口调用结果的字典或 None
        """
        if not os.path.exists(file_path):
            print(f"文件路径无效或文件不存在：{file_path}")
            return None
        coldplay_config = UtilService.load_coldplay_config()  # 加载Coldplay的配置文件
        apiserver_host = coldplay_config['DEFAULT'].get('apiserver_host')  # 从配置文件中获取API服务器的主机地址
        upload_url = f"{apiserver_host}/api/common/upload"  # 文件上传接口
        urdf_up_url = f"{apiserver_host}/api/task/urdf/up"  # URDF提交接口

        token = CurlService.get_token()
        if token is None:
            print("获取token失败")
            return None

        # 设置请求头
        headers = {
            "Authorization": f"Bearer {token}"
        }

        # 上传文件
        try:
            with open(file_path, 'rb') as file:
                file_name = os.path.basename(file_path)
                files = [('file', (file_name, open(file_path, 'rb'), 'application/octet-stream'))]
                upload_response = requests.post(upload_url, headers=headers, files=files)

                if upload_response.status_code == 200:
                    upload_data = upload_response.json()
                    if upload_data.get("code") == 200 and upload_data.get("success"):
                        print(f"文件上传成功: {upload_data.get('url')}")
                        urdf_file_name = upload_data.get("originalFilename")
                        urdf_save_file_uri = upload_data.get("fileName")
                    else:
                        print(f"文件上传失败: {upload_data.get('msg')}")
                        return None
                else:
                    print(f"文件上传请求失败，状态码：{upload_response.status_code}, 响应内容：{upload_response.text}")
                    return None
        except FileNotFoundError:
            print(f"文件未找到：{file_path}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"文件上传出现错误：{e}")
            return None

        # 提交 URDF 文件信息
        payload = {
            "taskId": task_id,
            "urdfFileName": urdf_file_name,
            "urdfFileUri": urdf_file_uri,
            "urdfSaveFileUri": urdf_save_file_uri
        }
        headers["Content-Type"] = "application/json"

        try:
            urdf_response = requests.post(urdf_up_url, headers=headers, json=payload)
            if urdf_response.status_code == 200:
                urdf_data = urdf_response.json()
                if urdf_data.get("code") == 200 and urdf_data.get("success"):
                    print(f"URDF文件上传成功: {urdf_data.get('msg')}")
                    return urdf_data
                else:
                    print(f"URDF文件上传失败: {urdf_data.get('msg')}")
            else:
                print(f"URDF提交请求失败，状态码：{urdf_response.status_code}, 响应内容：{urdf_response.text}")
        except requests.exceptions.RequestException as e:
            print(f"URDF提交出现错误：{e}")

        return None
    
    def upload_hp(task_id: str, hp_file_uri: str, file_path: str):
        """
        上传文件并请求 /api/task/hp/up 接口，添加任务超参数文件信息
        :param task_id: 任务ID
        :param file_path: 本地文件路径
        :return: 包含接口调用结果的字典或 None
        """
        if not os.path.exists(file_path):
            print(f"文件路径无效或文件不存在：{file_path}")
            return None
        coldplay_config = UtilService.load_coldplay_config()  # 加载Coldplay的配置文件
        apiserver_host = coldplay_config['DEFAULT'].get('apiserver_host')  # 从配置文件中获取API服务器的主机地址
        upload_url = f"{apiserver_host}/api/common/upload"  # 文件上传接口
        hp_up_url = f"{apiserver_host}/api/task/hp/up"  # 超参数文件提交接口

        token = CurlService.get_token()
        if token is None:
            print("获取token失败")
            return None

        # 设置请求头
        headers = {
            "Authorization": f"Bearer {token}"
        }

        # 上传文件
        try:
            with open(file_path, 'rb') as file:
                file_name = os.path.basename(file_path)
                files = [('file', (file_name, open(file_path, 'rb'), 'application/octet-stream'))]
                upload_response = requests.post(upload_url, headers=headers, files=files)

                if upload_response.status_code == 200:
                    upload_data = upload_response.json()
                    if upload_data.get("code") == 200 and upload_data.get("success"):
                        print(f"文件上传成功: {upload_data.get('url')}")
                        hp_file_name = upload_data.get("originalFilename")
                        hp_save_file_uri = upload_data.get("fileName")
                    else:
                        print(f"文件上传失败: {upload_data.get('msg')}")
                        return None
                else:
                    print(f"文件上传请求失败，状态码：{upload_response.status_code}, 响应内容：{upload_response.text}")
                    return None
        except FileNotFoundError:
            print(f"文件未找到：{file_path}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"文件上传出现错误：{e}")
            return None

        # 提交 HP 文件信息
        payload = {
            "taskId": task_id,
            "hpFileName": hp_file_name,
            "hpFileUri": hp_file_uri,
            "hpSaveFileUri": hp_save_file_uri
        }
        headers["Content-Type"] = "application/json"

        try:
            hp_response = requests.post(hp_up_url, headers=headers, json=payload)
            if hp_response.status_code == 200:
                hp_data = hp_response.json()
                if hp_data.get("code") == 200 and hp_data.get("success"):
                    print(f"HP文件上传成功: {hp_data.get('msg')}")
                    return hp_data
                else:
                    print(f"HP文件上传失败: {hp_data.get('msg')}")
            else:
                print(f"HP提交请求失败，状态码：{hp_response.status_code}, 响应内容：{hp_response.text}")
        except requests.exceptions.RequestException as e:
            print(f"HP提交出现错误：{e}")

        return None