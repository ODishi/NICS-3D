########################################################################################################################
## V1.0.1
##
## Changelog:
## - Made compatible with both Python2 and Python3

import sys

if sys.version_info[0] == 3: py3 = True
else: py3 = False

if py3:
    import tkinter as Tkinter
    import tkinter.constants as Tkconstants
    import tkinter.filedialog as tkFileDialog
    import tkinter.messagebox as tkMessageBox
    import tkinter.ttk as ttk
    import os, math, extract
    from tkinter import *
else:
    import Tkinter, Tkconstants, tkFileDialog, tkMessageBox, ttk, os, math, extract
    from Tkinter import *

class gui: #create gui

    def readUserSettings(self): # read pathway for last opened folder from appdata
        settingsFile=open(self.tracker)
        line=settingsFile.readline()
        while line:
            split = line.find('=')
            self.userSetting[line[:split]] = line[split+1:-1]
            line=settingsFile.readline()
        settingsFile.close

    def updateUserSettings(self): # creates/updates last file pathway traker
        settingsFile=open(self.tracker,'w')
        fileData=[]
        for key in list(self.userSetting.keys()):
            fileData.append(str(key) + '=' + str(self.userSetting[key]) + '\n')
        settingsFile.writelines(fileData)
        settingsFile.close

    def updateSettingsTab(self):
        for key in list(self.userSetting.keys()):
            if (self.userSetting[key] == 'True') or (self.userSetting[key] == 'False'):
                self.settingVars['Checkbox ' + key].set(eval(self.userSetting[key]))
                try: self.top.change_entry_state(self.top.child_objects['Entry ' + key], self.settingVars['Checkbox ' + key])
                except KeyError: pass
            elif 'combobox' in key:
                try:
                    self.top.child_objects['Combobox ' + key.split('_')[0]].current(self.top.child_objects['Combobox ' + key.split('_')[0]]['values'].index(self.userSetting[key]))
                except ValueError: continue
            else:
                try:
                    self.top.child_objects['Entry ' + key.split('_')[0]].insert(0,self.userSetting[key])
                except: continue

    def askopen(self): # dialog for opening files
        filenames = tkFileDialog.askopenfilename(initialdir = self.userSetting['lastDir'], defaultextension=['.txt'], filetypes=[('log files', '.log'),('com files', '.com'),('all files', '.*')], multiple = 1)
        tempdir = filenames
        try:
            self.userSetting['lastDir'] = '/'.join(list(tempdir)[0].split('/')[:-1])+'/'
        except:
            pass
        for filename in filenames:
            flnm=filename.split('/')[-1][:-4]
            if flnm not in self.top.Files: # if file hasn't been loaded yet
                self.top.child_objects['ListboxFiles'].insert(END,flnm) # adds filename to listbox
                self.top.Files[flnm] = filename # saves the filename and full filename

    def remove_files(self):
        to_remove = self.top.child_objects['ListboxFiles'].curselection()
        for file_index in range(len(to_remove)-1,-1,-1):
            del self.top.Files[self.top.child_objects['ListboxFiles'].get(to_remove[file_index])]
            self.top.child_objects['ListboxFiles'].delete(to_remove[file_index])

    def do_delete(self, event):
        self.general_warning(self.remove_files, 'Are you sure you with to delete these files?')
        return 'deleted'

    def invert_selection(self):
        selected = self.top.child_objects['ListboxFiles'].curselection()
        size = self.top.child_objects['ListboxFiles'].size()
        for line in range(size):
            if line in selected:
                self.top.child_objects['ListboxFiles'].selection_clear(line)
            else:
                self.top.child_objects['ListboxFiles'].selection_set(line)

    def launch_extraction(self):
        uniques = dict()
        for key in list(self.top.Files.keys()):
            f_name = self.top.Files[key]
            file_name = f_name.split('/')[-1]
            if 'Part' not in key:
                file_short_name = file_name.split('.')[0]
            else:
                file_short_name = file_name.split('Part')[0]
            if file_short_name not in list(uniques.keys()):
                uniques[file_short_name] = []
            uniques[file_short_name] += [f_name]
        mode = self.top.child_objects['Combobox extract'].get()
        for key in list(uniques.keys()):
            extract.process(key, uniques[key], mode, self.settingVars['Checkbox print'].get())

    def closeAll(self): # method to ensure that everything dies with the root
        self.saveSettings()
        self.updateUserSettings()
        self.top.window.destroy()

    def saveSettings(self):
        self.userSetting['bf'] = str(self.settingVars['Checkbox bf'].get())
        if not self.settingVars['Checkbox bf'].get(): self.userSetting['bf_value'] = self.top.child_objects['Entry bf'].get()
        self.userSetting['chk_combobox'] = self.top.child_objects['Combobox chk'].get()
        self.userSetting['chk_entry'] = self.top.child_objects['Entry chk'].get()
        self.userSetting['mem_combobox'] = self.top.child_objects['Combobox mem'].get()
        self.userSetting['mem_entry'] = self.top.child_objects['Entry mem'].get()
        self.userSetting['nprocs_combobox'] = self.top.child_objects['Combobox nprocs'].get()
        self.userSetting['nprocs_entry'] = self.top.child_objects['Entry nprocs'].get()
        self.userSetting['c'] = str(self.settingVars['Checkbox c'].get())
        if not self.settingVars['Checkbox c'].get(): self.userSetting['c_value'] = self.top.child_objects['Entry c'].get()
        self.userSetting['multi'] = str(self.settingVars['Checkbox multi'].get())
        if not self.settingVars['Checkbox multi'].get(): self.userSetting['multi_value'] = self.top.child_objects['Entry multi'].get()
        self.userSetting['interval_value'] = self.top.child_objects['Entry interval'].get()
        self.userSetting['margin_value'] = self.top.child_objects['Entry margin'].get()
        self.userSetting['addInp_value'] = self.top.child_objects['Entry addInp'].get()
        self.userSetting['nmr_value'] = self.top.child_objects['Entry nmr'].get()
        self.userSetting['extract_combobox'] = self.top.child_objects['Combobox extract'].get()
        self.userSetting['print'] = str(self.settingVars['Checkbox print'].get())
        

    def general_warning(self, func, text): # a warning function to prevent unintended actions
        if self.settingVars['enable_warnings'].get():
            if tkMessageBox.askokcancel('Warning', text):
                func()
            else:
                pass
        else:
            func()

    def print_var(self, var):
        print(var.get())

    def configRunSettings(self):
        if self.settingVars['Checkbox bf'].get():
            self.runSettings['bf'] = None
        else:
            self.runSettings['bf'] = self.top.child_objects['Entry bf'].get()
        if self.settingVars['Combobox chk'].get() == 'None':
            self.runSettings['chk'] = self.runSettings['path'] = None
        elif self.settingVars['Combobox chk'].get() == 'Custom':
            self.runSettings['chk'] = 'Custom'
            self.runSettings['path'] = self.top.child_objects['Entry chk'].get()
        else:
            self.runSettings['chk'] = 'Use Parent'
            self.runSettings['path'] = None
        if self.top.child_objects['Combobox mem'].get() == 'None':
            self.runSettings['mem'] = None
        elif self.top.child_objects['Combobox mem'].get() == 'Parent':
            self.runSettings['mem'] = 'Parent'
        else:
            self.runSettings['mem'] = self.top.child_objects['Entry mem'].get()
        if self.top.child_objects['Combobox nprocs'].get() == 'None':
            self.runSettings['nprocs'] = None
        elif self.top.child_objects['Combobox nprocs'].get() == 'Parent':
            self.runSettings['nprocs'] = 'Parent'
        else:
            self.runSettings['nprocs'] = self.top.child_objects['Entry nprocs'].get()
        if self.settingVars['Checkbox c'].get():
            self.runSettings['c'] = None
        else:
            self.runSettings['c'] = self.top.child_objects['Entry c'].get()
        if self.settingVars['Checkbox multi'].get():
            self.runSettings['multi'] = None
        else:
            self.runSettings['multi'] = self.top.child_objects['Entry multi'].get()
        if (self.top.child_objects['Entry interval'].get() is not None) and (self.top.child_objects['Entry interval'].get() != ''):
            self.runSettings['interval'] = float(self.top.child_objects['Entry interval'].get())
        else:
            self.runSettings['interval'] = 0.5
        if (self.top.child_objects['Entry margin'].get() is not None) and (self.top.child_objects['Entry margin'].get() != ''):
            self.runSettings['margin'] = float(self.top.child_objects['Entry margin'].get())
        else:
            self.runSettings['margin'] = 2.0
        if (self.top.child_objects['Entry nmr'].get() is not None) and (self.top.child_objects['Entry nmr'].get() != ''):
            self.runSettings['nmr'] = self.top.child_objects['Entry nmr'].get()
        else:
            self.runSettings['nmr'] = 'giao'
        if self.top.child_objects['Entry addInp'].get() is not None:
            self.runSettings['addInp'] = self.top.child_objects['Entry addInp'].get()
        else:
            self.runSettings['addInp'] = ''
        if self.top.child_objects['Entry suffix'].get() is not None:
            self.runSettings['suffix'] = self.top.child_objects['Entry suffix'].get()
        else:
            self.runSettings['suffix'] = ''

    def launch(self):
        self.configRunSettings()
        self.runSettings['Files'] = []
        for key in list(self.top.Files.keys()):
            f1 = g16File(self.top.Files[key])
            f1.xyzReorient()
            os.remove(f1.xyzName)
            f2 = outputFile(f1, margin = self.runSettings['margin'], interval = self.runSettings['interval'])
            f2.create(
                suffix = self.runSettings['suffix'],
                path = self.runSettings['path'],
                pathMode = self.runSettings['chk'],
                nProc = self.runSettings['nprocs'],
                memory = self.runSettings['mem'],
                base_func = self.runSettings['bf'],
                c = self.runSettings['c'],
                m = self.runSettings['multi'],
                method = self.runSettings['nmr'],
                addInp = self.runSettings['addInp'],
                fileTracker = self.runSettings['Files']
            )
        self.top.child_objects['ListboxFiles'].delete(0,END)


    def init_top(self): # creates main window
        self.top = self.windows('NICS-3D')
        self.top.window.protocol("WM_DELETE_WINDOW",self.closeAll)
        self.top.child_objects['Notebook'] = self.top.notebook
        self.top.child_objects['Main Tab'] = self.top.child_objects['Notebook'].add_tab('Files')
        self.top.child_objects['Settings Tab'] = self.top.child_objects['Notebook'].add_tab('Create')
        self.top.child_objects['Settings Tab'].columnconfigure(1, weight=1)
        self.top.child_objects['Extract Tab'] = self.top.child_objects['Notebook'].add_tab('Extract')
        self.top.child_objects['Extract Tab'].columnconfigure(1, weight=1)
        self.top.child_objects['Extract Tab'].grid_columnconfigure(0, weight=1)
        self.top.add_listbox('Files', self.top.child_objects['Main Tab'], 'bottom', 'both', True, width = 400)
        self.top.window.bind('<Delete>', self.do_delete)
        setattr(self.top,'Files',{})
        self.settingVars['enable_warnings'] = Tkinter.BooleanVar()
        self.settingVars['enable_warnings'].set(True)
        self.top.child_objects['Button Frame'] = self.top.add_label_frame(
            '',
            self.top.child_objects['Main Tab'],
            'top',
            'both',
            True)
        self.top.add_button(
            'Remove Selected Files',
            lambda: self.general_warning(self.remove_files, 'Are you sure you with to delete these files?'),
            self.top.child_objects['Button Frame'],
            fill = 'both',
            expand = True
            )
        self.top.add_button(
            'Invert Selection',
            self.invert_selection,
            self.top.child_objects['Button Frame'],
            fill = 'both',
            expand = True
            )
        self.top.child_objects['Launch Button'] = self.top.add_button(
            'Launch',
            self.launch,
            self.top.child_objects['Settings Tab'],
            row = 12,
            column = 1
            )
        self.top.child_objects['Launch Button'].grid(columnspan = 2, ipadx =  self.top.width)
        self.add_L_E_CB1_trio(
            self.top,
            self.top.child_objects['Settings Tab'],
            'bf',
            'Basis/Functional:',
            True,
            'Use Parent',
            row = 3
            )
        self.add_L_E_CB2_trio(
            self.top,
            self.top.child_objects['Settings Tab'],
            'chk',
            'Checkpoint file:',
            True,
            ['Use Parent', 'None', 'Custom'],
            'Custom',
            row = 0
            )
        self.add_L_E_CB2_trio(
            self.top,
            self.top.child_objects['Settings Tab'],
            'mem',
            'Memory Limit (GB):',
            True,
            ['Use Parent', 'None', 'Custom'],
            'Custom',
            row = 1
            )
        self.add_L_E_CB2_trio(
            self.top,
            self.top.child_objects['Settings Tab'],
            'nprocs',
            'Shared Processors:',
            True,
            ['Use Parent', 'None', 'Custom'],
            'Custom',
            row = 2
            )
        self.add_L_E_CB1_trio(
            self.top,
            self.top.child_objects['Settings Tab'],
            'c',
            'Charge:',
            True,
            'Use Parent',
            row = 4
            )
        self.add_L_E_CB1_trio(
            self.top,
            self.top.child_objects['Settings Tab'],
            'multi',
            'Multiplcity:',
            True,
            'Use Parent',
            row = 5
            )
        self.add_L_E_CB1_trio(
            self.top,
            self.top.child_objects['Settings Tab'],
            'interval',
            'Grid Interval:',
            False,
            row = 6
            )
        self.add_L_E_CB1_trio(
            self.top,
            self.top.child_objects['Settings Tab'],
            'margin',
            'Grid Margin:',
            False,
            row = 7
            )
        self.add_L_E_CB1_trio(
            self.top,
            self.top.child_objects['Settings Tab'],
            'addInp',
            'Additional Input:',
            False,
            row = 9
            )
        self.add_L_E_CB1_trio(
            self.top,
            self.top.child_objects['Settings Tab'],
            'nmr',
            'NMR Method: (nmr=)',
            False,
            row = 8
            )
        self.add_L_E_CB1_trio(
            self.top,
            self.top.child_objects['Settings Tab'],
            'suffix',
            'Suffix:',
            False,
            row = 10
        )
        self.top.child_objects['Mode Frame'] = self.top.add_label_frame(
            label = 'Mode',
            location = self.top.child_objects['Settings Tab'],
            column = 1,
            row = 11
        )
        self.top.child_objects['Mode Frame'].grid(
            columnspan = 2,
            ipadx =  self.top.width
        )
        self.top.child_objects['Combobox extract'] = self.top.add_combobox(
            ['Isotropic', 'Anisotropy', 'XX', 'YX', 'ZX', 'XY', 'YY', 'ZY', 'XZ', 'YZ', 'ZZ'],
            self.top.child_objects['Extract Tab'],
            row = 0,
            column = 0
        )
        if ('Checkbox print') not in list(self.settingVars.keys()):
            self.settingVars['Checkbox print'] = Tkinter.BooleanVar()
            self.settingVars['Checkbox print'].set(False)
        self.top.child_objects['Checkbox print'] = self.top.add_checkbox(
            'Create Images',
            self.settingVars['Checkbox print'],
            self.top.child_objects['Extract Tab'],
            row = 1,
            column = 1
        )
        self.top.add_button(
            'Launch Extraction',
            self.launch_extraction,
            self.top.child_objects['Extract Tab'],
            row = 0,
            column = 2
            )
        self.top.child_objects['Menu'] = self.top.menu
        self.top.child_objects['Menu'].add_menu(
            self.top.child_objects['Menu'].menubar,
            'File',
            menu_items = [
                ('Open', self.askopen, False, 'command'),
                ('Exit', self.closeAll, False, 'command')
                ]
            )
        self.top.child_objects['Menu'].add_menu(
            self.top.child_objects['Menu'].menubar,
            'Settings',
            menu_items = [
                ('Warnings Enabled',
                 [self.settingVars['enable_warnings'], True],
                 False,
                 'checkbutton')
                ]
            )
        self.top.window.deiconify()

    def add_L_E_CB1_trio(self, parent, location, id_tag = '', l_text = '', add_CB = True, cb_text = '', row = 0):
        parent.add_label(
            l_text,
            location,
            column = 0,
            row = row,
            sticky='w'
            )
        parent.child_objects['Entry ' + id_tag] = parent.add_entry(
            location,
            column = 1,
            row = row,
            sticky='new'
            )
        if add_CB:
            if ('Checkbox ' + id_tag) not in list(self.settingVars.keys()):
                self.settingVars['Checkbox ' + id_tag] = Tkinter.BooleanVar()
                self.settingVars['Checkbox ' + id_tag].set(True)
            parent.child_objects['Checkbox ' + id_tag] = parent.add_checkbox(
                cb_text,
                self.settingVars['Checkbox ' + id_tag],
                location,
                cmnd = lambda: parent.change_entry_state(parent.child_objects['Entry ' + id_tag], self.settingVars['Checkbox ' + id_tag]),
                column = 3,
                row = row
                )
            parent.change_entry_state(parent.child_objects['Entry ' + id_tag], self.settingVars['Checkbox ' + id_tag])

    def add_L_E_CB2_trio(self, parent, location, id_tag = '', l_text = '', add_CB = True, cb_values = [], enable_value = None, row = 0):
        parent.add_label(
            l_text,
            location,
            column = 0,
            row = row,
            sticky='w'
            )
        parent.child_objects['Entry ' + id_tag] = parent.add_entry(
            location,
            column = 1,
            row = row,
            sticky='new'
            )
        if add_CB:
            parent.child_objects['Combobox ' + id_tag] = parent.add_combobox(
                cb_values,
                location,
                column = 3,
                row = row
                )
            if enable_value is not None:
                if ('Combobox ' + id_tag) not in list(self.settingVars.keys()):
                    self.settingVars['Combobox ' + id_tag] = Tkinter.BooleanVar()

                def update_status():
                    if parent.child_objects['Combobox ' + id_tag].get() == enable_value:
                        self.settingVars['Combobox ' + id_tag].set(False)
                    else:
                        self.settingVars['Combobox ' + id_tag].set(True)

                update_status()
                parent.change_entry_state(parent.child_objects['Entry ' + id_tag], self.settingVars['Combobox ' + id_tag])
                
                def bind_E_CB(event):
                    update_status()
                    parent.change_entry_state(parent.child_objects['Entry ' + id_tag], self.settingVars['Combobox ' + id_tag])
                    
                parent.child_objects['Combobox ' + id_tag].bind('<<ComboboxSelected>>', bind_E_CB)

    def __init__(self):
        import platform
        if py3: self.location = os.path.dirname(os.path.realpath(__name__))
        else: self.location = os.path.dirname(os.path.realpath(__file__))
        if platform.system() == 'Linux':
            self.tracker = self.location + '/Settings' #tracker file location for last opened directory
        elif platform.system() == 'Windows':
            self.tracker = self.location + '\\Settings.txt'
        self.userSetting = {}
        self.settingVars = {}
        self.runSettings = {}
        self.init_top() # sets up main window
        try:
            self.readUserSettings() # checks if tracker exists
        except IOError:
            self.userSetting['lastDir'] = '.'
            self.updateUserSettings() # if tracker doesn't exist, creates it
        self.updateSettingsTab()
        self.top.window.mainloop()

    class windows: #creation of windows

        def centerScreen(self, w, h, scw, sch, w_shift, h_shift): # get syntax for positioning in center of the screen
            return str(w)+'x'+str(h)+'+'+str(int(((scw/2) - w/2) + w_shift))+'+'+str(int(((sch/2) - h/2) + h_shift))

        def __init__(self, title, width = 400, height = 400, hor_shift = 0, ver_shift = 0):
            self.title = title
            self.window = Tk()
            self.window.title(title)
            self.width = width
            self.height = height
            self.screen_width = self.window.winfo_screenwidth()
            self.screen_height = self.window.winfo_screenheight()
            self.window.geometry(self.centerScreen(self.width, self.height, self.screen_width, self.screen_height, hor_shift, ver_shift))
            self.menu = self.menuBar(self.window)
            self.notebook = self.tabs(self.window)
            self.child_objects = {}
            self.child_variables = {}
            self.window.withdraw()
            self.window.update()

        def add_button(self, bText, cmnd, location = 'root', side = None, fill = None, expand = None, column = None, row = None, width = None, sticky = None):
            if location == 'root':
                location = self.window
            B = Tkinter.Button(location, text = bText, command = cmnd, width = width)
            if (column is not None) or (row is not None) or (row is not sticky):
                B.grid(column = column, row = row, sticky = sticky)
            else:
                B.pack(side = side, fill = fill, expand = expand)
            return B

        def switch(self, bool_var):
            bool_var.set(not bool_var.get())

        def add_checkbox(self, bText, var, location = 'root', cmnd = None, side = None, fill = None, expand = None, column = None, row = None):
            if location == 'root':
                location = self.window
            CB = Checkbutton(location, text = bText, variable = var, onvalue = True, offvalue = False, command = cmnd)
            if (column is not None) or (row is not None):
                CB.grid(column = column, row = row, sticky = 'W')
            else:
                CB.pack(side = side, fill = fill, expand = expand, anchor = W)
            return CB

        def add_label_frame(self, label = '', location = 'root', side = None, fill = None, expand = None, anchor = 'center', column = None, row = None):
            if location == 'root':
                location = self.window
            L = LabelFrame(location, text = label)
            if (column is not None) or (row is not None):
                L.grid(column = column, row = row)
            else:
                L.pack(side = side, fill = fill, expand = expand, anchor = anchor)
            return L

        def add_frame(self, label = '', location = 'root', side = None, fill = None, expand = None, anchor = 'center', column = None, row = None):
            if location == 'root':
                location = self.window
            F = Frame(location, text = label)
            if (column is not None) or (row is not None):
                F.grid(column = column, row = row)
            else:
                F.pack(side = side, fill = fill, expand = expand, anchor = anchor)
            return F

        def add_combobox(self, values = [], location = 'root', side = None, fill = None, expand = None, anchor = 'center', column = None, row = None, sticky = None):
            if location == 'root':
                location = self.window
            CB2 = ttk.Combobox(location, values = values, state='readonly')
            if (column is not None) or (row is not None) or (row is not sticky):
                CB2.grid(column = column, row = row, sticky = sticky)
            else:
                CB2.pack(side = side, fill = fill, expand = expand, anchor = anchor)
            return CB2

        def add_label(self, label = '', location = 'root', side = None, fill = None, expand = None, anchor = 'center', column = None, row = None, sticky = None):
            if location == 'root':
                location = self.window
            L = Label(location, text = label, justify = LEFT)
            if (column is not None) or (row is not None) or (row is not sticky):
                L.grid(column = column, row = row, sticky = sticky)
            else:
                L.pack(side = side, fill = fill, expand = expand, anchor = anchor)
            return L

        def add_entry(self, location = 'root', textvar = None, state = NORMAL, side = None, fill = None, expand = None, anchor = 'center', column = None, row = None, sticky = None):
            if location == 'root':
                location = self.window
            E = Entry(location, state = state, textvariable = textvar)
            if (column is not None) or (row is not None) or (row is not sticky):
                E.grid(column = column, row = row, sticky = sticky)
            else:
                E.pack(side = side, fill = fill, expand = expand, anchor = anchor)
            return E

        def change_entry_state(self, entry, bool_var):
            if bool_var.get():
                entry.config(state=DISABLED)
            else:
                entry.config(state=NORMAL)

        def add_listbox(self, id_tag, location = 'root', side = None, fill = None, expand = None, anchor = None, width = None):
            if location == 'root':
                location = self.window
            if width is None:
                width = location.winfo_width()
            self.child_objects['Top Labelframe' + id_tag] = self.add_label_frame(id_tag, location, side, fill, expand, anchor)
            self.child_objects['Listbox' + id_tag] = Listbox(self.child_objects['Top Labelframe' + id_tag], selectmode = EXTENDED, width = width)
            self.child_objects['Scrollbar' + id_tag] = Scrollbar(self.child_objects['Top Labelframe' + id_tag], command = self.child_objects['Listbox' + id_tag].yview)
            self.child_objects['Listbox' + id_tag].configure(yscrollcommand = self.child_objects['Scrollbar' + id_tag].set)
            self.child_objects['Scrollbar' + id_tag].pack(side = 'right', fill = 'y', expand = True, anchor = E)
            self.child_objects['Listbox' + id_tag].pack(side = 'top', fill = 'both', expand = True, anchor = W)

        class tabs:

            def __init__(self, parent):
                self.notebook = ttk.Notebook(parent)

            def add_tab(self, tab_title):
                newTab = ttk.Frame(self.notebook)
                self.notebook.add(newTab, text = tab_title)
                self.notebook.pack(expand = True, fill = 'both')
                return newTab
            
        class menuBar:

            def __init__(self, parent):
                self.menubar = Menu(parent)
                parent.config(menu = self.menubar)

            def add_menu(self, parent_menu, menu_title, menu_items, tear = 0):
                newMenu = Menu(parent_menu,tearoff = tear)
                for menu_item in menu_items:
                    if len(menu_item) == 2:
                        self.add_menu(newMenu,menu_item[0],menu_item[1])
                    elif len(menu_item) == 4:
                        if menu_item[3] == 'command':
                            newMenu.add_command(label = menu_item[0], command = menu_item[1])
                        elif menu_item[3] == 'checkbutton':
                            newMenu.add_checkbutton(label = menu_item[0], variable = menu_item[1][0], onvalue = menu_item[1][1], offvalue = (not menu_item[1][1]))
                        if menu_item[2]:
                            newMenu.add_separator()
                parent_menu.add_cascade(label = menu_title, menu = newMenu)

