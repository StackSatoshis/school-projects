# Ryan Carroll
# CTI 110 (I01) Web, Pgm, & Db Foundation
# Python program that generates a list of secure passwords with the option to omit special characters
# saves all passwords into a .csv file

import secrets # using secrets over the random python module for security
import string # import the string module for string constants
import csv # import the csv module for saving password data


class PasswordGenerator:
    # list of allowed special characters by default
    special_chars = ['@', '#', '$', '=', ':', '?', '.', '/', '|', '~', '>', '*', '<']

    def __init__(self):
        # sets the filename and path
        self.csv_path = 'passwords.csv'

        # defines usable characters

        # letters: 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        letters = string.ascii_letters

        # digits: '0123456789'
        digits = string.digits

        # creates a variable of all available characters including special characters
        self.alphabet = letters + digits + ''.join(self.special_chars)

    def main(self):
        while True:
            print("Enter 'q' anytime to quit...")
            # assigning a name to the password run
            if (pass_name := input('Enter the name for the new password(s) you wish to generate: ')) == 'q':
                break

            # local variables set from functions
            pw_length = self.get_password_length()
            num_passwords = self.get_num_passwords()

            # asking the user if they wish to omit any special characters from the available pool
            omit_special_chars = input("Do you want to omit any specific special characters? (y/n): ") == 'y'
            if omit_special_chars:
                # shows the user the current list of available special characters
                print("Current list of available special characters:", self.special_chars)
                omitted_chars = self.get_omitted_chars()
                alphabet = self.alphabet
                for char in omitted_chars:
                    alphabet = alphabet.replace(char, '')  # Remove each omitted character from the alphabet
            else:
                alphabet = self.alphabet

            # creating a list to store generated passwords
            generated_passwords = []

            # this code checks to see if the user wishes to re-run the generation for any reason
            regenerate = True
            while regenerate:
                # clears the current list of passwords
                generated_passwords.clear()
                # loop runs for number of passwords requested
                for _ in range(num_passwords):
                    # creates a random password using the password_gen function
                    new_password = self.password_gen(pw_length, alphabet)
                    # appends the created password to the new_password list
                    generated_passwords.append(new_password)

                # prints the passwords into the console for verification
                print(f'{num_passwords} new passwords for "{pass_name}":')
                for password in generated_passwords:
                    print(password)

                # asks the user if they wish to save the passwords to a .csv file
                if (response := input('Would you like to save these new passwords? (y/n/r): ')) == 'y':
                    self.save_password(pass_name, generated_passwords)
                    print(f'{num_passwords} passwords saved successfully.')
                    # checks to see if regenerate is set to true, if so would repeat the loop
                    regenerate = False
                elif response == 'n':
                    # checks to see if regenerate is set to true, if so would repeat the loop
                    regenerate = False

    def get_num_passwords(self):
        """Gets the number of passwords to generate"""
        while True:
            try:
                num_passwords = int(input("Enter the number of passwords to generate: "))

        # error handling
                if num_passwords < 1:
                    print("Number of passwords should be at least 1.")
                else:
                    return num_passwords
            except ValueError:
                print("Invalid input. Please enter a valid number.")


    def get_password_length(self):
        """Gets the desired password character length and checks that it is at least 10 characters"""
        pw_length = int(input("Please enter password length (character count): "))

        # error handling
        if pw_length >= 10:
            return pw_length
        else:
            print("Password length selected is less than 10, please try again:")
            return self.get_password_length()

    def get_omitted_chars(self):
        """Prompts the user to enter specific special characters to omit"""
        # local variable to store omitted characters as a string
        omitted_chars = ""
        while True:
            char = input("Enter a special character to omit (or 'f' to finish): ")
            # this code checks for the f command (finish) and allows us to break the loop
            if char == 'f':
                break
            # checks if there are any ',' present in the input, if so we know multiple characters are being omitted
            elif ',' in char:
                # Split the input string by ',' and remove any whitespaces
                for c in char.split(','):
                    c = c.strip()  # Remove leading and trailing whitespaces from each character
                    if c in self.special_chars:
                        omitted_chars += c
                    else:
                        print(f"'{c}' is not a valid special character.")
            elif char in self.special_chars:
                # Adds the specified special character to the omitted_chars string
                omitted_chars += char
            else:
                print("Invalid special character. Please try again.")
            print(f"Updated list of available special characters: {list(set(self.special_chars) - set(omitted_chars))}")
        return omitted_chars

    def password_gen(self, pw_length, alphabet):
        """Generates a random password of given length using the characters in the specified alphabet"""
        return ''.join([secrets.choice(alphabet) for _ in range(pw_length)])

    def save_password(self, name, passwords):
        """
        Saves the generated passwords to a CSV file.

        Args:
            name (str): The name associated with the passwords.
            passwords (list): A list of generated passwords.

        Writes each password along with the associated name to a CSV file.
        The CSV file is opened in append mode, so the passwords are added to the existing file (if any).
        Each password and its associated name are written as a separate row in the CSV file, with a comma as the delimiter.
        """
        with open(self.csv_path, 'a', newline='') as file:
            password_writer = csv.writer(file, delimiter=',')
            for password in passwords:
                password_writer.writerow([name, password])


if __name__ == '__main__':

    # Entry point of the script.
    #
    # Creates an instance of the PasswordGenerator class and calls its main method.
    # This code block ensures that the main method is executed only when the script is run directly,
    # rather than being imported as a module.

    password_generator = PasswordGenerator()
    password_generator.main()
