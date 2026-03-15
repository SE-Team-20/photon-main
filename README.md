sudo# Photon main (team 20)
[quick link to the main branch](https://github.com/SE-Team-20/photon-main/tree/main)

## Quick Run Instructions (Linux)
## nstall.sh has two versions—Mac and Windows. Please use the version appropriate for your system.
1. Fix line endings
```
sed -i 's/\r$//' install.sh run.sh
```

2. Make scripts executable:
```
chmod +x install.sh run.sh
```

3. Install software:
```
./install.sh
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
- [ ] create play action entry screen - template button created, widget screen needs to be configured.
- [ ] ensure inputted hardware IDs are carried over to the play action screen.
- [x] update trello card assignments for all team members.
- [ ] code up game start countdown timer in play action screen (for simplicity).
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
