# ShadowLure Attack Simulation Guide

This guide explains how to test your ShadowLure honeypot using a second machine (like a VM) as the attacker.

- **Your Target Machine:** The Windows computer where ShadowLure is running.
- **Your Attacker Machine:** Your Arch Linux VM.

---

### Step 1: Find Your Target's IP Address (on Windows)

The attacker needs the target's address.

1.  On your **Windows machine**, open a Command Prompt (cmd).
2.  Run this command:
    ```bash
    ipconfig
    ```
3.  Find the **IPv4 Address** (e.g., `192.168.1.15`). This is your **Target IP**.

---

### Step 2: Launch Attacks from Your Arch Linux VM

Switch to your **Arch Linux VM** and open a terminal. Use the **Target IP** you just found in the commands below.

**(Remember to replace `YOUR_WINDOWS_IP` with the real IP address)**

#### Attack 1: FTP Service (Port 21)
```bash
ftp YOUR_WINDOWS_IP 21
```
- At the `ftp>` prompt, type the following commands, pressing Enter after each one:
  1. `user admin` (or any fake username)
  2. `pass password123` (or any fake password)
- The honeypot will log these credentials and then disconnect you.

#### Attack 2: HTTP Service (Port 80)

**Method 1: Web Browser (Recommended)**
1. Open a web browser on your Arch Linux VM.
2. Navigate to `http://YOUR_WINDOWS_IP`.
3. You will see a fake "System Login" page.
4. Enter a fake username (e.g., `root`) and password (e.g., `12345`) and click the Login button.
5. The honeypot will log the credentials you submitted.

**Method 2: Terminal (using curl)**
```bash
# This command simulates submitting the login form
curl -X POST -d "username=root&password=12345" http://YOUR_WINDOWS_IP
```
- This will send the login data directly to the honeypot, which will be recorded in the log.

#### Attack 3: SSH Service (Port 22)
```bash
ssh fakeuser@YOUR_WINDOWS_IP -p 22
```
- The honeypot will ask for a password. Type anything. The attempt will be logged.

---

### Step 3: Review the Evidence (on Windows)

After launching the attacks, check the results on your Windows machine.

1.  **The Running ShadowLure Terminal:** You will see live log output for each connection you made.
2.  **The `shadowlure.log` File:** Open this file in a text editor. It will contain a permanent, timestamped record of every attack, including the IP address of your Arch Linux VM and any credentials you used.

This process validates that your honeypot is successfully detecting and logging unauthorized activity on your network.
