# Импорт библиотек для работы с customtkinter и отсальными
import customtkinter as ctk
import tkinter as tk 
from tkinter import messagebox
import db
from PIL import Image, ImageTk

class ToDoApp(ctk.CTk):
    # Иницализация
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        self.geometry("900x600")
        self.create_widgets()
        db.init_db()
        self.load_tasks_from_db()
        self.load_completed_tasks_from_db()
        
    def create_widgets(self):
        
        # Название задачи
        self.label_title = ctk.CTkLabel(self, text='Название:')
        self.label_title.place(x=40, y=20)

        self.entry_title = ctk.CTkEntry(self, placeholder_text='Название')
        self.entry_title.place(x=40, y=60)

        # Описание задачи
        self.label_description = ctk.CTkLabel(self, text='Задача:')
        self.label_description.place(x=40, y=100)

        self.textbox_description = ctk.CTkTextbox(self, width=200, height=200)
        self.textbox_description.place(x=40, y=140)
        
        # Задачи
        self.label_tasks = ctk.CTkLabel(self, text='Задачи:')
        self.label_tasks.place(x=420, y=20)
        
        self.listbox = tk.Listbox(self)
        self.listbox.place(x=400, y=50, width=400, height=300)
        
        # Выполнение задачи
        self.label_completed = ctk.CTkLabel(self, text='Выполнение:')
        self.label_completed.place(x=40, y=360)
        
        self.listbox_completed = tk.Listbox(self)
        self.listbox_completed.place(x=40, y=400, width=200, height=150)
          
        # Кнопка добавления задачи
        self.btn_add = ctk.CTkButton(self, text='Добавить', command=self.add_task, width=120, height=40)
        self.btn_add.place(x=400, y=400)
        
        # Кнопка удаления задачи
        self.btn_del = ctk.CTkButton(self, text='Удалить', command=self.delete_task, width=120, height=40)
        self.btn_del.place(x=400, y=450)
        
        # Кнопка для добавления задачи в выполненные
        self.btn_add_completed = ctk.CTkButton(self, text='Выполнен', command=self.add_to_completed, width=120, height=40)
        self.btn_add_completed.place(x=550, y=400)
        
        # Кнопка для редактирования задачи
        self.btn_edit = ctk.CTkButton(self, text='Редактировать', command=self.edit_task, width=120, height=40)
        self.btn_edit.place(x=550, y=450)
                
        # Кнопка для очистки выполненных задач
        self.btn_clear_completed_tasks = ctk.CTkButton(self, text='Очистить выполненные', command=self.clear_completed_tasks, width=120, height=40)
        self.btn_clear_completed_tasks.place(x=700, y=400)
        
        # Кнопка для возврата задачи
        self.btn_return = ctk.CTkButton(self, text='Вернуть в список', command=self.return_to_tasks, width=120, height=40)
        self.btn_return.place(x=700, y=450)
        
        # Кнопка для смены темы
        
        light_theme = Image.open('images/light_icon.png')
        dark_theme = Image.open('images/dark_icon.png')
        
        light_theme = light_theme.resize((20, 20), Image.Resampling.LANCZOS)
        dark_theme = dark_theme.resize((20, 20), Image.Resampling.LANCZOS)
        
        self.light_photo = ImageTk.PhotoImage(light_theme)
        self.dark_photo = ImageTk.PhotoImage(dark_theme)
        
        self.btn_theme = ctk.CTkButton(self, image=self.dark_photo, text='', width=20, height=35, hover_color='#333333', command=self.toggle_theme)
        self.btn_theme.place(x=850, y=10)
    
    # Функция для добавления задачи в базу данных также в listbox
    def add_task(self):
        try:
            title = self.entry_title.get().strip()
            description = self.textbox_description.get('1.0', tk.END).strip()
            if title and description:
                db.add_task_to_db(title, description)
                text = f'{title}: {description}'
                self.listbox.insert(tk.END, text)
                self.entry_title.delete(0, tk.END)
                self.textbox_description.delete('1.0', tk.END)
            else:
                messagebox.showwarning('Ошибка', 'Напишите название и саму задачу для добавления')
        except Exception as e:
            messagebox.showerror('Ошибка', f'Произошла ошибка: {e}')
    
    # Функция для удаления задачи из базы данных также из listbox
    def delete_task(self):
        try:
            if self.listbox.curselection():
                if messagebox.askyesno('Подтверждение', 'Удалить задачу?'):
                    selected_task_index = self.listbox.curselection()[0]
                    full_text = self.listbox.get(selected_task_index)
                    title, description = full_text.split(': ', 1)      
                    db.delete_task_from_db(title, description)
                    self.listbox.delete(selected_task_index)
        except IndexError:
            messagebox.showwarning('Ошибка', 'Выберите задачу для удаления')
        except Exception as e:
            messagebox.showerror('Ошибка', f'Произошла ошибка: {e}')
    
    # Функция для добавления задачи в выполненных    
    def add_to_completed(self):
        try:
            selected_task_index = self.listbox.curselection()[0]
            full_text = self.listbox.get(selected_task_index)
            title, description = full_text.split(': ', 1)
            db.mark_task_completed(title, description)
            text  = f'{title}: {description}'
            self.listbox_completed.insert(tk.END, text)
            self.listbox.delete(selected_task_index)
        except Exception as e:
            messagebox.showerror('Ошибка', f'Не удалось добавить в выполненные задачи: {e}')
    
    # Функция для редактирования задачи    
    def edit_task(self):
        try:
            selected_task_index = self.listbox.curselection()[0]
            full_text = self.listbox.get(selected_task_index)
            title, description = full_text.split(': ', 1)
            self.entry_title.delete(0, tk.END)
            self.entry_title.insert(0, title)
            self.textbox_description.delete('1.0', tk.END)
            self.textbox_description.insert('1.0', description)
            db.delete_task_from_db(title, description)
            self.listbox.delete(selected_task_index)
        except Exception as e:
            messagebox.showerror('Ошибка', f'Не удалось добавить в выполненные задачи: {e}')
            
    # Функция для удаления всех выполненных задач
    def clear_completed_tasks(self):
        result = messagebox.askyesno('Предупреждение', 'Вы точно хотите удалить все выполненные задачи?')
        
        if result:
            try:
                db.clear_all_completed_tasks()
                self.listbox_completed.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror('Ошибка', f'Не удалось очистить выполненные задачи: {e}')
    
    # Функция для возврата задачи из выполненных в список задач
    def return_to_tasks(self):
        try:
            selected_task_index = self.listbox_completed.curselection()[0]
            full_text = self.listbox_completed.get(selected_task_index)
            title, description = full_text.split(': ', 1)
            
            db.return_task_to_active(title, description)
            self.listbox.insert(tk.END, full_text)
            self.listbox_completed.delete(selected_task_index)
            
        except IndexError:
            messagebox.showerror('Ошибка', 'Выберите задачу в списке выполненных для возврата')
        except Exception as e:
            messagebox.showerror('Ошибка', f'Не удалось вернуть задачу: {e}')
            
    # Функция для загрузки данных в listbox
    def load_tasks_from_db(self):
        try:
            tasks = db.get_all_tasks()
            
            for title, description in tasks:
                text = f'{title}: {description}'
                self.listbox.insert(tk.END, text)
        except Exception as e:
            messagebox.showerror('Ошибка', f'Не удалось загрузить задачи: {e}')
        
    # Функция для загрузки выполненных задач в listbox_completed    
    def load_completed_tasks_from_db(self):
        try:
            tasks = db.get_completed_tasks()
            
            for title, description in tasks:
                text = f'{title}: {description}'
                self.listbox_completed.insert(tk.END, text)
        except Exception as e:
            messagebox.showerror('Ошибка', f'Не удалось загрузить задачи: {e}')
    
    def toggle_theme(self):
        if ctk.get_appearance_mode() == 'Light':
            ctk.set_appearance_mode("Dark")
            self.btn_theme.configure(image=self.dark_photo)
        else:
            ctk.set_appearance_mode("Light")
            self.btn_theme.configure(image=self.light_photo)
            
app = ToDoApp()
app.mainloop()