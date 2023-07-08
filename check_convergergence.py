import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

smb_folder = r'\\sbsabe01p033.file.core.windows.net\sbsabe01p033'
simulation_folder = os.path.join(smb_folder, 'simulations')

# Set monitor labels:
iteration_label = 'Iteration: Iteration'
Cz_label = 'Cz Monitor: Force Coefficient'
Cx_label = 'Cx Monitor: Force Coefficient'
Czf_label = 'Czf Monitor: Expression'
Czr_label = 'Czr Monitor: Expression'

mean_variance_mean_Cx_label = 'Mean_Variance_Mean_Cx Monitor: Statistics of Variance_Mean_Cx Monitor'
mean_variance_mean_Czf_label = 'Mean_Variance_Mean_Czf Monitor: Statistics of Variance_Mean_Czf Monitor'
mean_variance_mean_Czr_label = 'Mean_Variance_Mean_Czr Monitor: Statistics of Variance_Mean_Czr Monitor'

# Create a list of colours to be used by the plots:
colours = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']


group = 'Z01'
runs = ['001', '002', '003']
condition = 'FC-00-00-00-00-50'
convergence_threshold = 1E-6

# Loop through the simulations and check if they have converged:
group_folder = os.path.join(simulation_folder, group)

# Create a figure with 4 subplots 2x2:
fig, ax = plt.subplots(2, 2, figsize=(10, 10))

# Set the subplot titles as Cz, Cx, Czf and Czr:
ax[0, 0].set_title('Cz')
ax[0, 1].set_title('Cx')
ax[1, 0].set_title('Czf')
ax[1, 1].set_title('Czr')

counter = 0
for run in runs:
    print('Processing run: {}'.format(run))
    run_folder = os.path.join(group_folder, run)
    condition_folder = os.path.join(run_folder, condition)
    data_folder = os.path.join(condition_folder, 'Data')

    # if monitor.csv does not exists then create it:
    if not os.path.exists(os.path.join(condition_folder, 'monitors.csv')):
        # Load all the monitors in the data folder with the first column as index, then concatenate them into one dataframe:
        monitors = [os.path.join(data_folder, monitor) for monitor in os.listdir(data_folder) if monitor.endswith('.csv')]
        df = pd.concat([pd.read_csv(monitor, index_col=0) for monitor in monitors], axis=1)

        # save dataframe to csv:
        df.to_csv(os.path.join(condition_folder, 'monitors.csv'))

    # Load the monitors.csv into a dataframe:
    df = pd.read_csv(os.path.join(condition_folder, 'monitors.csv'))
    print(df.head())

    # Add the Cz, Cx, Czf and Czr as a function of iterations to the subplots, use the counter to select the colour:
    ax[0, 0].plot(df[iteration_label], df[Cz_label], label=run, color=colours[counter])
    ax[0, 1].plot(df[iteration_label], df[Cx_label], label=run, color=colours[counter])
    ax[1, 0].plot(df[iteration_label], df[Czf_label], label=run, color=colours[counter])
    ax[1, 1].plot(df[iteration_label], df[Czr_label], label=run, color=colours[counter])

    # Add a scatter point at the first iteration in which the mean variance mean of Cx, Czf and Czr is below the convergence threshold:
    # Get the index of the first iteration in which the mean variance mean of Cx, Czf and Czr is below the convergence threshold:
    try:
        convergence_index = df.index[(df[iteration_label] > 900) & (df[mean_variance_mean_Cx_label] < convergence_threshold)  & 
                                    (df[mean_variance_mean_Czf_label] < convergence_threshold) & (df[mean_variance_mean_Czr_label] < convergence_threshold)].tolist()[0]
        print('Convergence index: {}'.format(convergence_index))

        # Add a scatter point at the convergence index:
        ax[0, 0].scatter(df[iteration_label][convergence_index], df[Cz_label][convergence_index], color=colours[counter])
        ax[0, 1].scatter(df[iteration_label][convergence_index], df[Cx_label][convergence_index], color=colours[counter])
        ax[1, 0].scatter(df[iteration_label][convergence_index], df[Czf_label][convergence_index], color=colours[counter])
        ax[1, 1].scatter(df[iteration_label][convergence_index], df[Czr_label][convergence_index], color=colours[counter])
    except:
        print('No convergence index found for run {}'.format(run))


    counter += 1


# Set the x and y labels:
ax[0, 0].set_xlabel('Iteration')
ax[0, 1].set_xlabel('Iteration')
ax[1, 0].set_xlabel('Iteration')
ax[1, 1].set_xlabel('Iteration')
ax[0, 0].set_ylabel('Cz')
ax[0, 1].set_ylabel('Cx')
ax[1, 0].set_ylabel('Czf')
ax[1, 1].set_ylabel('Czr')

# Add a legend to the plots:
ax[0, 0].legend()
ax[0, 1].legend()
ax[1, 0].legend()
ax[1, 1].legend()

# Set the y limits to be +- 0.2 from the mean of the last iteration:
ax[0, 0].set_ylim([df[Cz_label].iloc[-1] - 0.2, df[Cz_label].iloc[-1] + 0.2])
ax[0, 1].set_ylim([df[Cx_label].iloc[-1] - 0.2, df[Cx_label].iloc[-1] + 0.2])
ax[1, 0].set_ylim([df[Czf_label].iloc[-1] - 0.2, df[Czf_label].iloc[-1] + 0.2])
ax[1, 1].set_ylim([df[Czr_label].iloc[-1] - 0.2, df[Czr_label].iloc[-1] + 0.2])


# Show the figure:
plt.show()

    



