# Cryptography

## Acronyms

__AES__ (_vs_ DES) Advanced Encryption Standard.  
__DES__ (_vs_ AES) Data Encryption Standard.  
__ECC__ Elliptic Curve Cryptography.  
__KDF__ Key derivation function.  
__RSA__ Rivest-Shamir-Adleman, a widely used public-key cryptosystem that enables secure data transmission and is foundational in modern cryptography.  

## Glossary

__asymmetric cryptography__ (_vs_ symmetric cryptography) Uses a pair of keys: a public key for encryption and a private key for decryption. Examples include RSA and ECC.  
__cipher__ _v_ (cypher) Convert ordinary language into a coded format or to write in a secret code.   
__crypto-__ (crypt-) Secret, hidden, or concealed.  
__cryptogram__ (_vs_ plaintext) A message or writing in code or cipher.  
__cryptographic key__ A piece of information, typically a string of numbers or letters _stored in a file_, used to encode or decode cryptographic data through a cryptographic algorithm. They are used for (1) encryption, (2) decryption, (3) authentication (to verify the identity of users or devices in a system), and (4) digital signatures (keys help ensure the integrity of messages and confirm the identity of the sender).  
__cryptography__ The practice of securing information by transforming it into a format that is unreadable to unauthorized users.  
__cyphertext__ The result of encryption performed on plaintext using an algorithm, known as a cipher.  
__decryption__ (_vs_ encryption) The reverse of encryption, converting ciphertext back into readable plain text.  
__digital signatures__ These are used to verify the authenticity and integrity of a message, software, or digital document. They use asymmetric cryptography to create a signature that can be verified by anyone with the public key.  
__encryption__ (_vs_ decryption) The process of converting plain text into a coded format (ciphertext) to prevent unauthorized access.  
__hash functions__ These are algorithms that take an input and produce a fixed-size string of bytes. The output, called a hash, is unique to each unique input. Hash functions are used for data integrity verification.  
__key derivation function (KDF)__ A cryptographic algorithm that derives _one or more secret keys_ from a secret value such as a master key, a password, or a passphrase using a pseudorandom function.  
__key management__ This involves the generation, exchange, storage, use, and replacement of cryptographic keys. Effective key management is crucial for maintaining the security of a cryptographic system.  
__pepper__ (_vs_ salt) A secret value that is added to a password before it is hashed, enhancing the security of the stored password hashes. Unlike salt, which is unique for each user and stored alongside the hash, a pepper is typically a fixed, secret string that is not stored in the database. This separation aims to provide an additional layer of security against attacks.  
__plaintext__ (_vs_ cryptogram) The intelligible original message of a cryptogram, as opposed to the coded or enciphered version.  
__salt__ (_vs_ pepper) A random value that is added to the input of a cryptographic function, particularly when hashing passwords. Its primary purpose is to ensure that even if two users have the same password, their hashed outputs will be different due to the unique salt values used for each password. [:scroll: It draws an analogy from cooking, where salt is used to enhance flavor and preserve food. In a similar vein, adding “salt” enhances security by making hashed outputs more robust against attacks. Just as a pinch of salt can transform a dish by adding complexity and depth, adding a random value (salt) transforms simple password hashes into complex outputs that are much harder to reverse-engineer or crack.]
__scrypt__ A password-based KDF designed to produce a secure cryptographic key from a password. Key features of scrypt include _deterministic output_ (given the same input parameters (password, salt, cost factor, etc.), scrypt will always produce the same output key) and _irreversibility_ (scrypt is a password-based key derivation function (KDF) designed to produce a secure cryptographic key from a password).  
__symmetric cryptography__ (_vs_ asymmetric cryptography ) Uses the same key for both encryption and decryption. Examples include DES (Data Encryption Standard) and AES (Advanced Encryption Standard).  
__symmetric encryption__ Symmetric encryption uses the _same key_ for both _encryption_ and _decryption_. It’s _efficient for encrypting data at rest_ (e.g., files, databases) because the same key is used for both operations. AES-256 is a popular symmetric key encryption algorithm.  