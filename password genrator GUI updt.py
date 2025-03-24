import random
import string
import tkinter as tk
from tkinter import messagebox

class PasswordGen:

    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('500x650')
        self.root.title('Password Generator')

        self.label_name = tk.Label(self.root, text='Enter the length of the password', font=('Arial', 15))
        self.label_name.pack(padx=10, pady=10)

        # for the user to enter the length of the password
        self.len_entry = tk.Entry(self.root)
        self.len_entry.pack()

        self.included_chars = tk.Label(self.root, text='''Choose the characters  you want to
        include in your password:''', font=('Arial', 14))
        self.included_chars.pack(padx=20, pady=10)

        # checkboxes for the users to tick the type of characters they want included in their
        # password(upper case and lowercase letters, numbers, symbols)

        self.check_state_lwr = tk.IntVar()
        self.check_state_upr = tk.IntVar()
        self.check_state_nums = tk.IntVar()
        self.check_state_sym = tk.IntVar()

        self.check_lwr = tk.Checkbutton(self.root, text='Lower-case letters', variable=self.check_state_lwr)
        self.check_lwr.pack()
        self.check_upr = tk.Checkbutton(self.root, text='Upper-case letters',variable=self.check_state_upr)
        self.check_upr.pack()
        self.check_nums = tk.Checkbutton(self.root, text='Numbers', variable=self.check_state_nums)
        self.check_nums.pack(padx=200)
        self.check_sym = tk.Checkbutton(self.root, text='symbols', variable=self.check_state_sym)
        self.check_sym.pack()

        # the button that triggers the password generator func
        self.generate_button = tk.Button(self.root, text='Generate', font=('Arial', 14), command=self.generate_password)
        self.generate_button.pack(padx=10, pady=10)

        # this textbox is where the generated password is displayed
        self.display = tk.Text(self.root, height=5, width=20)
        self.display.pack()

        # to copy the password to clipboard
        self.copy_button = tk.Button(self.root, text='Copy', command=self.copy_to_clipboard)
        self.copy_button.pack(pady=10)

        # this creates a button that will clear what's in the display textbox
        self.clear_button = tk.Button(self.root, text='Clear', command=self.clear)
        self.clear_button.pack(pady=1)

        # a button for saving the passwords in a file
        self.save_button = tk.Button(self.root, text='Save in a file', command=self.save_password_to_file)
        self.save_button.pack(pady=10)

        # a button that triggers a func that resets app
        reset_button = tk.Button(self.root, text='Reset', command=self.reset)
        reset_button.pack()

        self.checker_for_save = 0 # this is used to keep the save_password_to_file func
                                    # from doing what it does over and over again every time it's clicked.
        self.root.mainloop()

    # create a function that does the work of the generate_button
    def generate_password(self):
        # create a dictionary that holds all the ticked characters based on the conditions provided
        # the .get() method tells us whether the checkbox is checked or not. gives 1 if checked and 0 if not

        character_sets = {
            'lowercase': string.ascii_lowercase if self.check_state_lwr.get() == 1 else '',
            'uppercase': string.ascii_uppercase if self.check_state_upr.get() == 1 else '',
            'numbers': string.digits if self.check_state_nums.get() == 1 else '',
            'special': string.punctuation if self.check_state_sym.get() == 1 else ''
        }

        password = ''
        temp_word = ''.join(character_sets.values()) # pile up all the checked chars in one string to choose from randomly

        try:
            for i in range(int(self.len_entry.get())):
                password += random.choice(temp_word)

            # this line of code displays the generated password in the display textbox
            # and makes sure every time a password is generated, it is displayed on a new line
            self.display.config(state=tk.NORMAL)
            self.display.insert(tk.END, password + '\n')
            self.display.config(state=tk.DISABLED)

        except ValueError:    # incase the user enters a non-numeric character for the length
            messagebox.showerror('Invalid Input!', 'Please enter a valid number for the length.')
        except IndexError:    # incase the user doesn't select any type of character to be included in the password
            messagebox.showerror('ERROR!', 'You need to select at least one character to be included in your password.')

    def copy_to_clipboard(self):
        # the function that does the work of copy_button
        text = self.display.get(1.0, tk.END).strip()
        self.root.clipboard_append(text)
        self.root.update()

    def clear(self):
        # the function that does the work of the clear button
        self.root.clipboard_clear()
        self.display.config(state=tk.NORMAL)
        self.display.delete(1.0, tk.END)
        self.display.config(state=tk.DISABLED)

    def save_password_to_file(self):
        # this func doesn't save the password, but makes the entry for the label,
        # and the ok button(that does the work) appear.
        if self.checker_for_save == 0: # if not clicked previously

            self.ask_for_label = tk.Label(self.root, text='Enter a label for your password.', font=('Arial', 9))
            self.ask_for_label.pack()

            self.label_name = tk.Entry(self.root)
            self.label_name.pack()

            self.ok_button = tk.Button(self.root, text='Ok', command=self.ok)
            self.ok_button.pack(pady=10)

            self.checker_for_ok = 0 # keeps the ok button from doing what it does over and over again whenever clicked
            self.checker_for_save += 1 # it's incremented means it has been clicked already,won't work the next click

        else:
            pass

    def ok(self, filename='passwords.txt'):
        # this func is the one that saves the password
        password = self.display.get(1.0, tk.END).strip() # get what's on the display

        if password: # saving not possible without generating a password 1st

            if self.checker_for_ok == 0: # if the ok button has not been clicked previously

                if self.label_name.get(): # if the lable for the password is not empty

                    with open(filename, 'a') as file:
                        file.write(f">>Label:{self.label_name.get()} \n>>Passwords:\n{password}\n_________\n")

                    self.success_label = tk.Label(self.root, text=f"Password (label: '{self.label_name.get()}') saved to {filename} successfully!", font=('Areal', 8))
                    self.success_label.pack()

                    self.checker_for_ok += 1 # incremented means, wont work next time clicked

                else:
                    messagebox.showerror('Label not given!', "You haven't given any label for your password.")
            else:
                messagebox.showerror('Already done!', "You have already saved your pass word successfully. Press the "
                                                      "Reset button to save another password.")
        else:
            messagebox.showerror('Nothing to save!', "You haven't generated any password yet.")

    def reset(self):
        # severs the check_for_ok and checker_for_save effects, clears the password display
        # makes it as it was before the save button was clicked

        if self.checker_for_ok == 0: # if ok isn't clicked, reset doesn't work
            pass
        else:
            self.clear()
            self.ask_for_label.destroy()
            self.label_name.destroy()
            self.success_label.destroy()
            self.ok_button.destroy()
            self.checker_for_save -= 1
            self.checker_for_ok -= 1


# creating an instant of our class
PasswordGen()
