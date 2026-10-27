from openai import OpenAI
import json
import config_data as config

client = OpenAI(
    api_key=config.api_key,
    base_url="https://ws-fybpg29h6nlemy6l.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
schemA = ["日期", "股票名称", "开盘价", "收盘价", "成交量"]
examples_data=[
    {
      "content": "2023-01-10，股市震荡。股票强大科技A股今日开盘价100人民币，一度飙升至105人民币，随后回落至98人民币，最终以102人民币收盘，成交量达到520000。",
      "answers": {
        "日期": "2023-01-10",
        "股票名称": "强大科技A股",
        "开盘价": "100人民币",
        "收盘价": "102人民币",
        "成交量": "520000"
      }
    },
    {
      "content": "2024-05-16，股市利好。股票英伟达美股今日开盘价105美元，一度飙升至109美元，随后回落至100美元，最终以116美元收盘，成交量达到3560000。",
      "answers": {
        "日期": "2024-05-16",
        "股票名称": "英伟达美股",
        "开盘价": "105美元",
        "收盘价": "116美元",
        "成交量": "3560000"
      }
    }
  ]
questions = [
    "2025-06-16，股市利好。股票传智教育A股今日开盘价66人民币，一度飙升至70人民币，随后回落至65人民币，最终以68人民币收盘，成交量达到123000。",
    "2025-06-06，股市利好。股票黑马程序员A股今日开盘价200人民币，一度飙升至211人民币，随后回落至201人民币，最终以206人民币收盘。"
  ]

messages = [{"role":"system","content":f"你是一个金融分析师，需要根据json数据提取下面的信息：{schemA},以下是示例"}]

for e in examples_data:
       messages.append({"role":"user","content":e["content"]})
       messages.append({"role":"assistant","content":json.dumps(e["answers"],ensure_ascii=False)})

for q in questions:
    response = client.chat.completions.create(
        model="qwen3.8-max",
        messages = messages + [{"role": "user","content":f"回答这个数据{q}"}]
    )
    print(response.choices[0].message.content)

