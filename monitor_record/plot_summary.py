import os; os.system('clear')
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np


folder = 'piloto_solo_monitor'


data  = pd.read_csv(os.path.join(folder, 'AS3ExportData.csv'),skiprows =2 )

# Convert the 'Date' column to datetime
data['Date'] = pd.to_datetime(data['Date'])

# Set the first date as the reference
reference_date = data['Date'].iloc[0]

# Calculate the difference in seconds
data['Seconds'] = (data['Date'] - reference_date).dt.total_seconds()




# Plot only non cero data
VARIABLES = {}
for column in data.columns:

    if column.strip() == 'BIS SQI' or column.strip() == 'Seconds':
        continue

    if column != 'Date' and column != 'Time':
        values = data[column].tolist()

        if len(set(values)) <= 2:
            continue
        

        new_values = []
        for v in values:
            if v == '-':
                new_values.append(np.nan)
            else:
                new_values.append(np.float64(v))

        values = new_values
        VARIABLES[column] = values



# Plot with slider in time, a window of  X seconds is shown
# for each variable
fig, ax = plt.subplots(len(VARIABLES),1, figsize=(10,10))

plt.suptitle('Variables plot', fontsize=16)

for i, variable in enumerate(VARIABLES):
    ax[i].plot(data['Seconds'], VARIABLES[variable])
    ax[i].set_ylabel(variable)
    # remove ticks
    if i == len(VARIABLES)-1:
        ax[i].set_xlabel('Time (s)')
    else:
        ax[i].set_xticks([])
    #ax[i].grid(True)

plt.show()

        

