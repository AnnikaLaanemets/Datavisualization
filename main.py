import csv
import matplotlib.pyplot as plt
from cycler import cycler
import numpy as np

""" DATA_SOURCE = (
    "HYDE (2023); Gapminder (2022); UN WPP (2024) – with major processing by Our World in Data."
    " 'Number of people using the Internet' [dataset]. International Telecommunication Union (via World Bank),"
    " 'World Development Indicators'; Various sources, 'Population' [original data]."
    " Retrieved January 11, 2025 from https://ourworldindata.org/grapher/number-of-internet-users"
)"""

def generate_population_dictionary(filename):
  """Generates population dictionary from csv file data and adds internet users proposition to dictionary.
   Return dictionary following this sructure:
   {"Africa": {total_population: [1, 2, 2, 3],internet_population: [0, 1, 1, 2], years: [2000, 2010, 2015, 2020]}
  "Asia": {total_population: [2, 3, 4, 5],internet_population: [1, 2, 3, 4], years: [2000, 2010, 2015, 2020]}"""
  output = {}
  with open(filename, "r") as csvfile:
      reader = csv.DictReader(csvfile)
      for line in reader:
          continent = line["continent"]
          year = int(line["year"])
          internet_population = int(line["internet_population"])
          total_population = int(line["total_population"])
          
          if continent not in output:
              output[continent] = {"total_population": [], "internet_population": [], "years": []}
          output[continent]["total_population"].append(total_population)
          output[continent]["internet_population"].append(internet_population)
          output[continent]["years"].append(year)
       
  return output

def generate_world_users_data(population_dictionary):
     world_data=population_dictionary["World"]
     years = world_data["years"]
     grouped_labels = [f"{years[i]}-{years[i+2]}" for i in range(0, len(years), 3)]
     grouped_population = [sum(world_data["total_population"][i:i+3]) for i in range(0, len(years), 3)]
     grouped_users = [sum(world_data["internet_population"][i:i+3]) for i in range(0, len(years), 3)]
     return grouped_labels, grouped_population, grouped_users
    
  
def setup_figure(fig):
    """Generates a multi-panel plot"""
    plt.rcParams['axes.prop_cycle'] = cycler(color='krycbgm')
    plt.rcParams.update({'font.size': 10})
    grid = fig.add_gridspec(2, 2, height_ratios=[1, 1]) 
    return grid

def generate_population_plots_from_dictionary(population_dictionary, world_population, grid, fig):
   """Adds graphs to figure
   1. First row: Bar chart of world population (1991-2020) in 3 years intervals and world internet users as a line on top of bars
   2. Second row: Left - Internet users growth by continent. Right - Population growth by continent. """
   def display_world_population():
       """First row plot. Bar chart with gradient bars showing world population and overlay line showing internet users"""
       ax1 = fig.add_subplot(grid[0, :]) 
       cmap = plt.cm.viridis
       bar_width = 0.8
       x_positions = np.arange(len(world_population[0]))
       ax1.set_xticks(x_positions)
       ax1.set_xticklabels(world_population[0], rotation=10)
       ax1.set_title("World Population Growth & Internet Users 1991-2020")
       ax1.set_xlabel("Years")
       ax1.set_ylabel("Population")
       ax1.set_ylim(top=(max(world_population[1])*1.1))
       for x, value in zip(x_positions, world_population[1]):
           gradient = np.linspace(0, 1, 256).reshape(-1, 1)
           gradient = cmap(gradient)
           ax1.imshow( gradient, aspect='auto', extent=(x - bar_width / 2, x + bar_width / 2, 0, value))
           ax1.plot(x_positions, world_population[2], color="#0D0A28", marker=".", markersize=5, linewidth=2)
       
   
   def display_population_by_continents():
       """Row 2: Internet users growth by continents"""
       ax2 = fig.add_subplot(grid[1, 0]) # Left plot in the second row
       ax3 = fig.add_subplot(grid[1, 1]) # Right plot in the second row
       ax2.set_title("Internet Users Growth by Continent")
       ax3.set_title("Population Growth by Continent")
       
       for continent, data in population_dictionary.items():
           ax2.plot(data["years"], data["internet_population"], label=continent, marker="o", markersize=3, linewidth=2)
           ax3.plot(data["years"], data["total_population"], label=continent, marker="8",markersize=3, linewidth=2)
           ax2.set_xlabel("Year")
           ax2.set_ylabel("Internet users (billions) ")
           ax2.legend()
           ax3.set_xlabel("Year")
           ax3.set_ylabel("Population (billions)")
           ax3.legend()
        
   display_world_population()
   display_population_by_continents()
   plt.subplots_adjust(hspace=0.4, wspace=0.15) 
   plt.show()
 
   
   
fig = plt.figure()
grid = setup_figure(fig)
filename = "data.csv"

#Display graphs
population_dictionary = generate_population_dictionary(filename)
world_population = generate_world_users_data(population_dictionary)
generate_population_plots_from_dictionary(population_dictionary, world_population, grid, fig)