class g16File:

    def readCom(self):
        fileData = open(self.fullName)
        coordinates = []
        base_func = []
        connections = []
        line = fileData.readline()
        done_with_atoms = False
        prev_line = False
        while line:
            if not done_with_atoms:
                if not base_func:
                    if '#' in line:
                        params = line.split()
                        for par in params:
                            if '/' in par:
                                base_func = par
                                break
                if not self.chk:
                    if '%chk' in line:
                        self.chk = line[5:-(len(self.fileType)+2)]
                if not self.mem:
                    if '%mem' in line:
                        self.mem = line[5:-3]
                if not self.nProcs:
                    if '%nproc' in line:
                        self.nProcs = line[13:-1]
                if (not self.charge) or (not self.multiplicity):
                    if len(line.split()) == 2:
                        cmData = line.split()
                        if not self.charge:
                            self.charge = cmData[0]
                        if not self.multiplicity:
                            self.multiplicity = cmData[1]
                try:
                    line_len = len(line.split())
                except: line_len = None
                if line_len != 4:
                    if prev_line:
                        done_with_atoms = True
                elif '#' not in line:
                    coordinates.append(line.split())
                    prev_line = True
            elif len(line) != 1:
                connections.append(line[:-1])
            line = fileData.readline()
        fileData.close()
        return coordinates, base_func, connections

    def readLog(self):
        fileData = open(self.fullName)
        coordinates = []
        base_func = []
        line = fileData.readline()
        fullData = []
        start_markers = []
        stop_markers = []
        counter = 0
        chk_found = False
        while line:
            if not base_func:
                if '#' in line:
                    params = line.split()
                    for par in params:
                        if '/' in par:
                            base_func = par
                            break
            if not chk_found:
                if '%chk' in line:
                    if '.chk' in line:
                        self.chk = line[6:-(len(self.fileType)+2)]
                        chk_found = True
                    else:
                        self.chk = line[6:-1]
                elif '.chk' in line:
                    self.chk += line[:-(len(self.fileType)+2)]
                    chk_found = True
            if not self.mem:
                if '%mem' in line:
                    self.mem = line[6:-3]
            if not self.nProcs:
                if '%nproc' in line:
                    self.nProcs = line[14:-1]
            if (not self.charge) or (not self.multiplicity):
                if 'Charge' in line:
                    cmData = line.split()
                    if not self.charge:
                        self.charge = cmData[2]
                    if not self.multiplicity:
                        self.multiplicity = cmData[5]
            if 'GINC-' in line:
                start_markers.append(counter)
            elif '@' in line:
                stop_markers.append(counter+1)
            fullData.append(line.split())
            counter += 1
            line = fileData.readline()
        tempData = []
        for line in fullData[start_markers[-1]:stop_markers[-1]]:
            tempData += line
        for line in (''.join(tempData)).split('\\'):
            try: line_len = len(line.split(','))
            except: line_len = None
            if line_len == 4:
                coordinates.append(line.split(','))
            elif line_len == 5:
                toAdd = line.split(',')
                toAdd.pop(1)
                coordinates.append(toAdd)
        new_molecule = molecule(coordinates)
        connections = new_molecule.return_connections()
        return coordinates, base_func, connections

    def readFile(self):
        if self.fileType == 'com':
            return self.readCom()
        if self.fileType == 'log':
            return self.readLog()
    
    def __init__(self, fullname, coordinates = None, chk = None, mem = None, nProcs = None, charge = None, multiplicity = None):
        self.fullName = fullname
        import platform
        if platform.system() == 'Windows':
            self.fileNameLong = (fullname.split('/'))[-1]
        elif platform.system() == 'Linux':
            self.fileNameLong = (fullname.split('/'))[-1]
        self.fileNameShort = self.fileNameLong.split('.')[0]
        self.fileType = self.fileNameLong.split('.')[1]
        self.filePath = fullname[:-len(self.fileNameLong)]
        self.chk = chk
        self.mem = mem
        self.nProcs = nProcs
        self.charge = charge
        self.multiplicity = multiplicity
        if coordinates is None:
            self.coordinates, self.base_func, self.connections = self.readFile()
        self.xyzName = self.filePath + self.fileNameShort + '.xyz'

    def xyzFormat(self):
        outputFile = [str(len(self.coordinates)) + '\n','\n']
        for line in self.coordinates:
            outputFile.append('\t'.join(line) + '\n')
        outputFile.append('')
        return outputFile

    def xyzCreate(self):
        newFile = open(self.xyzName,'w')
        newFile.writelines(self.xyzFormat())
        newFile.close
        return

    def xyzReorient(self):
        self.xyzCreate()
        os.system(os.path.dirname(os.path.realpath(__file__)) + '/orient.py ' + self.xyzName + ' -op -ry 90')
        fileData = open(self.xyzName)
        line = fileData.readline()
        self.coordinates = []
        while line:
            new_line = line.split()
            if len(new_line) == 4:
                self.coordinates.append(new_line)
            line = fileData.readline()
        fileData.close
        return

    def createCom(self, data):
        outputData = []
        for line in data[:-1]:
            outputData.append(str(line) + '\n')
        outputData.append(str(data[-1]))
        os.umask(0)
        newFile = os.fdopen(os.open(self.fullName, os.O_CREAT | os.O_WRONLY, 0o777), 'w')
        newFile.writelines(outputData)
        newFile.close
        return

