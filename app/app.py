import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
import csv
from cs50 import SQL
import subprocess
import binascii
import time

from psets import check_card, luhns_algo, check_grade, dna, compare_dict, sort_roster, substitute, check_repitition

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
#app.jinja_env.filters["usd"] = usd

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///extras///database.db")



@app.route("/")
def index():

    return render_template("parody_index.html")

''' PEOPLE '''

@app.route("/malan", methods=["GET", "POST"])
def malan():

        return render_template("people/malan.html")

@app.route("/richmond", methods=["GET", "POST"])
def richmond():

        return render_template("people/richmond.html")

@app.route("/lloyd", methods=["GET", "POST"])
def lloyd():

        return render_template("people/lloyd.html")

@app.route("/yu", methods=["GET", "POST"])
def yu():

        return render_template("people/yu.html")




''' STAFF/SYLLABUS/FAQs/COMMUNITIES '''

@app.route("/staff", methods=["GET", "POST"])
def staff():

        return render_template("others/staff.html")

@app.route("/syllabus", methods=["GET", "POST"])
def syllabus():

        return render_template("others/syllabus.html")

@app.route("/faqs", methods=["GET", "POST"])
def faqs():

        return render_template("others/faqs.html")

@app.route("/communities", methods=["GET", "POST"])
def communities():

        return render_template("others/communities.html")

@app.route("/cult", methods=["GET", "POST"])
def cult():

        return render_template("others/cult.html")



''' Final Project '''

@app.route("/final_project", methods=["GET", "POST"])
def final_project():

        return render_template("final_project/final_project.html")



''' WEEK ZERO '''

@app.route("/week_zero", methods=["GET", "POST"])
def week_zero():

        return render_template("week_zero/week_zero.html")

@app.route("/scratch", methods=["GET", "POST"])
def scratch():

    if request.method == "POST":

        return render_template("week_zero/scratch.html")

    else:

        return render_template("week_zero/scratch.html")



''' WEEK ONE '''

@app.route("/week_one", methods=["GET", "POST"])
def week_one():

    return render_template("week_one/week_one.html")

@app.route("/hello", methods=["GET", "POST"])
def hello():

    if request.method == "POST":
        ''' Hello '''
        # Name from the user
        if request.form.get("name") == None:
            hello = ""
        else:
            name = request.form.get("name")
            # Replying to user
            hello = f"Hello, {name}"

        return render_template("week_one/hello.html", hello=hello)
    else:
        return render_template("week_one/hello.html")

@app.route("/mario", methods=["GET", "POST"])
def mario():

    if request.method == "POST":
        ''' Mario '''
        # List for each row of the pyrimid
        rows = []
        strings= ''
        # Height from user
        if request.form.get("height") == None:
            height = 0
        else:
            height = int(request.form.get("height"))
        # A loop to make the rows
        for i in range(1, height + 1):
            string = "\n\n"
            string = " " * (height - i)
            string = string + ("#" * i)
            string = string + ("  ")
            string = string + ("#" * i)
            string = string + (" " * (height - i))
            strings = strings + (string + "\n")
            rows.append(string)

        return render_template("week_one/mario.html", rows=rows, strings=strings)
    else:
        return render_template("week_one/mario.html")

@app.route("/credit", methods=["GET", "POST"])
def credit():

    if request.method == "POST":
        ''' Credit '''
        # Ensuring at least one field was filled out
        if (request.form.get('card_num_select') == "Choose a card number") and (request.form.get('card_num') == ""):
            card_num = ""
            card_check = ""
        # If both were filled out use card select
        elif request.form.get('card_num_select') != "Choose a card number":
            card_num = request.form.get('card_num_select')
            card_check = check_card(card_num)
        # If only card type was filled out use it
        else:
            card_num = request.form.get('card_num')

            # Transforming the users input if they use - or " "
            card_num = card_num.replace(" ", "")
            card_num = card_num.replace("-", "")

            # Make sure the input is only numbers
            if card_num.isdigit() == False:
                card_num = ''
                card_check = "Numbers only..."
            else:
                card_check = check_card(card_num)

        return render_template("week_one/credit.html", card_num=card_num, card_check=card_check)
    else:
        return render_template("week_one/credit.html")



''' WEEK TWO '''

@app.route("/week_two")
def week_two():

    return render_template("week_two/week_two.html")

@app.route("/readability", methods=["GET", "POST"])
def readability():

    if request.method == "POST":

        ''' Readability '''
        # Ensuring at least one field was filled out
        if (request.form.get('v1') == "Choose a text") and (request.form.get('v2') == ""):
            input = ""
            output = ""
        # If both were filled out use card select
        elif request.form.get('v2') != "Choose a text":
            input = request.form.get('v2')
            output = check_grade(input)
        # If only card type was filled out use it
        else:
            input = request.form.get('v1')
            output = check_grade(input)


        return render_template("week_two/readability.html", input=input, output=output)
    else:

        return render_template("week_two/readability.html")

