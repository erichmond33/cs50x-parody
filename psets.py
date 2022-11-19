from cs50 import get_string
from sys import exit
import csv
from sys import exit
from sys import argv
from cs50 import SQL


def check_card(card_number):
    # Intitating the card number string
    #card_number = ""
    # ensuring the string is all numbers
    #while (card_number.isdigit() == False):
        #card_number = get_string("Number: ")
    if card_number == "":
        return ""

        # Checking luhn's algorithm
    if(luhns_algo(card_number) == False):
        return "INVALID"
        exit(0)

    # Checking the length
    if (len(card_number) == 13):
        # checking the first character
        if (card_number[0] == "4"):
            #print(card_number[0])
            return "VISA"
        else:
            return "INVALID"

    elif (len(card_number) == 15):
        # checking the first and second character
        if ((card_number[0] == "3") and ((card_number[1] == "4") or (card_number[1] == "7"))):
            return "AMEX"
            #print(card_number[0], card_number[1])
        else:
            return "INVALID"

    elif (len(card_number) == 16):
        # checking the first character
        if (card_number[0] == "4"):
            return "VISA"
            #print(card_number[0])
        # checking the first and second character
        elif ((card_number[0] == "5") and ((card_number[1] == "5") or (card_number[1] == "1") or (card_number[1] == "2") or (card_number[1] == "3") or (card_number[1] == "4"))):
            return "MASTERCARD"
            #print(card_number[0], card_number[1])
        else:
            return "INVALID"


    else:
        return "INVALID"
        exit(0)

    exit(1)


def luhns_algo(card_number):

    # useless vairbles to impliment the algo
    temp_var = 0
    temp_var2 = 0
    # The final varible to determine whether the card is legit
    final_var = 0

    # looping through the card numbers backwards by two and skipping the first number
    for i in range(len(card_number) - 2, -1, -2):
        # Multiplying each number by 2
        temp_var = int(card_number[i]) * 2
        # Adding each individual digit to final var
        if (temp_var > 9):
            for j in range(2):
                temp_var2 = str(temp_var)[j]
                final_var += int(temp_var2)

        else:
            final_var += temp_var
    # looping through the rest of the numbers
    for k in range(len(card_number) - 1, -1, -2):
        # Adding them to final var
        final_var += int(card_number[k])
    # Checking to see if the last digete of final var is 0
    if (final_var % 10 == 0):
        return True
    else:
        return False
    # END OF ALGO

''' readability '''

def check_grade(text):

    if text == "":
        return
    # User Input
    #text = get_string("Text: ")

    # Vairble to store letters
    nof_letters = 0
    # Vairble to store words
    nof_words = 1
    # Vairble to store sentences
    nof_sentences = 0

    # Determining the number of words, letters, and sentences
    for c in text:
        if (c.isalpha()):
            nof_letters += 1
        elif (c.isspace()):
            nof_words += 1
        elif ((c == ".") or (c == "!") or (c == "?")):
            nof_sentences += 1

    # Claculating L
    L = (nof_letters * 100) / nof_words
    # Calculating S
    S = (nof_sentences * 100) / nof_words
    # Getting the index
    Liau_Index = 0.0588 * L - 0.296 * S - 15.8

    # determining what the Liau Index is and giving the correct responses
    if (round(Liau_Index) < 1):
        return ("Before Grade 1")
    elif ((round(Liau_Index) >= 1) and (round(Liau_Index) < 16)):
        return (f"Grade {round(Liau_Index)}")
    else:
        return ("Grade 16+")

''' Dna '''


