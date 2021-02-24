# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import pandas as pd
import numpy as np
from flask import Flask, render_template, request

import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

# Reading the csv file from dropbox to dataframe
fields = ['customer_email', 'net_revenue', 'year']
colnames = ['customer_email', 'net_revenue', 'year']
df = pd.read_csv("https://www.dropbox.com/sh/dl/xhy2fzjdvg3ykhy/AADAVKH9tgD_dWh6TZtOd34ia?dl=1/casestudy.csv",
                 names=colnames, index_col=[0], encoding='latin1', header=2, low_memory=False)

# Checking for missing values and cleaning data
print(df.isnull().sum())
df = df.dropna()
print(df[df.isnull().any(axis=1)])
df['year'] = df['year'].astype(int)

# Yearly Total Revenue
total_rev = df.groupby(['year'])[['net_revenue']].sum()
print(total_rev)

# New Customer
df = (df.assign(Occurence=np.where(~df['customer_email'].duplicated(), 'New', 'Existing')))
new_customer = df[df['Occurence'] == 'New'].groupby('year')[['net_revenue']].sum()
print(new_customer)

# Existing Customer
existing_customer = df[df['Occurence'] == 'Existing'].groupby('year')[['net_revenue']].sum()
print(existing_customer)

# Customer Count
customer_count = df.groupby('year')[['customer_email']].nunique()

# ----- Flask app ---------

# Creating Flask app

app = Flask(__name__)


@app.route('/')
# @app.route('/customer_order')
# @app.route('/hello/<user>')
def customer_order():
    return render_template('index.html', total_revenue=total_rev.to_html(),
                           new_customer_revenue=new_customer.to_html(),
                           existing_customer_revenue=existing_customer.to_html())


if __name__ == "__main__":
    app.run(debug=True)