@app.route("/substitution", methods=["GET", "POST"])
def substitution():

    if request.method == "POST":

        input2 = ""

        ''' Substitution '''
        # Ensuring at least one field was filled out
        if (request.form.get('v1') == "") and (request.form.get('v2') == "Choose a key"):
            input = ""
            output = "ERROR: You need a key"
        # making sure a text was filled out
        elif (request.form.get("v3") == "") and (request.form.get('v2') != "Choose a key"):
            input = request.form.get("v2")
            output = "ERROR: Type a sentence"
        elif (request.form.get("v3") == "") and (request.form.get('v1') != ""):
            input = request.form.get("v1")
            output = "ERROR: Type a sentence"
        # if a form was selected
        elif (request.form.get("v3") != "") and (request.form.get('v2') != "Choose a key"):
            input = request.form.get('v2')
            input2 = request.form.get('v3')
            output = substitute(input, input2)
            input2 = f"PLAINTEXT: {request.form.get('v3')}"
        # if the form was typed
        elif (request.form.get("v3") != "") and (request.form.get('v1') != ""):
            input = request.form.get('v1')
            input2 = request.form.get('v3')
            output = substitute(input, input2)
            input2 = f"PLAINTEXT: {request.form.get('v3')}"


        return render_template("week_two/substitution.html", input=input, input2=input2, output=output)
    else:

        return render_template("week_two/substitution.html")



''' WEEK THREE '''

@app.route("/week_three")
def week_three():

    return render_template("week_three/week_three.html")

@app.route("/plurality", methods=["GET", "POST"])
def plurality():

    if request.method == "POST":

        ''' Plurality '''
        input = int(request.form.get("v1"))
        input2 = int(request.form.get("v2"))

        #List of candidates
        candidates = ["Alice", "Bob", "Charlie", "Frank", "David"]

        return render_template("week_three/plurality2.html", input=input, input2=input2, candidates=candidates, nof_candidates=len(candidates))
    else:

        return render_template("week_three/plurality.html")

@app.route("/plurality2", methods=["GET", "POST"])
def plurality2():


    # List of candidates
    candidates = ["Alice", "Bob", "Charlie", "Frank", "David", ""]

    if request.method == "POST":

        ''' Plurality2 '''
        input = int(request.form.get("v1"))
        input2 = int(request.form.get("v2"))

        # Gathering votes
        votes = ["", "", "", "", "", "", "", "", "", ""]
        for i in range(input2):
            votes[i] = str(request.form.get(f"{i + 3}"))

        # Converting votes into a string to display
        string_votes = ''
        for vote in votes:
            if vote != "":
                string_votes = string_votes + vote + "\n"

        # Calculating c_indexes
        c_indexes = [0, 1, 2, 3 ,4]
        for j in range(5):
            if c_indexes[j] >= input:
                c_indexes[j] = 5

        # RUnning the c script
        run_c =  subprocess.Popen("./plurality " + str(input) + " " + str(input2) + " " + candidates[c_indexes[0]] + " " + candidates[c_indexes[1]] + " " + candidates[c_indexes[2]] + " " + candidates[c_indexes[3]] + " " + candidates[c_indexes[4]] +  " " + votes[0] +  " " + votes[1] +  " " + votes[2] +  " " + votes[3] +  " " + votes[4] +  " " + votes[5] +  " " + votes[6] +  " " + votes[7] +  " " + votes[8] +  " " + votes[9], shell=True, stdout=subprocess.PIPE).stdout
        return_c =  run_c.read()

        output = return_c.decode()
        output = "Winner(s): " + output

        return render_template("week_three/plurality2.html", input=input, output=output, input2=input2, candidates=candidates, c_indexes=c_indexes, votes=votes, string_votes=string_votes)
    else:

        return render_template("week_three/plurality2.html", candidates=candidates, c_indexes=c_indexes, votes=votes)


@app.route("/tideman", methods=["GET", "POST"])
def tideman():

    if request.method == "POST":

        ''' Tideman '''
        input = int(request.form.get("v1"))
        input2 = int(request.form.get("v2"))

        #List of candidates
        candidates = ["Alice", "Bob", "Charlie", "Frank", "David"]
        candidates_tideman = ["Alice  ", "Bob    ", "Charlie", "Frank  ", "David  "]

        return render_template("week_three/tideman2.html", input=input, input2=input2, candidates=candidates, candidates_tideman=candidates_tideman, len=len(candidates))
    else:

        return render_template("week_three/tideman.html")


