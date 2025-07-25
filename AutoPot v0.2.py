import CifFile
import os
import re
from collections import Counter
import tkinter as tk
import tkinter.filedialog as fd
from tkinter import ttk
#import pandas as pd
import sqlite3
from sqlite3 import Error
from itertools import combinations_with_replacement
#import numbers

nums = '1234567890?+-'

#excel to query
#df = pd.read_excel("data.xlsx")
#cols = len(df.axes[1])
#out = df.to_numpy().tolist()
#print(out)

def convertToSQL(list):
    text = "(Null, "
    for k in range(len(list[0])):
        if k == len(list[0])-1:
            text = text + "?)"
        else:
            text=text+"?,"+" "
    #print(text)
    return str(text)



class Db:
    """ класс База Данных"""
    def __init__(self):
        try:
            # Устанавливаем соединение с базой данных
            self.connection = sqlite3.connect('my_database.db')
            self.cursor = self.connection.cursor()
        except Error:
            print(Error)

    # Вывод содержимого таблицы tablename
    def DataBaseShowContent(self):
        tablename = str(input("Показать содержимое таблицы (название таблицы):"))
        self.cursor.execute('SELECT * FROM'+' '+tablename)
        self.rows = self.cursor.fetchall()
        for notes in self.rows:
            print(notes)

    # Добавление записей в таблицу
    def AddContent(self, tablename, content):
        self.cursor.executemany("INSERT INTO"+" "+tablename+" "+"VALUES"+convertToSQL(content), content)
        print(content)

    # Удаление содержимого таблицы
    def DeleteContent(self, tablename):
        self.cursor.execute("DELETE FROM"+" "+tablename+";")

    # Запрос к БД
    def Query(self, query_body):
        self.cursor.execute(query_body)
        self.rows = self.cursor.fetchall()
        return self.rows

    # Сохраняем изменения и закрываем соединение
    def ConnectionClose(self):
        self.connection.commit()
        self.connection.close()



