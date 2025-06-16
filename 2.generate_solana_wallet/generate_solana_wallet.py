# 安装库：pip install pandas mnemonic solana bip-utils openpyxl
import datetime
import pandas as pd
from mnemonic import Mnemonic
from solders.keypair import Keypair
from solana.rpc.api import Client
from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes

# 生成钱包数量
num = int(input("请输入要生成的钱包数量："))
now_str = datetime.datetime.now().strftime("%Y%m%d")
mnemo = Mnemonic("english")
wallets = []

for i in range(num):
    # 生成助记词
    words = mnemo.generate(strength=128)
    # 通过助记词生成种子
    seed = Bip39SeedGenerator(words).Generate()
    # 通过BIP44规范生成Solana私钥
    bip44_def_ctx = Bip44.FromSeed(seed, Bip44Coins.SOLANA)
    privkey = bip44_def_ctx.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0).PrivateKey().Raw().ToHex()
    # Create Keypair from private key bytes (seed)
    kp = Keypair.from_seed(bytes.fromhex(privkey))
    # Get public key using pubkey() method
    pubkey = str(kp.pubkey())  # Updated to use pubkey()
    wallets.append({
        "index": i + 1,
        "mnemonic": words,
        "private_key": privkey,
        "public_key": pubkey
    })

# 输出到 txt 文件
with open(f"solana_wallets_{now_str}.txt", "w", encoding="utf-8") as f:
    for w in wallets:
        f.write(
            f"==============================\n"
            f"第{w['index']}个钱包: \n"
            f"助记词: {w['mnemonic']}\n"
            f"钱包地址: {w['public_key']}\n"
            f"私钥: {w['private_key']}\n"
            f"==============================\n\n"
        )

# 输出到 excel 文件
df = pd.DataFrame(wallets)
df = df.rename(columns={
    "index": "序号",
    "mnemonic": "助记词",
    "public_key": "钱包地址",
    "private_key": "私钥"
})
df.to_excel(f"solana_wallets_{now_str}.xlsx", index=False, engine="openpyxl")

print(f"已生成 {num} 个 Solana 钱包，信息已保存到 solana_wallets_{now_str}.txt 和 solana_wallets_{now_str}.xlsx")
