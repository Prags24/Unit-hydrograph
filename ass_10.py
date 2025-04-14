#import all the libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#time values
t_DRH = np.arange(0.5, 8.5, 0.5)
#Given Drh ordinates
DRH = np.array([12, 22.5, 33, 42, 42, 35, 28.5, 27, 29, 26.5,20, 13, 7.5, 5, 3, 1 ])
#rvolume= sum(DRH ordinates) *time
runoff_volume= np.sum(DRH) *0.5*3600
t_ERH= 0.5
ERH_rate = np.array([2.5,6,8.5,0,4.5,1])  # excess rainfall rates
ERH = ERH_rate * t_ERH                    # excess rainfall
effective_rainfall_m = np.sum(ERH)     
catchment_area = (runoff_volume/ effective_rainfall_m)  #area*excess rainfall=volume

#print the values
print(f"Total Runoff Volume: {runoff_volume:.2f} m³")
#total catchment area
print(f"Catchment Area: {catchment_area*1e-3:.2f} km²")

# Define n and m
n = len(DRH)  # Total DRH points
m = len(ERH)  # Total ERH points
rows = n # Number of rows in matrix P
col=n-m+1 ## Number of column in matrix P

#precipitation matrix
P = np.zeros((rows,col))
for i in range(col):
    P[i:i+m, i] = ERH  # Shifting ERH downward per column

#showing the matrix of P
df_P = pd.DataFrame(P, columns=[f"R {i+1}" for i in range(col)])
print("Corrected P Matrix:")
print(df_P)

U = np.linalg.lstsq(P, DRH, rcond=None)[0]  # (P^T P)^-1 P^T Q

#Print the computed Unit Hydrograph
print("Unit Hydrograph Ordinates (m³/sec per mm):")

U = np.insert(U, 0, 0)
U=np.insert(U,len(U),0)
t_u=np.arange(0,6.5,0.5)

#plot the graph for UH

plt.plot(t_u,U,'o-', label='30 min UH')
plt.xlabel('Time (hours)')
plt.ylabel('Flow (m³/s/mm)')
plt.grid()
plt.legend()
plt.tight_layout()
plt.show()

#Interolation of UH to get 15 min UH

UH_15min = np.zeros(2*len(U)-1)
UH_15min[0::2] = U
UH_15min[1::2] = (U[:-1] + U[1:]) / 2
UH_15min= np.append(UH_15min, [0,0,0,0,0,0,0,0,0])
t_UH_15min = np.arange(0, len(UH_15min) * 0.25, 0.25)
print(UH_15min)

#Scurve 
S_curve = np.cumsum(UH_15min) * 0.25
print("S curve values")
print(S_curve)

#75 min UH calculation
S_shifted_75 = np.zeros_like(S_curve)
S_shifted_75[5:] = S_curve[:-5]  # Lag by 3 steps
UH_75min = (S_curve- S_shifted_75 ) / (75/60)  
#to avoid negative values
UH_75min[UH_75min < 0] = 0 
#time duration for plotting
t_UH_75 = np.arange(0, len(UH_75min) * 0.25, 0.25)
#print the values
print()

plt.plot(t_UH_75, UH_75min, 'o-', label="75-min UH", color="green")
plt.xlabel("Time (hours)")
plt.ylabel("Flow (m³/s/mm)")
plt.grid()
plt.legend()
plt.tight_layout()
plt.show()

# Create DataFrame for 15-min and 75-min results
df_result_15_75 = pd.DataFrame({
    "Time (hours)": t_UH_15min,
    "UH (15-min)": UH_15min,
    "S-curve (15-min)": S_curve[:34],
    "Lagged S-curve (75-min)": S_shifted_75,
    "UH (75-min)": UH_75min
})

print("\nFinal Data Table (15-min and 75-min UH):")
print(df_result_15_75.head)

# Compute S-curve from original 30-min UH
S_curve_30min = np.cumsum(U) * 0.5  # 30-min time step

# Shift S-curve by 90 minutes (3 time steps of 30 min)
S_shifted_90_30min = np.zeros_like(S_curve_30min)
S_shifted_90_30min[3:] = S_curve_30min[:-3]  

# Compute 90-minute Unit Hydrograph
UH_90min_from_30min = (S_curve_30min - S_shifted_90_30min) / 1.5  # Divide by (90/60)

# Ensure no negative values
UH_90min_from_30min[UH_90min_from_30min < 0] = 0  
UH_90min_from_30min=np.append(UH_90min_from_30min,0)
# Time array for 90-minute UH
t_UH_90_from_30min = np.arange(0, len(UH_90min_from_30min) * 0.5, 0.5)  # 30-min intervals

# plot results

plt.plot(t_UH_90_from_30min, UH_90min_from_30min, marker="o", linestyle="--", label="90-min UH ", color="purple")
plt.xlabel("Time (hours)")
plt.ylabel("Flow (m³/s/mm)")
plt.grid()
plt.legend()
plt.tight_layout()
plt.show()

# Create a DataFrame with all values
df_result = pd.DataFrame({
    "Time (hours)": t_u,
    "UH (30-min)": U,
    "S-curve (30-min)": S_curve_30min,
    "Lagged S curve": S_shifted_90_30min,
    "UH (90-min)": UH_90min_from_30min[:len(t_u)]
})

# Print the DataFrame
print("\nFinal Data Table:")
print(df_result)











