from matplotlib import pyplot as plt
import os; os.system('clear')
import pandas as pd
import numpy as np

folder = 'piloto_solo_monitor'
variables = ['CO2', 'ECG', 'INVP', 'PLETH']
window = 10

VALUES = {}
SAMPLE_RATE = []
DURATION = []
for variable in variables:
    file = os.path.join(folder, f"AS3ExportData{variable}.csv")

    data = pd.read_csv(file,skiprows =2 )

    time = data[data.columns[0]]
    values =data[data.columns[1]].tolist()
    
    # Stimate sample rate by the mode of the time
    sample_rate = time.groupby(time).count().mode()[0]
    print(f"{variable} Sample rate: {sample_rate}")

    new_values  =[]
    for v in values:
        if v != '-':
            new_values.append(np.float64(v))
        else:
            new_values.append(np.nan)
    values = new_values


    VALUES[variable] = new_values
    SAMPLE_RATE.append(sample_rate)
    DURATION.append(len(values)/sample_rate)


# Plot with slider in time, a window of  X seconds is shown 
# for each variable
fig, ax = plt.subplots(4,1, figsize=(10,10))
fig.subplots_adjust(bottom=0.25)
plt.subplots_adjust(hspace = 0.5)
plt.suptitle('Variables plot', fontsize=16)

for i, variable in enumerate(variables):
    ax[i].plot(np.linspace(0, window, SAMPLE_RATE[i]*window),VALUES[variable][:SAMPLE_RATE[i]*window])
    ax[i].set_title(variable)
    ax[i].set_ylabel('Amplitude')
    if i == len(variables)-1:
        ax[i].set_xlabel('Time (s)')
    ax[i].grid(True)

axcolor = 'lightgoldenrodyellow'
axtime = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
stime = plt.Slider(axtime, 'Time (s)', 0, np.mean(DURATION), valinit=0)

def update(val):
    p_time = stime.val
    for i, variable in enumerate(variables):
        ax[i].cla()
        ax[i].plot(np.linspace(p_time, p_time+window, SAMPLE_RATE[i]*window),VALUES[variable][int(p_time*SAMPLE_RATE[i]):int((p_time+window)*SAMPLE_RATE[i])])
        ax[i].set_title(variable)
        ax[i].set_ylabel('Amplitude')
        ax[i].set_xlabel('Time (s)')
        ax[i].grid(True)
    fig.canvas.draw_idle()


stime.on_changed(update)
plt.show()




