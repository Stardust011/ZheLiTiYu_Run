import base64
from Crypto.Hash import SHA512
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

def to_sign_with_private_key(plain_text):
  with open('rsa-prv.pem', 'r') as f:
    private_key = f.read()
  #私钥签名
  signer_pri_obj = PKCS1_v1_5.new(RSA.importKey(private_key))
  rand_hash = SHA512.new()
  rand_hash.update(plain_text.encode())
  signature = signer_pri_obj.sign(rand_hash)
  return signature
 
def to_verify_with_public_key(signature, plain_text):
  with open('rsa-pub.pem', 'r') as f:
    public_key = f.read()
  #公钥验签
  verifier = PKCS1_v1_5.new(RSA.importKey(public_key))
  _rand_hash = SHA512.new()
  _rand_hash.update(plain_text.encode())
  verify = verifier.verify(_rand_hash, signature)
 
  return verify #true / false
 
def executer_with_signature():
 
  #签名/验签
  text = "I love CA!"
  assert to_verify_with_public_key(to_sign_with_private_key(text), text)
  print("rsa Signature verified!")

if __name__ == '__main__':
  with open('gps.txt', 'r') as f:
    text = f.read()
  signature = to_sign_with_private_key(text)
  with open('updata.py.sig', 'w') as f:
    f.write(base64.b64encode(signature).decode())


  # with open('updata.py.sig', 'r') as f:
  #   signature = f.read()
  # signature = base64.b64decode(signature)
  # assert to_verify_with_public_key(signature, text)
  # print("Signature verified!")