@app.route("/tideman2", methods=["GET", "POST"])
def tideman2():


    # List of candidates
    candidates = ["Alice", "Bob", "Charlie", "Frank", "David", ""]

    if request.method == "POST":

        ''' Tideman2 '''
        input = int(request.form.get("v1"))
        input2 = int(request.form.get("v2"))

        # Gathering votes
        votes = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
        for i in range(input2 * input):
            votes[i] = str(request.form.get(f"{i + 3}"))

        # Converting votes into a string to display
        string_votes = ''
        for h in range(0, 51):
            if h == 0:
                string_votes = "VOTER 1\n"

            if votes[h] == "":
                break
            elif int(h + 1) % input == 1:
                string_votes = string_votes + "Rank 1: " + votes[h ] + "\n"
            elif int(h + 1) % input == 2:
                string_votes = string_votes + "Rank 2: " + votes[h ] + "\n"
            elif int(h + 1) % input == 3:
                string_votes = string_votes + "Rank 3: " + votes[h ] + "\n"
            elif int(h + 1) % input == 4:
                string_votes = string_votes + "Rank 4: " + votes[h ] + "\n"
            elif int(h + 1) % input == 0:
                if (votes[h + 1] == ""):
                    string_votes = string_votes + "Rank " + str(input) + ": " + votes[h ]
                else:
                    string_votes = string_votes + "Rank " + str(input) + ": " + votes[h ] + "\n" + "VOTER " + str(int((h +1) / input) + 1) + "\n"

        # Calculating c_indexes
        c_indexes = [0, 1, 2, 3 ,4]
        for j in range(5):
            if c_indexes[j] >= input:
                c_indexes[j] = 5

        # RUnning the c script
        run_c =  subprocess.Popen("./tideman " + str(input) + " " + str(input2) + " " + candidates[c_indexes[0]] + " " + candidates[c_indexes[1]] + " " + candidates[c_indexes[2]] + " " + candidates[c_indexes[3]] + " " + candidates[c_indexes[4]] +  " " + votes[0] +  " " + votes[1] +  " " + votes[2] +  " " + votes[3] +  " " + votes[4] +  " " + votes[5] +  " " + votes[6] +  " " + votes[7] +  " " + votes[8] +  " " + votes[9] +  " " + votes[10]
        +  " " + votes[11] +  " " + votes[12] +  " " + votes[13] +  " " + votes[14] +  " " + votes[15] +  " " + votes[16] +  " " + votes[17] +  " " + votes[18] +  " " + votes[19]
        +  " " + votes[20] +  " " + votes[21] +  " " + votes[22] +  " " + votes[23] +  " " + votes[24] +  " " + votes[25] +  " " + votes[26] +  " " + votes[27] +  " " + votes[28] +  " " + votes[29]
        +  " " + votes[30] +  " " + votes[31] +  " " + votes[32] +  " " + votes[33] +  " " + votes[34] +  " " + votes[35] +  " " + votes[36] +  " " + votes[37] +  " " + votes[38] +  " " + votes[39]
        +  " " + votes[40] +  " " + votes[41] +  " " + votes[42] +  " " + votes[43] +  " " + votes[44] +  " " + votes[45] +  " " + votes[46] +  " " + votes[47] +  " " + votes[48] +  " " + votes[49], shell=True, stdout=subprocess.PIPE).stdout

        return_c =  run_c.read()

        output = return_c.decode()
        output = "Winner(s): " + output

        return render_template("week_three/tideman2.html", input=input, output=output, input2=input2, candidates=candidates, c_indexes=c_indexes, votes=votes, string_votes=string_votes)
    else:

        return render_template("week_three/tideman2.html", candidates=candidates, c_indexes=c_indexes, votes=votes)




''' WEEK FOUR '''

@app.route("/week_four")
def week_four():

    return render_template("week_four/week_four.html")

@app.route("/filter", methods=["GET", "POST"])
def filter():

    if request.method == "POST":

        ''' Filter '''
        input = request.form.get("v1")
        input2 = request.form.get("v2")

        # RUnning the c script
        run_c =  subprocess.Popen("./filterrr" + input + input2 + "static/out.bmp", shell=True, stdout=subprocess.PIPE).stdout
        # run_c = subprocess.run("./filter.c" + input + input2 + "static/out.bmp", shell=True)
        return_c =  run_c.read()

        output = return_c.decode()

        # Getting the regular image
        out = "static/out.bmp"
        regular = str(input2)

        return render_template("week_four/filter.html", input=input, input2=input2, output=output, regular=regular, out=out)
    else:

        return render_template("week_four/filter.html")

