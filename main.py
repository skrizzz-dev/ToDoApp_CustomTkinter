import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

class ToDoApp(ctk.CTk):
    def __init__(self):
        ctk.set_appearance_mode("dark")
        super().__init__()
        self.geometry("900x600")
        self.create_widgets()
        
    def create_widgets(self):
        
        # Название задачи
        self.label_title = ctk.CTkLabel(self, text='Название:')
        self.label_title.place(x=40, y=20)

        self.entry_title = ctk.CTkEntry(self, placeholder_text='Название')
        self.entry_title.place(x=40, y=60)

        # Описание задачи
        #self.label_description = ctk.CTkLabel(self, text='Задача:')
        #self.label_description.place(x=40, y=100)
        #self.entry_description = ctk.CTkEntry(self, placeholder_text='Задача')
        #self.entry_description.place(x=40, y=140)

        self.label_description = ctk.CTkLabel(self, text='Задача:')
        self.label_description.place(x=40, y=100)

        self.textbox_description = ctk.CTkTextbox(self, width=200, height=200)
        self.textbox_description.place(x=40, y=140)
        
        # Задачи
        self.label_tasks = ctk.CTkLabel(self, text='Задачи:')
        self.label_tasks.place(x=420, y=20)
        
        self.listbox = tk.Listbox(self)
        self.listbox.place(x=400, y=50, width=400, height=300)
        
        # Кнопка добавления задачи
        self.btn_add = ctk.CTkButton(self, text='Добавить', command=self.add_task)
        self.btn_add.place(x=400, y=400)
        
        # Кнопка удаления задачи
        self.btn_del = ctk.CTkButton(self, text='Удалить', command=self.delete_task)
        self.btn_del.place(x=400, y=450)
    def add_task(self):
        try:
            title = self.entry_title.get().strip()
            description = self.textbox_description.get('1.0', tk.END).strip()
            if title and description:
                text = f'{title}: {description}'
                self.listbox.insert(tk.END, text)
                self.entry_title.delete(0, tk.END)
                self.textbox_description.delete('1.0', tk.END)
            else:
                messagebox.showwarning('Ошибка', 'Напишите название и саму задачу для добавления')
        except Exception as e:
            messagebox.showerror('Ошибка', f'Произошла ошибка: {e}')
    def delete_task(self):
        try:
            selected_task_index = self.listbox.curselection()[0]
            self.listbox.delete(selected_task_index)
        except:
            messagebox.showwarning('Ошибка', 'Выберите задачу для удаления')
        
app = ToDoApp()
app.mainloop()