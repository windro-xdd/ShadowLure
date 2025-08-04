# ShadowLure Deployment Guide: Exposing to the Internet

This guide explains the concepts and steps required to make your ShadowLure honeypot visible to attackers on the public internet.

---

### **! ! ! MAJOR SECURITY WARNING ! ! !**

Exposing any service directly to the internet is **extremely risky**. You are intentionally inviting real-world attackers to connect to your network. 

**DO NOT PROCEED UNLESS YOU FULLY UNDERSTAND THESE RISKS:**
- **Network Compromise:** A sophisticated attacker could potentially find a vulnerability in your honeypot, your operating system, or your router to gain access to your entire local network.
- **Legal and ISP Issues:** Your Internet Service Provider (ISP) may have policies against running servers or attracting malicious traffic.
- **Recommendation:** Only run an internet-facing honeypot on a **completely isolated network** that does not contain any personal or important devices.

---

### Concept: Local vs. Public Networks

- **Local Network (LAN):** This is your private, internal network at home (e.g., `192.168.x.x`). Devices can see each other, like your PC and your VM.
- **Public Network (WAN):** This is the global internet. Your router has one **Public IP address** that represents your entire home network to the outside world.

To allow an external attacker to reach your honeypot, you must tell your router to "forward" specific traffic from the public side to the private machine running ShadowLure. This is called **Port Forwarding**.

---

### Steps to Expose DecoyNet

**Step 1: Find Your Public and Private IP Addresses**

1.  **Public IP:** On any device, open a browser and search "what is my IP". This is the address the attacker will use.
2.  **Private IP:** On the Windows machine running ShadowLure, open Command Prompt (`cmd`) and run `ipconfig`. Find the "IPv4 Address". This is your target machine's local address.

**Step 2: Access Your Router's Admin Page**

1.  Open a web browser and navigate to your router's IP address. This is commonly `192.168.1.1` or `192.168.0.1`.
2.  Log in with your router's administrator username and password.

**Step 3: Configure Port Forwarding**

1.  Find the "Port Forwarding," "Virtual Servers," or a similarly named section in your router's settings.
2.  Create a new rule for each service you want to expose. You will need to provide the following information for each rule:

    - **Rule Name:** A descriptive name (e.g., `FTP-Honeypot`).
    - **Protocol:** `TCP`.
    - **External Port (or WAN Port):** The port the attacker sees (e.g., `21` for FTP).
    - **Internal Port (or LAN Port):** The port ShadowLure is listening on (e.g., `21`).
    - **Internal IP Address (or Device IP):** The private IPv4 address of your Windows machine.

3.  **Example Rules:**
    - **FTP Rule:** External Port `21` -> Internal Port `21` -> Your Windows IP
    - **HTTP Rule:** External Port `80` -> Internal Port `80` -> Your Windows IP
    - **SSH Rule:** External Port `22` -> Internal Port `22` -> Your Windows IP

**Step 4: Save and Test**

1.  Save your new rules in the router's interface.
2.  To test, you can use a smartphone on its cellular data network (NOT your Wi-Fi) and a mobile app (like an SSH or FTP client) to try and connect to your **Public IP address** on the forwarded ports. If it works, your honeypot is now live on the internet.
