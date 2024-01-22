# efsbk

"Do you know how Encrypted File System works?" Challenge.

This ["Random Indian Guy on YouTube"](https://www.youtube.com/playlist?list=PLmW31MWCFahVkyC58bNG0ipJkovjPk-kC) really helped me to understand how EFS works.

## Extract EFEK

First we need to divide encrypted file data and EFEK. We can bruteforce the
boundary of two file using parser.

EFEK is pfx file and we can extract private key. Password is `SECCON CTF 2023 Finals`

`bash
openssl pkcs12 -in extracted.pfx -nocerts -out drlive.key
openssl rsa -in drlive.key -out priv.key
`

## Get File Decryption Key

We can get Encrypt/Decrypt key by decrypting the encrypted key. Also we can know
that the file was encrypted with AES by looking 0x6610 in the data.

## Decrypt File

We can get original data by decrypting with AES CBC. However, we need to decrypt
512 byte at a time and different IV on each block.

See this [link](https://diyinfosec.medium.com/symmetric-key-usage-in-efs-81924bee27ab) for more information.
