import requests
from XMZAPI.headers import CustomRequestHeaders

class sql:
    def __init__(self):
        # 初始化sql类，创建一个CustomRequestHeaders实例
        self.headers = CustomRequestHeaders()

    def get_response(self, data):
        """
        发送包含uuid、question和answer的POST请求到指定URL。

        参数:
        data (dict): 包含traceid、continent、country、zipcode、owner、isp、adcode、prov、city、district和ip的字典。

        返回:
        None
        """
        trace_id = data.get("traceid")
        continent = data.get("continent")
        country = data.get("country")
        zipcode = data.get("zipcode")
        owner = data.get("owner")
        isp = data.get("isp")
        adcode = data.get("adcode")
        prov = data.get("prov")
        city = data.get("city")
        district = data.get("district")
        ip = data.get("ip")
        url = "https://hwapi.mizhoubaobei.top/ipsql"
        headers = self.headers.reset_headers()
        body = {
            "trace_id": trace_id,
            "continent": continent,
            "country": country,
            "zipcode": zipcode,
            "owner": owner,
            "isp": isp,
            "adcode": adcode,
            "prov": prov,
            "city": city,
            "district": district,
            "ip": ip,
        }

        response = requests.post(url, headers=headers, json=body)

        # 检查响应状态码和内容
        if response.status_code == 200:
            print(f"Request successful: {response.json()}")
        else:
            print(f"Request failed with status code {response.status_code}: {response.text}")
