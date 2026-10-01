# Quantum Key Distribution Framework for Secure UAV Swarms

## Overview

This project presents a secure UAV communication framework designed to protect MAVLink telemetry against cyber attacks. The framework combines a software-based BB84-inspired Quantum Key Distribution (QKD) mechanism with AES-256-GCM authenticated encryption.

The system was implemented and evaluated using PX4 SITL, Gazebo, QGroundControl, Python, MAVLink and Wireshark.

> **Note:** The QKD component is a software-based BB84-inspired simulation for research and experimental purposes. It does not use physical quantum communication hardware.

## Project Objectives

- Design a secure communication framework for UAV systems.
- Integrate BB84-inspired key establishment with AES-256-GCM encryption.
- Protect MAVLink communication against Man-in-the-Middle (MITM) attacks.
- Detect and reject Replay attacks using sequence-number validation.
- Compare secured and unsecured MAVLink communication.
- Evaluate the processing overhead introduced by the security framework.

## System Architecture

The experimental communication pipeline is based on:

```text
PX4 SITL → Alice Security Gateway → Bob Security Gateway → QGroundControl
```

**Alice Gateway**
- Receives MAVLink traffic.
- Uses the established session key.
- Encrypts data using AES-256-GCM.
- Adds sequence information for replay protection.
- Forwards protected traffic to Bob.

**Bob Gateway**
- Receives protected packets.
- Performs AES-GCM authentication.
- Rejects modified or unauthenticated packets.
- Validates packet sequence numbers.
- Decrypts valid packets and forwards MAVLink traffic.

## Security Mechanisms

### BB84-Inspired QKD

A software-based BB84-inspired mechanism is used to simulate secure session-key establishment for the experimental framework.

### AES-256-GCM

AES-256-GCM provides authenticated encryption, protecting both the confidentiality and integrity of MAVLink data.

### Replay Protection

Sequence-number validation is used to identify previously processed packets and reject replayed traffic.

## Security Evaluation

The framework was evaluated using controlled MITM and Replay attack experiments.

### Man-in-the-Middle Attack

In the unsecured configuration, MAVLink traffic could be intercepted and modified. In the secured configuration, modification of encrypted traffic causes AES-GCM authentication to fail, allowing altered packets to be rejected.

### Replay Attack

Previously captured packets were retransmitted to demonstrate Replay attacks against the unsecured communication path. In the secured framework, sequence-number validation is used to identify and reject previously processed packets.

## Performance Evaluation

Processing-delay experiments were conducted to compare unsecured communication with AES-256-GCM-protected communication.

The evaluation also considered multiple packet loads:

`20, 40, 60, 80, 100, 150, 200 and 250 bytes`

Each packet-load configuration was tested over 1,000 iterations to analyse the relationship between packet size and cryptographic processing delay.

## Technologies Used

- Python
- PX4 SITL
- Gazebo
- QGroundControl
- MAVLink
- Wireshark
- AES-256-GCM
- BB84-inspired QKD
- UDP networking
- WSL / Ubuntu

## Key Python Components

| File | Purpose |
|---|---|
| `bb84.py` | BB84-inspired QKD simulation |
| `aes_crypto.py` | AES-GCM cryptographic operations |
| `alice_px4.py` | Alice secure MAVLink gateway |
| `bob_px4.py` | Bob secure MAVLink gateway |
| `alice_px4_timing.py` | Alice-side timing measurements |
| `bob_px4_timing.py` | Bob-side timing measurements |
| `baseline_delay_test.py` | Baseline processing-delay testing |
| `qkd_aes_integration.py` | QKD and AES integration |
| `mitm_attack.py` | Controlled MITM experiment |
| `secure_mitm_attack.py` | MITM experiment against protected traffic |
| `replay_attack.py` | Controlled Replay attack experiment |

## Experimental Results

The experiments demonstrated:

- Successful interception/modification in the unsecured MITM configuration.
- Successful retransmission of captured traffic in the unsecured Replay experiment.
- Detection of ciphertext modification through AES-GCM authentication.
- Replay protection through sequence-number validation.
- Measurable processing overhead introduced by the security layer.
- Continued low-latency processing across the tested packet-load range.

## Research Context

This repository contains the implementation developed as part of an MSc Cyber Security major project at Nottingham Trent University.

**Project:** Quantum Key Distribution Framework for Secure UAV Swarms

## Disclaimer

This project was developed for academic research, cybersecurity education and controlled experimental testing. Attack simulation scripts included in this repository are intended only for authorised laboratory environments.

## Author

**Azaruddin Mohammad**  
MSc Cyber Security  
Nottingham Trent University(United Kingdom)
