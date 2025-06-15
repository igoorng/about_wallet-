import os
import sys
from eth_account import Account
from mnemonic import Mnemonic
from openpyxl import Workbook
import datetime


# 获取命令行参数，指定生成数量，默认为1
now_str = datetime.datetime.now().strftime("%Y%m%d")

# 设置 需要生成的钱包数量
num = 
if len(sys.argv) > 1:
    try:
        num = int(sys.argv[1])
    except ValueError:
        print("参数错误，使用默认数量1")

mnemo = Mnemonic("english")

Account.enable_unaudited_hdwallet_features()

# 创建Excel工作簿和表头
wb = Workbook()
ws = wb.active
ws.title = "ETH Wallets"
ws.append(["序号", "助记词", "钱包地址", "私钥"])

for i in range(num):
    mnemonic_words = mnemo.generate(strength=128)
    seed = mnemo.to_seed(mnemonic_words)
    acct = Account.from_mnemonic(mnemonic_words)
    print(f"第{i+1}个钱包:")
    print("助记词:", mnemonic_words)
    print("钱包地址:", acct.address)
    print("私钥:", acct.key.hex())
    print("-"*30)
    ws.append([i+1, mnemonic_words, acct.address, "0x" + acct.key.hex()])
    # 将私钥追加写入 private_keys.txt
    with open(f"eth_private_keys_{now_str}.txt", "a", encoding="utf-8") as pkf:
        pkf.write(
            f"==============================\n"
            f"第{i+1}个钱包: \n"
            f"助记词: {mnemonic_words}\n"
            f"钱包地址: {acct.address}\n"
            f"私钥: 0x{acct.key.hex()}\n"
            f"==============================\n\n"
        )

# 保存Excel文件
excel_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"eth_wallets_{now_str}.xlsx")
wb.save(excel_path)
print(f"所有钱包信息已保存到: {excel_path}")
