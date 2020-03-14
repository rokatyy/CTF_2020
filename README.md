# CTF_2020

* [Stegano](https://github.com/rokatyy/CTF_2020/tree/master/Stegano) 
* [Crypto](https://github.com/rokatyy/CTF_2020/tree/master/Crypto) 
* [Osint](https://github.com/rokatyy/CTF_2020/tree/master/Osint)
* [Reverse](https://github.com/rokatyy/CTF_2020/tree/master/Reverse)
 

## Authors

* **Katerina Rogatova** - [Github](https://github.com/rokatyy)

* **Anna Korshikova** - [Github](https://github.com/annkooo)

## Writeups

### Stegano
#### task1:

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
