# Product Management System



## Authors

**FU Guanhe**	SQL connection build

**LI Yifeng**	GUI creation

**SUN Hansong**	GUI creation, FileIO creation, and Code combination

**KWOK Ting Fai**	Data processing

The system, which can access any remote MySQL database, was developed through Python.



## Function Properties

1. Database login window (The initial database is our remote database located in the US. The delay of operation can be seen easily. If you want a smoother experience, you can log in to your local database. ) **REMIND: When you occur a lag, please wait for database corresponding. Unknown errors may occur if you do extra operations during a lag.**
2. Remote database access is available.
3. Straightforward operations with buttons.
4. Two databases interaction: 
    1. When you create a piece of sales information, the related inventory information will change correspondingly.
    2. When you delete the information of a product, the related sales information will be deleted accordingly. If you undo the operation, all data will come back.
    3. When you add sales information, the related product MUST be already in the database or may result in Add Operation Fail.
5. About products database:
    1. You CAN NOT add two products with the same name or ID, which may result in Add Operation Fail.
    2. You CAN NOT add the wrong type of information in the add operation. (Example: write a word in the "Quantities" section.)
    3. You SHOULD NOT add any quotation mark(" ") at the front or back of a string type information, which may result in an error occurring in the database (VERY SEVERE, CAN NOT BE SOLVED).
6. About sales database:
    1. It is the same as the product database, but two pieces of sales information CAN have the same product name.
    1. It is recommended to use the same format for the dates in each piece of information as "YYYY/MM/DD" or "YYYY.MM.DD" or the sort function with the date as keywords may be invalid.
7. In the filter operation, the filter is case-insensitive.
8. We also have other operations like sort operation, select-all operation, and undo operation.
9. About FileIO operation:
    1. Import: You can only choose txt(.txt) files with information in the following format. The two properties within a piece of information are ONLY separated by a single comma(,). And each line represents one piece of information. (Example: 5,Apple3,1,1,1,Apple Inc). If you have the wrong format or the data type of a property is wrong, it may cause a failure in import.
    2. Export: You can choose ANY folder you like to generate a PDF(.pdf) report in the folder.
10. The Right-Click and Left-Drag function is available. You can choose the delete operation or the update operation.
11. More updates about the function and interface beautification are on the way.



## Keyboard Shortcuts

| Key        | Effect |
| ---------- | ------ |
| `Delete`   | Delete |
| `Ctrl`+`n` | Add    |
| `Ctrl`+`z` | Undo   |
| `Ctrl`+`f` | Filter |



## Installation

### External dependent libraries

1. `tkinter` Creating GUI Functions.
2. `fpdf2` Generating PDF reports.
3. `pymysql` Connecting to the database

#### Installation

```
pip install tk
pip install fpdf2
pip install pymysql
```

#### Launch

```
python3 main.py
```

The default information filled in the login window is the information of our remote database, which is accessable. Just click the `submit` button to login.

**It is tested that the program can be launched in MacOS and Windows(10,11)**



## Update Journal

2023-11-27 First version released.
