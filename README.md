# Photon main (team 20)
[quick link to the main branch](https://github.com/SE-Team-20/photon-main/tree/main)

## Quick Run Instructions (Linux)
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

## Install Instructions
# 1. Make scripts executable
chmod +x install.sh run.sh

# 2. Fix line endings if you see "$'\r': command not found"
sed -i 's/\r$//' install.sh run.sh

# 3. Install dependencies (Python, PostgreSQL, required packages)
./install.sh

# 4. Run the application
./run.sh

## TODOs (week 2)
by February 10th
- [x] create splash screen (Thomas)
- [x] create player entry screen (Thomas)
- [ ] link database to application (RyoB)
- [ ] add two players via application
- [x] set up UDP sockets, broadcast equipment codes
- [ ] have option to select different network for UDP sockets

--- 
by 15th
- [x] include an install script to the repository
- [x] modify this readme to include the install instruction
- [x] enhance README



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
