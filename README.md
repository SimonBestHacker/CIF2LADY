# CIF2LADY
Program for automatic data conversion from Crystallographic Information File (CIF) format to LADY-input(.inp) format(https://sourceforge.net/projects/ladytool/) 
Database(DB) file contains some force constants for semi-empirical lattice dynamics calculations using LADY programm. Throught this app you can modify this file by adding your own values as bond constants of any chemical elements pairs. 

Example of usage:
1. Choose cif-file using the topmost one button.
2. Press second from the top button. Choose path where you want to have converted inp-file for LADY programm.
3. Optional: checkbox let programm automatically write potential part in inp-file if there is information about atoms from CIF-file in app's database(DB).
4. CONGRATS! You have your INP.ldy-file with structure from CIF (with potential)
5. In the latest version you can modify DB-file. Press the 'FCDB' button: 
   a) Add to FCDB: Clicking on this button opens the menu for adding an entry to the FCDB database.
   b) Delete from FCDB: When this button is clicked, the highlighted entry in the treeview is deleted from the FCDB.
   All of this actions are accompanied by text in the text-area in the main window
