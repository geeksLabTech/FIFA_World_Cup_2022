import pandas as pd
import json
# load json file to dictionary
with open('resuts1.json') as f:
    data = json.load(f)

df = pd.DataFrame(columns=["Team","1st Group","2nd Group","8th Finals","4th Finals","Semi Finals", "Final", "Winner", "Third"])

# add new line to dataframe
for key in data:
    newline = [key] 
    newline.append(data[key]["1st Group"])   
    newline.append(data[key]["2nd Group"])
    newline.append(data[key]["8th Finals"])
    newline.append(data[key]["4th Finals"])
    newline.append(data[key]["Semi Finals"])
    newline.append(data[key]["Final"])
    newline.append(data[key]["Winner"])
    newline.append(data[key]["Third"])
    
    # append newlinw to dataframe
    df.loc[len(df)] = newline

df.to_csv("results1.csv", index=False)