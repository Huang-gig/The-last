import requests
import json
import re

def get_ssq():
    # 通过你的Cloudflare Worker代理中转
    proxy_url = "https://lottery-proxy.1106293639.workers.dev?target=https://www.cwl.gov.cn/cwl_admin/front/cwlkj/search/kjxx/findDrawNotice?name=ssq&issueCount=10"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    res = requests.get(proxy_url, headers=headers, timeout=20)
    res.raise_for_status()
    data = res.json()
    arr = []
    for item in data["result"]:
        red = list(map(int, item["red"].split(",")))
        blue = int(item["blue"])
        arr.append({
            "code": item["code"],
            "date": item["date"],
            "red": red,
            "blue": blue
        })
    return arr

def inject_data(html_path, draw_list):
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    js_lines = []
    for x in draw_list:
        js_lines.append(f'    {json.dumps(x, ensure_ascii=False)}')
    content = ",\n".join(js_lines)
    pattern = r'// === DRAW_DATA_START ===\n.*?\n// === DRAW_DATA_END ==='
    new_block = f'// === DRAW_DATA_START ===\n{content}\n// === DRAW_DATA_END ==='
    new_html = re.sub(pattern, new_block, html, flags=re.S)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(new_html)

if __name__ == "__main__":
    draw_data = get_ssq()
    inject_data("index.html", draw_data)
    print("✅ 开奖数据更新完成")
