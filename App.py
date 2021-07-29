import mysql.connector as connector
from tkinter import *
import tkinter as tk
from tkinter.scrolledtext import *
from tkinter import ttk, messagebox, filedialog
import csv
import os
from unitconvert import lengthunits, massunits

# =========================================================== #
# ==================== Button function ====================== #
# =========================================================== #
def clear_fields():         # clear the fileds 
    ent1.delete(0, END)
    ent2.delete(0, END)
    ent3.delete(0, END)
    ent4.delete(0, END)
    ent5.delete(0, END)
    ent2.focus()

con = connector.connect(     # Database Connection
        host = "localhost",
        user = 'root',
        password = 'rootpassword',
        database = 'BMI',
        auth_plugin='mysql_native_password',
    )
cursor = con.cursor()

# =================== Section 1 ================================= #
mydata = []

def getrow(event):          # get the data of row when double clicked
    item = trv.item(trv.focus())
    t1.set(item['values'][0])
    t2.set(item['values'][1])
    t3.set(item['values'][2])
    t4.set(item['values'][3])
    t5.set(item['values'][4])

def update_display(rows):   # Update the display 
    global mydata
    mydata = rows
    trv.delete(*trv.get_children())
    for i in rows:
        trv.insert("", 'end', values = i)

def export_csv():
    if len(mydata) < 1:
        messagebox.showerror("Error!", "No Data To Export!")
        return False
    fln = filedialog.asksaveasfilename(initialdir = os.getcwd(), title = "Save CSV", filetypes=(("CSV File", "*.csv"), ("All Files", "*.*")))
    with open(fln, mode = "w") as myfile:
        exp_writer = csv.writer(myfile, delimiter = ",")
        for i in mydata:
            exp_writer.writerow(i)
    messagebox.showinfo("Success!", "Your Data has been Exported Successfully to \n{}".format(os.path.abspath(fln)))

def import_csv():
    mydata.clear()
    fln = filedialog.askopenfilename(initialdir = os.getcwd(), title = "Open CSV", filetypes = (("CSV File", "*.csv"), ("All Files", "*.*")))
    with open(fln) as myfile:
        csv_reader = csv.reader(myfile, delimiter = ",")
        for i in csv_reader:
            mydata.append(i)
    update_display(mydata)

def save_data():
    if messagebox.askyesno("Confirmation!", "Are you sure want to save this data into your database?"):
        for i in mydata:
            fn = str(i[1])
            ln = str(i[2])
            h = float(i[3])
            w = float(i[4])
            query = "INSERT INTO user(id, f_name, l_name, height, weight) values(NULL, '{}', '{}', {}, {})".format(fn, ln, h, w)
            cursor.execute(query)
        con.commit()
        clear_screen()
        messagebox.showinfo("Success!", "Your data has been saved to the Database!")

def clear_data():
    if messagebox.askyesno("Confirmation!", "Are you sure want to Delete all the user Information?"):
        try:
            query = "TRUNCATE TABLE user;"
            cursor.execute(query)
            con.commit()
            clear_screen()
            messagebox.showinfo("Success!", "All the user data has been deleted from the Database!")
        except Exception as e:
            messagebox.showerror("Error!", e)

# =================== Section 2 ================================= #
def search_user():              # Search user and display
    q2 = q.get()
    if q2 == "":
        messagebox.showerror("Error!", "Please Enter a Search String")
    elif not q2.isalpha():
        messagebox.showerror("Error!", "Please Search using valid First Name")
    else:
        query = "SELECT * FROM user WHERE f_name = '{}'".format(q2)
        cursor.execute(query)
        rows = cursor.fetchall()
        update_display(rows)
    
def clear_screen():             # Clear the Search filter
    query = "SELECT * FROM user;"
    cursor.execute(query)
    rows = cursor.fetchall()
    update_display(rows)
    entSEARCH.delete(0, END)
    clear_fields()
    entSEARCH.focus()

