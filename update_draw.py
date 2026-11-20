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
    js_data = ",\n".join([f'    {json.dumps(x, ensure_ascii=False)}' for x in draw_list])
    # 替换两个标记中间的内容
    pattern = r'// === DRAW_DATA_START ===\n.*?\n// === DRAW_DATA_END ==='
    new_block = f'// === DRAW_DATA_START ===\n{js_data}\n// === DRAW_DATA_END ==='
    new_html = re.sub(pattern, new_block, html, flags=re.S)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(new_html)

if __name__ == "__main__":
    draw = get_ssq()
    inject_data("index.html", draw)
    print("✅ 开奖数据更新成功")
