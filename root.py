from tkinter import Tk , Label , Entry, Button , FALSE , END , TRUE , ttk , NORMAL  , messagebox
import sqlite3
import webbrowser



conn = sqlite3.connect("BLOODBANK.db")
c = conn.cursor()

latitude = ''
longitude = ''

#when search button pressed
def search():
    b_type = entry_type.get().upper()
    area = entry_area.get().upper()

    #delete everthing in tree
    for each in tree.get_children():
        tree.delete(each)

    #filter by both area and type
    if area!='' and b_type!='':
        if b_type == "A+":
            b_type = "A_p"
            
        elif b_type == "A-":
            b_type = "A_n"

        elif b_type == "B+":
            b_type = "B_p"
        elif b_type == "B-":
            b_type = "B_n"

        elif b_type == "O+":
            b_type = "O_p"
        elif b_type == "O-":
            b_type = "O_n"

        elif b_type == "AB+":
            b_type = "AB_p"
        elif b_type == "AB-":
            b_type = "AB_n"

        else:
            messagebox.showinfo('ERROR','Blood Type should be A-,A+,B-,B+,AB-,AB+,O-,O+')
            print('here')
            return

        sql = "select ID,NAME,X,Y from BANK where AREA = '"+area+"'"
        c.execute(sql)
        data = c.fetchone()
        print(data)

        if data == None:
            messagebox.showinfo('ERROR','Area not found')
            return
        
        sql = "select * from STOCK WHERE BANK_ID = "+str(data[0])+" and "+b_type+" > 0"
        c.execute(sql)
        stocks = c.fetchall()

    
        for each in stocks:
            tree_val = (data[1],area,each[2],each[3],each[4],each[5],each[6],each[7],each[8],each[9],data[2],data[3])
            tree.insert('',END , values= tree_val )    

    #filter by type
    elif b_type!="":
        if b_type == "A+":
            b_type = "A_p"
        elif b_type == "A-":
            b_type = "A_n"

        elif b_type == "B+":
            b_type = "B_p"
        elif b_type == "B-":
            b_type = "B_n"

        elif b_type == "O+":
            b_type = "O_p"
        elif b_type == "O-":
            b_type = "O_n"

        elif b_type == "AB+":
            b_type = "AB_p"
        elif b_type == "AB-":
            b_type = "AB_n"

        else:
            messagebox.showinfo('ERROR','Blood Type should be A-,A+,B-,B+,AB-,AB+,O-,O+')
            return

        sql = "select * from STOCK where "+b_type+" >0 "
        c.execute(sql)
        data = c.fetchall()

        if data == []:
            return

        for each in data:
            sql = "select ID,NAME,AREA,X,Y from BANK where ID = "+str(each[1])
            c.execute(sql)
            bank = c.fetchone()
            tree_val = (bank[1] , bank[2] , each[2],each[3],each[4],each[5],each[6],each[7],each[8],each[9] , bank[3] , bank[4])
            tree.insert('',END , values= tree_val) 

        


    #filter by area
    elif area!="":
        sql = "select ID,NAME,AREA,X,Y from BANK where AREA = '"+area+"'"
        c.execute(sql)
        data = c.fetchall()
        if data == []:
            messagebox.showinfo('ERROR','Area not found')
            return

        for each in data:
           
            sql = "select * from STOCK where BANK_ID = "+str(each[0])
            c.execute(sql)
            stocks = c.fetchone() 
            tree_val = (each[1],each[2],stocks[2],stocks[3],stocks[4],stocks[5],stocks[6],stocks[7],stocks[8],stocks[9],each[3],each[4])
            tree.insert('',END , values = tree_val)


#when view map button is pressed
def view_map():
    if latitude =="" or longitude =="":
        messagebox.showinfo('ERROR','Select Bank')
        return
    
    query = "https://www.google.com/maps/search/?api=1&query="+latitude+","+longitude
    print(query)
    webbrowser.open_new_tab(query)


#when item fom treeview is selected , latitude and longitudes aere stored
def enable_map(e):
    global latitude , longitude
    try:
        latlong = tree.focus()
        latlong = tree.item(latlong)
        latlong = latlong['values']
        latitude = latlong[10]
        longitude = latlong[11]
        
    except:
        pass



root = Tk()
root.geometry("1000x700")
style = ttk.Style()


Label(root , text = "Blood Type :-" , font = (14)).place(x = 20 , y = 20)
Label(root , text = "Area            :-" , font = (14)).place(x = 20 , y = 50)

entry_type = Entry(root , width = 10 , font = (14))
entry_area = Entry(root , width = 10 , font = (14))
btn_search = Button(root , text = "Search" , command = search)


tree = ttk.Treeview(root , height = 18  )
scroll = ttk.Scrollbar(root , orient = "vertical" , command = tree.yview)
tree.tag_configure('odd', background='#ebc3b7')
tree.tag_configure('even', background='#f4e0cd')
tree.configure(yscrollcommand = scroll.set)

tree.bind('<Double-Button-1>',enable_map)
#tree.bind('<Button-1>',enable_map)


tree['columns'] = ('0','1','2','3','4','5','6','7','8','9')
tree.column("#0" , width = 0)

tree.column('0' , width = 300 , anchor = "w" )
tree.heading('0' , text = 'Name' , anchor = 'w')

tree.column('1' , width = 200, anchor = "w")
tree.heading('1' , text = 'Area' , anchor = 'w')

tree.column('2' , width = 50 , anchor = "w")
tree.heading('2' , text = 'A+' , anchor = 'c')


tree.column('3' , width = 50, anchor = "w")
tree.heading('3' , text = 'A-' , anchor = 'c')

tree.column('4' , width = 50 , anchor = "w")
tree.heading('4' , text = 'B+' , anchor = 'c')


tree.column('5' , width = 50, anchor = "w")
tree.heading('5' , text = 'B-' , anchor = 'c')


tree.column('6' , width = 50 , anchor = "w")
tree.heading('6' , text = 'O+' , anchor = 'c')


tree.column('7' , width = 50, anchor = "w")
tree.heading('7' , text = 'O-' , anchor = 'c')


tree.column('8' , width = 50 , anchor = "w")
tree.heading('8' , text = 'AB+' , anchor = 'c')


tree.column('9' , width = 60, anchor = "w")
tree.heading('9' , text = 'AB-' , anchor = 'c')



btn_map = Button(text = "View in Maps" , command = view_map)


entry_type.place(x = 130 , y = 20)
entry_area.place(x = 130 , y = 50)
btn_search.place(x = 250 , y = 35)
tree.place(x = 20 , y = 120)
scroll.place(x = 933 , y = 120 , height = 387)
btn_map.place(x = 400 , y = 580)

root.mainloop()


