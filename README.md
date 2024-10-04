# ochakai-hardening
Ochakai Hardening is a tool that allows users to easily experience incident response training. It was created with the aim of serving as an icebreaker within teams participating in Japan's security hardening competition, the "[ハードニング競技会](https://wasforum.jp/hardening-project/)". Also, Ochakai Hardening was inspired by [ayato-hardening](https://github.com/ayato-shitomi/ayato-hardening/tree/master).

## Setup

```
git clone https://github.com/melonattacker/ochakai-hardening.git
cd ochakai-hardening
docker compose up --build -d
```

The following components will be launched:
- The environment to be hardened, which is provided to the players. (`playerX` (X: 1~7))
    - An SSH server runs on port 2X022 (login is possible with `root:root`)
    - An web application accessible at http://localhost:2X080
- Attacker server (`red`)
- Score server (`score-server`)
    - Accessible at http://localhost:3000

## Game Rule
- The competition time is 30 minutes.
- Attacks will begin 10 minutes after the start of the competition.
- The goal is to keep the web application operational.
- Use `apachectl` for managing Apache operations.

## Game Start
Click the `Start Game` button at http://localhost:3000.

<img width="813" alt="Screenshot 2024-10-04 at 13 01 56" src="https://github.com/user-attachments/assets/465f9365-9113-4884-b3fb-b0f3fe0d8142">

## Attack Scenario
- [Attack Scenario](./red/README.md)
