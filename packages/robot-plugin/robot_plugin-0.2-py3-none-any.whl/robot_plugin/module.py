import requests

base_url = "http://127.0.0.1:3000"


def sendText(msg, receiver, aters=None):
    data = {
        "msg": msg,
        "receiver": receiver,
        "aters": aters
    }
    return send_post_request(base_url + '/robot/sendText', json_data=data)


def send_get_request(url, params=None):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # 如果响应状态码不是 200，将引发 HTTPError 异常
        return response.json()  # 返回 JSON 响应内容
    except requests.RequestException as e:
        print(f"请求错误: {e}")
        return None


def send_post_request(url, json_data=None):
    try:
        response = requests.post(url, json=json_data)
        response.raise_for_status()  # 如果响应状态码不是 200，将引发 HTTPError 异常
        return response.json()  # 返回 JSON 响应内容
    except requests.RequestException as e:
        print(f"请求错误: {e}")
        return None
