from PIL import Image
from graphviz import Digraph
import os

import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from controller.dataset_manager import *
from controller.tree_manager import *
import customtkinter as ctk

import re

def escape_node_name(name):
    return re.sub(r'[:\s]', ' ', name)

current_image = None
def open_image(image_path):
    global current_image
    try:
        # Cerrar la imagen abierta si existe
        if current_image is not None:
            current_image.close()
        
        # Intentar abrir la nueva imagen
        current_image = Image.open(image_path)
        return current_image
    
    except FileNotFoundError:
        print(f"Error: El archivo '{image_path}' no existe.")
        current_image = None
        return None




class OptionWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        self.geometry("1600x1000")
        self.title("Operaciones")    
        self.configure(fg_color="white")
        self.titleLabel = ctk.CTkLabel(self, text="Operaciones", font=("Times", 50, "bold")).place(y=40,relx=0.5, anchor="center")

        #lado superior izquierdo del cuadro
        self.leftUpFrame=ctk.CTkFrame(self,width=485,height=440,fg_color="#fbf2e1")
        self.leftUpFrame.place(y=80,x=10)
        #Widgets del frame Superior Izquierdo
        #insertar nodos
        self.insertEntry=ctk.CTkEntry(self.leftUpFrame, placeholder_text="Insertar pelicula",font=("Times", 15,), width=300,height=30)
        self.insertEntry.place(y=10,x=10)
        self.result_frameI = ctk.CTkScrollableFrame(self.leftUpFrame, width=485, height=390, fg_color="#fbf2e1")
        self.result_frameI.place(y=50, x=10)
        self.insertEntry.bind("<KeyRelease>", lambda event: self.update_list(self.insertEntry, self.result_frameI, search_movie(self.insertEntry.get()), self.result_labels))
        self.result_labels = [] # Lista para guardar los labels que muestran los resultados
        self.btnEntry=ctk.CTkButton(self.leftUpFrame, text="Insertar",hover_color="#e9e9e9", corner_radius=40,fg_color="white", text_color="#9f4154",border_color="#9f4154",font=("Times", 20, "bold"), command=lambda:self.search_Ui(self.insertEntry.get()))
        self.btnEntry.place(y=10,x=320)
        self.warning=ctk.CTkLabel(self.leftUpFrame, text="", font=("Times", 12, "bold"))
        self.warning.place(y=40,x=320)
        

        #lado inferior izquierdo
        self.leftDownFrame=ctk.CTkFrame(self,width=485,height=450,fg_color="#fbf2e1")
        self.leftDownFrame.place(y=530,x=10)
        #Widgets del frame Inferior Izquierdo
        #Eliminar
        self.DeleteEntry=ctk.CTkEntry(self.leftDownFrame, placeholder_text="Eliminar pelicula", font=("Times", 15,),width=300,height=30)
        self.DeleteEntry.place(y=10,x=10)
        self.result_frameD = ctk.CTkScrollableFrame(self.leftDownFrame, width=485, height=390, fg_color="#fbf2e1")
        self.result_frameD.place(y=50, x=10)

        self.DeleteEntry.bind("<KeyRelease>", lambda event: self.update_list(self.DeleteEntry, self.result_frameD, search_in_tree(), self.result_labels))
        self.btnDelete=ctk.CTkButton(self.leftDownFrame, text="Eliminar", hover_color="#e9e9e9",corner_radius=40,fg_color="white", text_color="#9f4154",border_color="#9f4154",font=("Times", 20, "bold"),command=lambda: self.delete_Ui(self.DeleteEntry.get()))
        self.btnDelete.place(y=10,x=320)
        

        #lado central del cuadrado
        self.centerFrame=ctk.CTkFrame(self, width=485,height=900,fg_color="#fbf2e1")
        self.centerFrame.place(y=80,x=505)
        #Widgets del frame central
        #Buscar
        self.searchEntry=ctk.CTkEntry(self.centerFrame,placeholder_text="Buscar Pelicula",font=("Times", 15,), width=300,height=30)
        self.searchEntry.place(y=10,x=10)

        self.result_frameE = ctk.CTkScrollableFrame(self.centerFrame, width=485, height=380, fg_color="#fbf2e1")
        self.result_frameE.place(y=220, x=10)
        self.levelsBtn=ctk.CTkButton(self.centerFrame,text="Recorrido por niveles",fg_color="white",hover_color="#e9e9e9", text_color="#9f4154",border_color="#9f4154",corner_radius=40, font=("Times", 20, "bold"),command=self.show_data)
        self.levelsBtn.place(y=870,relx=0.5,anchor="center")


        self.searchEntry.bind("<KeyRelease>", lambda event: self.update_list2(self.searchEntry, self.result_frameE, search_filter(bool(self.yearCheck.get()),self.yearEntry.get(),bool(self.percentCheck.get()),bool(self.intIncomeCheck.get()),self.intIncome.get(),self.searchEntry.get()), self.result_labels))
        self.btnSearch=ctk.CTkButton(self.centerFrame, text="Buscar",fg_color="white",hover_color="#e9e9e9", text_color="#9f4154",border_color="#9f4154",corner_radius=40, font=("Times", 20, "bold"), command=self.fillData)
        self.btnSearch.place(y=10,x=320)
        #Filtros
        self.var_percentCheck=ctk.BooleanVar()
        self.percentCheck=ctk.CTkCheckBox(self.centerFrame, text="Ingresos nacional menor a ingresos internacional",font=("Times", 15,),variable=self.var_percentCheck, hover_color= "#9f4154" ,width=50, height=50, command= lambda: self.update_list2(self.searchEntry, self.result_frameE, search_filter(bool(self.yearCheck.get()),self.yearEntry.get(),bool(self.percentCheck.get()),bool(self.intIncomeCheck.get()),self.intIncome.get(),self.searchEntry.get()), self.result_labels))
        self.percentCheck.place(y=50,x=10)
        self.var_intIncome=ctk.BooleanVar()
        self.intIncomeCheck = ctk.CTkCheckBox(self. centerFrame, text="Ingresos internacionales mayores a",font=("Times", 17,), variable=self.var_intIncome,width=50,hover_color="#9f4154",height=50, command= lambda: self.update_list2(self.searchEntry, self.result_frameE, search_filter(bool(self.yearCheck.get()),self.yearEntry.get(),bool(self.percentCheck.get()),bool(self.intIncomeCheck.get()),self.intIncome.get(),self.searchEntry.get()), self.result_labels))
        self.intIncomeCheck.place(y=100,x=10)
        self.intIncome= ctk.CTkEntry(self.centerFrame,placeholder_text=" Ingresos internacionales",width=190, height=50, font=("Times", 17,))
        self.intIncome.place(y=100, x=270)

        self.var_yearCheck=ctk.BooleanVar()
        self.yearCheck=ctk.CTkCheckBox(self.centerFrame, text="Año", variable=self.var_yearCheck, width=50, height=50, hover_color= "#9f4154",font=("Times", 17,), command= lambda: self.update_list2(self.searchEntry, self.result_frameE, search_filter(bool(self.yearCheck.get()),self.yearEntry.get(),bool(self.percentCheck.get()),bool(self.intIncomeCheck.get()),self.intIncome.get(),self.searchEntry.get()), self.result_labels))
        self.yearCheck.place(y=160,x=10)


        self.yearEntry=ctk.CTkEntry(self.centerFrame,placeholder_text="año de estreno", width=120,height=50, font=("Times", 17,))
        self.yearEntry.place(y=160,x=80)

        #cuadro de derecha
        self.rigthFrame=ctk.CTkFrame(self, width=590,height=900,fg_color="#fbf2e1")
        self.rigthFrame.place(y=80,x=1000)
        self.title2Label = ctk.CTkLabel(self.rigthFrame, text="Datos", font=("Times", 50, "bold")).place(y=30,relx=0.5, anchor="center")

        #Datos del nodo 
        #Titulo
        self.movieTitleLbl=ctk.CTkLabel(self.rigthFrame,text="Titulo:", font=("Times", 20, "bold"))
        self.movieTitleLbl.place(y=100,x=10)

        #Año
        self.movieYearLbl=ctk.CTkLabel(self.rigthFrame, text="Año:", font=("Times", 20, "bold"))
        self.movieYearLbl.place(y=140, x=10)
        
        #Ingresos a nivel mundial
        self.movieWorldwideEarningsLbl= ctk.CTkLabel(self.rigthFrame, text="Ingresos mundiales:",font=("Times", 20, "bold"))
        self.movieWorldwideEarningsLbl.place(y=180,x=10)

        #Ingresos a nivel nacional 
        self.movieDomesticEarningsLbl=ctk.CTkLabel(self.rigthFrame, text="Ingresos nacionales:",font=("Times", 20, "bold"))
        self.movieDomesticEarningsLbl.place(y=220,x=10)

        #Ingresos a nivel internacional
        self.movieForeignEarningsLbl=ctk.CTkLabel(self.rigthFrame, text="Ingresos internacionales:",font=("Times", 20, "bold"))
        self.movieForeignEarningsLbl.place(y=260,x=10)

        #Porcentaje deganancias domestico
        self.movieDomesticPercentEarnings=ctk.CTkLabel(self.rigthFrame, text='Porcentaje de ingresos nacionales:',font=("Times", 20, "bold"))
        self.movieDomesticPercentEarnings.place(y=300,x=10)

        #porcentaje a nivel internacional
        self.movieForeignPercentEarnings=ctk.CTkLabel(self.rigthFrame, text="Porcentaje de Ingresos internacionales:",font=("Times", 20, "bold"))
        self.movieForeignPercentEarnings.place(y=340,x=10)

        #Cuadrado inferior derecho para dar datos
        self.frameDownRigth=ctk.CTkFrame(self.rigthFrame,width=590, height=180, fg_color="#f7e5c4")
        self.frameDownRigth.place(y=720,x=0)
        #Datos del cuadrado
        #nivel del nodo
        self.nodeLevelLbl=ctk.CTkLabel(self.frameDownRigth, text="Nivel del nodo:", font=("Times", 20, "bold"))
        self.nodeLevelLbl.place(y=2,x=10)
        #balance del nodo
        self.balanceLbl=ctk.CTkLabel(self.frameDownRigth, text="Factor de balanceo:", font=("Times", 20, "bold"))
        self.balanceLbl.place(y=32,x=10)
        #padre del nodo
        self.fatherLbl=ctk.CTkLabel(self.frameDownRigth, text="Padre del nodo:", font=("Times", 20, "bold"))
        self.fatherLbl.place(y=62,x=10)
        #abuelo del nodo
        self.gfatherLbl=ctk.CTkLabel(self.frameDownRigth, text="Abuelo del nodo:", font=("Times", 20, "bold"))
        self.gfatherLbl.place(y=92,x=10)
        #tio del nodo
        self.uncleLbl=ctk.CTkLabel(self.frameDownRigth, text="Tio del nodo:", font=("Times", 20, "bold"))
        self.uncleLbl.place(y=122,x=10)

    def fillData(self):
            p,pa = main_tree.search(self.searchEntry.get())
            #mostrando datos de la pelicula

            if p is not None:
                self.movieTitleLbl.configure(text="Titulo: "+p.data.title)
                self.movieYearLbl.configure(text="Año: "+str(p.data.year))
                self.movieWorldwideEarningsLbl.configure(text="Ingresos mundiales: "+str(p.data.we))
                self.movieDomesticEarningsLbl.configure(text="Ingresos nacionales: "+str(p.data.de))
                self.movieForeignEarningsLbl.configure(text="Ingresos internacionales: " +str(p.data.fe))
                self.movieDomesticPercentEarnings.configure(text="Porcentaje de ingresos nacionales: "+str(p.data.dpe)+ "%")
                self.movieForeignPercentEarnings.configure(text="Porcentaje de ingresos internacionales: "+str(p.data.fpe)+ "%")


            #mostrando nivel
            lvl=main_tree.calculate_level(p)
            self.nodeLevelLbl.configure(text="Nivel del nodo: "+str(lvl))
            #mostrando balance
            self.balanceLbl.configure(text="Factor de balanceo: "+str(p.balance))
            #mostrando padre
            pad= main_tree.find_parent(p)
            if(pad is not None):
                self.fatherLbl.configure(text="Padre del nodo: "+pad.data.title)
            else:
                self.fatherLbl.configure(text="Padre del nodo: Nulo ")
            #mostrando abuelo

            #error con el abuelo cuando no existe de backend
            granp= main_tree.find_grandparent(p)
            if(granp is not None):
                self.gfatherLbl.configure(text="Abuelo del nodo: "+granp.data.title)
            else:
                self.gfatherLbl.configure(text="Abuelo del nodo: Nulo ")
            #mostrando tio
            uncle=main_tree.find_uncle(p)
            if uncle is not None:
                self.uncleLbl.configure(text="Tio del nodo: "+uncle.data.title)
            else:
                self.uncleLbl.configure(text="Tio del nodo: Nulo")


    def update_list(self, entry, result_frame, data_list, result_labels, event=None):
        # Limpiar la lista actual de labels
        for label in result_labels:
            label.destroy()

        # Filtrar la lista según el texto en el Entry especificado
        search_term = entry.get().lower()
        
        # Si el texto de búsqueda está vacío, no mostrar resultados
        if not search_term:
            filtered_data = []
        else:
            filtered_data = [item.title for item in data_list if search_term in item.title.lower()]

        # Crear un nuevo label para cada resultado filtrado
        result_labels.clear()  # Limpia la lista de labels antes de agregar nuevos
        for idx, item in enumerate(filtered_data):
            label = ctk.CTkLabel(result_frame, text=item, font=("Helvetica", 16), width=280, height=30, anchor="w")
            label.pack(anchor="w", padx=10, pady=5) 
            # Pasar el Entry como parámetro a on_item_click
            label.bind("<Button-1>", lambda e, text=item: self.on_item_click(text, entry, result_labels))  # Agregar evento de clic
            result_labels.append(label)
    def update_list2(self, entry, result_frame, data_list, result_labels, event=None):
        # Limpiar la lista actual de labels
        for label in result_labels:
            label.destroy()

        # Filtrar la lista según el texto en el Entry especificado
        search_term = entry.get().lower()
        
        # Si el texto de búsqueda está vacío, no mostrar resultados
        filtered_data = [item.title for item in data_list if search_term in item.title.lower()]

        # Crear un nuevo label para cada resultado filtrado
        result_labels.clear()  # Limpia la lista de labels antes de agregar nuevos
        for idx, item in enumerate(filtered_data):
            label = ctk.CTkLabel(result_frame, text=item, font=("Helvetica", 16), width=280, height=30, anchor="w")
            label.pack(anchor="w", padx=10, pady=5) 
            # Pasar el Entry como parámetro a on_item_click
            label.bind("<Button-1>", lambda e, text=item: self.on_item_click(text, entry, result_labels))  # Agregar evento de clic
            result_labels.append(label)



    def on_item_click(self, text, entry, result_labels):

        # Colocar el texto seleccionado en el Entry y borrar la lista de resultados
        entry.delete(0, "end")
        entry.insert(0, text)

        # Limpiar los resultados después de hacer clic en uno
        for label in result_labels:
            label.destroy()

    def delete_Ui(self, movie):
        
        try:
             main_tree.delete(movie)
             self.DeleteEntry.delete(0, "end")
        except:
            self.warning.configure(text="Error")
        

    def search_Ui(self, movie):
        if len(search_movie(self.insertEntry.get())) is 0:
            self. warning.configure(text="no esta")
        else:
            add_film(movie)
            self.insertEntry.delete(0, "end")
            self. warning.configure(text="")

    def show_data(self,data_list=None):
        if data_list is None:
            # Lista de ejemplo con muchos elementos
            data_list = main_tree.levels()

        # Crear una nueva ventana
        new_window = ctk.CTkToplevel(self)
        new_window.geometry("500x300")
        new_window.title("Datos en Pestañas")

        # Crear un Tabview en la nueva ventana
        tabview = ctk.CTkTabview(new_window, width=450, height=250)
        tabview.pack(pady=20)

        # Crear una nueva pestaña dentro del Tabview
        new_tab = tabview.add("Datos")

        # Crear un frame con scroll dentro de la pestaña
        scrollable_frame = ctk.CTkScrollableFrame(new_tab, width=450, height=200)
        scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Agregar los datos de la lista al scrollable_frame
        for idx, item in enumerate(data_list):
            label = ctk.CTkLabel(scrollable_frame, text=f"{idx + 1}. {item}")
            label.pack(anchor='w', padx=10, pady=5)
   






