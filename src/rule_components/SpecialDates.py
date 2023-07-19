import csv
import random
import pandas as pd
from datetime import datetime, timedelta
from rule_components.Rule import Rule


class SpecialDates(Rule):

    def __init__(self,data_obj):
       super().__init__(data_obj)
       self.score, self.conflicts_df, self.plot_arr = self.compute()
    def compute(self):
        
        conflicts = []
       
        # check conflicts by itearing each row
        for index, row in self.data_obj.special_dates_df.iterrows():
            lastName = row['lastName']
            specialDate = row['specialDate']
          

         
           # '1. & 2. Pruefer' from array to singple elements
            examiners_df = self.data_obj.examiners_exams_df.explode('1. & 2. Pruefer')
 
            matches = examiners_df[(examiners_df['1. & 2. Pruefer'].str.contains(lastName)) & (examiners_df['Datum, Uhrzeit (ggf. sep. Zeitplan beachten)'].str.contains(specialDate))]

  
            # if there is a match, add the conflict values to the conflict list.
            if not matches.empty:
                conflicts.append({'Name': lastName, 'SpecialDate': specialDate, 'Exams': matches['Datum, Uhrzeit (ggf. sep. Zeitplan beachten)'].tolist()})

        # Turn the results into dataframe
        result_df = pd.DataFrame(conflicts)

        row_count = result_df.shape[0]

        if(row_count > 0): 
            score = 0
        else: 
            score = 1
        
        percentage_score = (score * 100)

        return percentage_score, result_df, None;

    def create_randomly_special_dates_csv():
                
        data = [
        "Keller, Stilgenbauer",
        "Biedermann, Schleif",
        "Schleif, Münch",
        "Dunphy, Schöning",
        "Kulesz, Braun",
        "Espenschied, Liebstückel",
        "Müller, Huffstadt",
        "Keller, Wübker",
        "Liebstückel, Hennermann",
        "Deinzer, Ebner, M.",
        "Wimmer, Braun",
        "Balzer, Deinzer",
        "Fertig, Braun",
        "Fertig, Schütz",
        "Aubele, Schillinger",
        "Schleif, Heusinger",
        "Reining, Schillinger",
        "Rott, Schleif",
        "Ansari,Richter, Aubele",
        "Saueressig, Schleif",
        "Biedermann, Weber",
        "Bachmeir, Balzer",
        "Müßig, Weber",
        "Rott, Huffstadt",
        "Wassermann, Kreiner-Wegener",
        "Müßig, Müller, N",
        "Wedlich, Hennermann",
        "Balzer, Ebner, M.",
        "Wedlich, Rott",
        "Weber, Wedlich",
        "John, Weber",
        "Lohre, Weber",
        "Deinzer, Fetzer",
        "Müßig, Müller",
        "Kulesz, Schleif",
        "Stilgenbauer, Wübker",
        "Weber, Rott",
        "Huffstadt, Müßig",
        "Wübker, Stilgenbauer",
        "Liebstückel, Wedlich",
        "Dahms, Aubele",
        "Fischer, Mario, Völkl-Wolf",
        "Aubele, Fischer, Mario",
        "Heinzl, Braun",
        "Gerhards, Schleif",
        "von Rotenhan,Heppt, Fischer, Mario",
        "Heinzl, Zilker",
        "Holleber, Ch., Völkl-Wolf",
        "Metzner,Spriestersbach, Fischer, Mario",
        "Kulesz, John",
        "Deinzer, John",
        "Huffstadt, John",
        "Zahn, Wedlich",
        "Schillinger, Wimmer, T.",
        "Deinzer, Kastner",
        "Schmeling, Heinzl",
        "Rott, Stilgenbauer",
        "Stilgenbauer, Keller",
        "Biedermann, Schinner",
        "Weber, Biedermann",
        "Storath, Diethelm",
        "Krimmer, Völkl-Wolf",
        "Schillinger, Wimmer",
        "Ehret, Meyer",
        "Ehret, Kraus, Christian",
        "Huffstadt, Müller"
        ]

        date_begin = datetime(2023, 7, 1)
        date_end = datetime(2023, 7, 30)

        data_list = []
        added_names = set()  # Create a set to watch added names

        for teacher in data:
            random_date = date_begin + timedelta(days=random.randint(0, (date_end - date_begin).days))
            names = teacher.split(", ")
            for name in names:
                name = name.strip()  # Remove the gaps from the beginning and ending of the names
                sub_names = name.split(",")  # Divide names with ,
                for sub_name in sub_names:
                    sub_name = sub_name.strip()  # Remove gaps from names that divided with ,
                    if sub_name not in added_names:  # if the name is not added before, add it.
                        data_list.append([sub_name, random_date.strftime("%Y-%m-%d")])
                        added_names.add(sub_name)  # Add the name to the set of added names

        with open("special_dates.csv", "w", newline="") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(["lastName", "specialDate"])
            writer.writerows(data_list)
