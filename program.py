import re
import os
import importlib.util
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from pygments import highlight
from pygments.lexers import guess_lexer, get_lexer_by_name
from pygments.formatters import get_formatter_by_name
#from ttkthemes import ThemedTk, ThemedStyle
import sys
import customtkinter as ctk
#from PIL import Image, ImageTk
from threading import Thread
import time
from pypresence import Presence
import pyperclip as pc

import MaxOSTkinter as mtk

client_id = "1142496418196627496"

class DiscordRpc:
    def __init__(self, client_id:str|int):
        self.rpc = Presence(str(client_id))

    def update(self, file_name:str):
        self.rpc.update(
            state=f"Редактирует {file_name}",
            start=time.time(),
            large_image="plundi",
            large_text="Plundi IDE",
        )

    def connect(self):
        self.rpc.connect()

    def close(self):
        self.rpc.close()

class TabText():
    def destroy(self):
        if self.change_file_state:
            self.master['cursor'] = ''
            def OK():
                ans2 = self.save_file()
                ans.destroy()
                if ans2:
                    self.master['cursor'] = ''
                    index = self.tabs.index(self)
                    self.tabs.remove(self)
                    try:
                        if self.tab_state:self.tabs[index-1].select_tab()
                    except:
                        pass
                    self.frame_text_widget.after_cancel(self.global_after)
                    self.frame_text_widget.destroy()
                    self.tab_frame.destroy()
                    self.root2.title(f"MS Code")

            def CLOSE():
                ans.destroy()
                self.master['cursor'] = ''
                index = self.tabs.index(self)
                self.tabs.remove(self)
                try:
                    if self.tab_state:self.tabs[index-1].select_tab()
                except:
                    pass
                self.frame_text_widget.after_cancel(self.global_after)
                self.frame_text_widget.destroy()
                self.tab_frame.destroy()
                self.root2.title(f"MS Code")
            ans = mtk.WhatDialogWin(self.root, title="Внимание!", text="Вы хотите сохранить внесенные изменения?", type='warning', command=OK, commandclose=CLOSE)
        else:
            self.master['cursor'] = ''
            index = self.tabs.index(self)
            self.tabs.remove(self)
            try:
                if self.tab_state:self.tabs[index-1].select_tab()
            except:
                pass
            self.frame_text_widget.after_cancel(self.global_after)
            self.frame_text_widget.destroy()
            self.tab_frame.destroy()
            self.root2.title(f"MS Code")
    def select_tab(self):
        self.tab_state = 1
        if self.hover_tab_state != 1:
            self.frame_text_widget.pack(fill='both', expand=1)
            self.tab_frame['bg'] = '#2E2E2E'
            self.tab_name['bg'] = '#2E2E2E'
            self.tab_name['fg'] = 'lightgray'
            self.change_state['bg'] = '#2E2E2E'
            if self.change_file_state == 0:self.change_state['fg'] = '#2E2E2E'
            if self.hover_close_state == 0 and self.active_close_state == 0:
                self.close_btn.configure(fg_color='#2E2E2E')
                self.close_btn.configure(text_color='lightgray')
            self.file_path2 = self.file_path
            if self.file_path != None:
                if len(self.file_path) > 100:
                    self.file_path2 = f"...{os.sep}{os.path.split(os.path.split(self.file_path)[0])[1]}{os.sep}{os.path.split(self.file_path)[1]}"
            else:
                self.file_path2 = 'new'
            self.root.title2(f"MS Code - {self.file_path2}")
    def unselect_tab(self):
        self.tab_state = 0
        if self.hover_tab_state != 1:
            self.frame_text_widget.pack_forget()
            self.tab_frame['bg'] = '#202020'
            self.tab_name['bg'] = '#202020'
            self.tab_name['fg'] = 'gray'
            self.change_state['bg'] = '#202020'
            if self.change_file_state == 0:self.change_state['fg'] = '#202020'
            if self.hover_close_state == 0 and self.active_close_state == 0:
                self.close_btn.configure(fg_color='#202020')
                self.close_btn.configure(text_color='gray')
    def change_syntax(self, syntax=''):
        self.syntax_var.set(syntax)
        self.highlight_syntax()
    def change_font_size(self, arg='+'):
        if arg == '+':
            self.font_size_plus()
        elif arg == '-':
            self.font_size_minus()
        if arg == '=':
            self.font_size_equal()
    def get_state(self):
        return self.tab_state
    def get_file_change_state(self):
        return self.change_file_state
    def change_auto_delete(self, value=0):
        self.auto_delete_var.set(value)
    def __init__(self, master_tabs='', master='', root='', tab_list=[], current_tab=[], file_path=None, editor=''):
        self.font_ = 'Cousine'
        self.font_size = 16
        self.editor = editor
        self.tabs = tab_list
        self.master = master
        self.change_file_state = 0
        self.root = root

        self.file_path = file_path

        self.line_num_change = 0

        self.select_text = ''


        self.current_str = ''

        self.tab_list = []
        def GlobalUpdate():
            self.global_after = self.frame_text_widget.after(100, GlobalUpdate)

            def check_file():
                if self.file_path == None:
                    file1 = ''
                    try:file2 = self.text_area.get(0.0, 'end')
                    except:file2 = ''
                    file2 = list(file2)
                    if file2[-1] == '\n':
                        file2.pop(-1)
                    file2 = ''.join(file2)

                    if file1 != file2:
                        self.change_file_state = 1
                        self.change_state['fg'] = '#4545ad'
                    else:
                        self.change_file_state = 0
                else:
                    try:
                        file1 = ''
                        with open(self.file_path, 'r', encoding='utf-8') as f:
                            file1 = f.read()
                        try:file2 = self.text_area.get(0.0, 'end')
                        except:file2 = ''
                        file2 = list(file2)
                        if file2[-1] == '\n':
                            file2.pop(-1)
                        file2 = ''.join(file2)

                        if file1 != file2:
                            self.change_file_state = 1
                            self.change_state['fg'] = '#4545ad'
                        else:
                            self.change_file_state = 0
                    except:
                        self.change_file_state = 1
                        self.change_state['fg'] = '#4545ad'
            #Thread(target=check_file, daemon=1).start()
            check_file()

            if self.text_area.tag_ranges("sel"):
                selection_from = self.text_area.index("sel.first")
                selection_to = self.text_area.index("sel.last")
                self.select_text = self.text_area.get(selection_from, selection_to)

            self.current_str = list(self.text_area.get(f"{self.text_area.index('insert').split('.')[0]}.0", float(self.text_area.index('insert'))+1))

            if self.current_str[-1] == '\n':
                self.current_str.pop(-1)

            self.current_str = ''.join(self.current_str)

            tab_list_ = []

            for i in range(len(self.current_str)//4):
                if r'    ' in self.current_str[0: int(self.text_area.index('insert').split('.')[1])]:
                    if self.last_symbol.isalpha() == False:
                        tab_list_.append('    ')
                        self.tab_list.append('    ')

                        if len(self.tab_list) > len(tab_list_):
                            l = len(self.tab_list)
                            while l != len(tab_list_):
                                self.tab_list.pop(0)
                                l = len(self.tab_list)

            if len(self.current_str) < 4:
                tab_list_.clear()
                self.tab_list.clear()


            self.tab_state2 = len(self.tab_list)


        #if self.file_path == None:
        #    self.editor.rpc.update('new')
        #else:
        #    self.editor.rpc.update(str(os.path.split(self.file_path)[1]))
        self.frame_text_widget = tk.Frame(master, bg="#2E2E2E")
        self.frame_text_widget.pack(fill='both', expand=1)

        self.tab_state = 0
        self.tab_state2 = 0
        self.hover_tab_state = 0
        self.hover_close_state = 0
        self.active_close_state = 0
        def hover_tab(e=''):
            self.tab_frame['bg'] = '#3E3E3E'
            self.tab_name['bg'] = '#3E3E3E'
            self.change_state['bg'] = '#3E3E3E'
            if self.change_file_state == 0:self.change_state['fg'] = '#3E3E3E'
            self.close_btn.configure(fg_color='#3E3E3E')
            self.hover_tab_state = 1
        def unhover_tab(e=''):
            if self.tab_state == 1:
                self.tab_frame['bg'] = '#2E2E2E'
                self.tab_name['bg'] = '#2E2E2E'
                self.change_state['bg'] = '#2E2E2E'
                if self.change_file_state == 0:self.change_state['fg'] = '#2E2E2E'
                if self.active_close_state == 0 and self.hover_close_state == 0:self.close_btn.configure(fg_color='#2E2E2E')
            else:
                self.tab_frame['bg'] = '#202020'
                self.tab_name['bg'] = '#202020'
                self.change_state['bg'] = '#202020'
                if self.change_file_state == 0:self.change_state['fg'] = '#202020'
                if self.active_close_state == 0 and self.hover_close_state == 0:self.close_btn.configure(fg_color='#202020')
            self.hover_tab_state = 0

        self.tab_frame = tk.Frame(master_tabs, bg="#202020")
        self.tab_frame.pack(side='left', fill='y')

        if self.file_path == None:
            self.name = 'new'
        else:
            self.name = os.path.split(self.file_path)[1]

        if len(self.name) > 12:
            self.name2 = []
            for i in range(len(self.name)):
                if i < 9:
                    self.name2.append(self.name[i])
            self.name2 = ''.join(self.name2)
            self.name2 = f"{self.name2}..."
        else:
            self.name2 = self.name

        self.change_state = tk.Label(self.tab_frame, bg="#202020", fg='#202020', text='◉', width=1, font=(self.font_, 15))
        if self.change_file_state:
            self.change_state['fg'] = '#4545ad'
        def saving_file(e=''):
            if self.change_file_state:
                self.save_file()
        self.change_state.pack(side='left', fill='y', padx=5)
        self.change_state.bind('<Button-1>', saving_file)

        self.tab_name = tk.Label(self.tab_frame, bg="#202020", fg='gray', text=self.name2, width=15, font=(self.font_, 12))
        self.tab_name.pack(fill='both', expand=1, side='left')

        self.tab_frame.bind('<Enter>', hover_tab)
        self.tab_frame.bind('<Leave>', unhover_tab)
        self.tab_name.bind('<Enter>', hover_tab)
        self.tab_name.bind('<Leave>', unhover_tab)
        self.change_state.bind('<Enter>', hover_tab)
        self.change_state.bind('<Leave>', unhover_tab)
        def selected_tab(e=''):
            if self.file_path == None:
                self.editor.rpc.update('new')
            else:
                self.editor.rpc.update(str(os.path.split(self.file_path)[1]))
            for i in self.tabs:
                i.unselect_tab()
            self.select_tab()
        self.tab_name.bind('<Button-1>', selected_tab)

        def hover_close(e=''):
            if self.active_close_state:
                self.close_btn.configure(fg_color='#6f6fc7')
                self.close_btn.configure(text_color='lightgray')
            else:
                self.close_btn.configure(fg_color='#4545ad')
                self.close_btn.configure(text_color='lightgray')
            self.hover_close_state = 1
            master['cursor'] = 'hand2'
        def unhover_close(e=''):
            if self.tab_state == 1:
                self.close_btn.configure(fg_color='#2E2E2E')
                self.close_btn.configure(text_color='lightgray')
            else:
                self.close_btn.configure(fg_color='#202020')
                self.close_btn.configure(text_color='gray')
            self.hover_close_state = 0
            master['cursor'] = ''
        def active_close(e=''):
            self.close_btn.configure(fg_color='#6f6fc7')
            self.close_btn.configure(text_color='lightgray')
            self.active_close_state = 1
        def command_close(e=''):
            if self.hover_close_state:
                self.close_btn.configure(fg_color='#4545ad')
                self.close_btn.configure(text_color='lightgray')
                self.destroy()
            else:
                if self.tab_state == 1:
                    self.close_btn.configure(fg_color='#2E2E2E')
                    self.close_btn.configure(text_color='lightgray')
                else:
                    self.close_btn.configure(fg_color='#202020')
                    self.close_btn.configure(text_color='gray')
            self.active_close_state = 0
        self.close_btn = ctk.CTkLabel(self.tab_frame, fg_color='#202020', text_color='gray', text='×', font=(self.font_, 15), corner_radius=10, width=10, height=10)
        self.close_btn.pack(side='left', padx=5)
        self.close_btn.bind('<Enter>', hover_close)
        self.close_btn.bind('<Leave>', unhover_close)
        self.close_btn.bind('<ButtonPress-1>', active_close)
        self.close_btn.bind('<ButtonRelease-1>', command_close)

        self.scrollbar_x = ctk.CTkScrollbar(self.frame_text_widget, orientation='horizontal')
        self.scrollbar_x.pack(fill='x', anchor='s', side='bottom')

        self.scrollbar_x.configure(fg_color="#2E2E2E")
        self.scrollbar_x.configure(button_color="#2E2E2E")
        self.scrollbar_x.configure(button_hover_color="#3E3E3E")

        self.line_numbers = tk.Text(self.frame_text_widget, bg="#2E2E2E", fg="gray", width=4, insertbackground="white", highlightthickness=0, highlightbackground='#2E2E2E', relief='flat', selectbackground='#2E2E2E', selectforeground='gray', cursor='')
        self.line_numbers.pack(side="left", fill="y")
        self.line_numbers.configure(font=(self.font_, self.font_size), state="disabled")

        self.text_area = tk.Text(self.frame_text_widget, wrap="none", bg="#2E2E2E", fg="lightgray", insertbackground="lightgray", highlightthickness=0, highlightbackground='#2E2E2E', relief='flat', selectbackground='#4545ad', selectforeground='lightgray', width=0)
        self.text_area.pack(side="left", fill="both", expand=True)
        self.text_area.configure(font=(self.font_, self.font_size))#Source Code Pro
        self.text_area.bind("<KeyRelease-Return>", self.on_text_change)
        self.text_area.bind("<KeyRelease-BackSpace>", self.on_text_change)

        self.scrollbar_y = ctk.CTkScrollbar(self.frame_text_widget, orientation='vertical', command=self.text_area.yview)
        self.scrollbar_y.pack(fill='y', side='left')

        self.scrollbar_y.configure(fg_color="#2E2E2E")
        self.scrollbar_y.configure(button_color="#2E2E2E")
        self.scrollbar_y.configure(button_hover_color="#3E3E3E")

        self.scrollbar_x.configure(command=self.text_area.xview)

        self.line_numbers.bind('<FocusIn>', lambda e: self.text_area.focus())

        self.undo_stack = []
        self.redo_stack = []
        self.last_symbol = ''
        self.text_area.bind("<Control-z>", self.undo)
        self.text_area.bind("<Control-y>", self.redo)

        self.text_area.bind("<Control-s>", self.save_file)
        self.text_area.bind("<Control-a>", self.select_all)
        self.text_area.bind("<Control-c>", self.copy_text)
        self.text_area.bind("<Control-v>", self.paste_text)

        self.text_area.config(yscrollcommand=self.scroll_text)
        self.line_numbers.config(yscrollcommand=self.scroll_text)

        self.text_area.config(xscrollcommand=self.scrollbar_y.set)

        self.text_area.tag_configure("keyword", foreground="#BE90B7")
        self.text_area.tag_configure("function", foreground="#BE90B7")
        self.text_area.tag_configure("class_highlight", foreground="#EFA856")
        self.text_area.tag_configure("function_highlight", foreground="#5287B5")
        self.text_area.tag_configure("text_highlight", foreground="#91BC8E")
        self.text_area.tag_configure("special_highlight", foreground="#DD5D63")
        self.text_area.tag_configure("int", foreground="#EFA856")

        self.text_area.bind("<Control-plus>", self.font_size_plus)
        self.text_area.bind("<Control-minus>", self.font_size_minus)
        self.text_area.bind("<Control-equal>", self.font_size_equal)

        self.text_area.bind("<KeyRelease>", lambda event: self.on_key_press(event))
        self.text_area.bind("<Key>", self.check_symbol)
        self.text_area.bind("<Tab>", self.tab_bind)
        self.text_area.bind("<Return>", self.enter_bind)
        self.text_area.bind("<BackSpace>", self.back_space_bind)

        self.text_area.bind("<Button-3>", self.menu_popup)



        self.syntax_var = tk.StringVar()
        self.syntax_var.set('txt')

        self.auto_delete_var = tk.IntVar()
        self.auto_delete_var.set(0)

        GlobalUpdate()

    def menu_popup(self, event=''):
        menu = tk.Menu(self.text_area, tearoff=0)

        if self.text_area.tag_ranges("sel"):
            menu.add_command(label='Копировать', command=self.copy_text)

        if pc.paste():
            menu.add_command(label='Вставить', command=self.paste_text)

        menu.post(event.x_root, event.y_root)

    def save_file(self, e=''):
        if self.file_path:
            try:
                with open(self.file_path, "w", encoding='utf-8') as file:
                    content = self.text_area.get(0.0, 'end')
                    content = list(content)
                    if content[-1] == '\n':
                        content.pop(-1)
                    content = ''.join(content)
                    file.write(content)
                    return True
                    #messagebox.showinfo("Сохранено", "Файл успешно сохранен.")
            except Exception as e:
                if os.path.isfile(self.file_path) == False:
                    def OK():
                        file_path = WIN.getpath()
                        WIN.destroy()
                        try:
                            with open(file_path, "w", encoding='utf-8') as file:
                                content = self.text_area.get(0.0, 'end')
                                content = list(content)
                                if content[-1] == '\n':
                                    content.pop(-1)
                                content = ''.join(content)
                                file.write(content)
                                self.file_path = file_path

                                self.name = os.path.split(self.file_path)[1]

                                if len(self.name) > 12:
                                    self.name2 = []
                                    for i in range(len(self.name)):
                                        if i < 9:
                                            self.name2.append(self.name[i])
                                    self.name2 = ''.join(self.name2)
                                    self.name2 = f"{self.name2}..."
                                else:
                                    self.name2 = self.name
                                self.tab_name['text'] = self.name2
                                return True
                                #messagebox.showinfo("Сохранено", "Файл успешно сохранен.")
                        except Exception as e:
                            mtk.DialogWin(self.root, title="Ошибка", text=f"Ошибка при сохранении файла: {str(e)}", type='error')
                            return False
                    WIN = mtk.FileNameDialogWin(self.root, title='Сохранение', command=OK)
                else:
                    mtk.DialogWin(self.root, title="Ошибка", text=f"Ошибка при сохранении файла: {str(e)}", type='error')
                    return False
        else:
            def OK():
                file_path = WIN.getpath()
                WIN.destroy()
                try:
                    with open(file_path, "w", encoding='utf-8') as file:
                        content = self.text_area.get(0.0, 'end')
                        content = list(content)
                        if content[-1] == '\n':
                            content.pop(-1)
                        content = ''.join(content)
                        file.write(content)
                        self.file_path = file_path

                        self.name = os.path.split(self.file_path)[1]

                        if len(self.name) > 12:
                            self.name2 = []
                            for i in range(len(self.name)):
                                if i < 9:
                                    self.name2.append(self.name[i])
                            self.name2 = ''.join(self.name2)
                            self.name2 = f"{self.name2}..."
                        else:
                            self.name2 = self.name
                        self.tab_name['text'] = self.name2
                        return True
                        #messagebox.showinfo("Сохранено", "Файл успешно сохранен.")
                except Exception as e:
                    mtk.DialogWin(self.root, title="Ошибка", text=f"Ошибка при сохранении файла: {str(e)}", type='error')
                    return False
            WIN = mtk.FileNameDialogWin(self.root, title='Сохранение', command=OK, name='new.txt')

    def font_size_plus(self, event=''):
        self.font_size += 1
        self.text_area.configure(font=(self.font_, self.font_size))
        self.line_numbers.configure(font=(self.font_, self.font_size), state="disabled")

    def font_size_minus(self, event=''):
        if self.font_size > 1:
            self.font_size -= 1
            self.text_area.configure(font=(self.font_, self.font_size))
            self.line_numbers.configure(font=(self.font_, self.font_size), state="disabled")

    def font_size_equal(self, event=''):
        self.font_size = 16
        self.text_area.configure(font=(self.font_, self.font_size))
        self.line_numbers.configure(font=(self.font_, self.font_size), state="disabled")

    def copy_text(self, event=None):
        if self.text_area.tag_ranges("sel"):
            if event != None:
                pc.copy(self.text_area.get("sel.first", "sel.last"))
                return "break"
            else:
                pc.copy(self.text_area.get("sel.first", "sel.last"))

    def paste_text(self, event=None):
        #global clipboard, pasted
        #if not pasted:
        if event != None:
            self.text_area.insert("insert", pc.paste())
            return "break"
        else:
            if self.text_area.tag_ranges("sel"):
                self.text_area.delete("sel.first", "sel.last")
                self.text_area.insert("insert", pc.paste())
            else:
                self.text_area.insert("insert", pc.paste())
            #pasted = True
        #else:
            #pasted = False

    def on_key_press(self, event):
        self.highlight_syntax(event)
        self.set_last_symbol(event)
        self.update_line_numbers()

    def on_key_release(self, event):
        self.highlight_syntax(event)
        self.check_symbol(event)
        self.line_num_change = 0

    def select_all(self, event=None):
        event.widget.tag_add("sel", "1.0", "end")

    def on_text_change(self, event):
        current_text = self.text_area.get("1.0", "end")
        self.undo_stack.append(current_text)
        self.redo_stack.clear()
        self.update_line_numbers()

    def auto_delete(self, event):
        if self.auto_delete_var.get():
            div_ = len(str(self.text_area.index('insert')).split('.')[-1])
            if div_ == 1:
                min_ = 0.1
            elif div_ == 2:
                min_ = 0.01
            elif div_ == 3:
                min_ = 0.001
            elif div_ == 4:
                min_ = 0.0001
            elif div_ == 5:
                min_ = 0.00001
            index = str(round(float(self.text_area.index('insert'))+min_, div_))
            if len(str(index).split('.')[-1]) < div_:
                if str(index).split('.')[-1] == '1':
                    index = f"{round(float(self.text_area.index('insert'))+min_, div_)}{'0'*(div_-1)}"
                else:
                    index = f"{round(float(self.text_area.index('insert'))+min_, div_)}{'0'*(div_-1)}"
            if event.keysym == 'BackSpace':
                if self.last_symbol == '(':
                    if event.widget.get("insert", f"{index}") == ')':
                        event.widget.delete("insert", f"{index}")
                elif self.last_symbol == '[':
                    if event.widget.get("insert", f"{index}") == ']':
                        event.widget.delete("insert", f"{index}")
                elif self.last_symbol == '{':
                    if event.widget.get("insert", f"{index}") == '}':
                        event.widget.delete("insert", f"{index}")
                elif self.last_symbol == '"':
                    if event.widget.get("insert", f"{index}") == '"':
                        event.widget.delete("insert", f"{index}")
                elif self.last_symbol == '\'':
                    if event.widget.get("insert", f"{index}") == '\'':
                        event.widget.delete("insert", f"{index}")


    def tab_bind(self, event):
        #return 'break'
        event.widget.insert('insert', '    ')
        self.tab_state2 += 1
        return 'break'

    def back_space_bind(self, event):
        self.auto_delete(event)

    def enter_bind(self, event):
        text = self.text_area.get('1.0', 'end')

        text = list(''.join(text.split()))

        try:
            if text[-1] == '\n':
                text.pop(-1)
        except:
            pass

        if self.tab_state2 > 0:
            tab = '    '
            self.text_area.insert('insert', f'\n{tab*self.tab_state2}')
            return 'break'

        try:
            selected_syntax = self.syntax_var.get()
            if selected_syntax.lower() == "python":
                if text[-1] == ':':
                    self.tab_state2 += 1
                    tab = '    '
                    self.text_area.insert('end', f'\n{tab*self.tab_state2}')
                    return 'break'
        except:
            pass

    def check_symbol(self, event):
        if event.keysym == 'BackSpace':
            self.auto_delete(event)
        elif event.keysym == 'Return':
            self.auto_tab(event)
        else:
            if self.text_area.tag_ranges("sel"):

                selection_from = self.text_area.index("sel.first")
                selection_to = self.text_area.index("sel.last")

                div_ = len(str(selection_to).split('.')[-1])
                if div_ == 1:
                    min_ = 0.1
                elif div_ == 2:
                    min_ = 0.01
                elif div_ == 3:
                    min_ = 0.001
                elif div_ == 4:
                    min_ = 0.0001
                elif div_ == 5:
                    min_ = 0.00001
                index = str(round(float(selection_to)+min_, div_))
                if len(str(index).split('.')[-1]) < div_:
                    if str(index).split('.')[-1] == '1':
                        index = f"{round(float(selection_to)+min_, div_)}{'0'*(div_-1)}"
                    else:
                        index = f"{round(float(selection_to)+min_, div_)}{'0'*(div_-1)}"
                if event.char == '(':
                    event.widget.insert(float(selection_from), '(')
                    event.widget.insert(float(index), ')')
                    return "break"
                elif event.char == '[':
                    event.widget.insert(float(selection_from), '[')
                    event.widget.insert(float(index), ']')
                    return "break"
                elif event.char == '{':
                    event.widget.insert(float(selection_from), '{')
                    event.widget.insert(float(index), '}')
                    return "break"
                elif event.char == '"':
                    event.widget.insert(float(selection_from), '"')
                    event.widget.insert(float(index), '"')
                    return "break"
                elif event.char == '\'':
                    event.widget.insert(float(selection_from), '\'')
                    event.widget.insert(float(index), '\'')
                    return "break"

            else:
                div_ = len(str(self.text_area.index('insert')).split('.')[-1])
                if div_ == 1:
                    min_ = 0.1
                elif div_ == 2:
                    min_ = 0.01
                elif div_ == 3:
                    min_ = 0.001
                elif div_ == 4:
                    min_ = 0.0001
                elif div_ == 5:
                    min_ = 0.00001
                index = str(round(float(self.text_area.index('insert')), div_))
                if len(str(index).split('.')[-1]) < div_:
                    if str(index).split('.')[-1] == '1':
                        index = f"{round(float(self.text_area.index('insert')), div_)}{'0'*(div_-1)}"
                    else:
                        index = f"{round(float(self.text_area.index('insert')), div_)}{'0'*(div_-1)}"
                if event.char == '(':
                    event.widget.insert("insert", ')')
                    event.widget.mark_set("insert", f"{index}")
                elif event.char == '[':
                    event.widget.insert("insert", ']')
                    event.widget.mark_set("insert", f"{index}")
                elif event.char == '{':
                    event.widget.insert("insert", '}')
                    event.widget.mark_set("insert", f"{index}")
                elif event.char == '"':
                    event.widget.insert("insert", '"')
                    event.widget.mark_set("insert", f"{index}")
                elif event.char == '\'':
                    event.widget.insert("insert", '\'')
                    event.widget.mark_set("insert", f"{index}")


    def set_last_symbol(self, event):
        div_ = len(str(self.text_area.index('insert')).split('.')[-1])
        if div_ == 1:
            min_ = 0.1
        elif div_ == 2:
            min_ = 0.01
        elif div_ == 3:
            min_ = 0.001
        elif div_ == 4:
            min_ = 0.0001
        elif div_ == 5:
            min_ = 0.00001
        index = str(round(float(self.text_area.index('insert'))-min_, div_))
        if len(str(index).split('.')[-1]) < div_:
            if str(index).split('.')[-1] == '1':
                index = f"{round(float(self.text_area.index('insert'))-min_, div_)}{'0'*(div_-1)}"
            else:
                index = f"{round(float(self.text_area.index('insert'))-min_, div_)}{'0'*(div_-1)}"
        try:
            self.last_symbol = event.widget.get(index, 'insert')
        except:
            self.last_symbol = event.char

    def undo(self, event):
        if len(self.undo_stack) > 1:
            self.redo_stack.append(self.undo_stack.pop())
            previous_state = self.undo_stack.pop()
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", previous_state)
            self.update_line_numbers()

    def redo(self, event):
        if self.redo_stack:
            next_state = self.redo_stack.pop()
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", next_state)
            self.update_line_numbers()

    def scroll_text(self, *args):
        try:
            self.text_area.yview_moveto(args[0])
            self.line_numbers.yview_moveto(args[0])
            self.scrollbar_y.configure(command=self.text_area.yview)
            self.scrollbar_y.set(args[0], args[1])
        except:
            pass

    def update_line_numbers(self):
        text_content = self.text_area.get("1.0", "end-1c")
        lines = text_content.split('\n')

        if not lines[-1] and text_content.endswith('\n'):
            lines[-1] = ''

        line_count = len(lines)
        line_numbers_text = "\n".join(str(i) for i in range(1, line_count + 1))
        if line_numbers_text != self.line_numbers.get('1.0', 'end'):
            self.line_numbers.config(state="normal")
            self.line_numbers.delete("1.0", "end")
            self.line_numbers.insert("1.0", line_numbers_text)
            self.line_numbers.config(state="disabled")
            if len(str([str(i) for i in range(1, line_count + 1)][-1])) > 4:
                self.line_numbers['width'] = len(str([str(i) for i in range(1, line_count + 1)][-1]))
            if self.text_area.get("0.0", "end") == '\n':
                self.line_numbers.config(state="normal")
                self.line_numbers.delete("1.0", "end")
                self.line_numbers.config(state="disabled")
            self.line_numbers.yview_moveto(self.text_area.yview()[0])

    def highlight_syntax(self, event=None):
        selected_syntax = self.syntax_var.get()
        if selected_syntax.lower() in ['txt']:
            self.text_area.tag_delete("keyword")
            self.text_area.tag_configure("keyword", foreground="lightgray")

            self.text_area.tag_configure("function", foreground="lightgray")
            self.text_area.tag_delete("highlight")
            self.text_area.tag_configure("highlight", foreground="lightgray")
            self.text_area.tag_delete("function_highlight")
            self.text_area.tag_delete("text_highlight")
            self.text_area.tag_configure("function_highlight", foreground="lightgray")
            self.text_area.tag_configure("text_highlight", foreground="lightgray")
            self.text_area.tag_configure("special_highlight", foreground="lightgray")
            self.text_area.tag_configure("int", foreground="lightgray")

        elif selected_syntax.lower() == "python":
            self.text_area.tag_delete("keyword")
            self.text_area.tag_configure("keyword", foreground="#BE90B7")
            keywords = [
'include','pub','fn','macro','print','return','while','if','elsif','else'
]

            content = self.text_area.get("1.0", tk.END)
            pattern = r'(\b(?:' + '|'.join(map(re.escape, keywords)) + r')\b)|\n'
            for match in re.finditer(pattern, content, flags=re.IGNORECASE):
                start = match.start()
                end = match.end()
                self.text_area.tag_add("keyword", f"1.{start}", f"1.{end}")

            for line_number, line in enumerate(content.split("\n"), start=1):
                if not line.strip():
                    start = f"{line_number}.0"
                    end = f"{line_number}.end"
                    self.text_area.tag_add("keyword", start, end)
                elif line == "\n":
                    start = f"{line_number}.0"
                    end = f"{line_number}.end"
                    self.text_area.tag_add("keyword", start, end)

            for line_number, line in enumerate(content.split("\n"), start=1):
                for keyword in keywords:
                    pattern = r'\b' + re.escape(keyword) + r'\b'
                    for match in re.finditer(pattern, line):
                        start = match.start()
                        end = match.end()
                        start_position = f"{line_number}.{start}"
                        end_position = f"{line_number}.{end}"
                        self.text_area.tag_add("keyword", start_position, end_position)

            self.text_area.tag_configure("function", foreground="#BE90B7")

            function_pattern = r"\b[a-zA-Z_]+\s*(?=\()"
            start = 1.0
            while True:
                start = self.text_area.search(function_pattern, start, stopindex=tk.END, regexp=True)
                if not start:
                    break
                end = self.text_area.index(f"{start}+1c")
                self.text_area.tag_add("function", start, end)
                start = end

            self.text_area.tag_delete("highlight")
            content = self.text_area.get("1.0", tk.END)
            lines = content.split("\n")
            class_pattern = r'class\s+([a-zA-Z_]\w*)\s*:'
            for line_number, line in enumerate(lines, start=1):
                for match in re.finditer(class_pattern, line, flags=re.DOTALL):
                    start = match.start(1)
                    end = match.end(1)

                    class_name = line[start:end]

                    self.text_area.tag_add("highlight", f"{line_number}.{start}", f"{line_number}.{end}")
                    self.text_area.tag_configure("highlight", foreground="#EFA856")


            self.text_area.tag_delete("function_highlight")
            self.text_area.tag_delete("text_highlight")

            content = self.text_area.get("1.0", tk.END)
            lines = content.split("\n")

            function_pattern = r'\b(\w+)\s*\(\s*.*?\s*\)\s*'
            for line_number, line in enumerate(lines, start=1):
                for match in re.finditer(function_pattern, line, flags=re.DOTALL):
                    start = match.start()
                    end = match.end()

                    function_name = line[start:end].split("(")[0].strip()

                    start = line.find(function_name)
                    end = start + len(function_name)

                    self.text_area.tag_add("function_highlight", f"{line_number}.{start}", f"{line_number}.{end}")
                    self.text_area.tag_configure("function_highlight", foreground="#5287B5")

            text_pattern = r'(["\'])(?:(?!\1|{)[^"\']*)\1|({[^{}]*})'
            for line_number, line in enumerate(lines, start=1):
                for match in re.finditer(text_pattern, line, flags=re.DOTALL):
                    start = match.start(0)
                    end = match.end(0)

                    if match.group(1):
                        self.text_area.tag_add("text_highlight", f"{line_number}.{start}", f"{line_number}.{end}")
                        self.text_area.tag_configure("text_highlight", foreground="#91BC8E")


            special_words = ["not", "self"]

            special_words_pattern = r'\b(' + '|'.join(map(re.escape, special_words)) + r')\b'
            for line_number, line in enumerate(lines, start=1):
                for match in re.finditer(special_words_pattern, line):
                    start = match.start()
                    end = match.end()

                    self.text_area.tag_add("special_highlight", f"{line_number}.{start}", f"{line_number}.{end}")
                    self.text_area.tag_configure("special_highlight", foreground="#DD5D63")

            int_pattern = r'(\d+)|='
            for line_number, line in enumerate(content.split("\n"), start=1):
                for match in re.finditer(int_pattern, line):
                    start = match.start()
                    end = match.end()
                    self.text_area.tag_add("int", f"{line_number}.{start}", f"{line_number}.{end}")
                    self.text_area.tag_configure("int", foreground="#EFA856")
        elif selected_syntax.lower() == "ruby":
            self.text_area.tag_delete("keyword")
            self.text_area.tag_configure("keyword", foreground="#BE90B7")
            keywords = ['BEGIN','END','alias','and','begin','break','case','class','def','defined?','do','else','elsif','end','false','for','if','in','module','next','nil','not','or','redo','rescue','retry','return','self','super','then','true','undef','unless','until','when','while','yield']

            content = self.text_area.get("1.0", tk.END)
            pattern = r'(\b(?:' + '|'.join(map(re.escape, keywords)) + r')\b)|\n'
            for match in re.finditer(pattern, content, flags=re.IGNORECASE):
                start = match.start()
                end = match.end()
                self.text_area.tag_add("keyword", f"1.{start}", f"1.{end}")

            for line_number, line in enumerate(content.split("\n"), start=1):
                if not line.strip():
                    start = f"{line_number}.0"
                    end = f"{line_number}.end"
                    self.text_area.tag_add("keyword", start, end)
                elif line == "\n":
                    start = f"{line_number}.0"
                    end = f"{line_number}.end"
                    self.text_area.tag_add("keyword", start, end)

            for line_number, line in enumerate(content.split("\n"), start=1):
                for keyword in keywords:
                    pattern = r'\b' + re.escape(keyword) + r'\b'
                    for match in re.finditer(pattern, line):
                        start = match.start()
                        end = match.end()
                        start_position = f"{line_number}.{start}"
                        end_position = f"{line_number}.{end}"
                        self.text_area.tag_add("keyword", start_position, end_position)

            self.text_area.tag_configure("function", foreground="#BE90B7")

            function_pattern = r"\b[a-zA-Z_]+\s*(?=\()"
            start = 1.0
            while True:
                start = self.text_area.search(function_pattern, start, stopindex=tk.END, regexp=True)
                if not start:
                    break
                end = self.text_area.index(f"{start}+1c")
                self.text_area.tag_add("function", start, end)
                start = end

            self.text_area.tag_delete("highlight")
            content = self.text_area.get("1.0", tk.END)
            lines = content.split("\n")
            class_pattern = r'class\s+([a-zA-Z_]\w*)\s*:'
            for line_number, line in enumerate(lines, start=1):
                for match in re.finditer(class_pattern, line, flags=re.DOTALL):
                    start = match.start(1)
                    end = match.end(1)

                    class_name = line[start:end]

                    self.text_area.tag_add("highlight", f"{line_number}.{start}", f"{line_number}.{end}")
                    self.text_area.tag_configure("highlight", foreground="#EFA856")


            self.text_area.tag_delete("function_highlight")
            self.text_area.tag_delete("text_highlight")

            content = self.text_area.get("1.0", tk.END)
            lines = content.split("\n")

            function_pattern = r'\b(\w+)\s*\(\s*.*?\s*\)\s*'
            for line_number, line in enumerate(lines, start=1):
                for match in re.finditer(function_pattern, line, flags=re.DOTALL):
                    start = match.start()
                    end = match.end()

                    function_name = line[start:end].split("(")[0].strip()

                    start = line.find(function_name)
                    end = start + len(function_name)

                    self.text_area.tag_add("function_highlight", f"{line_number}.{start}", f"{line_number}.{end}")
                    self.text_area.tag_configure("function_highlight", foreground="#5287B5")

            text_pattern = r'(["\'])(?:(?!\1|{)[^"\']*)\1|({[^{}]*})'
            for line_number, line in enumerate(lines, start=1):
                for match in re.finditer(text_pattern, line, flags=re.DOTALL):
                    start = match.start(0)
                    end = match.end(0)

                    if match.group(1):
                        self.text_area.tag_add("text_highlight", f"{line_number}.{start}", f"{line_number}.{end}")
                        self.text_area.tag_configure("text_highlight", foreground="#91BC8E")


            special_words = []#["not", "self"]

            special_words_pattern = r'\b(' + '|'.join(map(re.escape, special_words)) + r')\b'
            for line_number, line in enumerate(lines, start=1):
                for match in re.finditer(special_words_pattern, line):
                    start = match.start()
                    end = match.end()

                    self.text_area.tag_add("special_highlight", f"{line_number}.{start}", f"{line_number}.{end}")
                    self.text_area.tag_configure("special_highlight", foreground="#DD5D63")

            int_pattern = r'(\d+)|='
            for line_number, line in enumerate(content.split("\n"), start=1):
                for match in re.finditer(int_pattern, line):
                    start = match.start()
                    end = match.end()
                    self.text_area.tag_add("int", f"{line_number}.{start}", f"{line_number}.{end}")
                    self.text_area.tag_configure("int", foreground="#EFA856")
        elif selected_syntax.lower() == "c":
            self.text_area.tag_delete("keyword")
            self.text_area.tag_configure("keyword", foreground="#BE90B7")
            keywords = ['auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do', 'double', 'else', 'enum', 'extern', 'float', 'for', 'goto', 'if', 'int', 'long', 'register', 'return', 'short', 'signed', 'sizeof', 'static', 'struct', 'switch', 'typedef', 'union', 'unsigned', 'void', 'volatile', 'while']

            content = self.text_area.get("1.0", tk.END)
            pattern = r'(\b(?:' + '|'.join(map(re.escape, keywords)) + r')\b)|\n'
            for match in re.finditer(pattern, content, flags=re.IGNORECASE):
                start = match.start()
                end = match.end()
                self.text_area.tag_add("keyword", f"1.{start}", f"1.{end}")

            for line_number, line in enumerate(content.split("\n"), start=1):
                if not line.strip():
                    start = f"{line_number}.0"
                    end = f"{line_number}.end"
                    self.text_area.tag_add("keyword", start, end)
                elif line == "\n":
                    start = f"{line_number}.0"
                    end = f"{line_number}.end"
                    self.text_area.tag_add("keyword", start, end)

            for line_number, line in enumerate(content.split("\n"), start=1):
                for keyword in keywords:
                    pattern = r'\b' + re.escape(keyword) + r'\b'
                    for match in re.finditer(pattern, line):
                        start = match.start()
                        end = match.end()
                        start_position = f"{line_number}.{start}"
                        end_position = f"{line_number}.{end}"
                        self.text_area.tag_add("keyword", start_position, end_position)

            self.text_area.tag_configure("function", foreground="#BE90B7")

            function_pattern = r"\b[a-zA-Z_]+\s*(?=\()"
            start = 1.0
            while True:
                start = self.text_area.search(function_pattern, start, stopindex=tk.END, regexp=True)
                if not start:
                    break
                end = self.text_area.index(f"{start}+1c")
                self.text_area.tag_add("function", start, end)
                start = end

            self.text_area.tag_delete("highlight")
            content = self.text_area.get("1.0", tk.END)
            lines = content.split("\n")
            class_pattern = r'class\s+([a-zA-Z_]\w*)\s*:'
            for line_number, line in enumerate(lines, start=1):
                for match in re.finditer(class_pattern, line, flags=re.DOTALL):
                    start = match.start(1)
                    end = match.end(1)

                    class_name = line[start:end]

                    self.text_area.tag_add("highlight", f"{line_number}.{start}", f"{line_number}.{end}")
                    self.text_area.tag_configure("highlight", foreground="#EFA856")


            self.text_area.tag_delete("function_highlight")
            self.text_area.tag_delete("text_highlight")

            content = self.text_area.get("1.0", tk.END)
            lines = content.split("\n")

            function_pattern = r'\b(\w+)\s*\(\s*.*?\s*\)\s*'
            for line_number, line in enumerate(lines, start=1):
                for match in re.finditer(function_pattern, line, flags=re.DOTALL):
                    start = match.start()
                    end = match.end()

                    function_name = line[start:end].split("(")[0].strip()

                    start = line.find(function_name)
                    end = start + len(function_name)

                    self.text_area.tag_add("function_highlight", f"{line_number}.{start}", f"{line_number}.{end}")
                    self.text_area.tag_configure("function_highlight", foreground="#5287B5")

            text_pattern = r'(["\'])(?:(?!\1|{)[^"\']*)\1|({[^{}]*})'
            for line_number, line in enumerate(lines, start=1):
                for match in re.finditer(text_pattern, line, flags=re.DOTALL):
                    start = match.start(0)
                    end = match.end(0)

                    if match.group(1):
                        self.text_area.tag_add("text_highlight", f"{line_number}.{start}", f"{line_number}.{end}")
                        self.text_area.tag_configure("text_highlight", foreground="#91BC8E")


            special_words = ["not", "self"]

            special_words_pattern = r'\b(' + '|'.join(map(re.escape, special_words)) + r')\b'
            for line_number, line in enumerate(lines, start=1):
                for match in re.finditer(special_words_pattern, line):
                    start = match.start()
                    end = match.end()

                    self.text_area.tag_add("special_highlight", f"{line_number}.{start}", f"{line_number}.{end}")
                    self.text_area.tag_configure("special_highlight", foreground="#DD5D63")

            int_pattern = r'(\d+)|='
            for line_number, line in enumerate(content.split("\n"), start=1):
                for match in re.finditer(int_pattern, line):
                    start = match.start()
                    end = match.end()
                    self.text_area.tag_add("int", f"{line_number}.{start}", f"{line_number}.{end}")
                    self.text_area.tag_configure("int", foreground="#EFA856")
class CodeEditor:
    def get_current_tab(self):
        for i in self.tabs:
            if i.get_state():
                return i
    def get_tabs(self):
        return self.tabs
    def exit_editor(self, event=''):
        self.root.ExitDestroy()
    def __init__(self, root):
        self.font_ = 'Cousine'
        self.font_size = 16
        self.tabs = []

        self.after_update = ''

        def update_tabs():
            self.after_update = self.root.after(100, update_tabs)
            if len(self.tabs) > 0:
                for i in self.tabs:
                    if i.get_state():
                        i.select_tab()
                        self.syntax_var.set(i.syntax_var.get())
                        self.auto_delete_var.set(i.auto_delete_var.get())
                    else:
                        i.unselect_tab()

        self.root = root
        self.root.title2("MS Code")
        self.root.minsize(750, 500)
        self.root.geometry("900x600")
        self.root.exitfunc = self.exit_editor
        #self.rpc = DiscordRpc(client_id)
        #self.connect = self.rpc.connect()

        #self.style = ThemedStyle(self.root)
        #self.style.set_theme("plastik")

        self.frame_main = tk.Frame(self.root.content, bg="#2E2E2E")
        self.frame_main.pack(side='left', fill='both', expand=1)

        self.frame_tabs = ctk.CTkScrollableFrame(self.frame_main, orientation='horizontal', height=25, corner_radius=0)
        self.frame_tabs.pack(fill='x')
        self.frame_tabs.configure(fg_color='#202020')
        self.frame_tabs.configure(scrollbar_fg_color="#2E2E2E")
        self.frame_tabs.configure(scrollbar_button_color="#2E2E2E")
        self.frame_tabs.configure(scrollbar_button_hover_color="#3E3E3E")

        """self.file_path = None

        self.line_numbers = tk.Text(self.root, bg="#2E2E2E", fg="gray", width=4, insertbackground="white", highlightthickness=0, highlightbackground='#2E2E2E', relief='flat', selectbackground='#2E2E2E', selectforeground='gray', cursor='')
        self.line_numbers.pack(side="left", fill="y")
        self.line_numbers.configure(font=(self.font_, self.font_size), state="disabled")

        self.text_area = tk.Text(self.root, wrap="none", bg="#2E2E2E", fg="lightgray", insertbackground="lightgray", highlightthickness=0, highlightbackground='#2E2E2E', relief='flat', selectbackground='#4545ad', selectforeground='lightgray')
        self.text_area.pack(side="left", fill="both", expand=True)
        self.text_area.configure(font=(self.font_, self.font_size))#Source Code Pro
        self.text_area.bind("<KeyRelease-Return>", self.on_text_change)
        self.text_area.bind("<KeyRelease-BackSpace>", self.on_text_change)

        self.line_numbers.bind('<FocusIn>', lambda e: self.text_area.focus())
        """
        self.menu_bar = mtk.MaxOSMenu(self.root)
        #self.root.config(menu=self.menu_bar)
        """
        self.undo_stack = []
        self.redo_stack = []
        root.bind("<Control-z>", self.undo)
        root.bind("<Control-y>", self.redo)
        """
        self.file_menu = mtk.AddMenuButton(label='Файл', menu=self.menu_bar.master)
        self.file_menu.add_command(label="Открыть", command=self.open_file)
        self.file_menu.add_command(label="Сохранить", command=self.save_file)
        self.file_menu.add_command(label="Создать файл", command=self.create_new_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Выход", command=self.exit_editor)
        """

        root.bind("<Control-s>", self.save_file)
        root.bind("<Control-a>", self.select_all)
        root.bind("<Control-c>", self.copy_text)
        root.bind("<Control-v>", self.paste_text)"""

        """self.text_area.config(yscrollcommand=self.scroll_text)
        self.line_numbers.config(yscrollcommand=self.scroll_text)"""

        #self.text_area.bind("<KeyRelease>", lambda event: self.on_key_press(event))
        self.syntax_var = tk.StringVar()
        self.syntax_var.set("txt")
        self.syntax_menu = mtk.AddMenuButton(label='Синтаксис', menu=self.menu_bar.master)
        syntax_styles = ['txt', "Python", 'Ruby', 'C']
        for style in syntax_styles:
            self.syntax_menu.add_radiobutton(label=style.capitalize(), variable=self.syntax_var, value=style,
                                             command=self.change_syntax)

        self.settings_menu = mtk.AddMenuButton(label='Настройки', menu=self.menu_bar.master)

        self.view_menu = tk.Menu(self.settings_menu.menu, tearoff=0)
        self.settings_menu.add_cascade(label='Вид', menu=self.view_menu)

        self.font_menu = tk.Menu(self.view_menu, tearoff=0)
        self.view_menu.add_cascade(label='Шрифт', menu=self.font_menu)
        self.font_menu.add_command(label='Увеличить', command=lambda: self.change_font_size('+'))
        self.font_menu.add_command(label='Уменьшить', command=lambda: self.change_font_size('-'))
        self.font_menu.add_command(label='Стандартный размер', command=lambda: self.change_font_size('='))

        self.auto_delete_var = tk.IntVar()
        self.auto_delete_var.set(0)

        self.settings_menu.add_checkbutton(label='Автоматическое удаление скобок и кавычек', variable=self.auto_delete_var, command=self.change_auto_delete)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.root.bind('<Control-o>', lambda e:self.open_file())
        self.root.bind('<Control-n>', lambda e:self.create_new_file())

        """
        self.text_area.tag_configure("keyword", foreground="#BE90B7")
        self.text_area.tag_configure("function", foreground="#BE90B7")
        self.text_area.tag_configure("class_highlight", foreground="#EFA856")
        self.text_area.tag_configure("function_highlight", foreground="#5287B5")
        self.text_area.tag_configure("text_highlight", foreground="#91BC8E")
        self.text_area.tag_configure("special_highlight", foreground="#DD5D63")
        self.text_area.tag_configure("int", foreground="#EFA856")
        """

        try:
            if fileopen != '':
                file_path = fileopen
                with open(file_path, "r", encoding='utf-8') as file:
                    '''
                    content = file.read()
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(tk.END, content)
                    self.file_path = file_path

                    self.highlight_syntax()
                    current_text = self.text_area.get("1.0", tk.END)
                    self.undo_stack.append(current_text)
                    self.redo_stack.clear()
                    self.update_line_numbers()
                    self.scroll_text("moveto", self.text_area.yview()[0])
                    '''
                    self.file_path = file_path

                    tab = TabText(master_tabs=self.frame_tabs, master=self.frame_main, root=self.root, file_path=file_path, editor=self, tab_list=self.tabs)

                    for i in self.tabs:
                        i.unselect_tab()

                    self.tabs.append(tab)

                    tab.select_tab()

                    content = file.read()

                    tab.text_area.delete(1.0, tk.END)
                    tab.text_area.insert(tk.END, content)

                    if os.path.splitext(file_path)[1] in ['.py', '.pyw']:
                        tab.change_syntax('Python')
                    elif os.path.splitext(file_path)[1] in ['.rb']:
                        tab.change_syntax('Ruby')
                    elif os.path.splitext(file_path)[1] in ['.c']:
                        tab.change_syntax('C')
                    else:
                        tab.change_syntax('txt')
                    tab.highlight_syntax()
                    current_text = tab.text_area.get("1.0", tk.END)
                    tab.undo_stack.append(current_text)
                    tab.redo_stack.clear()
                    tab.update_line_numbers()
                    tab.scroll_text("moveto", tab.text_area.yview()[0])


        except:
            import traceback
            print(traceback.format_exc())

        update_tabs()

    def change_syntax(self):
        for i in self.tabs:
            if i.get_state():
                i.change_syntax(self.syntax_var.get())

    def change_auto_delete(self):
        for i in self.tabs:
            if i.get_state():
                i.change_auto_delete(self.auto_delete_var.get())

    def change_font_size(self, arg):
        for i in self.tabs:
            if i.get_state():
                i.change_font_size(arg)

    def load_plugins(self):
        plugin_folder = "./plugins"
        if os.path.exists(plugin_folder):
            for filename in os.listdir(plugin_folder):
                if filename.endswith(".py"):
                    plugin_name = os.path.splitext(filename)[0]
                    spec = importlib.util.spec_from_file_location(plugin_name, os.path.join(plugin_folder, filename))
                    module = importlib.util.module_from_spec(spec)
                    try:
                        spec.loader.exec_module(module)
                        if hasattr(module, 'activate'):
                            module.activate(self)
                    except Exception as e:
                        print(f"Ошибка при загрузке плагина {plugin_name}: {str(e)}")

    def font_size_plus(self, event=''):
        self.font_size += 1
        self.text_area.configure(font=(self.font_, self.font_size))
        self.line_numbers.configure(font=(self.font_, self.font_size), state="disabled")

    def font_size_minus(self, event=''):
        if self.font_size > 1:
            self.font_size -= 1
            self.text_area.configure(font=(self.font_, self.font_size))
            self.line_numbers.configure(font=(self.font_, self.font_size), state="disabled")

    def font_size_equal(self, event=''):
        self.font_size = 16
        self.text_area.configure(font=(self.font_, self.font_size))
        self.line_numbers.configure(font=(self.font_, self.font_size), state="disabled")

    def copy_text(self, event=None):
        global clipboard
        clipboard = event.widget.get("sel.first", "sel.last")

    def paste_text(self, event=None):
        global clipboard, pasted
        if not pasted:
            event.widget.insert("insert", clipboard)
            pasted = True
        else:
            pasted = False

    def on_key_press(self, event):
        self.highlight_syntax(event)
        self.update_line_numbers()

    def select_all(self, event=None):
        event.widget.tag_add("sel", "1.0", "end")

    def on_text_change(self, event):
        current_text = self.text_area.get("1.0", "end")
        self.undo_stack.append(current_text)
        self.redo_stack.clear()
        self.update_line_numbers()

    def undo(self, event):
        if len(self.undo_stack) > 1:
            self.redo_stack.append(self.undo_stack.pop())
            previous_state = self.undo_stack.pop()
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", previous_state)
            self.update_line_numbers()

    def redo(self, event):
        if self.redo_stack:
            next_state = self.redo_stack.pop()
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", next_state)
            self.update_line_numbers()

    def open_file(self):
        def OK():
            self.no_open = 1
            file_path = WIN.getpath()
            if file_path:
                try:
                    for i in self.tabs:
                        if i.file_path == file_path:
                            i.select_tab()
                            self.no_open = 0
                        else:
                            i.unselect_tab()

                    else:
                        if self.no_open:
                            with open(file_path, "r", encoding='utf-8') as file:
                                '''
                                content = file.read()
                                self.text_area.delete(1.0, tk.END)
                                self.text_area.insert(tk.END, content)
                                self.file_path = file_path

                                self.highlight_syntax()
                                current_text = self.text_area.get("1.0", tk.END)
                                self.undo_stack.append(current_text)
                                self.redo_stack.clear()
                                self.update_line_numbers()
                                self.scroll_text("moveto", self.text_area.yview()[0])
                                '''

                                tab = TabText(master_tabs=self.frame_tabs, master=self.frame_main, root=self.root, file_path=file_path, editor=self, tab_list=self.tabs)

                                for i in self.tabs:
                                    i.unselect_tab()

                                self.tabs.append(tab)

                                tab.select_tab()

                                content = file.read()

                                tab.text_area.delete(1.0, tk.END)
                                tab.text_area.insert(tk.END, content)

                                if os.path.splitext(file_path)[1] in ['.py', '.pyw']:
                                    tab.change_syntax('Python')
                                elif os.path.splitext(file_path)[1] in ['.rb']:
                                    tab.change_syntax('Ruby')
                                elif os.path.splitext(file_path)[1] in ['.c']:
                                    tab.change_syntax('C')
                                else:
                                    tab.change_syntax('txt')
                                tab.highlight_syntax()
                                current_text = tab.text_area.get("1.0", tk.END)
                                tab.undo_stack.append(current_text)
                                tab.redo_stack.clear()
                                tab.update_line_numbers()
                                tab.scroll_text("moveto", tab.text_area.yview()[0])
                except Exception as e:
                    mtk.DialogWin(self.root, text=f"Ошибка при открытии файла: {str(e)}", title='Ошибка', type='error')
            WIN.destroy()
        WIN = mtk.FileDialogWin(self.root, title='Выберите файл', command=OK)

    def save_file(self, event=None):
        '''
        if self.file_path:
            try:
                with open(self.file_path, "w", encoding='utf-8') as file:
                    content = self.text_area.get(1.0, tk.END)
                    file.write(content)
                    messagebox.showinfo("Сохранено", "Файл успешно сохранен.")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при сохранении файла: {str(e)}")
        else:
            messagebox.showerror("Ошибка", "Выберите файл для сохранения.")
        '''
        for i in self.tabs:
            if i.get_state():
                i.save_file()


    def create_new_file(self):
        tab = TabText(master_tabs=self.frame_tabs, master=self.frame_main, root=self.root, file_path=None, editor=self, tab_list=self.tabs)

        for i in self.tabs:
            i.unselect_tab()

        self.tabs.append(tab)

        tab.select_tab()

        tab.change_syntax('txt')

    def scroll_text(self, *args):
        try:
            self.text_area.yview_moveto(args[0])
            self.line_numbers.yview_moveto(args[0])
        except:
            pass

    def update_line_numbers(self):
        text_content = self.text_area.get("1.0", "end-1c")
        lines = text_content.split('\n')

        if not lines[-1] and text_content.endswith('\n'):
            lines[-1] = ''

        line_count = len(lines)
        line_numbers_text = "\n".join(str(i) for i in range(1, line_count + 1))
        self.line_numbers.config(state="normal")
        self.line_numbers.delete("1.0", "end")
        self.line_numbers.insert("1.0", line_numbers_text)
        self.line_numbers.config(state="disabled")

    def highlight_syntax(self, event=None):
        selected_syntax = self.syntax_var.get()
        if selected_syntax.lower() == "python":
            self.text_area.tag_delete("keyword")
            self.text_area.tag_configure("keyword", foreground="#BE90B7")
            keywords = ["if", "elif", "else", "for", "while", "def", "class", "import", "from", "return", "except", "try", "await", "async", "as", "raise", 'in']

            content = self.text_area.get("1.0", tk.END)
            pattern = r'(\b(?:' + '|'.join(map(re.escape, keywords)) + r')\b)|\n'
            for match in re.finditer(pattern, content, flags=re.IGNORECASE):
                start = match.start()
                end = match.end()
                self.text_area.tag_add("keyword", f"1.{start}", f"1.{end}")

            for line_number, line in enumerate(content.split("\n"), start=1):
                if not line.strip():
                    start = f"{line_number}.0"
                    end = f"{line_number}.end"
                    self.text_area.tag_add("keyword", start, end)
                elif line == "\n":
                    start = f"{line_number}.0"
                    end = f"{line_number}.end"
                    self.text_area.tag_add("keyword", start, end)

            for line_number, line in enumerate(content.split("\n"), start=1):
                for keyword in keywords:
                    pattern = r'\b' + re.escape(keyword) + r'\b'
                    for match in re.finditer(pattern, line):
                        start = match.start()
                        end = match.end()
                        start_position = f"{line_number}.{start}"
                        end_position = f"{line_number}.{end}"
                        self.text_area.tag_add("keyword", start_position, end_position)

            self.text_area.tag_configure("function", foreground="#BE90B7")

            function_pattern = r"\b[a-zA-Z_]+\s*(?=\()"
            start = 1.0
            while True:
                start = self.text_area.search(function_pattern, start, stopindex=tk.END, regexp=True)
                if not start:
                    break
                end = self.text_area.index(f"{start}+1c")
                self.text_area.tag_add("function", start, end)
                start = end

            self.text_area.tag_delete("highlight")
            content = self.text_area.get("1.0", tk.END)
            lines = content.split("\n")
            class_pattern = r'class\s+([a-zA-Z_]\w*)\s*:'
            for line_number, line in enumerate(lines, start=1):
                for match in re.finditer(class_pattern, line, flags=re.DOTALL):
                    start = match.start(1)
                    end = match.end(1)

                    class_name = line[start:end]

                    self.text_area.tag_add("highlight", f"{line_number}.{start}", f"{line_number}.{end}")
                    self.text_area.tag_configure("highlight", foreground="#EFA856")


            self.text_area.tag_delete("function_highlight")
            self.text_area.tag_delete("text_highlight")

            content = self.text_area.get("1.0", tk.END)
            lines = content.split("\n")

            function_pattern = r'\b(\w+)\s*\(\s*.*?\s*\)\s*'
            for line_number, line in enumerate(lines, start=1):
                for match in re.finditer(function_pattern, line, flags=re.DOTALL):
                    start = match.start()
                    end = match.end()

                    function_name = line[start:end].split("(")[0].strip()

                    start = line.find(function_name)
                    end = start + len(function_name)

                    self.text_area.tag_add("function_highlight", f"{line_number}.{start}", f"{line_number}.{end}")
                    self.text_area.tag_configure("function_highlight", foreground="#5287B5")

            text_pattern = r'(["\'])(?:(?!\1|{)[^"\']*)\1|({[^{}]*})'
            for line_number, line in enumerate(lines, start=1):
                for match in re.finditer(text_pattern, line, flags=re.DOTALL):
                    start = match.start(0)
                    end = match.end(0)

                    if match.group(1):
                        self.text_area.tag_add("text_highlight", f"{line_number}.{start}", f"{line_number}.{end}")
                        self.text_area.tag_configure("text_highlight", foreground="#91BC8E")


            special_words = ["not", "self"]

            special_words_pattern = r'\b(' + '|'.join(map(re.escape, special_words)) + r')\b'
            for line_number, line in enumerate(lines, start=1):
                for match in re.finditer(special_words_pattern, line):
                    start = match.start()
                    end = match.end()

                    self.text_area.tag_add("special_highlight", f"{line_number}.{start}", f"{line_number}.{end}")
                    self.text_area.tag_configure("special_highlight", foreground="#DD5D63")

            int_pattern = r'(\d+)|='
            for line_number, line in enumerate(content.split("\n"), start=1):
                for match in re.finditer(int_pattern, line):
                    start = match.start()
                    end = match.end()
                    self.text_area.tag_add("int", f"{line_number}.{start}", f"{line_number}.{end}")
                    self.text_area.tag_configure("int", foreground="#EFA856")
        elif selected_syntax.lower() == "ruby":
            self.text_area.tag_delete("keyword")
            self.text_area.tag_configure("keyword", foreground="#BE90B7")
            keywords = ['BEGIN','END','alias','and','begin','break','case','class','def','defined?','do','else','elsif','end','false','for','if','in','module','next','nil','not','or','redo','rescue','retry','return','self','super','then','true','undef','unless','until','when','while','yield']

            content = self.text_area.get("1.0", tk.END)
            pattern = r'(\b(?:' + '|'.join(map(re.escape, keywords)) + r')\b)|\n'
            for match in re.finditer(pattern, content, flags=re.IGNORECASE):
                start = match.start()
                end = match.end()
                self.text_area.tag_add("keyword", f"1.{start}", f"1.{end}")

            for line_number, line in enumerate(content.split("\n"), start=1):
                if not line.strip():
                    start = f"{line_number}.0"
                    end = f"{line_number}.end"
                    self.text_area.tag_add("keyword", start, end)
                elif line == "\n":
                    start = f"{line_number}.0"
                    end = f"{line_number}.end"
                    self.text_area.tag_add("keyword", start, end)

            for line_number, line in enumerate(content.split("\n"), start=1):
                for keyword in keywords:
                    pattern = r'\b' + re.escape(keyword) + r'\b'
                    for match in re.finditer(pattern, line):
                        start = match.start()
                        end = match.end()
                        start_position = f"{line_number}.{start}"
                        end_position = f"{line_number}.{end}"
                        self.text_area.tag_add("keyword", start_position, end_position)

            self.text_area.tag_configure("function", foreground="#BE90B7")

            function_pattern = r"\b[a-zA-Z_]+\s*(?=\()"
            start = 1.0
            while True:
                start = self.text_area.search(function_pattern, start, stopindex=tk.END, regexp=True)
                if not start:
                    break
                end = self.text_area.index(f"{start}+1c")
                self.text_area.tag_add("function", start, end)
                start = end

            self.text_area.tag_delete("highlight")
            content = self.text_area.get("1.0", tk.END)
            lines = content.split("\n")
            class_pattern = r'class\s+([a-zA-Z_]\w*)\s*:'
            for line_number, line in enumerate(lines, start=1):
                for match in re.finditer(class_pattern, line, flags=re.DOTALL):
                    start = match.start(1)
                    end = match.end(1)

                    class_name = line[start:end]

                    self.text_area.tag_add("highlight", f"{line_number}.{start}", f"{line_number}.{end}")
                    self.text_area.tag_configure("highlight", foreground="#EFA856")


            self.text_area.tag_delete("function_highlight")
            self.text_area.tag_delete("text_highlight")

            content = self.text_area.get("1.0", tk.END)
            lines = content.split("\n")

            function_pattern = r'\b(\w+)\s*\(\s*.*?\s*\)\s*'
            for line_number, line in enumerate(lines, start=1):
                for match in re.finditer(function_pattern, line, flags=re.DOTALL):
                    start = match.start()
                    end = match.end()

                    function_name = line[start:end].split("(")[0].strip()

                    start = line.find(function_name)
                    end = start + len(function_name)

                    self.text_area.tag_add("function_highlight", f"{line_number}.{start}", f"{line_number}.{end}")
                    self.text_area.tag_configure("function_highlight", foreground="#5287B5")

            text_pattern = r'(["\'])(?:(?!\1|{)[^"\']*)\1|({[^{}]*})'
            for line_number, line in enumerate(lines, start=1):
                for match in re.finditer(text_pattern, line, flags=re.DOTALL):
                    start = match.start(0)
                    end = match.end(0)

                    if match.group(1):
                        self.text_area.tag_add("text_highlight", f"{line_number}.{start}", f"{line_number}.{end}")
                        self.text_area.tag_configure("text_highlight", foreground="#91BC8E")


            special_words = ["not", "self"]

            special_words_pattern = r'\b(' + '|'.join(map(re.escape, special_words)) + r')\b'
            for line_number, line in enumerate(lines, start=1):
                for match in re.finditer(special_words_pattern, line):
                    start = match.start()
                    end = match.end()

                    self.text_area.tag_add("special_highlight", f"{line_number}.{start}", f"{line_number}.{end}")
                    self.text_area.tag_configure("special_highlight", foreground="#DD5D63")

            int_pattern = r'(\d+)|='
            for line_number, line in enumerate(content.split("\n"), start=1):
                for match in re.finditer(int_pattern, line):
                    start = match.start()
                    end = match.end()
                    self.text_area.tag_add("int", f"{line_number}.{start}", f"{line_number}.{end}")
                    self.text_area.tag_configure("int", foreground="#EFA856")

root = mtk.MaxOSTk(icon=f"{cwd}/icon.png")
app = CodeEditor(root)
app.load_plugins()