# =================== Section 3 functions ================== #
def add_user():                 # ADD new user
    try:
        fn = t2.get()
        ln = t3.get()
        h = float(t4.get())
        w = float(t5.get())
        bmi = float(w/(h**2))
        query = """INSERT INTO user(id, f_name, l_name, height, weight)
                VALUES(NULL, '{}', '{}', {}, {});""".format(fn, ln, h, w)
        cursor.execute(query)
        con.commit()
        messagebox.showinfo("Success", "Hi {} your BMI is {}".format(fn, round(bmi,2)))
        clear_screen()
        clear_fields()
    except connector.Error as e:
        print(e)
        if e.errno == 1264 and e.msg == "Out of range value for column 'weight' at row 1":
            messagebox.showerror("Error!", "Weight not possible!")
        elif e.errno == 1264 and e.msg == "Out of range value for column 'height' at row 1":
            messagebox.showerror("Error!", "Height not Possible!")
        elif e.errno == 1644:
            messagebox.showerror("Error!", e.msg)
        elif e.errno == 3819:
            messagebox.showerror("Error!", "Name should not be less than 2 characters!")
    except ValueError as e:
        print(e)
        messagebox.showerror("Error!","Height and Weight must be a number")
    except Exception as e:
        print(e)
        messagebox.showerror("ERROR!", e)
    
        

def update_user():              # Update existing user
    try:
        id = t1.get()
        fn = t2.get()
        ln = t3.get()
        h = float(t4.get())
        w = float(t5.get())
        bmi = float(w/(h**2))
        if messagebox.askyesno("Confirm Update?", "Are you sure want to update the user?"):
            query = """UPDATE user
                SET f_name = '{}', l_name = '{}', height = {}, weight = {}
                WHERE id = {};
                """.format(fn, ln, h, w, id)
            cursor.execute(query)
            con.commit()
            messagebox.showinfo("Success", "Hi {} your BMI is {}".format(fn, round(bmi,2)))
            clear_screen()
            clear_fields()
    except connector.Error as e:
        print(e)
        if e.errno == 1264 and e.msg == "Out of range value for column 'weight' at row 1":
            messagebox.showerror("Error!", "Weight not possible!")
        elif e.errno == 1264 and e.msg == "Out of range value for column 'height' at row 1":
            messagebox.showerror("Error!", "Height not Possible!")
        elif e.errno == 1644:
            messagebox.showerror("Error!", e.msg)
        elif e.errno == 3819:
            messagebox.showerror("Error!", "Name should not be less than 2 characters!")
    except ValueError as e:
        print(e)
        messagebox.showerror("Error!","Height and Weight must be a number")
    except Exception as e:
        messagebox.showerror("Error!", e)


def delete_user():              # Delete Existing User
    id = t1.get()
    if messagebox.askyesno("Confirm Delete?", "Are you sure want to delete the user?"):
        try:
            query = "DELETE FROM user WHERE id = {};".format(id)
            cursor.execute(query)
            con.commit()
            clear_screen()
        except Exception as e:
            messagebox.showerror("Error!", e)
            con.rollback()
    clear_fields()

def open_manual():
    root.withdraw()
    user_manual.deiconify()
    user_manual_DISPLAY.delete(1.0, END)
    instructions = [
        "While Adding new user dont fill the UserID field, as it is produced by the System itself.",
        "While Updating the existsing user fill all the fields.",
        "While Deleteing the existsing user only UserID field is requiered.",
        "To Select the data from the User List section double click on the user row you want to get the data.",
        "First name and Last name must contain only alphabets and no numbers or special characters.",
        "Height and Weight must be in meters and no anyother units are valid"
        ]
    x = 1
    info = "Instructions:"
    for i in instructions:
        info += "\n {}) {}".format(x,i)
        x += 1
    user_manual_DISPLAY.insert(INSERT, info)

def close_manual():
    user_manual.withdraw()
    root.deiconify()
# ==================== Section 4 ======================= #
def get_height():
    try:
        a = lengthunits.LengthUnit(h.get(), f'{variable.get()}', 'm').doconvert()
        meters.set("{} meters".format(round(a,2)))
    except Exception:
        messagebox.showerror("Error!", "Invalid Input!")

def get_weight():
    try:
        a = massunits.MassUnit(w.get(), f'{variable2.get()}', 'kg').doconvert()
        kgs.set("{} kgs".format(round(a,2)))
    except Exception:
        messagebox.showerror("Error!", "Invalid Input!")

# ==================== GUI Window ======================= #
# GUI Window:
root = Tk()

wrapper1 = LabelFrame(root, text="User List")
wrapper2 = LabelFrame(root, text="Search")
wrapper3 = LabelFrame(root, text = "User Data")
wrapper4 = LabelFrame(root, text='convert')

wrapper1.pack(fill = X, expand = True, ipady = 10, padx = 20, pady = 5)
wrapper2.pack(fill = BOTH, expand = True, ipady = 10, padx = 20, pady = 5)
wrapper3.pack(fill = BOTH, expand = True, ipady = 10, padx = 5, pady = 5, side = LEFT)
wrapper4.pack(fill = BOTH, expand = True, ipady = 10, padx = 5, pady = 5, side = LEFT)

