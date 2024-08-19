# Cryptography

## Resources

### Books

- [Awesome Cryptography](https://github.com/sobolevn/awesome-cryptography)’s [Books Section](https://github.com/sobolevn/awesome-cryptography?tab=readme-ov-file#books)
- [Free Ebook Foundation](https://github.com/EbookFoundation)’s compiled [Books on Security & Privacy](https://github.com/EbookFoundation/free-programming-books/blob/main/books/free-programming-books-subjects.md#security--privacy)
- [Internet Archive](https://archive.org/)’s [Introduction to Modern Cryptography](https://ia600907.us.archive.org/1/items/strategic_intelligence_network/communication/encryption/introduction_to_modern_cryptography.pdf) by Jonathan Katz and Yehuda Lindell
- Svetlin Nakov’s (unfinished) [Practical Cryptography for Developers](https://cryptobook.nakov.com/); [GitHub](https://github.com/nakov/Practical-Cryptography-for-Developers-Book)

### Libraries

- [Botan](https://botan.randombit.net/) — Crypto and TLS for Modern C++: [GitHub](https://github.com/randombit/botan); [Handbook](https://botan.randombit.net/handbook/)
- Crypto++: [GitHub](https://github.com/weidai11/cryptopp)
- OpenSSL: [GitHub](https://github.com/openssl/openssl)

### Miscellany

- [Awesome Cryptography](https://github.com/sobolevn/awesome-cryptography)
- [Comparison of cryptography libraries](https://en.wikipedia.org/wiki/Comparison_of_cryptography_libraries)

## Acronyms

__AES__ (_vs_ DES) Advanced Encryption Standard, AKA the Rijndael algorithm. It supersedes the DES which was published in 1977.  
__BIO__ In OpenSSL, BIO stands for Basic I/O abstraction, used to handle various data streaming types, such as files, memory buffers, and network connections.  
__CSR__ Certificate Signing Request. An encoded message sent from an applicant to a Certificate Authority (CA) to apply for an SSL/TLS certificate. It typically contains the public key, identifying information like a domain name, and proof of authenticity, and it must be generated on the server where the certificate will be used.  
__DES__ (_vs_ AES) Data Encryption Standard.  
__ECC__ Elliptic Curve Cryptography.  
__ECDSA__ Elliptic Curve Digital Signature Algorithm.  
__HMAC__ Keyed-hashing message authentication.  
__IV__ Initialization vector.  
__KDF__ Key derivation function.  
__MAC__ Message authentication code.  
__MD5__ The MD5 (Message-Digest Algorithm 5) is a cryptographic hash function that was developed in 1991 by Ronald Rivest as an improvement over its predecessor, MD4 3. It is specifically designed to produce a 128-bit hash value from any amount of data, making it suitable for various applications, including data integrity checks and digital signature verification.  
__PEM__ Privacy-enhanced mail, although its use has expanded beyond email. It’s a Base64-encoded format for storing various cryptographic objects.  
__PKCS__ Public key cryptography standards.  
__PRNG__ Pseudo-random number generator.  
__RSA__ Rivest-Shamir-Adleman, a widely used public-key cryptosystem that enables secure data transmission and is foundational in modern cryptography.  
__SHA__ Secure hash algorithm.  
__SHA-2__ The SHA-2 family is a group of cryptographic hash functions that includes SHA-224, SHA-256, SHA-384, and SHA-512. These functions were developed by the National Security Agency (NSA) and first published in 2001. The SHA-2 family is notable for its improved security over its predecessor, SHA-1.  
__SHA-256__ This is a specific member of the SHA-2 family of hash algorithms. The “256” indicates that it produces a 256-bit (32-byte) hash value.  
__SSL__ Secure Sockets Layer, a networking protocol that secures connections between web clients and servers through encryption.  
__TLS__ Transport Layer Security. A cryptographic protocol designed to provide secure communications over a network by encrypting data to prevent eavesdropping and tampering.  
__X.509__	Standard for public-key infrastructure.  

## Glossary

__asymmetric cryptography__ (_vs_ symmetric cryptography). See _public-key cryptography_.  
__brute-force attack__ (and _exhaustive key search_) [[Wikipedia]](https://en.wikipedia.org/wiki/Brute-force_attack)  
__cipher__ _v_ (cypher) Convert ordinary language into a coded format or to write in a secret code.   
__crypto-__ (crypt-) Secret, hidden, or concealed.  
__cryptogram__ (_vs_ plaintext) A message or writing in code or cipher.  
__cryptographic key__ A piece of information, typically a string of numbers or letters _stored in a file_, used to encode or decode cryptographic data through a cryptographic algorithm. They are used for (1) encryption, (2) decryption, (3) authentication (to verify the identity of users or devices in a system), and (4) digital signatures (keys help ensure the integrity of messages and confirm the identity of the sender).  
__cryptographic scheme__ A structured set of algorithms and protocols designed to achieve specific security goals, such as confidentiality, data integrity, authentication, and non-repudiation. These schemes typically involve a combination of cryptographic primitives, such as encryption and decryption algorithms, hash functions, digital signatures, and key exchange mechanisms. Examples of cryptographic schemes include RSA, AES, Diffie-Hellman Key Exchange, and ECDSA.  
__cryptography__ [:scroll: Derived from the Greek words “kryptos” (κρυπτός), meaning “hidden” or “secret,” and “graphia” (γραφή), meaning “writing” or “description.”] The practice of securing information by transforming it into a format that is unreadable to unauthorized users.  
__cyphertext__ The result of encryption performed on plaintext using an algorithm, known as a cipher.  
__decryption__ (_vs_ encryption) The reverse of encryption, converting ciphertext back into readable plain text.  
__digest__ A digest, also known as a hash, is a fixed-size string of bytes that is generated from an arbitrary block of data. The primary purpose of a digest is to ensure data integrity and authenticity.  
__digital signature__ Digital signatures are used to verify the authenticity and integrity of a message, software, or digital document. They use asymmetric cryptography to create a signature that can be verified by anyone with the public key. Usage example (see _public key_): Bob can sign a message with his private key. Anyone with Bob’s public key can verify that the message is indeed from Bob and hasn’t been altered.  
__encryption__ (_vs_ decryption) The process of converting plain text into a coded format (ciphertext) to prevent unauthorized access.  
__hash__ See _digest_.  
__hash algorithm/function__ These are algorithms that take an input and produce a fixed-size string of bytes. The output, called a hash, is unique to each unique input. A _hash function_ is a mathematical algorithm that transforms input data of any size into a fixed-size output, known as a hash value or message digest. This process is one-way, meaning it is computationally infeasible to reverse the hash value to obtain the original input data. Hash functions are crucial in various security applications, including password storage, data integrity checks, and digital signatures.  
__initialization vector__ (IV) A random or pseudorandom value used to initialize a cryptographic primitive, such as a block cipher or stream cipher. The primary purpose of an IV is to ensure that identical plaintexts, when encrypted with the same key, produce distinct ciphertexts. This is crucial for achieving semantic security, which prevents an attacker from inferring relationships between different segments of an encrypted message.  
__key derivation function (KDF)__ A cryptographic algorithm that derives _one or more secret keys_ from a secret value such as a master key, a password, or a passphrase using a pseudorandom function.  
__key management__ This involves the generation, exchange, storage, use, and replacement of cryptographic keys. Effective key management is crucial for maintaining the security of a cryptographic system.  
__nonce__ A random or pseudo-random number that is used only once in a specific communication session. The term “nonce” stands for “number used once,” emphasizing its unique and ephemeral nature. Nonces are crucial for ensuring the security and integrity of cryptographic protocols by preventing replay attacks, where an attacker intercepts and reuses valid messages to gain unauthorized access.  
__OpenSSL__ An open-source cryptographic toolkit that enables secure communications over networks, supports the TLS and SSL protocols, and allows for the creation of CSRs and private keys.  
__pepper__ (_vs_ salt) A secret value that is added to a password before it is hashed, enhancing the security of the stored password hashes. Unlike salt, which is unique for each user and stored alongside the hash, a pepper is typically a fixed, secret string that is not stored in the database. This separation aims to provide an additional layer of security against attacks.  
__plaintext__ (_vs_ cryptogram) The intelligible original message of a cryptogram, as opposed to the coded or enciphered version.  
__private key__ (_vs_ public key) Usage: Private keys are used to decrypt data that has been encrypted with the _corresponding_ public key. They must be kept secret. Function: The private key is also used to create digital signatures, which verify the authenticity and integrity of a message.  
__private-key cryptography__ (symmetric cryptography) _A private-key encryption scheme, or cipher, is comprised of three algorithms: the first is a procedure for generating keys, the second a procedure for encrypting, and the third a procedure for decrypting._  
__public key__ (_vs_ private key) Usage: Public keys are used to encrypt data. They can be freely shared with anyone. Function: When someone wants to send you a secure message, they use your public key to encrypt it. Only the corresponding private key can decrypt this message. If Alice wants to send a secure message to Bob, she encrypts it using Bob’s public key. Only Bob’s private key can decrypt it.  
__public-key cryptography__ (asymmetric cryptography) [[Wikipedia](https://en.wikipedia.org/wiki/Public-key_cryptography)] The field of cryptographic systems that use pairs of related keys (a public key for encryption and a private key for decryption). Examples include RSA and ECC.  
__salt__ (_vs_ pepper) A random value that is added to the input of a cryptographic function, particularly when hashing passwords. Its primary purpose is to ensure that even if two users have the same password, their hashed outputs will be different due to the unique salt values used for each password. [:scroll: It draws an analogy from cooking, where salt is used to enhance flavor and preserve food. In a similar vein, adding “salt” enhances security by making hashed outputs more robust against attacks. Just as a pinch of salt can transform a dish by adding complexity and depth, adding a random value (salt) transforms simple password hashes into complex outputs that are much harder to reverse-engineer or crack.]
__scrypt__ A password-based KDF designed to produce a secure cryptographic key from a password. Key features of scrypt include _deterministic output_ (given the same input parameters (password, salt, cost factor, etc.), scrypt will always produce the same output key) and _irreversibility_ (scrypt is a password-based key derivation function (KDF) designed to produce a secure cryptographic key from a password).  
__symmetric cryptography__ (_vs_ asymmetric cryptography ) Uses the same key for both encryption and decryption. Examples include DES and AES.  
__symmetric encryption__ Symmetric encryption uses the _same key_ for both _encryption_ and _decryption_. It’s _efficient for encrypting data at rest_ (e.g., files, databases) because the same key is used for both operations. AES-256 is a popular symmetric key encryption algorithm.  