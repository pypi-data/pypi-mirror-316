import base64,datetime


message = {
    "inputMessage_20241216" :'''gHgAsclUVPhWDv4S8Oa8SuRTDaj+V0dI4z2jrQwfvfSFWilWwMKwNULUI48UBLS2shZcm/yv2/e5Hq5VRDfXkdxCYQMdvdnvONtpm2yNiIaLpDV4Rs8fOXJ6kcaeT+mg4RkIIFgx35w4J1KgO72pSP8j1p+R9f9TNMafwJ91XmO4QTcOYkMKQMddKvhbyMXzJkSS0uZqEppNSIUnVX9b7m8PmMjV0uHShvb1Zc8UQWJWUJ3cOxwNasOeMQGxJrZXPkxIxDYzm3f0tXbCgvdgNZ8TQY7u+iCXjOtD6xnUsdSahnPq14BD30CilIfsG0r/klPHfxQ+psmHSX47Ylai0TtgfbHWJJ4lSo0ojMvTx6HYK8zmAoCmg4OGXDbv/IjJgYU1w24na0iXZCNtcjB9MLRNck00c20f/uS64Ss0Ixii8nmfsFOjQBCcIYN+HGmOnj5Uw8DVJrxlOmcfQciG3rzuIvYlbOdGMcyarTy2Ba7iZfoovYZObPscAwhNLWqbU4tuR78aOVxiXTFRY7+Y0x2eRT5sulcvB3vsKuDMlNrxaUgiFUohPBZGNsgQgyCPxxqk0NpUn0bbHLH+vBebjJxaim4AU28ctWW8xv7xpxVttb0EoohtK2cIHr79ep5XrU/rv4R58obD/o+QqI1Mrb4wwpX9tsL7ZbROw/MXJwM=''',
    "inputMessage_20240411" : '''Z93Khatj+AWZcpPwIqu8LzbJ8xb8CuVMI8okE0qwoQD2IC2lixg77mJZireOrbW7zFkDsk1hP67dROJZwVUDrYot2g5GxX/xy7lGjIblUX4iJVUtP4mHqZUgKROaLoh/gippMpP+8Ik2X/QRBx5gdhq0xam+wuVC+77/tyu8Fd/DohKbAMp8aaJsFr/W4mLDZ1gv4JK+2O3l+bAvpodBRTzb0ld5zD2ueYvjTudoDjdanQP1oVTH7pkDO2Vb+SsdIyTi2C410JEOF4Qm8mzVHtiOunOcLVpAlQsM6/LdhqsTNelXl/Myb84NGxwGWVmx6j2QejiL7S1hHeHlmQ9ExHeURPdZAvKhgMCemYXu3BGlFq3ydb5SkqwLFvM4vJ6XUBcWkHT8eijBFF6Y7YgOv9GRvBTnsAQhUBp4W4EAMtXkDdToG+S8ZO7El8Gh8jaWC49n5CuUBRz3z2GeOVbsBamfLV06IO5v78jGHXig4saEFKHvYSIGewyUCVQEGoIR5xOTJBTUTePAdvQjfg28vZZxFB/hIYNDUHkaek1Mg1UH5HWGgsCX1In5hSX/9eBkznEhzeWnJ1yMsYkj+ddN34DLQSrHc83geXMcoW3Ah3cAQG8E8bszvKL3hme+T5rOeENjkOAgYhf84k4YlxDskdwvzyu8HkE9CSaBpDP6lKI=''',
    "inputMessage_20240305" : '''ckDSthpl5DDJMpBE26Jqk8EjaSq7MUntdwLHPouwx6D38un6WQfLJ9wgDyjh9GA/ICJR7WrwWsVinr6y3u9w+ubMZ0mqmtnphzQraagk8NkKc1u1+qGp8llsud3C8mvJWa4GYa9KEhnACDHwppPKJDCfr1HKwPbR0NIi+1Aunmy6DeOKRkFwysnrSco5QiiC9+gdXFhQDmN9KEiYW6Pc3mWVbqFiJgRW3/Df6638oGPm6AUcgRnEWMKiluyN81frM9VNtCeJ64YrU6Rgx4D153YxNNQbLTcyCQMamHTrJnhxPojkuDqbEcU+iiN4offwrQyr4eEu9ecvmyD2w/n7pAOsVnqSzroBujVA+CK6Zq8Uie15mL5yWG9hD5ZcbSwnRmtqK3yl0Xl91hgn1JqcIEKtf+MnMQPr80uoxT3mz8IX8pyVnyyw1x6F+IK1I2G+5w6rUDjhzIbME5XB9hopwcswsXrMo9PP6/5Sz1noJrsu6k6WN8ZM0MyRIav+xuKP1+cYzlPSQZrMo3L4ieHQnBbsoyzGVf9QONMwaooGOrxu88ZWlGe8e7eyCzteeNSVOC2zqtQiwQJIgfp2UwTymA/cEjOICWVzUXwbE5wWUBPCLp2C/XWc82byrOHAFXHLOVKgolVToUpZ5uOvizgk/ahaxdGxGa9CrRyr6sf+goA=''',

}