@app.route("/recover", methods=["GET", "POST"])
def recover():

    # Open in binary mode (so you don't read two byte line endings on Windows as one byte)
    # and use with statement (always do this to avoid leaked file descriptors, unflushed files)
    with open('extras/card.raw', 'rb') as f:
        # Slurp the whole file and efficiently convert it to hex all at once
        hexdata = (f.read()).hex()

    hexdata = hexdata[:30000]

    # Getting the pics and names and ids too
    pics = []
    names = []
    id_names = []
    jpgs = []
    for i in range(0, 50):
        if i < 10:
            pics.append("static/00" + str(i) + ".jpg")
            jpgs.append("00" + str(i) + ".jpg")
        else:
            pics.append("static/0" + str(i) + ".jpg")
            jpgs.append("0" + str(i) + ".jpg")

        names.append("j" * (i + 1))
        id_names.append("#" + "j" * (i + 1))

    if request.method == "POST":

        ''' Recover '''

        return render_template("week_four/recover.html",  hexdata=hexdata, pics=pics, names=names, id_names=id_names, jpgs=jpgs, header="Found \"50\" Images", len=50, len2=0 )
    else:

        return render_template("week_four/recover.html", hexdata=hexdata, pics="", names="", id_names="", jpgs="", header = "Lost Images File", len=0, len2=1)



''' WEEK FIVE '''

@app.route("/week_five")
def week_five():

    return render_template("week_five/week_five.html")


@app.route("/speller", methods=["GET", "POST"])
def speller():

     # Open in binary mode (so you don't read two byte line endings on Windows as one byte)
    # and use with statement (always do this to avoid leaked file descriptors, unflushed files)
    with open('extras/large', 'rb') as f:
        # Slurp the whole file and efficiently convert it to hex all at once
        dicdata = str(f.read())
    dicdata = str(dicdata[2:-1])
    dicdata = dicdata.replace("\\n", " ")

    if request.method == "POST":

        ''' Speller '''
        input = request.form.get("v1")
        input2 = request.form.get("v2")

        # RUnning the c script
        run_c =  subprocess.Popen("./speller extras/large texts/" + input2, shell=True, stdout=subprocess.PIPE).stdout
        return_c =  run_c.read()

        output = return_c.decode()
        summary = output[-237:-1]

        # Getting the regular image
        out = "static/out.bmp"
        regular = str(input2)

        return render_template("week_five/speller.html", input=input, input2=input2, output=output, regular=regular, out=out, summary=summary, dicdata=dicdata, len=1, len2= 1)
    else:

        return render_template("week_five/speller.html", len=0, len2=1, dicdata=str(dicdata))



''' WEEK SIX '''

@app.route("/week_six")
def week_six():

    return render_template("week_six/week_six.html")

@app.route("/dna", methods=["GET", "POST"])
def read_dna():

    if request.method == "POST":

        # Ensuring at least one field was filled out
        if (request.form.get('v1') == "Choose a sequence"):
            input = ""
            output = ""
        # If only card type was filled out use it
        else:
            input = request.form.get('v1')
            output = dna(input)

        return render_template("week_six/dna.html", input=input, output=output)

    else:

        return render_template("week_six/dna.html")



''' WEEK SEVEN '''

@app.route("/week_seven")
def week_seven():

    return render_template("week_seven/week_seven.html")

@app.route("/movies", methods=["GET", "POST"])
def movies():

    if request.method == "POST":

         # Ensuring at least one field was filled out
        if (request.form.get('v2') == "Choose a query"):
            input = ""
            output = ""
        # If only card type was filled out use it
        else:


            ''' Processing the users input '''

            input = request.form.get('v2')
            output = db.execute(f"{input}")

            # Lists to hold the return values
            columns = ""
            rows = []

            # Get the colums
            columns = list(output[0].keys())

            # get rows
            for dic in output:
                rows.append(list(dic.values()))

        return render_template("week_seven/movies.html", input=input, columns=columns, rows=rows, len=len(rows))

    else:

        return render_template("week_seven/movies.html", len=0)


@app.route("/houses", methods=["GET", "POST"])
def houses():

    if request.method == "POST":

         # Ensuring at least one field was filled out
        if (request.form.get('v2') == "Choose a query"):
            input = ""
            output = ""
        # If only card type was filled out use it
        else:


            ''' Processing the users input '''

            input = request.form.get('v2')
            output = sort_roster(input)

        return render_template("week_seven/houses.html", input=input, output=output)

    else:

        return render_template("week_seven/houses.html")



''' WEEK EIGHT '''

@app.route("/week_eight")
def week_eight():

    return render_template("week_eight/week_eight.html")

@app.route("/homepage")
def homepage():

    return render_template("week_eight/index.html")

@app.route("/movies_blog")
def movies_blog():

    return render_template("week_eight/movies.html")

@app.route("/books_blog")
def books_blog():

    return render_template("week_eight/books.html")

@app.route("/quotes_blog")
def quotes_blog():

    return render_template("week_eight/quotes.html")