trv = ttk.Treeview(wrapper1, columns=(1,2,3,4,5,6), show='headings', height='7')
trv.pack()


trv.heading(1, text="User ID")
trv.heading(2, text="Frist Name")
trv.heading(3, text="Last Name")
trv.heading(4, text="Height")
trv.heading(5, text="Weight")
trv.heading(6, text="BMI")

trv.bind('<Double 1>', getrow)
trv.column(1, width = 90)
trv.column(2, width = 160)
trv.column(3, width = 160)
trv.column(4, width = 110)
trv.column(5, width = 110)
trv.column(6, width = 110)

query = "SELECT * FROM user;"
cursor.execute(query)
rows = cursor.fetchall()
update_display(rows)

# ================= User List SECTION ========================== #
btnEXPORT = Button(wrapper1, text = "Export", font=(None,12,'bold'), command = export_csv)
btnIMPORT = Button(wrapper1, text = "Import", font=(None,12,'bold'), command = import_csv)
btnSAVE = Button(wrapper1, text = "Save Data", font=(None,12,'bold'), command = save_data)
btnCLEARDATA = Button(wrapper1, text = "Clear Data", font=(None,12,'bold'), command = clear_data)
btnEXIT = Button(wrapper1, text = "Exit", font=(None,12,'bold'), command = lambda: exit())

btnEXPORT.pack(side = LEFT, padx = 10, pady = 10, ipadx = 5, ipady = 5)
btnIMPORT.pack(side = LEFT, padx = 10, pady = 10, ipadx = 5, ipady = 5)
btnSAVE.pack(side = LEFT, padx = 10, pady = 10, ipadx = 5, ipady = 5)
btnCLEARDATA.pack(side = LEFT, padx = 10, pady = 10, ipadx = 5, ipady = 5)
btnEXIT.pack(side = LEFT, padx = 10, pady = 10, ipadx = 5, ipady = 5)
# ================= SEARCH SECTION ========================== #
q = StringVar()
lblSEARCH = Label(wrapper2, text = "Search by First Name: ", font=(None,12,'bold'))
entSEARCH = Entry(wrapper2, textvariable = q, font=(None,12,'bold'))
btnSEARCH = Button(wrapper2, text = 'Search', font=(None,12,'bold'), command = search_user)
btnCLEARSEARCH = Button(wrapper2, text = "Clear Search", font=(None,12,'bold'), command = clear_screen)

lblSEARCH.pack(side = LEFT, padx = 10)
entSEARCH.pack(side = LEFT, padx = 10)
btnSEARCH.pack(side = LEFT, padx = 10, ipadx = 5, ipady = 5)
btnCLEARSEARCH.pack(side = LEFT, padx = 10, pady = 10, ipadx = 5, ipady = 5)

# ================== USER DATA section =========================== #
t1 = IntVar()
lbl1 = Label(wrapper3, text="User ID", font=(None,12,'bold'))
ent1 = Entry(wrapper3, textvariable = t1, font=(None,12,'bold'))
lbl1.grid(row = 0, column = 0, padx = 10, pady = 6, sticky = 'E')
ent1.grid(row = 0, column = 1, padx = 10, pady = 6, sticky = 'W', columnspan = 2)

t2 = StringVar()
lbl2 = Label(wrapper3, text="First Name", font=(None,12,'bold'))
ent2 = Entry(wrapper3, textvariable = t2, font=(None,12,'bold'))
lbl2.grid(row = 1, column = 0, padx = 10, pady = 6, sticky = 'E')
ent2.grid(row = 1, column = 1, padx = 10, pady = 6, sticky = 'W', columnspan = 2)

t3 = StringVar()
lbl3 = Label(wrapper3, text="Last Name", font=(None,12,'bold'))
ent3 = Entry(wrapper3, textvariable = t3, font=(None,12,'bold'))
lbl3.grid(row = 2, column = 0, padx = 10, pady = 6, sticky = 'E')
ent3.grid(row = 2, column = 1, padx = 10, pady = 6, sticky = 'W', columnspan = 2)

t4 = Variable()
lbl4 = Label(wrapper3, text="Height (m)", font=(None,12,'bold'))
ent4 = Entry(wrapper3, textvariable = t4, font=(None,12,'bold'))
lbl4.grid(row = 3, column = 0, padx = 10, pady = 6, sticky = 'E')
ent4.grid(row = 3, column = 1, padx = 10, pady = 6, sticky = 'W', columnspan = 2)

