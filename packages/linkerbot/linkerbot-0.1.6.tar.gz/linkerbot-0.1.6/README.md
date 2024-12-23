# LinkerBot Python SDK

A simple Python SDK example with two utility methods.

## Installation

```bash
pip install linkerbot-sdk
```

## Usage

```python
from linkerbot_sdk import LinkerBot
bot = LinkerBot()
# 下载数据集
print("开始下载数据集...")
result = bot.download_dataset(dataset="graspnet/objects",cache_dir="../test")
print(f"下载完成，文件保存在: {result}")
```

## Features

- Simple arithmetic operations
- Greeting message generation

## License

This project is licensed under the MIT License.
