# Ryan O'Connell
# 5/5/23 - 10/18/23
#   Work done 5/5/23, 7/1 - 7/4/23, 9/25/23, 10/17 - 10/18/23
# Converting my Hunt Showdown spreadsheet into a tkinter program for easy input
# and to reduce scrolling times on a Google sheet.

import pandas as pd
import matplotlib.pyplot as plt
import tkinter
from tkinter import *
from tkinter.ttk import *
import os
from hs_entry import Entry 


# Main class - displays the GUI and holds Entry items
class Spreadsheet :
    # Global variables for path name and entry list
    g_path = ''
    stored_items = []
    assumed_id = 0

    # Count and percentage for the first roll reward
    # 2,500 / 2,000 XP
    roll_one_c = 0
    roll_one_p = 0

    # Count and percentage for the second roll reward
    # 5,000 / 4,000 XP
    roll_two_c = 0
    roll_two_p = 0

    # Count and percentage for the third roll statistic
    # 7,000 / 5,500 XP
    roll_three_c = 0
    roll_three_p = 0

    # Count and percentage for the first roll statistic
    # 10,000 / 8,000 XP
    roll_four_c = 0
    roll_four_p = 0

    # Statistics for:
    #   - Total Hunt Dollars granted
    #   - Number of Hunt Dollar rewards granted
    #   - Percentage of rewards which are Hunt Dollars
    #   - Average dollar value of Hunt Dollar rewards
    hd_total = 0
    hd_count = 0
    hd_percent = 0
    hd_average = 0

    # Statistics for:
    #   - Total Blood Bonds granted
    #   - Number of Blood Bond rewards granted
    #   - Percentage of rewards which are Blood Bonds
    #   - Average dollar value of Blood Bond rewards
    bb_total = 0
    bb_count = 0
    bb_percent = 0
    bb_average = 0

    # Reward type by percentage of pulls
    weapon_p = 0
    legeni_p = 0
    legenu_p = 0
    huntsl_p = 0
    experi_p = 0
    upgrad_p = 0
    consum_p = 0
    tool_p   = 0
    loadou_p = 0
    legenh_p = 0
    badhan_p = 0

    # Constructor, responsible for GUI building
    def __init__(self, path) :
        # Edit global path as according to class instance call
        global g_path
        global assumed_id
        g_path = path

        # If the storage file doesn't exist, read from a existing CSV
        # If the flag is true, this signals they have a CSV to read from.
        if( not os.path.isfile(path) ) :
            self.import_csv()
        # If no flag or the storage file does exist, open the entries and read into program
        else :
            self.load_entries(path)

        # Statistics refresh - calculate stats for BBs, HDs, and roll percentages.
        # Anytime items are loaded or a CSV is read these stats should be redone.
        # Boolean flag is to signal whether or not the pie chart will be generated.
        self.refresh(False)


        # Create the main window in antique white, aesthetic with Hunt: Showdown
        # which takes place in the late 1800s.
        self.main_window = tkinter.Tk()
        self.main_window.configure(bg = 'antique white', padx=20, pady=20)

        # Set font globally to Times New Roman and align the background color.
        self.main_window.option_add("*Font", "Times")
        self.main_window.option_add("*Label.Font", "Times")
        self.main_window.option_add("*Background", "antique white")        

        # Print to the GUI console for visual communication with user.
        # Initialize a blank box
        self.message_box = tkinter.Label(self.main_window,
                                         textvar = '',
                                         font = ('Times 10'))
        self.message_box.grid(row = 7, column = 1, pady = 20)
        
        # Print to the GUI console for visual communication with user.
        # Controlling the actual message printed
        def print_to_console(msg) :
            self.message = tkinter.StringVar()
            self.message.set(msg)
            self.message_box.config(text=self.message.get())


        # Tool title.
        self.desc = tkinter.Label(self.main_window,
                                  text = 'Hunt: Showdown Chary Tracker', 
                                  font = ('Times 15 bold'))
        self.desc.grid(row = 0, column = 1, sticky = W, pady = 10)

        # Calculate the number of entries in the database.
        assumed_id = len(stored_items) + 1

        # Display the entries counted in storage file.
        # The ID field autopopulates based on the stored number of entries in
        # the storage document. Printing the number of rows makes it clearer why
        # a number appears for users.
        self.entries = tkinter.IntVar()
        self.entries.set(assumed_id - 1)

        self.entry_cnt = tkinter.Label(self.main_window,
                                       text = 'Total entries:',
                                       font = ('Times 10'))
        self.entry_cnt.grid(row = 6, column = 0, sticky = W, pady = 10, padx = 10)
        def entry_cnt_figure() :
            self.entry_cnt_fig = tkinter.Label(self.main_window,
                                               textvar = self.entries,
                                               font = ('Times 10'))
            self.entry_cnt_fig.grid(row = 6, column = 0, sticky = E, pady = 10, padx = 10)
        entry_cnt_figure()


        # Width of all entry boxes
        width_val = 28

        # FIELD 1 - ENTRY NUMBER
        # The ID number of each entry, primary key.

        self.id_prompt = tkinter.Label(self.main_window,
                                       text = 'Entry Number:')
        self.id_value = tkinter.Entry(self.main_window,
                                      width = width_val)
        self.id_value.insert(0, assumed_id)
        self.id_field = tkinter.Label(self.main_window,
                                      textvar = self.id_value)

        self.id_prompt.grid(row = 2, column = 0, sticky = E, pady = 5, padx = 10)
        self.id_value.grid(row = 2, column = 1, sticky = W, pady = 5)
        self.id_field.grid(row = 2, column = 2, pady = 5)


        # FIELD 2 - REWARD INFORMATION
        # The actual drop information in text.

        self.reward_prompt = tkinter.Label(self.main_window,
                                           text = 'Reward Description:')
        self.reward_value = tkinter.Entry(self.main_window,
                                          width = width_val)
        self.reward_field = tkinter.Label(self.main_window,
                                          textvar = self.reward_value)

        self.reward_prompt.grid(row = 3, column = 0, sticky = E, pady = 5, padx = 10)
        self.reward_value.grid(row = 3, column = 1, sticky = W, pady = 5)
        self.reward_field.grid(row = 3, column = 2, pady = 5)


        # FIELD 3 - REWARD NUMBER
        # The roll number of the tribute, 1-4. 

        self.position_prompt = tkinter.Label(self.main_window,
                                             text = 'Roll Number:')
        self.position_value = tkinter.Entry(self.main_window,
                                            width = width_val)
        self.position_field = tkinter.Label(self.main_window,
                                            textvar  = self.position_value)

        self.position_prompt.grid(row = 4, column = 0, sticky = E, pady = 5, padx = 10)
        self.position_value.grid(row = 4, column = 1, sticky = W, pady = 5)
        self.position_field.grid(row = 4, column = 2, pady = 5)

        # FIELD 4 - REWARD CODE
        # The code category corresponding to the reward type, 0-12.

        self.code_prompt = tkinter.Label(self.main_window,
                                         text = 'Reward Code:')
        self.code_value = tkinter.Entry(self.main_window,
                                        width = width_val)
        self.code_field = tkinter.Label(self.main_window,
                                        textvar = self.code_value)

        self.code_prompt.grid(row = 5, column = 0, sticky = E, pady = 5, padx = 10)
        self.code_value.grid(row = 5, column = 1, sticky = W, pady = 5)
        self.code_field.grid(row = 5, column = 2, pady = 5)



        # ROLL NUMBER PRESELECTS
        # Display four buttons to the right, labeled 1-4, which when clicked easily populate the roll number.

        # TODO: fix inconsistent background colorations

        self.instruction = Label(self.main_window, text = "Roll Number presets:",
                                 font = ('Times 10'))
        self.roll_one = Button(self.main_window, text = "1",
                               command = lambda: [self.position_value.delete(0, END),
                                                  self.position_value.insert(0, 1)])
        self.roll_two = Button(self.main_window, text = "2",
                               command = lambda: [self.position_value.delete(0, END),
                                                  self.position_value.insert(0, 2)])
        self.roll_three = Button(self.main_window, text = "3",
                                 command = lambda: [self.position_value.delete(0, END),
                                                    self.position_value.insert(0, 3)])
        self.roll_four = Button(self.main_window, text = "4",
                                command = lambda: [self.position_value.delete(0, END),
                                                   self.position_value.insert(0, 4)])


        self.instruction.grid(row = 6, column = 3, padx = 15)
        self.roll_one.grid(row = 2, column = 3, padx = 15)
        self.roll_two.grid(row = 3, column = 3, padx = 15)
        self.roll_three.grid(row = 4, column = 3, padx = 15)
        self.roll_four.grid(row = 5, column = 3, padx = 15)


        # REWARD TYPES PRESELECTS
        # Display thirteen buttons in a keypad format, labeled 0-12, which when clicked easily populate
        # the code number - and translate the numeric values from text for the user. 

        self.re_instruction = Label(self.main_window,
                                    text = "Reward Code presets:",
                                    font = ('Times 10'))
        self.legendary_code1 = Label(self.main_window,
                                     text = 'I = Instance',
                                     font = ('Times 10'))
        self.legendary_code2 = Label(self.main_window,
                                     text = 'U = Unlock',
                                     font = ('Times 10'))
        self.legendary_code3 = Label(self.main_window,
                                     text = 'H = Hunter',
                                     font = ('Times 10'))
        self.button_wep = Button(self.main_window, text = "1 - Weapon",
                                 command = lambda: [self.code_value.delete(0, END),
                                                    self.code_value.insert(0, 1),
                                                    self.reward_value.delete(0, END)])
        self.button_lgi = Button(self.main_window, text = "2 - Legendary (I)",
                                 command = lambda: [self.code_value.delete(0, END),
                                                    self.code_value.insert(0, 2),
                                                    self.reward_value.delete(0, END)])
        self.button_lgu = Button(self.main_window, text = "3 - Legendary (U)",
                                 command = lambda: [self.code_value.delete(0, END),
                                                    self.code_value.insert(0, 3),
                                                    self.reward_value.delete(0, END)])
        self.button_bbs = Button(self.main_window, text = "4 - Blood Bonds",
                                 command = lambda: [self.code_value.delete(0, END),
                                                    self.code_value.insert(0, 4),
                                                    self.reward_value.delete(0, END)])
        self.button_hds = Button(self.main_window, text = "5 - Hunt Dollars",
                                 command = lambda: [self.code_value.delete(0, END),
                                                    self.code_value.insert(0, 5),
                                                    self.reward_value.delete(0, END)])
        self.button_htr = Button(self.main_window, text = "6 - Hunter Slot",
                                 command = lambda: [self.code_value.delete(0, END),
                                                    self.code_value.insert(0, 6),
                                                    self.reward_value.delete(0, END),
                                                    self.reward_value.insert(0, "Hunter Slot")])
        self.button_exp = Button(self.main_window, text = "7 - Experience",
                                 command = lambda: [self.code_value.delete(0, END),
                                                    self.code_value.insert(0, 7),
                                                    self.reward_value.delete(0, END),
                                                    self.reward_value.insert(0, "500 XP")])
        self.button_upg = Button(self.main_window, text = "8 - Upgrade Points",
                                 command = lambda: [self.code_value.delete(0, END),
                                                    self.code_value.insert(0, 8),
                                                    self.reward_value.delete(0, END),
                                                    self.reward_value.insert(0, "2 Upgrade Points")])
        self.button_con = Button(self.main_window, text = "9 - Consumable",
                                 command = lambda: [self.code_value.delete(0, END),
                                                    self.code_value.insert(0, 9),
                                                    self.reward_value.delete(0, END)])
        self.button_too = Button(self.main_window, text = "10 - Tool",
                                 command = lambda: [self.code_value.delete(0, END),
                                                    self.code_value.insert(0, 10),
                                                    self.reward_value.delete(0, END)])
        self.button_lds = Button(self.main_window, text = "11 - Loadout Slot",
                                 command = lambda: [self.code_value.delete(0, END),
                                                    self.code_value.insert(0, 11),
                                                    self.reward_value.delete(0, END),
                                                    self.reward_value.insert(0, "Loadout Slot")])
        self.button_lhr = Button(self.main_window, text = "12 - Legendary (H)",
                                 command = lambda: [self.code_value.delete(0, END),
                                                    self.code_value.insert(0, 12),
                                                    self.reward_value.delete(0, END)])
        self.button_bhd = Button(self.main_window, text = "0 - Bad Hand",
                                 command = lambda: [self.code_value.delete(0, END),
                                                    self.code_value.insert(0, 0),
                                                    self.reward_value.delete(0, END),
                                                    self.reward_value.insert(0, "Bad Hand")])

        self.re_instruction.grid(row = 6, column = 4, sticky = W)
        self.legendary_code1.grid(row = 3, column = 7, padx = 5, sticky = E)
        self.legendary_code2.grid(row = 4, column = 7, padx = 5, sticky = E)
        self.legendary_code3.grid(row = 5, column = 7, padx = 5, sticky = E)
        
        self.button_wep.grid(row = 2, column = 4, padx = 5, sticky = W)
        self.button_lgi.grid(row = 3, column = 4, padx = 5, sticky = W)
        self.button_lgu.grid(row = 4, column = 4, padx = 5, sticky = W)
        self.button_bbs.grid(row = 5, column = 4, padx = 5, sticky = W)

        self.button_hds.grid(row = 2, column = 5, sticky = W)
        self.button_htr.grid(row = 3, column = 5, sticky = W)
        self.button_exp.grid(row = 4, column = 5, sticky = W)
        self.button_upg.grid(row = 5, column = 5, sticky = W)

        self.button_con.grid(row = 2, column = 6, padx = 5, sticky = W)
        self.button_too.grid(row = 3, column = 6, padx = 5, sticky = W)
        self.button_lds.grid(row = 4, column = 6, padx = 5, sticky = W)
        self.button_lhr.grid(row = 5, column = 6, padx = 5, sticky = W)

        self.button_bhd.grid(row = 2, column = 7, padx = 5, sticky = E)

        def inner_refresh(addsubtract) :
            global assumed_id
            
            modifier = 1
            if addsubtract == "subtract" :
                modifier *= -1
                
            assumed_id += (1 * modifier)
            self.entries.set(assumed_id - 1)
            
            entry_cnt_figure()
            self.id_value.delete(0, END)
            self.id_value.insert(0, assumed_id)
        
        # ADD ENTRY BUTTON
        # Add a new entry to the file and list. Also calls a refresh on all stats.

        self.new_items = []
        self.add_entry = Button(self.main_window, text = "ADD ENTRY TO DATABASE",             
                                command = lambda: [(self.new_items.append(
                                                   Entry(self.id_value.get(), self.reward_value.get(),
                                                         self.position_value.get(), self.code_value.get())),
                                                   self.write_entries(self.new_items),
                                                   self.refresh(False), inner_refresh('add'),
                                                   self.reward_value.delete(0, END),
                                                   self.position_value.delete(0, END),
                                                   self.code_value.delete(0, END),
                                                   print_to_console("Successfully wrote entry to file."))
                                                   if self.is_invalid()
                                                   else print_to_console("Failed to write - all fields must be filled and in range.")])
        
        self.add_entry.grid(row = 6, column = 1, pady = 10, sticky = W)

        # Delete latest entry method
        def remove_last_line() :
            global stored_items
            file = open(path, 'r')
            entries = file.readlines()
            file.close()

            entries = entries[:-1]

            print_to_console("Successfully deleted entry.")
            inner_refresh('subtract')
            stored_items = entries

            file = open(path, 'w')
            for lines in stored_items :
                file.write(lines)
            file.close()

            self.refresh(False)
            
            
        # Delete latest entry button
        self.del_latest = Button(self.main_window, text = "DELETE LATEST ENTRY",
                                 command = lambda: [remove_last_line(),
                                                    print_to_console("Successfully deleted entry.")])
        self.del_latest.grid(row = 6, column = 1, pady = 10, sticky = E)
        

        # DISPLAY STATS

        def print_hd_stats() :
            # PRINT TOTAL OF HUNT DOLLARS FROM REWARDS
            self.hd_t = tkinter.Label(self.main_window,
                                      text = "Total HDs From Rewards:",
                                      font = ('Times 10'))
            self.hd_t.grid(row = 8, column = 1, sticky = W, padx = 10)
            self.hd_t_fig = tkinter.Label(self.main_window,
                                          text = hd_total,
                                          font = ('Times 10'))
            self.hd_t_fig.grid(row = 8, column = 1, sticky = E, padx = 10)
            # PRINT NUMBER OF HUNT DOLLAR ENTRIES
            self.hd_c = tkinter.Label(self.main_window,
                                      text = "Num. of HD Entries:",
                                      font = ('Times 10'))
            self.hd_c.grid(row = 9, column = 1, sticky = W, padx = 10)
            self.hd_c_fig = tkinter.Label(self.main_window,
                                          text = hd_count,
                                          font = ('Times 10'))
            self.hd_c_fig.grid(row = 9, column = 1, sticky = E, padx = 10)
            # PRINT PERCENTAGE OF REWARDS THAT ARE HUNT DOLLARS
            self.hd_p = tkinter.Label(self.main_window,
                                      text = "Percent of Entries as HDs:",
                                      font = ('Times 10'))
            self.hd_p.grid(row = 10, column = 1, sticky = W, padx = 10)
            self.hd_p_fig = tkinter.Label(self.main_window,
                                          text = hd_percent,
                                          font = ('Times 10'))
            self.hd_p_fig.grid(row = 10, column = 1, sticky = E, padx = 10)
            # PRINT AVERAGE PULL OF HUNT DOLLAR REWARDS
            self.hd_a = tkinter.Label(self.main_window,
                                      text = "Avg. HDs Per Pull:",
                                      font = ('Times 10'))
            self.hd_a.grid(row = 11, column = 1, sticky = W, padx = 10)
            self.hd_a_fig = tkinter.Label(self.main_window,
                                          text = hd_average,
                                          font = ('Times 10'))
            self.hd_a_fig.grid(row = 11, column = 1, sticky = E, padx = 10)

            # PRINT LINEBREAK FOR BETWEEN HD AND BB
            self.linebreak = tkinter.Label(self.main_window,
                                           text = "-----",
                                           font = ('Times 10'))
            self.linebreak.grid(row = 12, column = 1, padx = 10)


        def print_bb_stats() :
            # PRINT TOTAL OF BLOOD BONDS COLLECTED
            self.bb_t = tkinter.Label(self.main_window,
                                      text = "Total BBs From Rewards:",
                                      font = ('Times 10'))
            self.bb_t.grid(row = 13, column = 1, sticky = W, padx = 10)
            self.bb_t_fig = tkinter.Label(self.main_window,
                                          text = bb_total,
                                          font = ('Times 10'))
            self.bb_t_fig.grid(row = 13, column = 1, sticky = E, padx = 10)
            # PRINT NUMBER OF BLOOD BOND ENTRIES
            self.bb_c = tkinter.Label(self.main_window,
                                      text = "Num. of BB Entries:",
                                      font = ('Times 10'))
            self.bb_c.grid(row = 14, column = 1, sticky = W, padx = 10)
            self.bb_c_fig = tkinter.Label(self.main_window,
                                          text = bb_count,
                                          font = ('Times 10'))
            self.bb_c_fig.grid(row = 14, column = 1, sticky = E, padx = 10)
            # PRINT PERCENT OF BLOOD BONDS FROM REWARDS
            self.bb_p = tkinter.Label(self.main_window,
                                      text = "Percent of Entries as BBs:",
                                      font = ('Times 10'))
            self.bb_p.grid(row = 15, column = 1, sticky = W, padx = 10)
            self.bb_p_fig = tkinter.Label(self.main_window,
                                          text = bb_percent,
                                          font = ('Times 10'))
            self.bb_p_fig.grid(row = 15, column = 1, sticky = E, padx = 10)
            # PRINT AVG PULL OF BLOOD BOND REWARDS
            self.bb_a = tkinter.Label(self.main_window,
                                      text = "Avg. BBs Per Pull:",
                                      font = ('Times 10'))
            self.bb_a.grid(row = 16, column = 1, sticky = W, padx = 10)
            self.bb_a_fig = tkinter.Label(self.main_window,
                                          text = bb_average,
                                          font = ('Times 10'))
            self.bb_a_fig.grid(row = 16, column = 1, sticky = E, padx = 10)
            

        self.display_monetary = Button(self.main_window, text = "Display Currency Stats",
                                       command = lambda: [self.refresh(True),
                                                          print_hd_stats(),
                                                          print_bb_stats()])
        self.display_monetary.grid(row = 2, column = 9, sticky = W, pady = 5, padx = 10)

        # Run GUI!        
        tkinter.mainloop()

        
    # Import values to storage file from a CSV.
    def import_csv(self) :
        global stored_items
        db = pd.read_csv('hs_chary.csv', index_col = 0)
        entry_list = []
        for ind in db.index :
            ind = ind-1
            entry_list.append(Entry(ind+1,
                                   db.at[db.index[ind],"REWARD INFORMATION"],
                                   db.at[db.index[ind],"COLOR"],
                                   db.at[db.index[ind],"CODE"]))
        stored_items = entry_list
        self.write_entries(entry_list)
        print("Successfully read CSV import.")

    # Write entries from CSV or GUI to storage file.
    def write_entries(self, entry_list) :
        file = open(g_path, 'a')
        for item in entry_list :
            file.write(str(item))
            file.write('\n')
        file.close()
        print("Successfully appended to file.")

    # Read entries from storage file into program for stat calculation.
    def load_entries(self, path) :
        global stored_items
        file = open(path, 'r')
        entries = file.readlines()
        file.close()
        
        entry_list = []
        for line in entries :
            items = line.split(" : ")
            items[3] = items[3][0 : len(items[3])-1]
            entry_list.append(Entry(items[0], items[1], items[2], items[3]))
            
        print("Successfully read from storage file.")
        stored_items = entry_list
        
    # Calculate Hunt Dollar stats, as listed at document start.
    def get_hd_total(self) :
        # global stored_items
        global hd_total
        global hd_count
        global hd_percent
        global hd_average
        
        temp_c = 0
        temp_t = 0
        
        for item in stored_items :
            if(int(item.get_code()) == 5) :
                temp_c += 1
                temp_t += int(item.reward[:3])
                
        hd_count = temp_c
        hd_total = temp_t
        hd_percent = '{0:.5g}'.format(temp_c / len(stored_items) * 100)
        hd_average = int(temp_t / temp_c)

    # Calculate Blood Bond stats, as listed at document start.
    def get_bb_total(self) :
        global bb_total
        global bb_count
        global bb_percent
        global bb_average
        
        temp_c = 0
        temp_t = 0
        
        for item in stored_items :
            if(int(item.get_code()) == 4) :
                temp_c += 1
                temp_t += int(item.reward[:3])
                
        bb_count = temp_c
        bb_total = temp_t
        bb_percent = '{0:.5g}'.format(temp_c / len(stored_items) * 100)
        bb_average = int(temp_t / temp_c)

    # Calculate Roll Number statistics.
    def roll_num_stats(self) :
        global roll_one_c
        global roll_one_p
        temp_one_c = 0
        
        global roll_two_c
        global roll_two_p
        temp_two_c = 0
        
        global roll_three_c
        global roll_three_p
        temp_three_c = 0
        
        global roll_four_c
        global roll_four_p
        temp_four_c = 0

        for item in stored_items :
            if(int(item.get_rollnum()) == 1) :
                temp_one_c += 1
            elif(int(item.get_rollnum()) == 2) :
                temp_two_c += 1
            elif(int(item.get_rollnum()) == 3) :
                temp_three_c += 1
            else :
                temp_four_c += 1

        total_c = len(stored_items)

        roll_one_c = temp_one_c
        roll_two_c = temp_two_c
        roll_three_c = temp_three_c
        roll_four_c = temp_four_c

        roll_one_p = '{0:.5g}'.format(temp_one_c / total_c * 100)
        roll_two_p = '{0:.5g}'.format(temp_two_c / total_c * 100)
        roll_three_p = '{0:.5g}'.format(temp_three_c / total_c * 100)
        roll_four_p = '{0:.5g}'.format(temp_four_c / total_c * 100)

    def is_invalid(self) :
        if(self.id_value.get() != 0 and
           self.reward_value.get() != '' and
           self.position_value.get() != '' and
           self.code_value.get() != '') :
            if(int(self.position_value.get()) > 0 and
               int(self.position_value.get()) < 5 and
               int(self.code_value.get()) > -1 and
               int(self.code_value.get()) < 13) :
                return True
        return False
    

    def other_stats(self, button_flag) :
        global weapon_p
        global legeni_p
        global legenu_p
        global huntsl_p
        global experi_p
        global upgrad_p
        global consum_p
        global tool_p   
        global loadou_p 
        global legenh_p
        global badhan_p

        store = {0: self.badhan_p,
               1: self.weapon_p,
               2: self.legeni_p,
               3: self.legenu_p,
               6: self.huntsl_p,
               7: self.experi_p,
               8: self.upgrad_p,
               9: self.consum_p,
               10: self.tool_p,
               11: self.loadou_p,
               12: self.legenh_p }

        for items in stored_items:
            if(int(items.get_code()) != 4 and int(items.get_code()) != 5) :
                store[int(items.get_code())] += 1

        sizes = [0,0,0,0,
                 0,0,0,0,
                 0,0,0,0,0]
        pos = 0
        for items in store:
            if(pos != 4 and pos != 5) :
                sizes[int(pos)] = store[int(pos)]
            pos += 1
        sizes[4] = hd_count
        sizes[5] = bb_count
            
        labels = ["Badhand", "Weapon", "Legendary (I)", "Legendary (U)",
                  "Hunt Dollars", "Blood Bonds", "Hunter Slot", "Experience",
                  "Upgrade Points", "Consumable", "Tool", "Loadout Slot", "Legendary (H)"]

        if(button_flag):
            self.create_plot(sizes, labels)



    def create_plot(self, sizes, labels) :
        fig, ax = plt.subplots()
        labelplus = ['{0} - ({1})'.format(i,j) for i,j in zip(labels, sizes)]
        ax.pie(sizes, labels=labelplus, autopct='%1.1f%%',
               pctdistance=.7, labeldistance=1.2)
        ax.legend(labelplus,
                  title="Rewards",
                  loc="center left",
                  bbox_to_anchor=(1.3, 0, 0.5, 1))
        plt.show()

    # Call all statistics methods again, updating global variables.
    # Boolean value is for showing the pie chart - only show the pie chart if requested via "calc stats" button
    def refresh(self, is_launch) :
        self.load_entries(g_path)
        self.get_hd_total()
        self.get_bb_total()
        self.roll_num_stats()
        self.other_stats(is_launch)

        


def main() :
    run = Spreadsheet("hunt_spreadsheet.txt")


main()