def dna(text):
    # Vairbles used for counting how many times a STR occurs back to back
    repeats = 0
    max_repeats = 0

    # Reading the DNA
    #with open(text, "r") as sequences:
    dna_string = str(text)#sequences.read()

    # Reading the csv into a dictionary
    with open("extras/large.csv", "r") as small:
        dict = csv.DictReader(small)

        # Making a copy of a single row to compare to the other rows later
        for row in dict:
            dict2 = row.copy()
        # Filling the copied row with garbage
        for x in range(0, len(dict.fieldnames)):
            dict2[dict.fieldnames[x]] = False

        # Looping through each STR
        for j in range(1, len(dict.fieldnames)):
            # Looping through the DNA
            for i in range(0, len(dna_string)):
                # Checking if the bit of DNA we are looking at currently is each to the current STR
                if dict.fieldnames[j] in dna_string[i:i + len(dict.fieldnames[j])]:
                    # Burner vairble... it is basically repeats but used in the recursive function
                    str_count = 0
                    # calling the recursive function to see how many times each found STR repeats back to back
                    repeats = str_check(dict.fieldnames, dna_string, j, i, str_count)
                    # Keeping track of with repeat is the highest
                    if (repeats > max_repeats):
                        max_repeats = repeats

            # Returns us to the top of the file so we can loop it again
            small.seek(0)
            # Checking to see if anyone's STR counts are equal to the max_repeats vairble
            for row in dict:
                if (row[dict.fieldnames[j]] == str(max_repeats)):
                    # if so then we need to update our copied row
                    dict2[dict.fieldnames[j]] = str(max_repeats)

            # Clearing the vairble
            max_repeats = 0

        # Comparing the STR values of every person to the STR values of the current DNA sequence
        return compare_dict(dict2, dict, small)


# Checks how many times a string repeats back to back
def str_check(fieldnames, dna_string, j, i, str_count):
    # Base: If it doesn't repeat stop
    if fieldnames[j] not in dna_string[i: i + len(fieldnames[j])]:
        return str_count
    # If the next bit of dna is equal to the current STR then add one to the count, and call itself again
    elif fieldnames[j] in dna_string[i: i + len(fieldnames[j])]:
        str_count += 1

        # Note that when this is called recursivly i is updated
        return str_check(fieldnames, dna_string, j, i + len(fieldnames[j]), str_count)


# This compares the STR values ONLY of the copied dictionary and all the real dictionary values
def compare_dict(dict2, dict, small):
    # This determines if all of the STRs are equal later in the code
    key = 0

    # GOing to the top of the file
    small.seek(0)
    # Looping the rows of the dictionary
    for row in dict:
        # Looping over each STR value
        for i in range(1, len(dict.fieldnames)):
            # If the current persons STR value is equal to the current STR vaule of the DNA sequence
            if (row[dict.fieldnames[i]] == dict2[dict.fieldnames[i]]):
                # Add 1 to key to note that one STR value is the same
                key += 1
        # After one person, check to see if the number of STR values that were correct is equal to the total number of STR values. If so then that is our guy
        if (key == len(dict.fieldnames) - 1):
            return(row['Name'])
            exit(0)

        # Clearing the key after each person
        key = 0

    return("No Match")
    exit(1)



def sort_roster(house):
    # Inserting the database
    db = SQL("sqlite:///extras///students.db")

    # Filtering the first, middle, last, and birth columns from the db
    dic = db.execute("SELECT first, middle, last, birth FROM students WHERE house = ? ORDER BY last, first", house)

    results = ''

    # Looping through the list of dictionaries dc.execute returned
    for field in dic:
        # Checking if the person has a middle name, and printing the right output accordingly
        if field['middle'] == None:
            results = results + (f"{field['first']} {field['last']}, born {field['birth']}\n")
        else:
            results = results + (f"{field['first']} {field['middle']} {field['last']}, born {field['birth']}\n")

    return results

''' Substitution '''

def substitute(key, text):

    ciphertext = ''
    abc = "abcdefghijklmnopqrstuvwxyz"

    if (len(key) != 26):
        return "ERROR: Your key isn't 26 characters"
        exit(1)
    elif (key.isalpha() == False):
        return "ERROR: Only use letters for the key"
        exit(1)
    elif check_repitition(key) == True:
        return "ERROR: No repeating letters in the key"
        exit(1)

    for i in range(len(text)):
        if text[i].isalpha() == False:
            ciphertext = ciphertext + text[i]
        for j in range(26):
            uppercase = text[i].isupper()
            if ord(text[i].lower()) == ord(abc[j]):
                if uppercase == False:
                    ciphertext = ciphertext + key[j].lower()
                    break
                elif uppercase == True:
                    ciphertext = ciphertext + key[j].upper()
                    break
    return f"CIPHERTEXT: {ciphertext}"


def check_repitition(key):

    for i in range(len(key)):
        for j in range(i):
            if (ord(key[i]) == ord(key[j])) or (ord(key[i]) == (ord(key[j]) + 32)) or (ord(key[i]) == (ord(key[j]) - 32)):
                return True

    return False
