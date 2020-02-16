import sys
from hashlib import md5

flag = '*****************************'

expected_result = 'l867df48c73779d9358f5bb836ebd1f53fbcb07a7ca984e2e96caddfe35ff0720a9df4d1d76777a5ed72f7dae966482f9g08d7275318c5d60e816d0a823e5de15{27ab3281c01c3af2821c6a18a079fcfC85139dddc11d4b346cf4b3a7177ce3f468836f37d8d0f4ea86fddb987cebcf0Ne2aeb16f4c32b877468e7ee32cdbda5_832af9c5191981d208993f9c08d8d3eu94b45f5d65158002c7671e55bd12a35_18709e582e76342aa3012a02299c8des17c6821b6f724b3e460cf7ca4f41517p0517b2cb11c123af2b701b2e578b885329095ae349d00fdbc7806a8115270c44cf49e6e0926a652924a95075e1f216fk5856d2a9c3bcb41ee8f5c547fa3803e_ee2c7fa1d282c39a67923ef97766d4fp5b38aa0b54530171805bd38fe2452574afff717aa4e190c2f17a08f5c7ce9aara14aef1d19d1b061751d4a2afa820bcS3456e2fea68b8c9a7d2a97f02ae4ed639835340aba8d5907471fc745a49acc6la151bc395683b17026f3a8b5a001d27t20c2d0ace8b5490d9e8c388a85d8c214e83d9062c7966ce148c6669d23ac672na9698762377a02e0e9561bece4ff6329fb27e520ba91aa1f32bed037e79e35b?be03a78ca7cee12644dc2294d7c84b2}f5ba9441e936b459761ab0c13759e4c37875310406b938a0a94fd9a2848'


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


def encryption(plaintext):
    return permutation((implementation(plaintext)), len(plaintext))


if __name__ == "__main__":

    plaintext = input("Enter password: ")
    enc_text = encryption(plaintext)
    if enc_text == expected_result:
        print('Congratulations! Welcome to Slytherin!')
    else:
        print('A ty tochno haker?')
