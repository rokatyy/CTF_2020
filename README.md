# CTF_2020

* [Stegano](https://github.com/rokatyy/CTF_2020/tree/master/Stegano) 
* [Crypto](https://github.com/rokatyy/CTF_2020/tree/master/Crypto) 
* [Osint](https://github.com/rokatyy/CTF_2020/tree/master/Osint)
* [Reverse](https://github.com/rokatyy/CTF_2020/tree/master/Reverse)
 

## Authors

* **Katerina Rogatova** - [Github](https://github.com/rokatyy)

* **Anna Korshikova** - [Github](https://github.com/annkooo)

* **Alexander Krikun** - [Github](https://github.com/krikun98)

## Writeups

### OSINT
#### pictures:
    General help: all "pictures" tasks have an md5 hash 
    of one capitalized english word for an answer.
    
#### building:
    Introductory task: image search, see that this is the 
    National Library of Kazakhstan, and opposite it is
    Bayterek Monument. Flag is md5(Bayterek) 
    
#### cemetery:
    A bit harder: image search doesn't do much, so we hope the user 
    sees the green sign. Under it is faint writing, and googling
    "Cemetery Campo do Bom" gives the city. Flag is md5(Uberlandia)
    
#### taxi:
    More fun: image search flops completely, but reproducing the Chinese
    characters in Google Translate and googling "的土 taxi" gives 
    Hong Kong. "Hong Kong park many people" finds "Kowloon Walled City". 
    Flag is md5(Kowloon)

### Stegano
#### LENIVETS

[Lenivets](https://github.com/rokatyy/CTF_2020/tree/master/Stegano/Lenivets)


  You have a file - lenivets.jpg which has zip archive in the end of raw data. It could be seen with any hex-editor or any       automated tools like binwalk, scalpel and etc.

  ```
  ~CTF_2020/Stegano/task1 @ mac(rokatyy): binwalk -e lenivets.jpg 

  DECIMAL       HEXADECIMAL     DESCRIPTION
  --------------------------------------------------------------------------------
  0             0x0             JPEG image data, JFIF standard 1.01
  56355         0xDC23          End of Zip archive, footer length: 22
  ```

   Zip header starts with: ```0x50 0x4B``` (or PK)
  ```
  ~CTF_2020/Stegano/task1 @ mac(rokatyy): unzip hidden_archive.zip 
Archive:  hidden_archive.zip
 extracting: secret     
 ```
 In file we can see data that looks like base64, so just decode and get flag. Enjoy :)
 
```
~CTF_2020/Stegano/task1 @ mac(rokatyy): cat secret | base64 -D
Sup3r_eas4_FL4G111
```


#### Satan:
    The video is all about hiding images in spectrograms, and, as it happens,
    the flag is hidden in the audio. Extract the audio, analyze the spectrogram,
    get the F6L6A6G.

#### RAW

#### TRYOSHKA

There are three parts of flag in the task.
First part is hidden into `lol.jpg` metadata (comment):
```~/develop/python/CTF_2020/Stegano/tryoshka @ mac(rokatyy): exiftool lol.jpg 
ExifTool Version Number         : 11.70
File Name                       : lol.jpg
Directory                       : .
File Size                       : 54 kB
File Modification Date/Time     : 2020:03:17 16:18:21+03:00
File Access Date/Time           : 2020:03:18 18:38:05+03:00
File Inode Change Date/Time     : 2020:03:18 16:35:40+03:00
File Permissions                : rw-r--r--
File Type                       : JPEG
File Type Extension             : jpg
MIME Type                       : image/jpeg
JFIF Version                    : 1.01
Resolution Unit                 : inches
X Resolution                    : 72
Y Resolution                    : 72
Comment                         : ZmxhZ3tBX2wxdHRsM19CSVQK
Image Width                     : 544
Image Height                    : 483
Encoding Process                : Baseline DCT, Huffman coding
Bits Per Sample                 : 8
Color Components                : 3
Y Cb Cr Sub Sampling            : YCbCr4:2:0 (2 2)
Image Size                      : 544x483
```
Lets encode it from base64:
```
~/develop/python/CTF_2020/Stegano/tryoshka @ mac(rokatyy): echo 'ZmxhZ3tBX2wxdHRsM19CSVQK' | base64 --decode
flag{A_l1ttl3_BIT
```
Okey so, we have first part.
Now take a look into raw data (I recommend to use [010Editor](https://www.sweetscape.com/download/010editor/))
We can see `PK` header after `jpg` data. It could be extracted manually or with `binwalk` utility:
```
~/develop/python/CTF_2020/Stegano/tryoshka @ mac(rokatyy): binwalk -e lol.jpg 

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             JPEG image data, JFIF standard 1.01
55491         0xD8C3          Zip archive data, encrypted at least v1.0 to extract, compressed size: 24, uncompressed size: 12, name: second_part.txt
55689         0xD989          End of Zip archive, footer length: 22

```
Here we see zip archive. It has password. We can try the first part of the flag, and it right!
```
~/develop/python/CTF_2020/Stegano/tryoshka/_lol.jpg.extracted @ mac(rokatyy): ls
D8C3.zip
~/develop/python/CTF_2020/Stegano/tryoshka/_lol.jpg.extracted @ mac(rokatyy): unzip D8C3.zip 
Archive:  D8C3.zip
[D8C3.zip] second_part.txt password: 
 extracting: second_part.txt         
~/develop/python/CTF_2020/Stegano/tryoshka/_lol.jpg.extracted @ mac(rokatyy): cat second_part.txt 
_H4rD3r_BU7
```
So, we have the second part. And we can return to raw data view and see that in the end of all data third part of the flag:
`_ST111_f7n}`

And full flag: `flag{A_l1ttl3_BIT_H4rD3r_BU7_ST111_f7n}`

### CRYPTO
#### blaise:
    Vigenère cipher, key 'classic'.
    
#### cyrilic:
    Select all letters 'a' and find the answer.

#### easy_peasy:
    Caesar cipher. For decode use ROT11.
    
#### history:
    It's Cardan grille with holes in place '1'.
    
### Reverse
#### task1:

[Parseltang_magic](https://github.com/rokatyy/CTF_2020/tree/master/Reverse/Parseltang_magic)
You need to reverse python application and find a flag.
It's easy to find flag len(it was hardcoded) and then write method which revert changes firstly permutation and implementation then.

#### task2:
[checker](https://github.com/rokatyy/CTF_2020/tree/master/Reverse/checker)

You can find origin c++ code here: [code](https://github.com/rokatyy/CTF_2020/blob/master/Reverse/checker/easy_checker.cpp).
There are some ways to solve:
1. Easy strings:
  ```
~/ @ mac(rokatyy): strings checker 
Enter password:
Nope.
lfgar{g1thP_54}5
You are true hacker!
flag is: 
Nooooope.
  ```
  
  The most interesting string for us here is ```lfgar{g1thP_54}5```
  After some manipulations we can see that ```[2*i]``` elements placed to ```[2*i+1]``` and vice versa.