class App(tk.Tk):
    """ класс приложения"""
    def __init__(self):
        super().__init__()
        self.title("CIF2LADY")
        self.name = ''
        self.checkbut = 0
        self.but_text = 0
        btn_file = tk.Button(self, text="Choose cif-file", command = self.choose_file)
        btn_file.pack(padx=60, pady=10)
        btn_run = tk.Button(self, text="Generate inp.LDY-file", command=self.run)
        btn_run.pack(padx=50, pady=10)
        enabled = tk.IntVar()
        enabled_checkbutton = tk.Checkbutton(self, text="Fill inter-atomic potential from FCDB", onvalue=1, offvalue=0, variable = enabled, command = lambda: self.status(enabled.get()))
        enabled_checkbutton.pack(padx=6, pady=6)
        btn_fcdb = tk.Button(self, text="FCDB", command=self.show)
        btn_fcdb.pack(padx=50, pady=10)
        self.text = tk.Text(width=80, height=5)
        self.text.pack(anchor="s")

    def finnadd(self):
        try:
            body = [self.atm1_lb.get().title(), self.atm2_lb.get().title(), int(self.checkbx.get()), float(self.param1_lb.get()), float(self.param2_lb.get()), float(self.distmin_lb.get()), float(self.distmax_lb.get()), "added"]
        except ValueError:
            return self.text.insert("end", "\nParametrs should be numbers!")
        if (sum(body[3:7])!=0) and (body[0]!=None) and (body[1]!=None) and (len(body[0])<3) and (len(body[1])<3):
            db1 = Db()
            body[0] = db1.cursor.execute('select id from Atoms where Atoms.atom1 ="'+body[0]+'"').fetchall()[0][0]
            body[1] = db1.cursor.execute('select id from Atoms where Atoms.atom1 ="'+body[1]+'"').fetchall()[0][0]
            check_if_exist = db1.cursor.execute('select * from FCDB where FCDB.id_atom1 ='+str(body[0])+' AND FCDB.id_atom2 ='+str(body[1])+' AND FCDB.NF ='+str(body[2])+' AND FCDB.Param1 ='+str(body[3])+' AND FCDB.Param2 ='+str(body[4])+' AND FCDB.R1 ='+str(body[5])+' AND FCDB.R2 ='+str(body[6])+' OR FCDB.id_atom2 ='+str(body[0])+' AND FCDB.id_atom1 ='+str(body[1])+' AND FCDB.NF ='+str(body[2])+' AND FCDB.Param1 ='+str(body[3])+' AND FCDB.Param2 ='+str(body[4])+' AND FCDB.R1 ='+str(body[5])+' AND FCDB.R2 ='+str(body[6])).fetchone()
            #print(check_if_exist)
            if check_if_exist == None:
                print([tuple(body)])
                db1.cursor.executemany("INSERT INTO FCDB VALUES"+convertToSQL([tuple(body)]), (body,))
                self.text.insert("end", "\nThe record was successfully added to the FCDB")
            else:
                return self.text.insert("end", "\nSuch a record is already in the FCDB.")
                #db.AddContent("FCDB", body)
            db1.ConnectionClose()
        else:
            return self.text.insert("end", "\nAt least 1 parameter must be non-zero")

    def add_note(self):
        add = tk.Toplevel()
        add.wm_title("Add")
        atoms_lb = tk.Label(add, text="Symbols of atoms pair:")
        atoms_lb.grid(column=1, row=0)
        self.atm1_lb = tk.Entry(add,width=10)
        self.atm1_lb.grid(column=2, row=0, pady=10, padx=6)
        self.atm2_lb = tk.Entry(add, width=10)
        self.atm2_lb.grid(column=4, row=0, pady=10, padx=6)
        param_lb = tk.Label(add, text="Parameters values:")
        param_lb.grid(column=1, row=1)
        self.param1_lb = tk.Entry(add, width=10)
        self.param1_lb.grid(column=2, row=1, pady=10, padx=6)
        self.param1_lb.insert(0,"0")
        self.param2_lb = tk.Entry(add, width=10)
        self.param2_lb.grid(column=4, row=1, pady=10, padx=6)
        self.param2_lb.insert(0, "0")
        dist_lb = tk.Label(add, text="Range of action(min, max):")
        dist_lb.grid(column=1, row=2)
        self.distmin_lb = tk.Entry(add, width=10)
        self.distmin_lb.grid(column=2, row=2, pady=10, padx=6)
        self.distmin_lb.insert(0,"0")
        self.distmax_lb = tk.Entry(add, width=10)
        self.distmax_lb.grid(column=4, row=2, pady=10, padx=6)
        self.distmax_lb.insert(0, "0")
        self.dist_lb = tk.Label(add, text="Type of potential:\n1 - BKE\n2 - EXP\n3 - POW")
        self.dist_lb.grid(column=1, row=3)
        self.checkbx = ttk.Combobox(add, width=6)
        self.checkbx['values'] = (1,2,3)
        self.checkbx.current(0)
        self.checkbx.grid(column=2, row=3)
        btn_fin_add = tk.Button(add, text="Add to FCDB", command = self.finnadd)
        btn_fin_add.grid(column=4, row=5, pady=10, padx=6)


    def status(self, stat):
        self.checkbut = stat

    def choose_file(self):
        filetypes = (("cif-file", "*.cif"),
                     ("Text file", "*.txt"))
        filename = fd.askopenfilename(title="Open origianl cif-file", initialdir="/", filetypes=filetypes)
        if filename:
            self.name = filename
            print(filename)

    def run(self):
        if (len(self.name)>0):
            self.text.delete(1.0, tk.END)
            result = self.cif_parser()
        else:
            self.text.insert(1.0,"First, select the file and destination directory")


    def cb(self, event):
        item_id = event.widget.identify_row(event.y) # Get the item ID
        tags = event.widget.item(item_id, "tags") # Get tags for the item
        #print(f"Item clicked! Item ID: {item_id}, Tags: {tags}")
        self.deletion = tags[0] 
        #print(self.deletion)
        
    def show(self):
        win = tk.Toplevel()
        win.wm_title("FCDB")
        db = Db()
        query = "select tab1.atom1, Atoms.atom1, tab1.NF, R1, R2, Param1, Param2, Ref from (select * FROM  Atoms, FCDB WHERE Atoms.id = FCDB.id_atom1) as tab1, Atoms WHERE Atoms.id = tab1.id_atom2"
        table = db.Query(query)
        db.ConnectionClose()
        columns = ("atom 1", "atom 2", "NF", "R_min", "R_max", "Param_1", "Param_2", "Ref")
        tree = ttk.Treeview(win, columns=columns, show="headings")
        tree.pack(fill=tk.BOTH, expand=1)
        tree.heading("atom 1", text="atom 1",anchor=tk.W)
        tree.heading("atom 2", text="atom 2",anchor=tk.W)
        tree.heading("NF", text="NF",anchor=tk.W)
        tree.heading("R_min", text="R_min",anchor=tk.W)
        tree.heading("R_max", text="R_max",anchor=tk.W)
        tree.heading("Param_1", text="Param_1",anchor=tk.W)
        tree.heading("Param_2", text="Param_2",anchor=tk.W)
        tree.heading("Ref", text="Ref",anchor=tk.W)
        tree.column("atom 1", stretch=tk.YES, width=60)
        tree.column("atom 2", stretch=tk.YES, width=60)
        tree.column("NF", stretch=tk.YES, width=60)
        tree.column("R_min", stretch=tk.YES, width=60)
        tree.column("R_max", stretch=tk.YES, width=60)
        tree.column("Param_1", stretch=tk.YES, width=60)
        tree.column("Param_2", stretch=tk.YES, width=60)
        tree.column("Ref", stretch=tk.YES, width=60)
        # добавляем данные
        for i,item in enumerate(table):
            tree.insert("", tk.END, values=item, tags=(item,"enable"))
        tree.tag_bind("enable", '<1>', self.cb)
        btn_add = tk.Button(win, text="Add to FCDB", command = self.add_note)
        btn_add.pack(side=tk.LEFT, pady=10, padx=6)
        btn_del = tk.Button(win, text="Delete from FCDB", command = self.del_note)
        btn_del.pack(side=tk.RIGHT, pady=10, padx=6)

        
    
    def del_note(self):
        if self.deletion != None:
            atom1 = self.deletion.split(" ")[0]
            atom2 = self.deletion.split(" ")[1]
            db = Db()
            query = 'SELECT FCDB.id from FCDB,(SELECT id FROM Atoms WHERE atom1 = "'+str(atom1)+'") as at1 LEFT JOIN (SELECT id FROM Atoms WHERE atom1 = "'+str(atom2)+'") as at2 where FCDB.id_atom1 = at1.id AND FCDB.id_atom2 = at2.id'
            table = db.Query(query)
            del_query = 'DELETE FROM FCDB WHERE FCDB.id='+str(table[0][0])
            table = db.Query(del_query)
            self.text.insert("end", "\nThe record was successfully deleted from the FCDB")
            db.ConnectionClose()
        


    def cif_parser(self):
        cif_file_name = self.name
        dic = {
            'name': '',
            'symmetry': '',
            'alpha': '',
            'beta': '',
            'gamma': '',
            'a': '',
            'b': '',
            'c': '',
            'label': [],
            'type_symbol': [],
            'x': [],
            'y': [],
            'z': []
        }
        cf = CifFile.ReadCif(cif_file_name)
        block = cf.first_block()
        try:
            dic['name'] = block['_chemical_formula_sum']
        except KeyError:
            dic['name'] = os.path.basename(self.name).split('.')[0]
            self.text.insert('end', "\nChemical properties are not specified in this file. The name is automatically assigned"+" "+dic['name'])
        try:
            dic['symmetry'] = block['_symmetry_space_group_name_H-M']
        except KeyError:
            try:
                dic['symmetry'] = block['_symmetry_space_group_name_H_M']
            except KeyError:
                try:
                    dic['symmetry'] = block['_space_group_name_H-M_alt']
                except KeyError:
                    return self.text.insert('end', "\nAn error occurred in defining the symmetry group")

        #if 'P -1' in dic['symmetry']:
        #    dic['symmetry'] = block['_symmetry_space_group_name_H-M'].replace(' ', '')
        if ':H' in dic['symmetry']:
            dic['symmetry'] = block['_symmetry_space_group_name_H-M'].replace(':', '')

        dic['alpha'] = re.sub(r'\([^()]*\)', '', block['_cell_angle_alpha'])

        dic['beta'] = re.sub(r'\([^()]*\)', '', block['_cell_angle_beta'])

        dic['gamma'] = re.sub(r'\([^()]*\)', '', block['_cell_angle_gamma'])

        dic['a'] = re.sub(r'\([^()]*\)', '', block['_cell_length_a'])

        dic['b'] = re.sub(r'\([^()]*\)', '', block['_cell_length_b'])

        dic['c'] = re.sub(r'\([^()]*\)', '', block['_cell_length_c'])

        lb = block.GetLoop('_atom_site_fract_x')

        label = lb.GetItemOrder()

        SYMBOL = 0

        for item in range(0, len(label)):
            if label[item] == '_atom_site_label':
                LABEL = item
            if label[item] == '_atom_site_type_symbol':
                SYMBOL = item
            if label[item] == '_atom_site_fract_x':
                X = item
            if label[item] == '_atom_site_fract_y':
                Y = item
            if label[item] == '_atom_site_fract_z':
                Z = item

        for atoms in lb:
            dic['label'].append(atoms[LABEL])
            dic['x'].append(re.sub(r'\([^()]*\)', '', atoms[X]))
            dic['y'].append(re.sub(r'\([^()]*\)', '', atoms[Y]))
            dic['z'].append(re.sub(r'\([^()]*\)', '', atoms[Z]))
            if SYMBOL != -1:
                dic['type_symbol'].append(atoms[SYMBOL])

        if len(dic['type_symbol']) == 0:
            for atom_name in range(0, len(dic['label'])):
                for c in dic['label'][atom_name]:
                    if c in nums:
                        dic['label'][atom_name] = dic['label'][atom_name].replace(c, '')
            num = Counter(dic['label'])
            for key in num:
                k = 1
                for atom_num in range(0, len(dic['label'])):
                    if key in dic['label'][atom_num] and k <= num[key] and len(dic['label'][atom_num])<2:
                        dic['label'][atom_num] = dic['label'][atom_num] + '_' + str(k)
                        k = k + 1
                    elif key in dic['label'][atom_num] and k <= num[key] and len(dic['label'][atom_num])>=2:
                        dic['label'][atom_num] = dic['label'][atom_num]+ str(k)
                        k = k + 1
        else:
            for atom_name in range(0, len(dic['type_symbol'])):
                for c in dic['type_symbol'][atom_name]:
                    if c in nums:
                        dic['type_symbol'][atom_name] = dic['type_symbol'][atom_name].replace(c, '')
            num = Counter(dic['type_symbol'])
            for key in num:
                k = 1
                for atom_num in range(0, len(dic['type_symbol'])):
                    if key in dic['type_symbol'][atom_num] and k <= num[key] and len(dic['type_symbol'][atom_num])<2:
                        dic['type_symbol'][atom_num] = dic['type_symbol'][atom_num] + '_' + str(k)
                        k = k + 1
                    elif key in dic['type_symbol'][atom_num] and k <= num[key] and len(dic['type_symbol'][atom_num])>=2:
                        dic['type_symbol'][atom_num] = dic['type_symbol'][atom_num] + str(k)
                        k = k+1

        #print(dic)
        #print(num)

        findir = self.name.split(self.name.split('/')[len(self.name.split('/'))-1])[0]

        if not os.path.isdir(findir  + dic['name']):
            os.mkdir(findir  + dic['name'])

        with open(findir  + dic['name'] + '/inp.ldy', "w+")as my_file:
            my_file.writelines([dic['name'] + '\n',
                                '\n',
                                'STRUCTURE:\n',
                                dic['symmetry'] + '\n',
                                dic['a'] + ',' + dic['b'] + ',' + dic['c'] + '\n',
                                dic['alpha'] + ',' + dic['beta'] + ',' + dic['gamma'] + '\n'])

            for atoms in range(0, len(dic['label'])):
                if SYMBOL == -1:
                    my_file.writelines(dic['label'][atoms] + '\n')
                    my_file.writelines(dic['x'][atoms] + ',' + dic['y'][atoms] + ',' + dic['z'][atoms] + ',' + '0' + '\n')
                else:
                    my_file.writelines(dic['type_symbol'][atoms] + '\n')
                    my_file.writelines(dic['x'][atoms] + ',' + dic['y'][atoms] + ',' + dic['z'][atoms] + ',' + '0' + '\n')

            txt = ""

            if self.checkbut:
                pairs_of_atoms = list(combinations_with_replacement(list(num), 2))
                pot1 = [tuple(elem) for elem in pairs_of_atoms]
                print(pot1)
                db = Db()
                db.AddContent("ATOMWORK", pot1)
                query = "select * from (select first_id, tab1.atom1, symbol_atom2, Atoms.id as sec_id FROM Atoms,(SELECT Atoms.id AS first_id, Atoms.atom1, ATOMWORK.symbol_atom2 FROM Atoms, ATOMWORK WHERE Atoms.atom1 = ATOMWORK.symbol_atom1) as tab1 WHERE Atoms.atom1 = tab1.symbol_atom2 order by first_id) as tab2 left JOIN FCDB as tab3 on (first_id=id_atom1 and sec_id=id_atom2) or (first_id=id_atom2 and sec_id=id_atom1);"
                notes = db.Query(query)
                for k in range(len(notes)):
                    if None in notes[k]:
                        continue
                    elif notes[k][7] == 1:
                        txt = txt+str(notes[k][1])+"*"+" "+str(notes[k][2])+"*"+" "+"BKE"+'\n'+str(notes[k][10])+", "+str(notes[k][11])+", "+str(notes[k][8])+", "+str(notes[k][9])+'\n'
                    elif notes[k][7] == 2:
                        txt = txt+str(notes[k][1])+" "+str(notes[k][2])+" "+"BKB"+'\n'+str(notes[k][10])+", "+str(notes[k][11])+", "+str(notes[k][8])+", "+str(notes[k][9])+'\n'
                    elif notes[k][7] == 3:
                        txt = txt + str(notes[k][1]) + " " + str(notes[k][2]) + " " + "BKE" + '\n' + str(notes[k][10]) + ", " + str(notes[k][11]) + ", " + str(notes[k][8]) + ", " + str(notes[k][9]) + '\n'

                db.DeleteContent("ATOMWORK")
                db.ConnectionClose()

                my_file.writelines(['end\n',
                                    '\n',
                                    'POTENTIAL:\n',
                                    'IAP\n',
                                    txt,
                                    'end\n',
                                    'END'
                                    ])
                final_text = "The file with the selected force constants has been successfully created and is located in the folder:"
            else:
                my_file.writelines(['end\n',
                                    '\n',
                                    'POTENTIAL:\n',
                                    'IAP\n',
                                    'ALL', ' ', 'ALL', ' ', 'BKE\n',
                                    '2, 4, 250.17, 0.1\n',
                                    'end\n',
                                    'END'
                                    ])
                final_text = "The file has been successfully created and is located in the folder:"
            return self.text.insert(1.0, final_text+findir + dic['name']+'\n'+txt)


if __name__ == "__main__":
    app = App()
    app.mainloop()