class outputFile:

    def defineBounds(self):
        x_list = []
        y_list = []
        z_list = []
        for atom in self.coordinates:
            x_list.append(float(atom[1]))
            y_list.append(float(atom[2]))
            z_list.append(float(atom[3]))
        return round(min(x_list) - self.margin), math.ceil(max(x_list) + self.margin), round(min(y_list) - self.margin), math.ceil(max(y_list) + self.margin), round(min(z_list) - self.margin), math.ceil(max(z_list) + self.margin)

    def __init__(self, g16Fil, margin = 2.0, interval = 0.5, doDummies = True):
        self.parent = g16Fil
        self.coordinates = self.parent.coordinates
        self.connections = self.parent.connections
        self.margin = margin
        self.interval = interval
        self.minX, self.maxX, self.minY, self.maxY, self.minZ, self.maxZ = self.defineBounds()
        self.dummyNumber = None
        if doDummies:
            self.dummyList, self.dummyConnections = self.createDummyList()

    def createDummyList(self):
        dummyList = []
        dummyConnections = []
        dummy_start_index = len(self.coordinates) + 1
        currentX = self.minX
        while currentX < self.maxX + self.interval:
            currentY = self.minY
            while currentY < self.maxY + self.interval:
                currentZ = self.minZ
                while currentZ < self.maxZ + self.interval:
                    dummyList.append(['Bq', currentX, currentY, currentZ])
                    dummyConnections.append(str(dummy_start_index))
                    dummy_start_index += 1
                    currentZ += self.interval
                currentY += self.interval
            currentX += self.interval
        self.dummyNumber = len(dummyList)
        return dummyList, dummyConnections

    def create(self, suffix = '', path = None, pathMode = None, nProc = None, memory = None, base_func = None, c = None, m = None, method = None, addInp = None, addDummies = True, fileTracker = []):
        outputDataBlock = []
        if not nProc:
            if not self.parent.nProcs:
                outputDataBlock.append('%nprocshared=' + str(self.parent.nProcs))
        else:
            outputDataBlock.append('%nprocshared=' + str(nProcs))
        if not memory:
            if not self.parent.mem:
                 outputDataBlock.append('%mem=' + str(self.parent.mem) + 'GB')
        else:
            outputDataBlock.append('%mem=' + str(memory) + 'GB')
        if pathMode is not None:
            if pathMode == 'Use Parent':
                path = self.parent.chk
            elif pathMode == 'Custom':
                path += self.parent.fileNameShort
            outputDataBlock.append('%chk=' + str(path) + '-NICS-3D' + suffix + '.chk')
        if not base_func:
            base_func = self.parent.base_func
        if not c:
            c = self.parent.charge
        if not m:
            m = self.parent.multiplicity
        if not method:
            method = 'giao'
        if not addInp:
            addInp = ''
        outputDataBlock += [
            '# ' + base_func + ' nmr=' + method + ' geom=connectivity ' + addInp,
            '',
            '',
            '',
            c + ' ' + m
        ]
        if addDummies:
            if self.dummyNumber < 50000:
                outputData = outputDataBlock [:]
                outputData[-3] = self.parent.fileNameShort + '-NICS-3D' + suffix
                fileCoordinates = self.coordinates + self.dummyList
                for line in fileCoordinates:
                    new_line = []
                    for item in line:
                        new_line.append(str(item))
                    outputData.append('\t'.join(new_line))
                fileConnections = self.connections + self.dummyConnections
                outputData.append('')
                for line in fileConnections:
                    outputData.append(line)
                outputData.append('')
                outputFile = g16File(self.parent.filePath + self.parent.fileNameShort + '-NICS-3D' + suffix + '.com', coordinates = fileCoordinates)
                outputFile.createCom(outputData)
                fileTracker.append(str(path) + '-NICS-3D' + suffix + '.com')
            else:
                nparts = int(self.dummyNumber/25000.0)
                z_len = int(self.maxZ - self.minZ)
                segment_size = int(z_len / nparts)
                if segment_size < 1: segment_size = 1
                clone_dummies = self.dummyList
                for index in range(1, z_len+1):
                    if len(clone_dummies) <= 0:
                        break
                    currentDummyList= []
                    pop_index = 0
                    while pop_index < len(clone_dummies):
                        if float(clone_dummies[pop_index][3]) < (float(self.minZ) + float(segment_size*index)):
                            atom = clone_dummies.pop(pop_index)
                            currentDummyList.append(atom)
                        else:
                            pop_index += 1
                    outputData = outputDataBlock [:]
                    outputData[-3] = self.parent.fileNameShort + '-NICS-3D' + suffix + '-Part' + str(index)
                    if pathMode is not None:
                        outputData[-6] = outputData[-6][:-4] + '-Part' + str(index) + outputData[-6][-4:]
                    fileCoordinates = self.coordinates + currentDummyList
                    for line in fileCoordinates:
                        new_line = []
                        for item in line:
                            new_line.append(str(item))
                        outputData.append('\t'.join(new_line))
                    outputData.append('')
                    for line in self.connections:
                        outputData.append(line)
                    len_coordinates = len(self.coordinates)
                    len_dummies = len(currentDummyList)
                    for sub_index in range(len_dummies):
                        outputData.append(str((sub_index + len_coordinates + 1)))
                    outputData.append('')
                    outputFile = g16File(self.parent.filePath + self.parent.fileNameShort + '-NICS-3D' + suffix + '-Part' + str(index) + '.com',
                                         coordinates = fileCoordinates,)
                    outputFile.createCom(outputData)
                    fileTracker.append(str(path) + '-NICS-3D' + suffix + '-Part' + str(index) + '.com')

