# 安装库：pip install pandas mnemonic  bip-utils
import datetime
import pandas as pd
from mnemonic import Mnemonic
from bip_utils import Bip39SeedGenerator, Bip44Coins, Bip44, base58, Bip44Changes

# 生成钱包数量
create_amount = int(input("请输入要生成的钱包数量："))
now_str = datetime.datetime.now().strftime("%Y%m%d")
mnemo = Mnemonic("english")
wallets = []

for i in range(create_amount):
    # 生成助记词
    words = mnemo.generate(strength=128)
    # words = "scatter embody steak chase spin law era danger brass execute tone toward"
    # 由助记词生成种子
    seed_bytes = Bip39SeedGenerator(words).Generate() 
    # 生成BIP44主路径上下文
    bip44_mst_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.SOLANA)
    # 生成 Solana 钱包
    bip44_acc_ctx = bip44_mst_ctx.Purpose().Coin().Account(i)
    bip44_chg_ctx = bip44_acc_ctx.Change(Bip44Changes.CHAIN_EXT)
    # 获取私钥字节
    priv_key_bytes = bip44_chg_ctx.PrivateKey().Raw().ToBytes()
    # 获取压缩公钥（去掉前缀）
    pub_key_bytes = bip44_chg_ctx.PublicKey().RawCompressed().ToBytes()[1:]
    # 拼接私钥和公钥
    key_pair = priv_key_bytes + pub_key_bytes
    # 生成 Solana 钱包地址      
    sol_addr = bip44_chg_ctx.PublicKey().ToAddress()  
    # 生成 Solana 钱包私钥
    private_key = base58.Base58Encoder.Encode(key_pair)

    wallets.append({
        "index": i + 1,
        "mnemonic": words,
        "address": sol_addr,
        "private_key": private_key,
    })

# 输出到 txt 文件
with open(f"solana_wallets_{now_str}.txt", "w", encoding="utf-8") as f:
    for w in wallets:
        f.write(
            f"==============================\n"
            f"第{w['index']}个钱包: \n"
            f"助记词: {w['mnemonic']}\n"
            f"钱包地址: {w['address']}\n"
            f"私钥: {w['private_key']}\n"
            f"==============================\n\n"
        )

# 输出到 excel 文件
df = pd.DataFrame(wallets)
df = df.rename(columns={
    "index": "序号",
    "mnemonic": "助记词",
    "address": "钱包地址",
    "private_key": "私钥"
})
df.to_excel(f"solana_wallets_{now_str}.xlsx", index=False, engine="openpyxl")

print(f"已生成 {create_amount} 个 Solana 钱包，信息已保存到 solana_wallets_{now_str}.txt 和 solana_wallets_{now_str}.xlsx")
