import os
import time

import requests
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("MINERU_TOKEN")

def upload_pdf():


    url = "https://mineru.net/api/v4/file-urls/batch" # 访问端点/接口地址，注意这个地址是固定的
    header = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    data = {
        "files": [
            {"name": "demo.pdf", "data_id": "abcd"}
        ],
        "model_version": "vlm"
    }


    file_path = ["./assets/sample.pdf"]

    try:

        # 接口目的：连接MinerU服务器，获取一个签名地址
        # 调用远程接口的几个要素
        # 远程接口的地址：接口地址
        # 请求参数：可以转成json的字典数据，必须包含files和model_version两个键
        # 请求头：包含Content-Type和Authorization两个键，其中Authorization是身份认证的凭证
        # 响应结果：response 已签名url（经过授权的url），利用这个地址进行文件上传
        # 请求方式：get
        response = requests.post(url, headers=header, json=data)

        # 响应码200表示响应成功
        if response.status_code == 200:
            result = response.json()
            print('response success. result:{}'.format(result))

            if result["code"] == 0:

                # 从响应结果中解析出当前任务的任务id
                batch_id = result["data"]["batch_id"]
                # 从响应结果中解析出已签名的url
                urls = result["data"]["file_urls"]
                print('batch_id:{},urls:{}'.format(batch_id, urls))
                for i in range(0, len(urls)):

                    with open(file_path[i], 'rb') as f:

                        # 将本地文件上传，上传api的接口地址是 urls[i]
                        res_upload = requests.put(urls[i], data=f)

                        if res_upload.status_code == 200:
                            print(f"{urls[i]} upload success")
                        else:
                            print(f"{urls[i]} upload failed")

                return batch_id

            else:
                print('apply upload url failed,reason:{}'.format(result["msg"]))
        else:
            print('response not success. status:{} ,result:{}'.format(response.status_code, response))
    except Exception as err:
        print(err)


def download_zip(batch_id):


    url = f"https://mineru.net/api/v4/extract-results/batch/{batch_id}"
    header = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    res = requests.get(url, headers=header)
    print(res.status_code)
    print(res.json())
    print(res.json()["data"])


    # 轮询pdf解析的状态
    while res.json()['data']['extract_result'][0]['state'] != 'done':
        time.sleep(0.5)
        res = requests.get(url, headers=header)

    return res.json()['data']['extract_result'][0]['full_zip_url']

if __name__ == '__main__':

    batch_id = upload_pdf()
    res = download_zip(batch_id)
    print(res)


