
'''
Assignment 4 - Python For All Project

Our project will explore the ideas of web scraping, plotting data, and using a GUI 
framework in order to present our plots and graphs.

The data that will be analyzed in this project is the salary data of Python Developers
from each state, city, or country. Hopefully, this will inspire the high school students
to start exploring Python and what it can do.

Charles Cabauatan, Arjun Athian, and Tim Asher have contributed equally to this project.
'''


import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import matplotlib 
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt

import tkinter as tk
import tkinter.font as tkFont

def parse_column_title(data):
   column_titles = data.find_all('strong')
   titles = [title.text for title in column_titles]
   return titles

def write_to_csv(filename, titles, parsed_data):
   with open(filename, mode='w+') as file:
       data_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
       data_writer.writerow(titles)

       for row in parsed_data:
           data = row.find_all('td')
           data_row = [td.text.strip() for td in data]
           data_writer.writerow(data_row)

def scrape_data():
   url = 'https://www.daxx.com/blog/development-trends/python-developer-salary-usa#:~:text=contact%20us-,Average%20Python%20Developer%20Salary%20in%20the%20US%20and%20World%20in,Is%20Python%20Programming%20So%20Popular%3F&text=According%20to%20Indeed%2C%20the%20average,in%20the%20USA%20is%20%2488%2C492.'
   r = requests.get(url)

   soup = BeautifulSoup(r.content, 'html5lib') 
   web_content = soup.find(class_='col-sm-12 col-md-8')
   table_data = soup.find_all('tbody')

   # Average Python Developer Salary by State 2020
   salary_data_state = table_data[0]
   salary_titles = parse_column_title(salary_data_state)

   salary_data = salary_data_state.find_all('tr')
   salary_data = salary_data[1:]
   filename = 'average_salary_state.csv'
   write_to_csv(filename, salary_titles, salary_data)

   # Highest Paying Cities for Python Developers in the US
   cities_data = table_data[1]
   cities_titles = parse_column_title(cities_data)

   cities_salary_data = cities_data.find_all('tr')
   cities_salary_data = cities_salary_data[1:]
   filename = 'average_salary_cities.csv'
   write_to_csv(filename, cities_titles, cities_salary_data)

   # Average Python Developer Salary in the World
   world_data = table_data[2]
   world_titles = parse_column_title(world_data)

   world_salary_data = world_data.find_all('tr')
   world_salary_data = world_salary_data[1:]
   filename = 'average_salary_world.csv'
   write_to_csv(filename, world_titles, world_salary_data)

def plot_salary_state():
    # salary state
    data1 = pd.read_csv('average_salary_state.csv')

    salary_data = []
    for row in data1["Average Python salary 2020"]:
        row = row.replace(',', '')
        row = row.replace('$', '')
        row = int(row)
        salary_data.append(row)

    plt.style.use('ggplot')

    x=data1["State"]
    y=salary_data
    z=data1["Employees, users, and past/ present job ads"]

    x_pos = [i for i, _ in enumerate(x)]
    plt.bar(x_pos, y, color='blue')

    plt.xlabel("States")
    plt.ylabel("Salary in Dollars")
    plt.title("AVERAGE PYTHON SALARY 2020 By State")
    plt.xticks(x_pos, x, rotation="50")

    plt.savefig("state-salary.png")
    plt.show()

    fig = plt.figure()
    ax = fig.add_axes([0,0,3,2])
    ax.bar(x,z)

    ax.set_xlabel('STATE', fontsize=30, color='black') 
    ax.set_ylabel('JOB ADVERTISEMENTS', fontsize=30, color='black')

    plt.savefig("state-advertisements.png")

def plot_salary_cities():
    # salary cities
    data1 = pd.read_csv('average_salary_cities.csv')

    salary_data = []
    for row in data1["Average Salary 2020"]:
        row = row.replace(',', '')
        row = row.replace('$', '')
        row = int(row)
        salary_data.append(row)

    plt.style.use('ggplot')

    x=data1["City"]
    y=salary_data

    x_pos = [i for i, _ in enumerate(x)]
    plt.bar(x_pos, y, color='blue')

    plt.xlabel("Cities")
    plt.ylabel("Salary in Dollars")
    plt.title("AVERAGE PYTHON SALARY 2020 By City")
    plt.xticks(x_pos, x, rotation="50")

    plt.savefig("city-salary.png")
    plt.show()

def plot_salary_world():
    # salary world
    data1 = pd.read_csv('average_salary_world.csv')

    salary_data = []
    for row in data1["Python developer salary"]:
        row = row.replace(',', '')
        row = row.replace('$', '')
        row = int(row)
        salary_data.append(row)

    plt.style.use('ggplot')

    x=data1["Country"]
    y=salary_data

    x_pos = [i for i, _ in enumerate(x)]
    plt.bar(x_pos, y, color='blue')

    plt.xlabel("Country")
    plt.ylabel("Salary in Dollars")
    plt.title("AVERAGE PYTHON SALARY 2020 By Country")
    plt.xticks(x_pos, x, rotation="45")

    plt.savefig("country-salary.png")
    plt.show()
    

class SalaryApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('Salary App')
        container = tk.Frame(self)
        container.grid_propagate(False)
        container.pack(side="top", fill="both", expand=True)
        container.configure(width=400, height=450)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        frame = StartWindow(container, self)
        self.frames[StartWindow] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(StartWindow)


    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="#30475e")
        titleFont = tkFont.Font(family="Helvetica", size=28, weight="bold")
        title = tk.Label(self, text="Salary Checker", font=titleFont,
                         bg="#30475e", fg="#ececec")
        title.pack(pady=20, padx=10)

        buttonFont = tkFont.Font(family="Helvetica", size=16)
        stateButton = tk.Button(self, text="Salary By State", command=lambda: plot_salary_state(),
                                  width=15, height=2, font=buttonFont, bg="#ececec", highlightbackground="#c1a57b", highlightthickness=2)
        stateButton.pack(pady=20, padx=10)

        citiesButton = tk.Button(self, text="Salary By City", command=lambda: plot_salary_cities(),
                                  width=15, height=2, font=buttonFont, bg="#ececec", highlightbackground="#c1a57b", highlightthickness=2)
        citiesButton.pack(pady=20, padx=10)

        worldButton = tk.Button(self, text="Salary By Country", command=lambda: plot_salary_world(),
                                  width=15, height=2, font=buttonFont, bg="#ececec", highlightbackground="#c1a57b", highlightthickness=2)
        worldButton.pack(pady=20, padx=10)

        exitButton = tk.Button(self, text="Exit", command=lambda: self.quit(),
                                  width=15, height=2, font=buttonFont, bg="#ececec", highlightbackground="#c1a57b", highlightthickness=2)
        exitButton.pack(pady=20, padx=10)

scrape_data()
app = SalaryApp()
app.mainloop()