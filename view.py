from controller import Controller
import customtkinter as ctk
from PIL import ImageTk
from tkinter import messagebox, filedialog
import win32clipboard, os
from datetime import datetime
import ctypes


class View():
    def __init__(self, master):

        self.root = master
        self.controller = None

        # paleta kolorów
        self.header_color = '#45818E'
        self.sidebar_color = '#A2C4C9'
        self.sidebar_button_color = '#45818E'
        self.sidebar_button_click_color = '#A2C4C9'
        self.main_frame_color = '#0B343D'
        self.main_button_color = '#D9D9D9'
        self.main_button_click_color = '#434343'
        self.main_textbox_bg_color = '#D0E0E3'
        self.main_text_color = '#212121'
        self.sidebar_app_name_color = '#E9F3F5'
        self.main_inner_frame_color = '#10444F'
        self.help_header_text_color = '#E6C44C'

        # wymiary/nazwy okien i ich elementów
        self.main_window_width = 1024
        self.main_window_height = 600

        self.sidebar_width = 0.2*self.main_window_width
        self.sidebar_height = self.main_window_height

        self.sidebar_logo_height = 0.2*self.sidebar_height
        self.sidebar_logo_width = 0.8*self.sidebar_width
        self.sidebar_button_width = 0.8*self.sidebar_width
        self.sidebar_button_height = 0.05*self.sidebar_height

        self.header_width = 0.8*self.main_window_width
        self.header_height = 0.1*self.main_window_height

        self.workspace_width = 0.8*self.main_window_width
        self.workspace_height = 0.9*self.main_window_height+0.5

        # nagłówki
        self.main_window_name = 'Gene Helper'
        self.sidebar_button_text = ['Start', 'Nić komplementarna', 'Transkrypcja', 'Splicing', 'Translacja', 'Analiza mutacji', 'Pomoc/FAQ']

        # ścieżki do obrazów
        self.logo_img = 'images\\app_logo.png'

        # zmienne
        self.input_sequence = None
        self.output = None
        self.exons = None
        self.mutations = None
        self.html_output = None

        # właściwości głównego okna
        self.root.geometry(f'{self.main_window_width}x{self.main_window_height}')
        self.root.title(self.main_window_name)
        self.root.resizable(False, False) 
        ctk.set_appearance_mode("light")

        myappid = u'nocompany.app.genehelper.001'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        self.root_icon = ImageTk.PhotoImage(file = self.logo_img)
        self.root.iconphoto(False, self.root_icon)

        self.current_frame_no = 1

        # ramka panelu nawigacyjnego
        self.sidebar = ctk.CTkFrame(self.root, fg_color=self.sidebar_color, bg_color=self.sidebar_color, 
                                    width=self.sidebar_width, height=self.sidebar_height)
        self.sidebar.place(relx=0.0, rely=0.0)

        # widżety panelu nawigacyjnego
        self.sidebar_logo = ctk.CTkLabel(self.sidebar, text='Gene \nHelper', text_color=self.sidebar_app_name_color, 
                                         height=self.sidebar_logo_height, width=self.sidebar_logo_width, justify="left")
        self.sidebar_logo.place(relx=0.5, rely=0.14, anchor='center')  
        self.sidebar_logo.cget("font").configure(weight="bold", size=48)

        self.sidebar_button_start = ctk.CTkButton(self.sidebar, text=self.sidebar_button_text[0],
                                            command=lambda:self.show_frame(self.frame1, 1, self.sidebar_button_start, self.current_frame_no), 
                                            fg_color=self.sidebar_button_color, hover_color=self.main_frame_color, 
                                            width=self.sidebar_button_width, height=self.sidebar_button_height)
        self.sidebar_button_start.place(relx=0.5, rely=0.3, anchor='center')
        self.sidebar_button_start.cget("font").configure(weight="bold")
        
        self.sidebar_button_compl = ctk.CTkButton(self.sidebar, text=self.sidebar_button_text[1],
                                            command=lambda:self.show_frame(self.frame2, 2, self.sidebar_button_compl, self.current_frame_no), 
                                            fg_color=self.sidebar_button_color, hover_color=self.main_frame_color, 
                                            width=self.sidebar_button_width, height=self.sidebar_button_height)
        self.sidebar_button_compl.place(relx=0.5, rely=0.37, anchor='center')
        self.sidebar_button_compl.cget("font").configure(weight="bold")
        
        self.sidebar_button_transcript = ctk.CTkButton(self.sidebar, text=self.sidebar_button_text[2], 
                                            command=lambda:self.show_frame(self.frame3, 3, self.sidebar_button_transcript, self.current_frame_no),
                                            fg_color=self.sidebar_button_color, hover_color=self.main_frame_color, 
                                            width=self.sidebar_button_width, height=self.sidebar_button_height)
        self.sidebar_button_transcript.place(relx=0.5, rely=0.44, anchor='center')
        self.sidebar_button_transcript.cget("font").configure(weight="bold")

        self.sidebar_button_splicing = ctk.CTkButton(self.sidebar, text=self.sidebar_button_text[3],
                                            command=lambda:self.show_frame(self.frame4, 4, self.sidebar_button_splicing, self.current_frame_no), 
                                            fg_color=self.sidebar_button_color, hover_color=self.main_frame_color, 
                                            width=self.sidebar_button_width, height=self.sidebar_button_height)
        self.sidebar_button_splicing.place(relx=0.5, rely=0.51, anchor='center')
        self.sidebar_button_splicing.cget("font").configure(weight="bold")
        
        self.sidebar_button_translate = ctk.CTkButton(self.sidebar, text=self.sidebar_button_text[4],
                                            command=lambda:self.show_frame(self.frame5, 5, self.sidebar_button_translate, self.current_frame_no), 
                                            fg_color=self.sidebar_button_color, hover_color=self.main_frame_color, 
                                            width=self.sidebar_button_width, height=self.sidebar_button_height)
        self.sidebar_button_translate.place(relx=0.5, rely=0.58, anchor='center')
        self.sidebar_button_translate.cget("font").configure(weight="bold")
        
        self.sidebar_button_analyze = ctk.CTkButton(self.sidebar, text=self.sidebar_button_text[5],
                                            command=lambda:self.show_frame(self.frame6, 6, self.sidebar_button_analyze, self.current_frame_no), 
                                            fg_color=self.sidebar_button_color, hover_color=self.main_frame_color, 
                                            width=self.sidebar_button_width, height=self.sidebar_button_height)
        self.sidebar_button_analyze.place(relx=0.5, rely=0.65, anchor='center')
        self.sidebar_button_analyze.cget("font").configure(weight="bold")
        
        self.sidebar_button_help = ctk.CTkButton(self.sidebar, text=self.sidebar_button_text[6],
                                            command=lambda:self.show_frame(self.frame7, 7, self.sidebar_button_help, self.current_frame_no), 
                                            fg_color=self.sidebar_button_color, hover_color=self.main_frame_color, 
                                            width=self.sidebar_button_width, height=self.sidebar_button_height)
        self.sidebar_button_help.place(relx=0.5, rely=0.95, anchor='center')

        # ramka nagłówka
        self.header = ctk.CTkFrame(self.root, fg_color=self.header_color, bg_color=self.header_color, 
                                   width=self.header_width, height=self.header_height)
        self.header.place(relx=0.2, rely=0.0)

        # widżety nagłówka (nazwa wybranej zakładki)
        self.header_label = ctk.CTkLabel(self.header, text='Nazwa wybranej zakładki', text_color='white')
        self.header_label.place(relx=0.02, rely=0.46, anchor='w')
        self.header_label.cget("font").configure(weight="bold", size=20)

        # główna ramka
        self.workspace = ctk.CTkFrame(self.root, fg_color=self.main_frame_color, bg_color=self.main_frame_color, 
                                      width=self.workspace_width, height=self.workspace_height)
        self.workspace.place(relx=0.2, rely=0.099)

        # ramka 1. (Start)
        self.frame1 = ctk.CTkFrame(self.workspace, fg_color=self.main_frame_color, 
                                   width=self.workspace_width, height=self.workspace_height)
        self.frame1.grid_columnconfigure(0, weight=1)
        self.frame1.grid_rowconfigure((0,1,3), weight=1)
        self.frame1.grid_rowconfigure(2, weight=6)

        # widżety ramki 1. (Start)
        self.start_label0 = ctk.CTkLabel(self.frame1, 
                           text='', 
                           fg_color=self.main_frame_color, text_color='white', justify='left', corner_radius=9, 
                           width=self.workspace_width-40, anchor='w')
        self.start_label0.grid(row=0, column=0, padx=20, pady=0)

        self.start_label1 = ctk.CTkLabel(self.frame1, 
                           text='\nAplikacja Gene Helper stworzona została jako część pracy magisterskiej na kierunku Informatyka.\n', 
                           fg_color=self.main_inner_frame_color, text_color='white', justify='left', corner_radius=9, 
                           width=self.workspace_width-40, anchor='w')
        self.start_label1.grid(row=1, column=0, padx=20, pady=10)
        self.start_label1.cget("font").configure(size=14, weight="bold")

        self.start_label2 = ctk.CTkLabel(self.frame1, 
                           text='\nOprócz strony startowej, na której się obecnie znajdujesz, dostępnych jest sześć zakładek:\n\n' +
                            '    - Nić komplementarna,\n\n' +
                            '    - Transkrypcja,\n\n' +
                            '    - Splicing,\n\n' +
                            '    - Translacja,\n\n' +
                            '    - Analiza mutacji.\n', 
                           fg_color=self.main_inner_frame_color, text_color='white', justify='left', corner_radius=9, 
                           width=self.workspace_width-40, anchor='w')
        self.start_label2.grid(row=2, column=0, padx=20, pady=10, sticky='news')
        self.start_label2.cget("font").configure(size=14, weight="bold")

        self.start_label3 = ctk.CTkLabel(self.frame1, 
                           text='\nPomocne informacje dostępne są na ostatniej zakładce "Pomoc/FAQ".\n', 
                           fg_color=self.main_inner_frame_color, text_color='white', justify='left', corner_radius=9, 
                           width=self.workspace_width-40, anchor='w')
        self.start_label3.grid(row=3, column=0, padx=20, pady=10, sticky='news')
        self.start_label3.cget("font").configure(size=14, weight="bold")

        # wyświetlenie ramki 1. (Start) - ramka domyślna przy uruchomieniu programu
        self.show_frame(self.frame1, 1, self.sidebar_button_start, 1)

        # ramka 2. (Nić komplementarna)
        self.frame2 = ctk.CTkFrame(self.workspace, fg_color=self.main_frame_color, 
                                   width=self.workspace_width, height=self.workspace_height)

        #widżety ramki 2. (Nić komplementarna)
        self.frame2_input_label = ctk.CTkLabel(self.frame2, text='Podaj sekwencję nici:', text_color='white')
        self.frame2_input_label.place(relx=0.03, rely=0.05)

        self.frame2_input_textbox = ctk.CTkTextbox(self.frame2, width=0.8*self.workspace_width, height=0.3*self.workspace_height, 
                                                   fg_color=self.main_textbox_bg_color)
        self.frame2_input_textbox.place(relx=0.03, rely=0.1)

        self.frame2_fromfile_button = ctk.CTkButton(self.frame2, text="Załaduj z pliku",
                                                    fg_color=self.sidebar_color, hover_color=self.main_button_color, text_color='black',
                                                    width=100, height=0.05*self.workspace_height, command=lambda: self.load_from_file(2))
        self.frame2_fromfile_button.place(relx=0.855, rely=0.1)

        self.frame2_analyze_button = ctk.CTkButton(self.frame2, text="Analizuj!",
                                                    fg_color=self.sidebar_color, hover_color=self.main_button_color, text_color='black',
                                                    width=100, height=0.05*self.workspace_height, command=self.start_2_analyze)
        self.frame2_analyze_button.place(relx=0.855, rely=0.35)

        self.frame2_res_label = ctk.CTkLabel(self.frame2, text='Nić komplementarna i odwrotnie komplementarna:', text_color='white')
        self.frame2_res_label.place(relx=0.03, rely=0.5)

        self.frame2_res_textbox = ctk.CTkTextbox(self.frame2, width=0.8*self.workspace_width, height=0.3*self.workspace_height, 
                                                 fg_color=self.main_textbox_bg_color)
        self.frame2_res_textbox.place(relx=0.03, rely=0.55)
        self.frame2_res_textbox.configure(state="disabled") 

        self.frame2_copy_button = ctk.CTkButton(self.frame2, text="Kopiuj",
                                                    fg_color=self.sidebar_color, hover_color=self.main_button_color, text_color='black',
                                                    width=100, height=0.05*self.workspace_height, command=lambda: self.copy_output(2))
        self.frame2_copy_button.place(relx=0.855, rely=0.55)

        self.frame2_tofile_button = ctk.CTkButton(self.frame2, text="Zapisz do pliku",
                                                    fg_color=self.sidebar_color, hover_color=self.main_button_color, text_color='black',
                                                    width=100, height=0.05*self.workspace_height, command=lambda: self.load_to_file(2))
        self.frame2_tofile_button.place(relx=0.855, rely=0.61)

        # ramka 3. (Transkrypcja)
        self.frame3 = ctk.CTkFrame(self.workspace, fg_color=self.main_frame_color, 
                                   width=self.workspace_width, height=self.workspace_height)

        # widżety ramki 3. (Transkrypcja)
        self.frame3_input_label = ctk.CTkLabel(self.frame3, text='Podaj sekwencję nici:', text_color='white')
        self.frame3_input_label.place(relx=0.03, rely=0.05)

        self.frame3_input_textbox = ctk.CTkTextbox(self.frame3, width=0.8*self.workspace_width, 
                                                   height=0.3*self.workspace_height, fg_color=self.main_textbox_bg_color)
        self.frame3_input_textbox.place(relx=0.03, rely=0.1)

        self.frame3_fromfile_button = ctk.CTkButton(self.frame3, text="Załaduj z pliku",
                                                    fg_color=self.sidebar_color, hover_color=self.main_button_color, text_color='black',
                                                    width=100, height=0.05*self.workspace_height, command=lambda: self.load_from_file(3))
        self.frame3_fromfile_button.place(relx=0.855, rely=0.1)

        self.frame3_analyze_button = ctk.CTkButton(self.frame3, text="Analizuj!",
                                                    fg_color=self.sidebar_color, hover_color=self.main_button_color, text_color='black',
                                                    width=100, height=0.05*self.workspace_height, command=self.start_3_analyze)
        self.frame3_analyze_button.place(relx=0.855, rely=0.35)

        self.frame3_res_label = ctk.CTkLabel(self.frame3, text='Wynik transkrypcji:', text_color='white')
        self.frame3_res_label.place(relx=0.03, rely=0.5)

        self.frame3_res_textbox = ctk.CTkTextbox(self.frame3, width=0.8*self.workspace_width, height=0.35*self.workspace_height, 
                                                 fg_color=self.main_textbox_bg_color)
        self.frame3_res_textbox.place(relx=0.03, rely=0.55)
        self.frame3_res_textbox.configure(state="disabled")

        self.frame3_copy_button = ctk.CTkButton(self.frame3, text="Kopiuj",
                                                    fg_color=self.sidebar_color, hover_color=self.main_button_color, text_color='black',
                                                    width=100, height=0.05*self.workspace_height, command=lambda: self.copy_output(3))
        self.frame3_copy_button.place(relx=0.855, rely=0.55)

        self.frame3_tofile_button = ctk.CTkButton(self.frame3, text="Zapisz do pliku",
                                                    fg_color=self.sidebar_color, hover_color=self.main_button_color, text_color='black',
                                                    width=100, height=0.05*self.workspace_height, command=lambda: self.load_to_file(3))
        self.frame3_tofile_button.place(relx=0.855, rely=0.61)


        # ramka 4. (Splicing)
        self.frame4 = ctk.CTkFrame(self.workspace, fg_color=self.main_frame_color, 
                                   width=self.workspace_width, height=self.workspace_height)
        
        # widżety ramki 4. (Splicing)
        self.frame4_input_seq_label = ctk.CTkLabel(self.frame4, text='Podaj sekwencję nici:', text_color='white')
        self.frame4_input_seq_label.place(relx=0.03, rely=0.05)

        self.frame4_input_seq_textbox = ctk.CTkTextbox(self.frame4, width=0.8*self.workspace_width, height=0.2*self.workspace_height, 
                                                       fg_color=self.main_textbox_bg_color)
        self.frame4_input_seq_textbox.place(relx=0.03, rely=0.1)

        self.frame4_fromfile_button = ctk.CTkButton(self.frame4, text="Załaduj z pliku",
                                                    fg_color=self.sidebar_color, hover_color=self.main_button_color, text_color='black',
                                                    width=100, height=0.05*self.workspace_height, command=lambda: self.load_from_file(4))
        self.frame4_fromfile_button.place(relx=0.855, rely=0.1)

        self.frame4_input_ex_label = ctk.CTkLabel(self.frame4, text='Podaj miejsca eksonów:', text_color='white')
        self.frame4_input_ex_label.place(relx=0.03, rely=0.3)

        self.frame4_input_ex_textbox = ctk.CTkTextbox(self.frame4, width=0.8*self.workspace_width, height=0.2*self.workspace_height, 
                                                      fg_color=self.main_textbox_bg_color)
        self.frame4_input_ex_textbox.place(relx=0.03, rely=0.35)

        self.frame4_analyze_button = ctk.CTkButton(self.frame4, text="Analizuj!",
                                                    fg_color=self.sidebar_color, hover_color=self.main_button_color, text_color='black',
                                                    width=100, height=0.05*self.workspace_height, command=self.start_4_analyze)
        self.frame4_analyze_button.place(relx=0.855, rely=0.5)

        self.frame4_res_label = ctk.CTkLabel(self.frame4, text='Wynik splicing\'u:', text_color='white')
        self.frame4_res_label.place(relx=0.03, rely=0.6)

        self.frame4_res_textbox = ctk.CTkTextbox(self.frame4, width=0.8*self.workspace_width, height=0.25*self.workspace_height, 
                                                 fg_color=self.main_textbox_bg_color)
        self.frame4_res_textbox.place(relx=0.03, rely=0.65)
        self.frame4_res_textbox.configure(state="disabled")

        self.frame4_copy_button = ctk.CTkButton(self.frame4, text="Kopiuj",
                                                    fg_color=self.sidebar_color, hover_color=self.main_button_color, text_color='black',
                                                    width=100, height=0.05*self.workspace_height, command=lambda: self.copy_output(4))
        self.frame4_copy_button.place(relx=0.855, rely=0.65)

        self.frame4_tofile_button = ctk.CTkButton(self.frame4, text="Zapisz do pliku",
                                                    fg_color=self.sidebar_color, hover_color=self.main_button_color, text_color='black',
                                                    width=100, height=0.05*self.workspace_height, command=lambda: self.load_to_file(4))
        self.frame4_tofile_button.place(relx=0.855, rely=0.71)

        # ramka 5. (Translacja)
        self.frame5 = ctk.CTkFrame(self.workspace, fg_color=self.main_frame_color, 
                                   width=self.workspace_width, height=self.workspace_height)

        # widżety ramki 5. (Translacja)
        self.frame5_input_label = ctk.CTkLabel(self.frame5, text='Podaj sekwencję nici:', text_color='white')
        self.frame5_input_label.place(relx=0.03, rely=0.05)

        self.frame5_input_textbox = ctk.CTkTextbox(self.frame5, width=0.8*self.workspace_width, height=0.3*self.workspace_height, 
                                                   fg_color=self.main_textbox_bg_color)
        self.frame5_input_textbox.place(relx=0.03, rely=0.1)

        self.frame5_fromfile_button = ctk.CTkButton(self.frame5, text="Załaduj z pliku",
                                                    fg_color=self.sidebar_color, hover_color=self.main_button_color, text_color='black',
                                                    width=100, height=0.05*self.workspace_height, command=lambda: self.load_from_file(5))
        self.frame5_fromfile_button.place(relx=0.855, rely=0.1)

        self.frame5_range_label = ctk.CTkLabel(self.frame5, text='Wybierz zakres:', text_color='white')
        self.frame5_range_label.place(relx=0.03, rely=0.405)

        self.frame5_range_combob = ctk.CTkComboBox(self.frame5, values=['Do końca sekwencji','Do kodonu STOP'], width=200, 
                                                   button_color=self.sidebar_color, button_hover_color=self.sidebar_button_color, 
                                                   fg_color=self.main_textbox_bg_color,
                                                   command=self.select_range)
        self.frame5_range_combob.place(relx=0.15, rely=0.407)

        self.frame5_analyze_button = ctk.CTkButton(self.frame5, text="Analizuj!",
                                                    fg_color=self.sidebar_color, hover_color=self.main_button_color, text_color='black',
                                                    width=100, height=0.05*self.workspace_height, command=self.start_5_analyze)
        self.frame5_analyze_button.place(relx=0.855, rely=0.4)

        self.frame5_res_label = ctk.CTkLabel(self.frame5, text='Wynik translacji:', text_color='white')
        self.frame5_res_label.place(relx=0.03, rely=0.5)

        self.frame5_res_textbox = ctk.CTkTextbox(self.frame5, width=0.8*self.workspace_width, height=0.35*self.workspace_height, 
                                                 fg_color=self.main_textbox_bg_color)
        self.frame5_res_textbox.place(relx=0.03, rely=0.55)
        self.frame5_res_textbox.configure(state="disabled")

        self.frame5_copy_button = ctk.CTkButton(self.frame5, text="Kopiuj",
                                                    fg_color=self.sidebar_color, hover_color=self.main_button_color, text_color='black',
                                                    width=100, height=0.05*self.workspace_height, command=lambda: self.copy_output(5))
        self.frame5_copy_button.place(relx=0.855, rely=0.55)

        self.frame5_tofile_button = ctk.CTkButton(self.frame5, text="Zapisz do pliku",
                                                    fg_color=self.sidebar_color, hover_color=self.main_button_color, text_color='black',
                                                    width=100, height=0.05*self.workspace_height, command=lambda: self.load_to_file(5))
        self.frame5_tofile_button.place(relx=0.855, rely=0.61)

        # ramka 6. (Analiza mutacji)
        self.frame6 = ctk.CTkFrame(self.workspace, fg_color=self.main_frame_color, 
                                   width=self.workspace_width, height=self.workspace_height)
        
        # widżety ramki 6. (Analiza mutacji)
        self.frame6_input_label = ctk.CTkLabel(self.frame6, text='Podaj dane wejściowe:', text_color='white')
        self.frame6_input_label.place(relx=0.03, rely=0.05)

        self.frame6_input_textbox = ctk.CTkTextbox(self.frame6, width=0.8*self.workspace_width, height=0.4*self.workspace_height, 
                                                   fg_color=self.main_textbox_bg_color)
        self.frame6_input_textbox.place(relx=0.03, rely=0.1)

        self.frame6_fromfile_button = ctk.CTkButton(self.frame6, text="Załaduj z pliku",
                                                    fg_color=self.sidebar_color, hover_color=self.main_button_color, text_color='black',
                                                    width=100, height=0.05*self.workspace_height, command=lambda: self.load_from_file(6))
        self.frame6_fromfile_button.place(relx=0.855, rely=0.1)

        self.frame6_analyze_button = ctk.CTkButton(self.frame6, text="Analizuj!",
                                                    fg_color=self.sidebar_color, hover_color=self.main_button_color, text_color='black',
                                                    width=100, height=0.05*self.workspace_height, command=self.start_6_analyze)
        self.frame6_analyze_button.place(relx=0.855, rely=0.45)

        self.frame6_res_label = ctk.CTkLabel(self.frame6, text='Wynik analizy:', text_color='white')
        self.frame6_res_label.place(relx=0.03, rely=0.5)

        self.frame6_res_textbox = ctk.CTkTextbox(self.frame6, width=0.8*self.workspace_width, height=0.4*self.workspace_height, 
                                                 fg_color=self.main_textbox_bg_color)
        self.frame6_res_textbox.place(relx=0.03, rely=0.55)
        self.frame6_res_textbox.configure(state="disabled")

        self.frame6_copy_button = ctk.CTkButton(self.frame6, text="Kopiuj",
                                                    fg_color=self.sidebar_color, hover_color=self.main_button_color, text_color='black',
                                                    width=100, height=0.05*self.workspace_height, command=lambda: self.copy_output(6))
        self.frame6_copy_button.place(relx=0.855, rely=0.55)

        self.frame6_tofile_button = ctk.CTkButton(self.frame6, text="Zapisz do pliku",
                                                    fg_color=self.sidebar_color, hover_color=self.main_button_color, text_color='black',
                                                    width=100, height=0.05*self.workspace_height, command=lambda: self.load_to_file(6))
        self.frame6_tofile_button.place(relx=0.855, rely=0.61)

        self.frame6_generate_compare_button = ctk.CTkButton(self.frame6, text="Generuj plik z porównaniem",
                                                    fg_color=self.sidebar_color, hover_color=self.main_button_color, text_color='black',
                                                    width=100, height=0.08*self.workspace_height, command=self.save_comparison_to_file)
        self.frame6_generate_compare_button._text_label.configure(wraplength=100)
        self.frame6_generate_compare_button.place(relx=0.855, rely=0.67)

        # ramka 7. (Pomoc/FAQ)
        self.frame7 = ctk.CTkScrollableFrame(self.workspace, width=self.workspace_width-20, height=self.workspace_height-10, 
                                             fg_color=self.main_frame_color)
        self.frame7.grid_columnconfigure(0, weight=1)

        # widżety ramki 7. (Pomoc/FAQ)
        ## Kontakt ze wsparciem
        self.frame7_help_label0 = ctk.CTkLabel(self.frame7, 
                           text='', 
                           fg_color=self.main_frame_color, text_color='white', justify='left', corner_radius=9, 
                           width=self.workspace_width-40, anchor='w')
        self.frame7_help_label0.grid(row=0, column=0, padx=20, pady=0)

        self.frame7_help_label1 = ctk.CTkLabel(self.frame7, 
                           text='\nKontakt ze wsparciem technicznym:\n', 
                           fg_color=self.main_inner_frame_color, text_color=self.help_header_text_color, justify='left', corner_radius=9, 
                           width=self.workspace_width-40, anchor='w')
        self.frame7_help_label1.grid(row=1, column=0, padx=20, pady=0)
        self.frame7_help_label1.cget("font").configure(size=14, weight="bold")

        self.frame7_help_label2 = ctk.CTkLabel(self.frame7, 
                           text='\nchx101919@student.chorzow.merito.pl\n', 
                           fg_color=self.main_inner_frame_color, text_color='white', justify='left', corner_radius=9, 
                           width=self.workspace_width-40, anchor='w')
        self.frame7_help_label2.grid(row=2, column=0, padx=20, pady=10)
        self.frame7_help_label2.cget("font").configure(size=14)

        ## Pliki wejściowe - txt
        self.frame7_help_label3 = ctk.CTkLabel(self.frame7, 
                           text='', 
                           fg_color=self.main_frame_color, text_color='white', justify='left', corner_radius=9, 
                           width=self.workspace_width-40, anchor='w')
        self.frame7_help_label3.grid(row=3, column=0, padx=20, pady=0)

        self.frame7_help_label4 = ctk.CTkLabel(self.frame7, 
                           text='\nZ jakiego rodzaju plików można ładować dane?\n',
                           fg_color=self.main_inner_frame_color, text_color=self.help_header_text_color, justify='left', corner_radius=9, 
                           width=self.workspace_width-40, anchor='w')
        self.frame7_help_label4.grid(row=4, column=0, padx=20, pady=0, sticky='news')
        self.frame7_help_label4.cget("font").configure(size=14, weight="bold")

        self.frame7_help_label5 = ctk.CTkLabel(self.frame7, 
                           text='\nDane wejściowe można ładować z plików tekstowch - pliki z roszerzeniem .txt.\n', 
                           fg_color=self.main_inner_frame_color, text_color='white', justify='left', corner_radius=9, 
                           width=self.workspace_width-40, anchor='w')
        self.frame7_help_label5.grid(row=5, column=0, padx=20, pady=10, sticky='news')
        self.frame7_help_label5.cget("font").configure(size=14)

        ## Pliki z wynikami
        self.frame7_help_label6 = ctk.CTkLabel(self.frame7, 
                           text='', 
                           fg_color=self.main_frame_color, text_color='white', justify='left', corner_radius=9, 
                           width=self.workspace_width-40, anchor='w')
        self.frame7_help_label6.grid(row=6, column=0, padx=20, pady=0)

        self.frame7_help_label7 = ctk.CTkLabel(self.frame7, 
                           text='\nZ jaką nazwą zapisywany jest plik z wynikami?\n',
                           fg_color=self.main_inner_frame_color, text_color=self.help_header_text_color, justify='left', corner_radius=9, 
                           width=self.workspace_width-40, anchor='w')
        self.frame7_help_label7.grid(row=7, column=0, padx=20, pady=0, sticky='news')
        self.frame7_help_label7.cget("font").configure(size=14, weight="bold")

        self.frame7_help_label8 = ctk.CTkLabel(self.frame7, 
                           text='\nNazwa pliku generowana jest automatycznie – jest to połączenie oznaczenia zakładki, z której pochodzą wyniki oraz\n' + 
                                'daty i czasu zapisu.\n' + 
                                '\n\nPrzykładowo: 2_complementary_20250104_230518.txt \n\n' +
                                '\n\nOznaczenia poszczególnych zakładek: \n' +
                                '\n   - Nić komplementarna - 2_complementary\n' + 
                                '\n   - Transkrypcja - 3_transcription\n' +
                                '\n   - Splicing - 4_splicing\n' +
                                '\n   - Translacja - 5_translation\n' +
                                '\n   - Analiza mutacji - 6_mutation_analysis\n' +
                                '\n\nW zakładce "Analiza mutacji" plik HTML z porównaniem sekwencji również ma nazwę generowaną automatycznie.\n' + 
                                'Jest to połączenie "6_mutation_comparison" oraz daty i czasu zapisu.\n' +
                                '\n\n Przykładowo: 6_mutation_comparison_20250104_230518.html\n', 
                           fg_color=self.main_inner_frame_color, text_color='white', justify='left', corner_radius=9, 
                           width=self.workspace_width-40, anchor='w')
        self.frame7_help_label8.grid(row=8, column=0, padx=20, pady=10, sticky='news')
        self.frame7_help_label8.cget("font").configure(size=14)

        ## Zakładki Nić komplementarna, Transkrypcja, Translacja - dane wejściowe
        self.frame7_help_label9 = ctk.CTkLabel(self.frame7, 
                           text='', 
                           fg_color=self.main_frame_color, text_color='white', justify='left', corner_radius=9, 
                           width=self.workspace_width-40, anchor='w')
        self.frame7_help_label9.grid(row=9, column=0, padx=20, pady=0)

        self.frame7_help_label10 = ctk.CTkLabel(self.frame7, 
                           text='\nZakładki Nić komplementarna, Transkrypcja, Translacja:\n' + '\nJaki format powinny mieć dane wejściowe?\n',
                           fg_color=self.main_inner_frame_color, text_color=self.help_header_text_color, justify='left', corner_radius=9, 
                           width=self.workspace_width-40, anchor='w')
        self.frame7_help_label10.grid(row=10, column=0, padx=20, pady=0, sticky='news')
        self.frame7_help_label10.cget("font").configure(size=14, weight="bold")

        self.frame7_help_label11 = ctk.CTkLabel(self.frame7, 
                           text='\nDane wejściowe powinny zawierać jedną sekwencję nici bez innych dodatkowych znaków – zarówno, jeśli' + 
                                '\nwprowadzane są ręcznie w GUI, jak i gdy są ładowane z pliku. \n' + 
                                '\n\nPrzykładowo: ATGGCTTGGTGGAGGAGGAGGGCTTGA \n', 
                           fg_color=self.main_inner_frame_color, text_color='white', justify='left', corner_radius=9, 
                           width=self.workspace_width-40, anchor='w')
        self.frame7_help_label11.grid(row=11, column=0, padx=20, pady=10, sticky='news')
        self.frame7_help_label11.cget("font").configure(size=14)

        ## Zakładka Splicing
        self.frame7_help_label12 = ctk.CTkLabel(self.frame7, 
                           text='', 
                           fg_color=self.main_frame_color, text_color='white', justify='left', corner_radius=9, 
                           width=self.workspace_width-40, anchor='w')
        self.frame7_help_label12.grid(row=12, column=0, padx=20, pady=0)

        self.frame7_help_label13 = ctk.CTkLabel(self.frame7, 
                           text='\nZakładka Splicing: Jaki format powinny mieć dane wejściowe?\n',
                           fg_color=self.main_inner_frame_color, text_color=self.help_header_text_color, justify='left', corner_radius=9, 
                           width=self.workspace_width-40, anchor='w')
        self.frame7_help_label13.grid(row=13, column=0, padx=20, pady=0, sticky='news')
        self.frame7_help_label13.cget("font").configure(size=14, weight="bold")

        self.frame7_help_label14 = ctk.CTkLabel(self.frame7, 
                           text='\nDane wprowadzane bezpośrednio w GUI powinny zawierać sekwencję jednej nici w pierwszym polu wejściowym oraz\n' + 
                                'miejsca występowania eksonów w drugim polu wejściowym. ' + 
                                '\n\nPrzykładowo dla pola pierwszego: ATGGCTTGGTGGAGGAGGAGGGCTTGA \n' + 
                                'Przykładowo dla pola drugiego:  1-21, 25-27\n' +
                                '\n\nW przypadku ładowania danych z pliku, sekwencja wejściowa i lista miejsc eksonów powinny być oddzielone od siebie\n' + 
                                'średnikiem.'+
                                '\n\nPrzykładowo: ATGGCTTGGTGGAGGAGGAGGGCTTGA; 1-21, 25-27\n', 
                           fg_color=self.main_inner_frame_color, text_color='white', justify='left', corner_radius=9, 
                           width=self.workspace_width-40, anchor='w')
        self.frame7_help_label14.grid(row=14, column=0, padx=20, pady=10, sticky='news')
        self.frame7_help_label14.cget("font").configure(size=14)

        ## Zakładka Analiza mutacji
        self.frame7_help_label15 = ctk.CTkLabel(self.frame7, 
                           text='', 
                           fg_color=self.main_frame_color, text_color='white', justify='left', corner_radius=9, 
                           width=self.workspace_width-40, anchor='w')
        self.frame7_help_label15.grid(row=15, column=0, padx=20, pady=0)

        self.frame7_help_label16 = ctk.CTkLabel(self.frame7, 
                           text='\nZakładka Analiza mutacji: Jaki format powinny mieć dane wejściowe?\n',
                           fg_color=self.main_inner_frame_color, text_color=self.help_header_text_color, justify='left', corner_radius=9, 
                           width=self.workspace_width-40, anchor='w')
        self.frame7_help_label16.grid(row=16, column=0, padx=20, pady=0, sticky='news')
        self.frame7_help_label16.cget("font").configure(size=14, weight="bold")

        self.frame7_help_label17 = ctk.CTkLabel(self.frame7, 
                           text='\nSekwencja wejściowa, lista miejsc eksonów oraz miejsca mutacji powinny być oddzielone od siebie średnikiem.'+
                                '\n\nPrzykładowo: ATGGCTTGGTGGAGGAGGAGGGCTTGA; 1-21, 25-27;G9A, G14C, G21T\n' +
                                '\n\nW przypadku jednoczesnego analizowania wielu zestawów danych, poszczególne zestawy danych powinny być\n' + 
                                'oddzielone od siebie znakiem nowej linii.' +
                                '\n\nPrzykładowo:\n ' +
                                '   ATGGCTTGGTGGAGGAGGAGGGCTTGA; 1-21, 25-27; G9A, G14C, G21T\n' +
                                '    ATGGCTTGGTGGAGGAGGAGGGCTTGA; 1-27; G4A, T6C\n', 
                           fg_color=self.main_inner_frame_color, text_color='white', justify='left', corner_radius=9, 
                           width=self.workspace_width-40, anchor='w')
        self.frame7_help_label17.grid(row=17, column=0, padx=20, pady=10, sticky='news')
        self.frame7_help_label17.cget("font").configure(size=14)

        # testowanie
        # self.frame1_analyze_button = ctk.CTkButton(self.frame1, text="Testuj!",
        #                                             fg_color=self.sidebar_color, hover_color=self.main_button_color, text_color='black',
        #                                             width=100, height=0.05*self.workspace_height, command=self.testing)
        # self.frame1_analyze_button.grid(row=4)

    def show_frame(self, frame, frame_number, button, prev_frame_no):
        '''
        Zmiana wyświetlanej ramki - wywoływana przez kliknięcie przycisku na panelu nawigacyjnym.
        '''
        # pokazanie tekstu nagłówka dla wybranej ramki
        self.header_label.configure(text=self.sidebar_button_text[frame_number-1].upper())

        # przywrócenie przycisków na pasku nawigacji do konfiguracji domyślnej
        self.default_button_config()

        # zmiana wyglądu przycisku dla wybranej ramki
        button.configure(fg_color=self.main_frame_color, state='disabled')

        # ukrycie pozostałych ramek
        self.hide_prev_frame(prev_frame_no)

        # pokazanie wybranej ramki
        frame.place(relx=0.0, rely=0.0)

        # aktualizacja numeru wyświetlanej ramki
        self.current_frame_no = frame_number

    def default_button_config(self):
        '''
        Przywrócenie konfiguracji wszystkich przycisków na panelu nawigacyjnym do ustawień domyślnych.
        '''
        self.sidebar_button_start.configure(fg_color=self.sidebar_button_color, hover_color=self.main_frame_color, state='normal')
        self.sidebar_button_compl.configure(fg_color=self.sidebar_button_color, hover_color=self.main_frame_color, state='normal')
        self.sidebar_button_transcript.configure(fg_color=self.sidebar_button_color, hover_color=self.main_frame_color, state='normal')
        self.sidebar_button_splicing.configure(fg_color=self.sidebar_button_color, hover_color=self.main_frame_color, state='normal')
        self.sidebar_button_translate.configure(fg_color=self.sidebar_button_color, hover_color=self.main_frame_color, state='normal')
        self.sidebar_button_analyze.configure(fg_color=self.sidebar_button_color, hover_color=self.main_frame_color, state='normal')
        self.sidebar_button_help.configure(fg_color=self.sidebar_button_color, hover_color=self.main_frame_color, state='normal')

    def hide_prev_frame(self, frame_number):
        '''
        Ukrywanie poprzednio wyświetlanej ramki.
        '''
        if frame_number==1:
            self.frame1.place_forget()
        elif frame_number==2:
            self.frame2.place_forget()
        elif frame_number==3:
            self.frame3.place_forget()
        elif frame_number==4:
            self.frame4.place_forget()
        elif frame_number==5:
            self.frame5.place_forget()
        elif frame_number==6:
            self.frame6.place_forget()
        elif frame_number==7:
            self.frame7.place_forget()

    def set_controller(self, controller):
        self.controller = controller

    def start_2_analyze(self):
        '''
        Uruchamiane przez przycisk 'Analizuj!' na zakładce 2. - Nić komplementarna
        Przeprowadzenie procesu szukania nici komplementarnej i nici odwrotniekomplementarnej
        '''
        self.output = None

        self.input_sequence = self.frame2_input_textbox.get("0.0", "end").strip()

        self.frame2_res_textbox.configure(state="normal") 
        self.frame2_res_textbox.delete("1.0",ctk.END)
        self.frame2_res_textbox.configure(state="disabled") 

        if self.input_sequence != '':
            self.controller.set_input_sequence(self.input_sequence)
            self.output = self.controller.run_complementary()
            if self.output[0] == None:
                messagebox.showerror('Błąd', 'Niepoprawny format sekwencji wejściowej!')
            else:
                self.output = "Nić komplementarna:\n" + str(self.output[0]) + "\n\nNić odwrotnie komplementarna:\n" + str(self.output[1])
                self.frame2_res_textbox.configure(state="normal") 
                self.frame2_res_textbox.insert("0.0",self.output)
                self.frame2_res_textbox.configure(state="disabled") 
        else:
            messagebox.showerror('Błąd', 'Brak danych wejściowych!')

    def start_3_analyze(self):
        '''
        Uruchamiane przez przycisk 'Analizuj!' na zakładce 3. - Transkrypcja
        Przeprowadzenie procesu transkrypcji
        '''
        self.output = None

        self.input_sequence = self.frame3_input_textbox.get("0.0", "end").strip()

        self.frame3_res_textbox.configure(state="normal") 
        self.frame3_res_textbox.delete("1.0",ctk.END)
        self.frame3_res_textbox.configure(state="disabled") 

        if self.input_sequence != '':
            self.controller.set_input_sequence(self.input_sequence)
            self.output = self.controller.run_transcribe_seq()
            if self.output == None:
                messagebox.showerror('Błąd', 'Niepoprawny format sekwencji wejściowej!')
            else:
                self.frame3_res_textbox.configure(state="normal")
                self.frame3_res_textbox.insert("0.0",self.output)
                self.frame3_res_textbox.configure(state="disabled")
        else:
            messagebox.showerror('Błąd', 'Brak danych wejściowych!')
    
    def start_4_analyze(self):
        '''
        Uruchamiane przez przycisk 'Analizuj!' na zakładce 4. - Splicing
        Przeprowadzenie procesu splicingu
        '''
        self.output = None

        self.input_sequence = self.frame4_input_seq_textbox.get("0.0", "end").strip()

        exons = self.frame4_input_ex_textbox.get("0.0", "end").strip()

        self.frame4_res_textbox.configure(state="normal") 
        self.frame4_res_textbox.delete("1.0",ctk.END)
        self.frame4_res_textbox.configure(state="disabled") 

        if self.input_sequence != '' and exons != None and exons != '':
            self.controller.set_input_sequence(self.input_sequence)
            self.exons = self.frame4_input_ex_textbox.get("0.0", "end").strip()
            self.controller.set_exons(self.exons)
            self.output = self.controller.run_splicing()
            if self.output == None:
                messagebox.showerror('Błąd', 'Niepoprawny format danych wejściowych!')
            else:
                self.frame4_res_textbox.configure(state="normal")
                self.frame4_res_textbox.insert("0.0",self.output)
                self.frame4_res_textbox.configure(state="disabled")
        else:
            messagebox.showerror('Błąd', 'Brak danych wejściowych!')
    
    def select_range(self, selected_range):
        '''
        Aktualizacja zmiennej zawierającej wybór zakresu dla procesu translacji
        '''
        self.controller.set_translate_range(selected_range)

    def start_5_analyze(self):
        '''
        Uruchamiane przez przycisk 'Analizuj!' na zakładce 5. - Translacja
        Przeprowadzenie procesu translacji
        '''
        self.output = None

        self.input_sequence = self.frame5_input_textbox.get("0.0", "end").strip()

        self.frame5_res_textbox.configure(state="normal") 
        self.frame5_res_textbox.delete("1.0",ctk.END)
        self.frame5_res_textbox.configure(state="disabled") 

        if self.input_sequence != '':
            self.controller.set_input_sequence(self.input_sequence)
            self.output = self.controller.run_translate_seq(5)
            
            if self.output == None:
                messagebox.showerror('Błąd', 'Niepoprawny format sekwencji wejściowej!')
            else:
                self.frame5_res_textbox.configure(state="normal")
                self.frame5_res_textbox.insert("0.0",self.output)
                self.frame5_res_textbox.configure(state="disabled")
        else:
            messagebox.showerror('Błąd', 'Brak danych wejściowych!')

    def start_6_analyze(self):
        '''
        Uruchamiane przez przycisk 'Analizuj!' na zakładce 6. - Analiza mutacji
        Przeprowadzenie procesu analizy mutacji
        '''
        self.output = None
        self.html_output = None

        input = self.frame6_input_textbox.get("0.0", "end").strip()

        self.frame6_res_textbox.configure(state="normal") 
        self.frame6_res_textbox.delete("1.0",ctk.END)
        self.frame6_res_textbox.configure(state="disabled") 

        if input != '':
            input = self.controller.run_separate_input(input)
            
            is_enough_data = 1

            for i in input:
                if len(i) != 3:
                    is_enough_data = 0

            if is_enough_data == 1:

                self.output = ''
                self.html_output = ''
                self.html_output = "<html><body> <h3><tt>"
                self.html_output += "Legenda:<br><ul>"
                self.html_output += "&#129001;&nbsp;Mutacja synonimiczna<br>"
                self.html_output += "&#128997;&nbsp;Mutacja zmiany sensu<br>"
                self.html_output += "&#128998;&nbsp;Mutacja nonsensowna<br>"
                self.html_output += '</ul><br><hr style="height:2px">'

                for i in range(0,len(input)):
                    self.input_sequence = input[i][0]
                    self.exons = input[i][1]
                    self.mutations = input[i][2]
                    self.controller.set_input_sequence(self.input_sequence)
                    self.controller.set_exons(self.exons)
                    self.controller.set_mutations(self.mutations)
                    res = self.controller.run_analyze_mutations()
                    if res == None:
                        messagebox.showerror('Błąd', 'Niepoprawny format danych wejściowych!')
                        return -1
                    else:
                        cds = res[0]
                        mutated_cds = res[1] 
                        cds_mutation_list = res[2] 
                        protein_coding= res[3] 
                        protein_mutated_coding = res[4] 
                        protein_mutation_list = res[5]
                        cds_mutation_print = [f'{i[0]}{i[1]}{i[2]}' for i in cds_mutation_list]
                        protein_mutated_print = [f'{i[0]}{i[1]}{i[2]}' for i in protein_mutation_list]
                        self.output += '\n'.join(
                            ['Sekwencja kodująca: ', str(cds), '\n',
                            'Sekwencja kodująca po mutacji: ', str(mutated_cds),  '\n',
                            'Miejsca mutacji w sekwencji kodującej: ', str(', '.join(cds_mutation_print)), '\n\n',
                            'Sekwencja białka: ', str(protein_coding),  '\n',
                            'Sekwencja białka po mutacji: ', str(protein_mutated_coding),  '\n',
                            'Miejsca mutacji w białku:', str(', '.join(protein_mutated_print)), '\n\n'])
                        self.html_output += f'Wyniki dla sekwencji nr {i+1}.<br><hr style="height:1px">'
                        self.html_output += "Sekwencja nukleotydów<br><br>"
                        self.html_output += self.controller.run_visualize_sequence_differences(str(cds),str(mutated_cds),cds_mutation_list)
                        self.html_output += '<br><hr style="height:1px">'
                        self.html_output += "Sekwencja aminokwasów<br><br>"
                        self.html_output += self.controller.run_visualize_sequence_differences(str(protein_coding),str(protein_mutated_coding),protein_mutation_list)
                        
                        if i<(len(input)-1):
                            self.output += '\n--------------------------------------------------------------------------------------------------------\n\n'
                            self.html_output += '<hr style="height:2px">'

                self.html_output += "</h3></body></html>"

                if self.output == None:
                    messagebox.showerror('Błąd', 'Niepoprawny format danych wejściowych!')
                else:
                    self.frame6_res_textbox.configure(state="normal")
                    self.frame6_res_textbox.insert("0.0",self.output)
                    self.frame6_res_textbox.configure(state="disabled")
            else:
                messagebox.showerror('Błąd', 'Niepoprawny format danych wejściowych!')
        else:
            messagebox.showerror('Błąd', 'Brak danych wejściowych!')


    def copy_output(self, frame_no):
        '''
        Uruchamiane przez przycisk 'Kopiuj'
        Kopiowanie wyników do schowka
        '''
        if frame_no == 2:
            text = self.frame2_res_textbox.get("0.0", "end").strip()
        elif frame_no == 3:
            text = self.frame3_res_textbox.get("0.0", "end").strip()
        elif frame_no == 4:
            text = self.frame4_res_textbox.get("0.0", "end").strip()
        elif frame_no == 5:
            text = self.frame5_res_textbox.get("0.0", "end").strip()
        elif frame_no == 6:
            text = self.frame6_res_textbox.get("0.0", "end").strip()

        if text == '':
            messagebox.showerror('Błąd', 'Pole z wynikami jest puste!')
        else:
            text = str(text)
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardText(text)
            win32clipboard.CloseClipboard()

    def load_from_file(self, frame_no):
        '''
        Uruchamiane przez przycisk 'Załaduj z pliku' 
        Ładowanie danych wejściowych z wybranego pliku tekstowego
        '''
        filename = filedialog.askopenfilename(
            title = 'Wybierz plik tekstowy',
            filetypes=[('Pliki tekstowe','.txt')]
        )

        if filename == '':
            messagebox.showerror('Błąd', f'Nie wybrano poprawnego pliku!')
            return -1

        content=''
        try:
            with open(filename, "r") as file:
                content = file.read()
        except Exception as e:
            messagebox.showerror('Błąd', f'Wystąpił problem z odczytem danych: {e}')
            return -1

        if filename != '' and content != '':
            if frame_no == 2:
                self.frame2_input_textbox.delete("0.0", "end") 
                self.frame2_input_textbox.insert("0.0",content)
            elif frame_no == 3:
                self.frame3_input_textbox.delete("0.0", "end") 
                self.frame3_input_textbox.insert("0.0",content)
            elif frame_no == 4:
                content = self.controller.run_input_multiple_semicol(content)
                self.frame4_input_seq_textbox.delete("0.0", "end")
                self.frame4_input_seq_textbox.insert("0.0",content[0])
                self.frame4_input_ex_textbox.delete("0.0", "end")
                self.frame4_input_ex_textbox.insert("0.0",content[1])
            elif frame_no == 5:
                self.frame5_input_textbox.delete("0.0", "end") 
                self.frame5_input_textbox.insert("0.0",content)
            elif frame_no == 6:
                self.frame6_input_textbox.delete("0.0", "end") 
                self.frame6_input_textbox.insert("0.0",content)
            return 0
        else:
            messagebox.showerror('Błąd', f'Wystąpił problem z odczytem danych!')
            return -1

    def load_to_file(self, frame_no):
        '''
        Uruchamiane przez przycisk 'Zapisz do pliku' 
        Zapisywanie danych wyjściowych do wybranego pliku tekstowego
        '''
        file_path = ''
        content = ''
        if frame_no == 2: 
            file_path = f'/2_complementary_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
            content = self.frame2_res_textbox.get("0.0", "end").strip()
        elif frame_no == 3: 
            file_path = f'/3_transcription_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
            content = self.frame3_res_textbox.get("0.0", "end").strip()
        elif frame_no == 4: 
            file_path = f'/4_splicing_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
            content = self.frame4_res_textbox.get("0.0", "end").strip()
        elif frame_no == 5:  
            file_path = f'/5_translation_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
            content = self.frame5_res_textbox.get("0.0", "end").strip()
        elif frame_no == 6:   
            file_path = f'/6_mutation_analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
            content = self.frame6_res_textbox.get("0.0", "end").strip()

        if content != '':
            dest_file_dir = filedialog.askdirectory(
            initialdir=os.getcwd(), 
            title='Zapisz dane do pliku')

            full_path = f'{dest_file_dir}{file_path}'

            if dest_file_dir!='':
                try:
                    with open(full_path, "w") as file:
                        file.write(content)
                except Exception as e:
                    messagebox.showerror('Błąd', f'Wystąpił problem z zapisem danych: {e}')
        else:
            messagebox.showerror('Błąd', f'Pole z wynikami jest puste!')

    def save_comparison_to_file(self):
        '''
        Uruchamiane przez przycisk 'Generuj plik z porównaniem' 
        Zapisywanie wygenerowanego porównania danych wyjściowych do pliku HTML
        '''
        
        if self.html_output == None:
            self.html_output = ''

        if self.html_output != '' and self.html_output[-7:]=="</html>":
            dest_file_dir = filedialog.askdirectory(
            initialdir=os.getcwd(), 
            title='Zapisz dane do pliku')

            file_path = f'/6_mutation_comparison_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html'
            full_path = f'{dest_file_dir}{file_path}'

            if dest_file_dir!='':
                try:
                    with open(full_path, "w") as file:
                        file.write(self.html_output)
                except Exception as e:
                    messagebox.showerror('Błąd', f'Wystąpił problem z zapisem danych: {e}')
        else:
            messagebox.showerror('Błąd', f'Pole z wynikami jest puste!') 

    def testing(self):
        '''
        Uruchamiane przez przycisk 'Testuj!' na zakładce Start (jeśli jest włączone testowanie) 
        Testowanie działania aplikacji (zwracanych wyników)
        '''
        testing_input_filepath = 'other\\testing_input.txt'
        testing_expected_output_filepath = 'other\\testing_expected_output.txt'
        testing_output_filepath = 'other\\testing_output.txt'

        with open(testing_input_filepath, 'r') as file: # wczytaj zawartość pliku z danymi wejściowymi
            content_input_file = file.read()

        with open(testing_expected_output_filepath, 'r') as file: # wczytaj zawartość pliku z oczekiwanymi wynikami
            content_expected_output_file = file.read()

        with open(testing_output_filepath, 'w') as file: # wyczyść plik wyjściowy
            pass 

        # podział danych na poszczególne zestawy
        input_separated = self.controller.run_separate_input(content_input_file)
        expected_output_separated = self.controller.run_separate_input(content_expected_output_file)

        for i in range(0,len(input_separated)):
            # Nić komplementarna
            print(f"Test {i+1}")
            self.input_sequence = input_separated[i][0]
            self.controller.set_input_sequence(self.input_sequence)
            self.output = self.controller.run_complementary()
            compl_out = self.output[0]
            rev_compl_out = self.output[1]
            if compl_out == expected_output_separated[i][0] and rev_compl_out == expected_output_separated[i][1]:
                res = "Zaliczony"
            else:
                res = "Niezaliczony"
            print(f"{res} - Nić komplementarna i odwortnie komplementarna" )

            with open(testing_output_filepath, 'a') as file:
                file.write(f"{compl_out}; {rev_compl_out};")

            # Transkrypcja
            self.input_sequence = input_separated[i][0]
            self.controller.set_input_sequence(self.input_sequence)
            self.output = self.controller.run_transcribe_seq()
            if self.output == expected_output_separated[i][2]:
                res = "Zaliczony"
            else:
                res = "Niezaliczony"
            print(f"{res} - Transkrypcja" )

            with open(testing_output_filepath, 'a') as file:
                file.write(f"{self.output}; ")

            # Splicing
            self.input_sequence = input_separated[i][0]
            self.controller.set_input_sequence(self.input_sequence)
            self.exons = input_separated[i][1]
            self.controller.set_exons(self.exons)
            self.output = self.controller.run_splicing()
            if self.output == expected_output_separated[i][3]:
                res = "Zaliczony"
            else:
                res = "Niezaliczony"
            print(f"{res} - Splicing" )

            with open(testing_output_filepath, 'a') as file:
                file.write(f"{self.output}; ")

            # Translacja
            self.input_sequence = expected_output_separated[i][3]
            self.controller.set_input_sequence(self.input_sequence)
            self.output = self.controller.run_translate_seq(5)
            if self.output == expected_output_separated[i][4]:
                res = "Zaliczony"
            else:
                res = "Niezaliczony"
                print(self.output)
                print(expected_output_separated[i][4])
            print(f"{res} - Translacja" )

            with open(testing_output_filepath, 'a') as file:
                file.write(f"{self.output}; ")

            # Analiza mutacji
            self.input_sequence = input_separated[i][0]
            self.exons = input_separated[i][1]
            self.mutations = input_separated[i][2]
            self.controller.set_input_sequence(self.input_sequence)
            self.controller.set_exons(self.exons)
            self.controller.set_mutations(self.mutations)

            result = self.controller.run_analyze_mutations()

            cds = result[0]
            cds_mutation_list = result[2] 
            protein_coding= result[3] 
            protein_mutation_list = result[5]
            cds_mutation_print = [f'{i[0]}{i[1]}{i[2]}' for i in cds_mutation_list]
            protein_mutated_print = [f'{i[0]}{i[1]}{i[2]}' for i in protein_mutation_list]
            cds_mutation_print = str(', '.join(cds_mutation_print))
            protein_mutated_print = str(', ').join(protein_mutated_print)

            if cds == expected_output_separated[i][3]:
                res = "Zaliczony"
            else:
                res = "Niezaliczony"
            print(f"{res} - Analiza mutacji - Sekwencja kodująca")

            if cds_mutation_print == expected_output_separated[i][5]:
                res = "Zaliczony"
            else:
                res = "Niezaliczony"
                print(cds_mutation_print)
                print(expected_output_separated[i][5])
            print(f"{res} - Analiza mutacji - Mutacje w CDS")

            if protein_coding == expected_output_separated[i][4]:
                res = "Zaliczony"
            else:
                res = "Niezaliczony"
            print(f"{res} - Analiza mutacji - Sekwencja aminokwasów")

            if protein_mutated_print == expected_output_separated[i][6]:
                res = "Zaliczony"
            else:
                res = "Niezaliczony"
                print(protein_mutated_print)
                print(expected_output_separated[i][6])
            print(f"{res} - Analiza mutacji - Mutacje w białku")


            with open(testing_output_filepath, 'a') as file:
                file.write(f"{cds_mutation_print}; {protein_mutated_print}\n")