class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Film Three")
        self.geometry('1700x1000')
        ctk.set_appearance_mode('light')
        self.btnOption=ctk.CTkButton(self,width=830,height=980,corner_radius=50,text="Operaciones",hover_color="#b26877", fg_color="#9f4154",font=("Times", 50, "bold"),command=self.openOptionWindow)
        self.btnOption.place(y=10,x=10)
        self.btnSeeTree=ctk.CTkButton(self,width=830,height=980,corner_radius=50,text="Ver Arbol", hover_color= "#b26877",fg_color="#9f4154",font=("Times", 50, "bold"),command=self.drawTree)
        self.btnSeeTree.place(y=10,x=850)
        self.Option_window=None

        


        


        self.mainloop()
    def graph_tree(self, tree: AVLT, filename='binary_tree'):
            def add_edges(graph, node: Node):
                if node is None:
                    return
                if node.left:
                    graph.node(escape_node_name(str(node.left.data.title)))
                    graph.edge(escape_node_name(str(node.data.title)), escape_node_name(str(node.left.data.title)))
                    add_edges(graph, node.left)
                if node.right:
                    graph.node(escape_node_name(str(node.right.data.title)))
                    graph.edge(escape_node_name(str(node.data.title)), escape_node_name(str(node.right.data.title)))
                    add_edges(graph, node.right)

            graph = Digraph()
            if tree.root:
                graph.node(escape_node_name(str(tree.root.data.title)))
                add_edges(graph, tree.root)
            
            # Eliminar archivo anterior si existe
            if os.path.exists(f"{filename}.png"):
                os.remove(f"{filename}.png")
            
            # Renderizar el nuevo gráfico
            graph.render(filename, format='png', cleanup=True)
            return f"{filename}.png"
    def drawTree(self):

        image_path = self.graph_tree(main_tree)
        image = open_image(image_path)
        if image:
            image.show()  # Muestra la imagen si se abrió correctamente
        print(f"Árbol graficado en: {image_path}")

    def openOptionWindow(self):
        if self.Option_window is None or not self.Option_window.winfo_exists():
            self.Option_window = OptionWindow(self)  # create window if its None or destroyed
        else:
            self.Option_window.focus()  # if window exists focus it


if __name__=='__main__':
    app=App()