def printMessage():
    for key, value in message.items():
        title = key.replace('inputMessage_', '')
        print("\033[1;31m" + "请使用组织分配的私钥解密后使用" + "\033[0m")
        title = datetime.datetime.strptime(title, '%Y%m%d').strftime('%Y-%m-%d')
        print("----------------------------------------------------------")
        print(title)
        print(value)
        print("----------------------------------------------------------")
        print("\n")


# 最新流通公钥
def getPublicKey():
    return b'''
    -----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAmziayo9Tddo1FYdrtOsw
yjLYJ5frYKEwm4rQTsKU8UcdnnDRgms+ZmStoqlH/qi6x+D1K3fvvioCnGZLFHZw
BUqbgT5x+qUmUaVMll9FOT7ZJ05w8n8Ljqa1akzFMU5G7YbCr3vQwN63vwvD9/63
TDbXkJrv1fGl2rHpPwp5OPCUeCB3nIFIRCWHpJU7sHJqIP5vzV8KNJtbxgR+dhsz
dg+NhoBDUpxoVN5lzSKr2TMOLFLZaQR9AWOV/aHV8gjTkTLDZfc+XlfhxiDMTQdi
UTbk/tynpt+JFrDA8vL5/TOmuxgumqgXZIPGrIUbwloTYyHD/XXmvXu5KE8g3eMK
gxNxuEKM5bMTESBK9A7Q2Kj3eNp0Rvb5Aleg7h8/YbQemGelY/o5xpUyHgHjsfNQ
3j/xhdhVCNVaXZF64V/YVpvC9Cq29F7qI+bl6FlN7zSpuHB3QgNS1uXOmjBCsA7y
pZoWmdXeaLIO+I3kP48BBSmue4nidJifiK/kSOcZ0iegRXV1hyZ6pYdDE7hM5V5t
5tvayJ31zRQNT2ALAFeCDozVWELHTnphkPkQO+SOPglrVz0S1dXicqRofXWMj7PJ
OFkBpWIX0aywMIh1woEAawUs3RM2pfLUNtqUTfodSCmWlwcpGrBWG5NACx7csPFt
zWn8oPZfzL346at5DDIwD2kCAwEAAQ==
-----END PUBLIC KEY-----
'''

def enctryptMessage(message):
    import base64
    message_bytes = message.encode('utf-8')  
    message_base64 = base64.b64encode(message_bytes).decode('utf-8')
    publicKey = getPublicKey()
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import padding
    from cryptography.hazmat.primitives import hashes
    public_key = serialization.load_pem_public_key(publicKey, backend=default_backend())
    encrypted = public_key.encrypt(
        message_base64.encode('utf-8'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    encrypted_base64 = base64.b64encode(encrypted).decode('utf-8')
    return encrypted_base64


printMessage()