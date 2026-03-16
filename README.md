sudo# Photon main (team 20)
[quick link to the main branch](https://github.com/SE-Team-20/photon-main/tree/main)

## Quick Run Instructions (Linux)
## Install script has two versions based on your native OS —Mac and Windows. Please use the version appropriate for your system:
Both install scripts are for a Debian Linux environment. If you are using a Virtual Machine (Debian Linux) on a Mac, please use the _macinstall.sh_ script. If you are either using a Virtual Machine (Debian Linux) on Windows _or_ just using a native Debian Linux machine, please use the _wininstall.sh_.

**TLDR: Use _wininstall.sh_ for Debian Linux or Windows(using Linux VM). Use _macinstall.sh_ for a Mac(using Linux VM).**
 
1. Fix line endings
```
sed -i 's/\r$//' ./<your install version>.sh run.sh
```

2. Make scripts executable:
```
chmod +x <your install version>.sh run.sh
```

3. Install software:
```
./<your install version>.sh
```

4. Launch main program:
```
./run.sh
```


## File organization

<table>
<thread>
 <tr>
  <th>folder</th><th>includes</th>
 </tr>
</thread>
<tr>
 <td>assets</td><td>images and sound used in App</td>
</tr>
<tr>
 <td>config</td><td>structured info outside the control of this repo</td>
</tr>
<tr>
 <td>doc</td><td>documentations and references</td>
</tr>
<tr>
 <td>src</td><td>source files (.py)</td>
</tr>
</table>

## TODOs (Sprint 3)
by March 15th
- [x] create clear entries button (Thomas)
- [x] create play action entry screen - template button created, widget screen needs to be configured.
- [x] ensure inputted hardware IDs are carried over to the play action screen.
- [x] update trello card assignments for all team members.
- [x] code up game start countdown timer in play action screen (for simplicity).
- [x] ensure install script executes as expected in a fresh Linux environment.



## Tech stacks
- Python
- PyQt6
- Postgre Sequel
- UDP Sockets

## GitHub Contributors
- aliibek : Mukhammadali Madaminov
- sultaniwahid240-cell : Wahid Sultani
- thoma-sH : Thomas Hamilton
- TrueRyoB : Ryoji Araki
