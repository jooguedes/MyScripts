import requests, ast
from base64 import b64decode

brcode = "00020101021226860014BR.GOV.BCB.PIX2564api.rendimento.com.br/q/v2/cobv/ec40269c3e5b45409437a3faf1e360485204000053039865802BR592549833229 MATEUS FARIAS PE6012Simoes Filho61084370000062070503***63047FB9"
brcode = brcode.replace('\\', '')
dados = {}
pos = 0

while pos < len(brcode):
    chave = str(brcode[pos:pos+2])
    pos += 2
    size = str(brcode[pos:pos+2])
    pos +=2
    _size = int(size)
    data = str(brcode[pos:pos+_size])
    pos += _size
    dados[chave] = data


payload = 'None'
response = requests.get("https://"+dados['26'][22:])

if response.status_code == 200:
    payload = response.text.split('.')[1]

    for i in range(3):
        try:
            pad = ''.ljust(i,'=')
            payload = b64decode(payload+pad).decode('utf-8')
            break
        except Exception as e:
            pass

print({
    "brcode": brcode,
    "payload": ast.literal_eval(payload)
})