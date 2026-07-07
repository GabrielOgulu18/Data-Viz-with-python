# import the neccesary libraries
import piplite
await piplite.install(['nbformat', 'plotly'])

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Then we read the airline data into pandas dataframe
from js import fetch
import io

URL = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv'
resp = await fetch(URL)
text = io.BytesIO((await resp.arrayBuffer()).to_py())

airline_data =  pd.read_csv(text,
                            encoding = "ISO-8859-1",
                            dtype={'Div1Airport': str, 'Div1TailNum': str, 
                                   'Div2Airport': str, 'Div2TailNum': str})

print('Data downloaded and read into a dataframe!')

# Preview the first 5 lines of the loaded data 
airline_data.head()

# Shape of the data
airline_data.shape

# Randomly sample 500 data points. Setting the random state to be 42 so that we get same result.
data = airline_data.sample(n=500, random_state=42)

# Get the shape of the trimmed data
data.shape


# we can visually see changes of how the Departure time changes with respect to airport distance with the help of a SCATTERPLOT.
#First we can create an empty figure ising go.Figure()
fig=go.Figure()

fig.add_trace(go.Scatter(x=data['Distance'], y=data['DepTime'], mode='markers', marker=dict(color='red')))
fig.update_layout(title='Distance vs Departure Time', xaxis_title='Distance', yaxis_title='DepTime')

# Display the figure
fig.show()

# we can use a Line plot to see the average monthly arrival delay time and see how it changes over the year by; 

# Group the data by Month and compute average over arrival delay time.
line_data = data.groupby('Month')['ArrDelay'].mean().reset_index()
# Display the data
line_data

##Next we will create a line plot by using the add_trace function and use the go.scatter() function within it
# In go.Scatter we define the x-axis data,y-axis data and define the mode as lines with color of the marker as green
fig.add_trace(go.Scatter(x=line_data['Month'], y=line_data['ArrDelay'], mode='lines', marker=dict(color='green')))

# Create line plot
## Here we update these values under function attributes such as title,xaxis_title and yaxis_title
fig.update_layout(title='Month vs Average Flight Delay Time', xaxis_title='Month', yaxis_title='ArrDelay')
fig.show()

# we can use a bar chart to extract number of flights from a specific airline that goes to a destination by;

# Group the data by destination state and reporting airline. Compute total number of flights in each combination
bar_data = data.groupby('DestState')['Flights'].sum().reset_index()

bar_data

fig = px.bar(bar_data, x="DestState", y="Flights", title='Total number of flights to the destination state split by reporting airline') 
fig.show()

# we can see the distribution of arrival delay using a histogram by;
# set missing values to zero first
data['ArrDelay'] = data['ArrDelay'].fillna(0)
fig = px.histogram(data, x="ArrDelay",title="Total number of flights to the destination state split by reporting air.")
fig.show()

# we can use a bubble plot to represent number of flights as per reporting airline by;

bub_data = data.groupby('Reporting_Airline')['Flights'].sum().reset_index()
bub_data

fig = px.scatter(bub_data, x="Reporting_Airline", y="Flights", size="Flights",
                 hover_name="Reporting_Airline", title='Reporting Airline vs Number of Flights', size_max=60)
fig.show()

# we can represent the proportion of Flights by Distance Group (Flights indicated by numbers)

fig = px.pie(data, values='Flights', names='DistanceGroup', title='Flight propotion by Distance Group')
fig.show()

# we can represent the hierarchical view in othe order of month and destination state holding value of number of flights by using SunBurst Charts

fig = px.sunburst(data, path=['Month', 'DestStateName'], values='Flights',title='Flight Distribution Hierarchy')
fig.show()

