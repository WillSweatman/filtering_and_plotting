# filter and plot

this program opens a file (typically csv), scans for data and datatypes.

it then allows you to select the columns by their headers, and plot them against each other, with a z variable for colour.

you can then choose filters to apply. because the filters are automatically appplied by looking at the data, you are limited to certain types (e.g. > and < are not valid for strings).

once these filters have been applied and added to the treeview list, you can plot again to see the affect they have had.

a good test case is plotting latitude, longitude, capacity (as z/colour), and clicking plot. this resulting plot will not be very clear as the points are clumped into two distant groups. however, by adding a filter for latitude > 20, and plotting, we get a plot of new york.