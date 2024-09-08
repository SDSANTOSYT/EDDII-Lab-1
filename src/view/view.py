import customtkinter as ctk
class OptionWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry("1000x1000")
        self.title("Operaciones")
        self.titleLabel = ctk.CTkLabel(self, text="Operaciones", font=("Helvetica", 50, "bold")).place(y=30,relx=0.5, anchor="center")

        #lado superior izquierdo del cuadro
        self.leftUpFrame=ctk.CTkFrame(self,width=485,height=440,fg_color="#d4d3da")
        self.leftUpFrame.place(y=80,x=10)
        #Widgets del frame Superior Izquierdo
        self.insertEntry=ctk.CTkEntry(self.leftUpFrame, placeholder_text="Insertar pelicula", width=300,height=30)
        self.insertEntry.place(y=10,x=10)
        self.btnEntry=ctk.CTkButton(self.leftUpFrame, text="Insertar", corner_radius=40, font=("Helvetica", 20, "bold"))
        self.btnEntry.place(y=10,x=320)
        #lado inferior izquierdo
        self.leftDownFrame=ctk.CTkFrame(self,width=485,height=450,fg_color="#d4d3da")
        self.leftDownFrame.place(y=530,x=10)
        #Widgets del frame Inferior Izquierdo
        self.DeleteEntry=ctk.CTkEntry(self.leftDownFrame, placeholder_text="Eliminar pelicula", width=300,height=30)
        self.DeleteEntry.place(y=10,x=10)
        self.btnDelete=ctk.CTkButton(self.leftDownFrame, text="Eliminar", corner_radius=40, font=("Helvetica", 20, "bold"))
        self.btnDelete.place(y=10,x=320)

        #lado derecho del cuadrado
        self.rightFrame=ctk.CTkFrame(self, width=485,height=900,fg_color="#d4d3da")
        self.rightFrame.place(y=80,x=505)
        #Widgets del frame derecho
        #Buscar
        self.searchEntry=ctk.CTkEntry(self.rightFrame,placeholder_text="Buscar Pelicula", width=300,height=30)
        self.searchEntry.place(y=10,x=10)
        self.btnSearch=ctk.CTkButton(self.rightFrame, text="Buscar", corner_radius=40, font=("Helvetica", 20, "bold"))
        self.btnSearch.place(y=10,x=320)
        #Filtros
        self.var_percentCheck=ctk.BooleanVar()
        self.percentCheck=ctk.CTkCheckBox(self.rightFrame, text="Ingresos nacional menor a ingresos internacional", variable=self.var_percentCheck, width=50, height=50)
        self.percentCheck.place(y=50,x=10)

        self.slider = ctk.CTkSlider(self.rightFrame, from_=0, to=10000000, command=self.changeSliderValue)
        self.slider.set(0)
        self.slider.place(y=100,x=10)
        self.value=self.slider.get()
        self.sliderValue= ctk.CTkLabel(self.rightFrame, text="", font=("Helvetica", 10, "bold"))
        self.sliderValue.place(y=95,x=300)


        self.var_yearCheck=ctk.BooleanVar()
        self.yearCheck=ctk.CTkCheckBox(self.rightFrame, text="Año", variable=self.var_yearCheck, width=50, height=50)
        self.yearCheck.place(y=120,x=10)
        self.yearEntry=ctk.CTkEntry(self.rightFrame,placeholder_text="año de estreno", width=120,height=30)
        self.yearEntry.place(y=130,x=80)


        #Cuadrado inferior derecho para dar
        self.frameDownRigth=ctk.CTkFrame(self.rightFrame,width=485, height=180, fg_color="#6d5eb2")
        self.frameDownRigth.place(y=720,x=0)
        #Datos del cuadrado
        self.nodeLevelLbl=ctk.CTkLabel(self.frameDownRigth, text="Nivel del nodo", font=("Helvetica", 20, "bold"))
        self.nodeLevelLbl.place(y=2)
        self.balanceLbl=ctk.CTkLabel(self.frameDownRigth, text="Factor de balanceo", font=("Helvetica", 20, "bold"))
        self.balanceLbl.place(y=32)
        self.fatherLbl=ctk.CTkLabel(self.frameDownRigth, text="Padre del nodo", font=("Helvetica", 20, "bold"))
        self.fatherLbl.place(y=62)
        self.gfatherLbl=ctk.CTkLabel(self.frameDownRigth, text="Abuelo del nodo", font=("Helvetica", 20, "bold"))
        self.gfatherLbl.place(y=92)
        self.uncleLbl=ctk.CTkLabel(self.frameDownRigth, text="Tio del nodo", font=("Helvetica", 20, "bold"))
        self.uncleLbl.place(y=122)


    def changeSliderValue(self, value):
        self.sliderValue.configure(text=str(value))
        





class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Film Three")
        self.geometry('1700x1000')
        ctk.set_appearance_mode('light')
        self.btnOption=ctk.CTkButton(self,width=830,height=980,corner_radius=50,text="Operaciones", fg_color="#6d5eb2",font=("Helvetica", 50, "bold"),command=self.openOptionWindow)
        self.btnOption.place(y=10,x=10)
        self.btnSeeTree=ctk.CTkButton(self,width=830,height=980,corner_radius=50,text="Ver Arbol", fg_color="#6d5eb2",font=("Helvetica", 50, "bold"))
        self.btnSeeTree.place(y=10,x=850)
        self.Option_window=None

        


        


        self.mainloop()


    def openOptionWindow(self):
        if self.Option_window is None or not self.Option_window.winfo_exists():
            self.Option_window = OptionWindow(self)  # create window if its None or destroyed
        else:
            self.Option_window.focus()  # if window exists focus it
if __name__=='__main__':
    app=App()

