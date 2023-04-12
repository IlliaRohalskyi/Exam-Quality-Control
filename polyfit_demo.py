import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import main

# Get the exam plan
df = main.split_date(main.read_data())
anzahl=df['Anzahl'].to_numpy()
start_date=df['start_date'].to_numpy()

anzahl_sorted=sorted(anzahl,reverse=True)
anzahl_mean = np.mean(anzahl)

# Assing a float value to the date
x = mdates.date2num(start_date)
y = anzahl_sorted

# Perform polynomial regression
degree = 3 # degree of the polynomial
coeffs = np.polyfit(x, y, degree)
p = np.poly1d(coeffs)

# Generate predicted y values
x_fit = np.linspace(x[0], x[-1], len(x))
y_fit = p(x_fit)


# Score the exam plan
y_split_index = len(anzahl) // 2  # Calculate the index to split the array
y_first = anzahl[:y_split_index]  # First half of the original data
y_second = anzahl[y_split_index:]  # Second half of the original data

yfit_split_index = len(y_fit) // 2  # Calculate the index to split the array
y_fit_first = y_fit[:yfit_split_index]  # First half of the fitted data
y_fit_second = y_fit[yfit_split_index:]  # Second part of the fitted data

# Compare first half
values_first = y_fit_first<=y_first
num_true_first = np.sum(values_first)
num_false_first =np.sum(~values_first)
print(f"True values of first half: {num_true_first}")
print(f"False values of the first half: {num_false_first}",end="\n\n")


# Compare second half
values_second=y_second<=y_fit_second
num_true_second = np.sum(values_second)
num_false_second =np.sum(~values_second)
print(f"True values of second half: {num_true_second}")
print(f"False values of the second half: {num_false_second}",end="\n\n")


score = ((num_true_first+num_true_second)/len(y))*100
print(f"Score: {score}")


# Plot the original data and the polynomial fit
plt.figure(figsize=(10, 6))
plt.scatter(start_date, anzahl, color='blue', label='Original Data')
plt.scatter(start_date, anzahl_sorted, color='orange', label='Sorted Data')
plt.plot([np.mean(x)]*len(anzahl),anzahl,color='purple',label='Middle of the Exam Plan')
plt.plot(x_fit, y_fit, color='red', label='Polynomial Fit')

plt.xlabel('Exam Date')
plt.ylabel('Number of Students')
plt.title('Polynomial Regression on Descending Sorted Data')
plt.legend()
plt.show()