t5 = Variable()
lbl5 = Label(wrapper3, text="Weight (kg)", font=(None,12,'bold'))
ent5 = Entry(wrapper3, textvariable = t5, font=(None,12,'bold'))
lbl5.grid(row = 4, column = 0, padx = 10, pady = 6, sticky = 'E')
ent5.grid(row = 4, column = 1, padx = 10, pady = 6, sticky = 'W', columnspan = 2)

btnADD = Button(wrapper3, text='ADD', font=(None,12,'bold'), command = add_user)
btnUPDATE = Button(wrapper3, text='UPDATE', font=(None,12,'bold'), command = update_user)
btnDELETE = Button(wrapper3, text='DELETE', font=(None,12,'bold'), command = delete_user)
btnINSTRUCTION = Button(wrapper3, text='User Manual', font=(None,12,'bold'), command = open_manual)

btnADD.grid(row = 5, column = 0, padx = 10, pady = 6, ipadx = 5, ipady = 5)
btnUPDATE.grid(row = 5, column = 1, padx = 10, pady = 6, ipadx = 5, ipady = 5)
btnDELETE.grid(row = 5, column = 2, padx = 10, pady = 6, ipadx = 5, ipady = 5)
btnINSTRUCTION.grid(row = 6, column = 0, columnspan = 3, padx = 10, pady = 6, ipadx = 5, ipady = 5)

# ===================== Section 4 ===================================== #
lblCONVERT = Label(wrapper4, text = "Convert Height from", font=(None,12,'bold'))
lblCONVERT.grid(row = 0, columnspan=3, padx = 10, pady = 5, ipadx = 5, ipady = 5)

h = DoubleVar()
entHEIGHT = Entry(wrapper4, textvariable = h)
entHEIGHT.grid(row = 2, column = 0, padx = 10, pady = 5, ipadx = 5, ipady = 5)

units_height = ['cm', 'mm', 'in', 'ft']
variable = StringVar(wrapper4)
variable.set(units_height[0])
dropHEIGHT = OptionMenu(wrapper4, variable, *units_height)
dropHEIGHT.grid(row = 2, column = 1, padx = 10, pady = 5, ipadx = 5, ipady = 5)

meters = Variable()
lblMETERS = Label(wrapper4, textvariable = meters, font=(None,12,'bold italic'))
lblMETERS.grid(row = 1, columnspan = 3, padx = 10, pady = 5, ipadx = 5, ipady = 5)

btnHEIGHT = Button(wrapper4, text = "Height", font=(None,12,'bold'), command = get_height)
btnHEIGHT.grid(row = 2, column = 3, padx = 10, pady = 5, ipadx = 5, ipady = 5)

#################################
lblCONVERT2 = Label(wrapper4, text = "Convert Weight from", font=(None,12,'bold'))
lblCONVERT2.grid(row = 4, columnspan=3, padx = 10, pady = 5, ipadx = 5, ipady = 5)

w = DoubleVar()
entWEIGHT = Entry(wrapper4, textvariable = w)
entWEIGHT.grid(row = 6, column = 0, padx = 10, pady = 5, ipadx = 5, ipady = 5)

units_weight = ['g', 'lb', 'oz']
variable2 = StringVar(wrapper4)
variable2.set(units_weight[0])
dropWEIGHT = OptionMenu(wrapper4, variable2, *units_weight)
dropWEIGHT.grid(row = 6, column = 1, padx = 10, pady = 5, ipadx = 5, ipady = 5)

kgs = Variable()
lblKGS = Label(wrapper4, textvariable = kgs)
lblKGS.grid(row = 5, columnspan = 3, padx = 10, pady = 10, ipadx = 5, ipady = 5)

btnWEIGHT = Button(wrapper4, text = "Weight", font=(None,12,'bold'), command = get_weight)
btnWEIGHT.grid(row = 6, column = 3, padx = 10, pady = 10, ipadx = 5, ipady = 5)

# ==================== User manual ======================= #
user_manual = Toplevel(root)
user_manual.geometry("1100x370")
user_manual.title("User Manual")

user_manual_DISPLAY = Text(user_manual, width = 110, height = 10, font = ("times new roman", 15))
user_manual_btnCLOSE = Button(user_manual, text = "CLOSE", width = 10, font = ('arial', 18, 'bold'), fg="white", bg="#FF8000", command = close_manual)
user_manual_DISPLAY.pack(padx = 10, pady = 10)
user_manual_btnCLOSE.pack(padx = 10, pady = 10)

user_manual.withdraw()

root.title("BMI App")
root.geometry("800x700")
root.mainloop()
