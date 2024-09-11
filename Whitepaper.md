Whitepaper: A Blockchain-Based DNS System for Digital Property Ownership

Abstract

This paper introduces a new blockchain system that addresses the problem of digital property ownership, specifically focusing on domain names. Our system integrates both a native coin and a decentralized Domain Name System (DNS) on a public, permissionless blockchain. Each block mined generates two distinct coinbase transactions: one for a native cryptocurrency and another that issues a new digital property in the form of a "full domain." This full domain consists of a domain name, top-level domain (TLD), and an IP address, all cryptographically linked to the owner's keys. By leveraging the blockchain's immutability and decentralization, this system guarantees true ownership and transferability of domains, addressing current issues in centralized DNS management.

1. Introduction

The current DNS system relies heavily on centralized authorities to manage and maintain domain names, introducing risks of censorship, high costs, and lack of true ownership. This paper proposes a decentralized DNS blockchain where domain names are treated as digital property that can be cryptographically owned, transferred, and modified.

Our system introduces a dual-coinbase mechanism, where each block mined produces both a native cryptocurrency (similar to Bitcoin) and a newly created full domain. Each full domain is unique and linked to a cryptographic key, allowing for decentralized and verifiable ownership.

2. Overview of the System

The key innovation in this blockchain is the introduction of a "full domain," which is issued to miners as a reward for each block mined. The full domain consists of the following components:

Domain Name: Up to 64 alphanumeric characters (case-insensitive, A-Z, 1-9), serialized in 6-bit values.
Max Size: 384 bits (64 characters * 6 bits).

Top-Level Domain (TLD): Up to 4 uppercase letters (A-Z), serialized in 5-bit values.
Max Size: 20 bits (4 characters * 5 bits).

IP Version Flag: A 1-bit flag indicating whether the domain is linked to an IPv4 or IPv6 address.
Size: 1 bit (0 for IPv4, 1 for IPv6).

IP Address:

IPv4: 4 bytes (32 bits).
IPv6: 16 bytes (128 bits).
The total size of a serialized full domain depends on the IP version:

For IPv4: 437 bits (384 + 20 + 1 + 32).
For IPv6: 533 bits (384 + 20 + 1 + 128).
When parsed, dots (.) and colons (:) are reintroduced for human-readable formats (e.g., "example.com:192.168.1.1").

3. Key Innovations

3.1 Full Domain Ownership

In this blockchain, the full domain (domain name + TLD + IP) is treated as a non-divisible, cryptographic asset. Ownership is secured through public-private key cryptography, allowing true ownership without relying on centralized registries. Domains can be transferred between addresses and modified (such as changing the associated IP address), creating a flexible system for digital property.

3.2 Dual Coinbase Transaction

Each block mined contains two coinbase transactions:

Native Coin Reward: Similar to Bitcoin, this transaction generates a native cryptocurrency as a reward for miners.
Full Domain Reward: A new full domain is issued to the miner. The domain follows the unique format described and is assigned to the miner's public key. The domain must not already exist within the blockchain.
4. Transaction Types

To accommodate the new concept of full domains, the blockchain introduces additional transaction types:

Coin Transaction: Follows the Bitcoin UTXO model for transferring the native cryptocurrency.

Domain Transfer Transaction: Allows a full domain to be transferred to another address. This transaction involves the full domain being signed by the current owner and transferred to the recipient's address. Miners verify that the domain is valid and owned by the sender.

IP Change Transaction: Enables the domain owner to update the IP address associated with their domain. The domain is signed by the owner, and the new IP address is linked to it. A transaction fee, in native coins, incentivizes miners to include the transaction in a block.

5. Protocol Design

The protocol closely mirrors Bitcoin in its coin issuance and validation mechanisms. The key differences arise in the handling of full domains, which are treated as digital property rather than monetary tokens. Each domain is linked to a unique cryptographic key pair, and transactions for domains follow the same principles as coin transfers but with additional domain-related fields.

5.1 Coin Issuance

The issuance of the native cryptocurrency will follow the same halving schedule and consensus mechanism as Bitcoin. Each block mined will reduce the coin reward over time, creating scarcity and increasing value for the currency.

5.2 Domain Issuance

Unlike coins, full domains are issued uniquely and cannot be duplicated. When a new block is mined, a new full domain is generated for the miner. The domain must not already exist on the blockchain, ensuring the uniqueness of digital property.

6. Security and Ownership

All domains and coins are owned through private-public key pairs, leveraging well-established cryptographic techniques to ensure security. As with Bitcoin, wallet generation and transaction validation use elliptic curve cryptography (specifically the secp256k1 curve).

7. Conclusion

This blockchain introduces a decentralized solution to the problem of digital property ownership for domains. By combining the proven model of cryptocurrency with a DNS system, we create a network where users can own, transfer, and modify domain names in a decentralized manner. The integration of dual coinbase transactions provides miners with both economic incentives and unique digital property rights, establishing a system for true, immutable ownership of digital assets.