class molecule:

    def __init__(self, data):

        def add_bond(atom1, atom2, bondLength):
            atom1.bonds.append(str(atom2.index))
            atom1.bonds.append(bondLength)
            atom1.connections.append(atom2)
            atom2.connections.append(atom1)

        self.atoms = {}
        for index in range(len(data)):
            self.atoms[index + 1] = atom(index + 1, *data[index])
        for index1 in range(len(self.atoms)):
            for index2 in range(index1 + 1, len(self.atoms)):
                atom1 = self.atoms[index1 + 1]
                atom2 = self.atoms[index2 + 1]
                dist = self.distance(atom1, atom2)
                if atom1.symbol == 'H' or atom2.symbol == 'H':
                    if dist < 1.1:
                        add_bond(atom1, atom2, '1.0')
                elif atom1.symbol == 'C' and atom2.symbol == 'C':
                    if dist < 1.25:
                        add_bond(atom1, atom2, '3.0')
                    elif dist < 1.3:
                        add_bond(atom1, atom2, '2.5')
                    elif dist < 1.4:
                        add_bond(atom1, atom2, '2.0')
                    elif dist < 1.45:
                        add_bond(atom1, atom2, '1.5')
                    elif dist < 2.0:
                        add_bond(atom1, atom2, '1.0')
                elif (atom1.symbol == 'O' and atom2.symbol == 'C') or (atom1.symbol == 'C' and atom2.symbol == 'O'):
                    if dist < 1.3:
                        add_bond(atom1, atom2, '2.0')
                    elif dist < 2.0:
                        add_bond(atom1, atom2, '1.0')
                elif dist < 1.25:
                    add_bond(atom1, atom2, '3.0')
                elif dist < 1.3:
                    add_bond(atom1, atom2, '2.5')
                elif dist < 2.0:
                    add_bond(atom1, atom2, '1.0')
        self.molSize = len(self.atoms)

    def add_atom(self, new_atom): # currently, only for dummy atoms as this doesn't update the bond data
        self.molSize += 1
        self.atoms[self.molSize] = atom(self.molSize, *new_atom)

    def distance(self, atom1, atom2):
        return math.sqrt((atom1.x-atom2.x)**2 + (atom1.y-atom2.y)**2 + (atom1.z-atom2.z)**2)

    def return_connections(self):
        connections = []
        for index in range(self.molSize):
            new_line = ' '.join(self.atoms[index + 1].bonds)
            connections.append(new_line)
        return connections

class atom:

    def __init__(self, index, symbol, x, y, z):
        self.index = index
        self.symbol = symbol
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.connections = []
        self.bonds = [str(self.index)]
        
A=gui()


