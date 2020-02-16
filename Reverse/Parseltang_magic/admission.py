import sys
from hashlib import md5

flag = '*****************************'

expected_result = 'lc4711082717e5235fa2a65c02c021f538bfb07a7ca984e2e96caddfe35ff072069dfad1d76777a5ed72f7dae966482f9708d72g5318c5d60e816d0a823e5de15d27ab328{c01c3af2821c6a18a079fcff85139dddcC1d4b346cf4b3a7177ce3f468836f37d8d4f4ea86fddb987cebcf08e2aeb16f4c32bN77468e7ee32cdbda5c832af9c5191981d_08993f9c08d8d3e794b45f5d65158002cu671e55bd12a35318709e582e76342aa30_2a02299c8de717c6821b6f724b3e460cfsca4f4151770517b2cb11c123af2b701b2p578b885929095ae349d00fdbc7806a8113270c4dcf49e6e0926a652924a95075e1f416f95856d2a9c3bcb41ee8f5c547fa380ke3ee2c7fa1d282c39a67923ef97766d4f_5b38aa0b54530171805bd38fe2452578apff717aa4e190c2f17a08f5c7ce9aafa144ef1d19d1b061751d4a2afa820bc53456erfea68b8c9a7d2a97f02ae4ed6b9835340Sba8d5907471fc745a49acc6ba151bc395383b17026f3a8b5a001d27820c2d0ace8bl490d9e8c388a85d8c213e83d9062c7966te148c6669d23ac6726a9698762377a02e4e9561bece4ff632efb27e520ba91aa1f3nbed037e79e35bbbe03a78ca7cee12644d92294d7c84b2df5ba9441e936b459761ab?c13759e4c37875310406b938a0a94fd9a}848'

def implementation(plaintext):
    for i in range(len(plaintext)):
        plaintext += md5(plaintext.encode('utf-8')).hexdigest()
    return plaintext


def permutation(plaintext, secret_int):
    splitted_pt = list(plaintext)
    pt_len = len(plaintext) // secret_int
    for i in range(secret_int):
        t = splitted_pt[i]
        splitted_pt[i] = splitted_pt[i * (pt_len - 1) + 1]
        splitted_pt[i * (pt_len - 1) + 1] = t
    return ''.join(splitted_pt)


def permutation(plaintext, secret_int):
    splitted_pt = list(plaintext)
    pt_len = len(plaintext) // secret_int
    for i in range(secret_int):
        t = splitted_pt[i]
        splitted_pt[i] = splitted_pt[i * (pt_len + 1) + 1]
        splitted_pt[i * (pt_len + 1) + 1] = t
    return ''.join(splitted_pt)

def encryption(plaintext):
    return permutation((implementation(plaintext)), len(plaintext))


if __name__ == "__main__":

    plaintext = input("Enter password: ")
    enc_text = encryption(plaintext)
    if enc_text == expected_result:
        print('Congratulations! Welcome to Slytherin!')
    else:
        print('A ty tochno haker?')
