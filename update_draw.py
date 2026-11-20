import requests
import json
import re

def get_ssq():
    url = "https://www.cwl.gov.cn/cwl_admin/front/cwlkj/search/kjxx/findDrawNotice?name=ssq&issueCount=10"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    res = requests.get(url, headers=headers, timeout=15)
    res.raise_for_status()
    data = res.json()
    return data["result"]

def inject_data(html_path, draw_list):
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    # 把开奖数据写入JS里的drawHistory
    js_data = json.dumps(draw_list, ensure_ascii=False)
    new_html = re.sub(r'const drawHistory = \[.*?\];', f'const drawHistory = {js_data};', html, flags=re.S)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(new_html)

if __name__ == "__main__":
    draw = get_ssq()
    inject_data("index.html", draw)
    print("✅ 开奖数据已更新到index.html")
