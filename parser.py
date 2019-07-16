import csv

nationPosition = dict()
nationalities = list()
artistsDict = dict()
artistsGender = dict()
csv_reader = []
with open('Artists.csv', mode='r', errors="ignore") as csv_file:
    csv_reader = list(csv.DictReader(csv_file))
    line_count = 0

    for row in csv_reader:
        if line_count != 0:
            
            if not(row['Nationality'] in nationPosition):
                nationPosition[row['Nationality']] = len(nationalities)
                nationalities.append(row['Nationality'])
        line_count += 1

    line_count = 0
    for row in csv_reader:
        if line_count != 0:

            if not(row['BeginDate'] in artistsGender):
                artistsGender[row['BeginDate']] = [0, 0]

            if row['Gender'] == 'Male':
                artistsGender[row['BeginDate']][0] += 1
            elif row['Gender'] == 'Female':
                artistsGender[row['BeginDate']][1] += 1

            if not(row['BeginDate'] in artistsDict):
                artistsDict[row['BeginDate']] = [0 for i in range(len(nationalities))]
            artistsDict[row["BeginDate"]][nationPosition[row['Nationality']]] += 1
        line_count += 1




with open('year_nationality.csv', mode='w') as artistsCSV:
    artistsWriter = csv.writer(artistsCSV, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    sortedKeys = sorted(artistsDict.keys())
    artistsWriter.writerow(["year"] + (nationalities))
    for i in range(1,len(sortedKeys)):
        year = sortedKeys[i]
        artistsWriter.writerow([year] + (artistsDict[year]))


def filterZero(x):
    return x[1] != 0

with open('fromatted_year_nationality.csv', mode='w', newline='') as artistsCSV:
    artistsWriter = csv.writer(artistsCSV, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    sortedKeys = sorted(artistsDict.keys())
    artistsWriter.writerow(["key","value","date"])

    top5EachYear = {}

    for key in artistsDict.keys():
        best5 = sorted(enumerate(artistsDict[key]), key=lambda x: x[1], reverse=True)[:5]
        best5 = list(filter(filterZero, best5))
        top5EachYear[key] = [nationalities[index[0]] for index in best5]

    for j in range(0, len(nationalities)):
        for i in range(1,len(sortedKeys)):
            if not(nationalities[j] == ""):
                year = sortedKeys[i]
                artistsWriter.writerow([nationalities[j]] + [artistsDict[year][j]] + ["%s" % year])
    
with open('fromatted_year_nationality_top10.csv', mode='w', newline='') as artistsCSV:
    artistsWriter = csv.writer(artistsCSV, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    sortedKeys = sorted(artistsDict.keys())
    artistsWriter.writerow(["key","value","date"])

    top10 = {}
    totalOccurences = [0 for i in range(len(nationalities))]
    for key, value in artistsDict.items():
        for i in range(len(value)):
            totalOccurences[i] += value[i]
    
    best10 = sorted(enumerate(totalOccurences), key=lambda x: x[1], reverse=True)[:6]
    
    
    top10 = list(map(lambda x:  nationalities[x[0]], best10))
    print(top10)

    for j in range(0, len(nationalities)):
        for i in range(1,len(sortedKeys)):
            if not(nationalities[j] == ""):
                nationality = nationalities[j]
                if not(nationalities[j] in top10):
                    nationality = "Other"
                year = sortedKeys[i]
                artistsWriter.writerow([nationality] + [artistsDict[year][j]] + ["%s" % year])

with open('gender_distribution.csv', mode='w', newline='') as artistsCSV:
    artistsWriter = csv.writer(artistsCSV, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    sortedKeys = sorted(artistsDict.keys())
    artistsWriter.writerow(["key","value","date"])
    
    for i in range(0,2):
        for key in sorted(artistsGender.keys()):
            gender = "Male"
            if i == 1:
                gender = "Female"
            artistsWriter.writerow([gender] + [artistsGender[key][i]] + ["%s" % key])


with open('parallel_artists.csv', mode='w', newline='') as artistsCSV:
    artistsWriter = csv.writer(artistsCSV, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    artistsWriter.writerow(["Nationality","isAlive","Gender"])
    print(top10)
    for row in csv_reader:
        nationality = row["Nationality"]
        if not(row["Nationality"] in top10) or row["Nationality"] == "":
            nationality = "Other"

        isAlive = "No"
        if row["EndDate"] == "0":
            isAlive = "Yes"

        artistsWriter.writerow([nationality] + [isAlive] + [row["Gender"]])