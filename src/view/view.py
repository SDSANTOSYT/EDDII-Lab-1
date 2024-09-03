import customtkinter as ctk
from PIL import *

class AnimatedSideBar(ctk.CTkFrame):
    def __init__(self, parent, color, cuadro:ctk.CTkFrame):
        self.width=90
        self.height=980
        self.cuadro=cuadro
        super().__init__(parent, fg_color=color, width=self.width, height=self.height, corner_radius=25)
        self.place(x=14, y=10)
        self.close=False
        self.optionsBtn=ctk.CTkButton(master=self,height=50, width=50, corner_radius=50,text="",command=self.Animation)
        self.optionsBtn.place(x=20, y=30)
        self.NameLbl=ctk.CTkLabel(master=self, text="Film Three",font=("Helvetica", 50, "bold"))
        self.NameLbl.place(x=90,y=30)

    def Animation(self):
        if not self.close and self.width==90:
            self.increaseSize()
            self.close=True
            print(self.width)
            
        elif self.width==440:
            self.decreasSize()
            self.close=False
            print(self.width)
            

    def increaseSize(self):
        if self.width<440:
            self.width+=2
            self.configure(width=self.width)
            self.cuadro.configure(width=1570-(20+(self.width-111)))
            self.cuadro.place(x=20+self.width)
            self.after(1,self.increaseSize)    
           
    def decreasSize(self):
        if self.width>90:
            self.width-=2
            self.configure(width=self.width)
            self.cuadro.configure(width=1570-(20+(self.width-111)))
            self.cuadro.place(x=20+self.width)
            self.after(1,self.decreasSize)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Film Three")
        self.geometry('1700x1000')
        ctk.set_appearance_mode('light')

        self.marcoPrueba=ctk.CTkFrame(self, width=1570,height=980, corner_radius=25, fg_color="#E77070")
        self.marcoPrueba.place(x=110,y=10)
        self.marcoPrueba.lower()
        self.bar=AnimatedSideBar(self, "#6d5eb2", self.marcoPrueba)
        self.bar.lift()

        

        self.mainloop()

if __name__=='__main__':
    app=App()


