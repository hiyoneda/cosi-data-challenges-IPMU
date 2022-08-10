# Imports:
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as colors

# Upload data:
df = pd.read_csv("extracted_image.dat",delim_whitespace=True)

x = df["Phi_center[deg]"]
y = df["Theta_center[deg]"]
z = df["Intensity[a.u.]"]

# Binning for all-sky map, in Galactic coordinates.
# This needs to match the mimrec output.
x_range = np.arange(-179.5,179.5,1)
y_range = np.arange(-89.5,90.5,1)

# Convert z data into array:
array_list = []
for each in x_range:
    this_column_index = x == each
    this_column = z[this_column_index]
    array_list.append(this_column)
array_list = np.array(array_list)

# Setup figure:
fig = plt.figure(figsize=(12,6))
ax = plt.gca()

# Plot:
img = ax.pcolormesh(np.flip(x_range),y_range,array_list.T,cmap="cubehelix",vmin=0,vmax=0.1)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)

# Overlay sources:
crab={"l":184.56,"b":-5.78}
cenA={"l":309.516,"b":19.417}
cygX1={"l":71.33496,"b":3.066917}
vela={"l":263.552,"b":-2.787}

plot_list = [crab,cenA,cygX1,vela]

for each in plot_list:
    this_l = each["l"]
    this_b = each["b"]
    if this_l > 180:
        this_l = this_l - 360
    plt.plot(this_l,this_b,color="red",ms=7,marker="+")

cbar = plt.colorbar(img,fraction=0.045)
cbar.set_label("Intensity [a.u.]",size=16,labelpad=12)
cbar.ax.tick_params(labelsize=12)

plt.ylabel('Galactic Latitude [$\circ$]',fontsize=18)
plt.xlabel('Galactic Longitude [$\circ$]',fontsize=18)
plt.title('Data Challenge 1 (preliminary)', fontsize=18)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)

ax.tick_params(axis='both',which='major',length=9)
ax.tick_params(axis='both',which='minor',length=5)

plt.grid(lw=1,ls="--",color="grey",alpha=0.3)
plt.xlim(179.5,-179.5)

plt.savefig("sim_image.png",bbox_inches='tight')
plt.show()
