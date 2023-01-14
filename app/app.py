from nsetools import Nse
from company_list import names
import csv
from tqdm import tqdm


nse = Nse()

def get_percentage_52(val):
    if val:
        return (
            round(.8*val, 2),
            round(.7*val, 2),
            round(.5*val,2)
        )
    else:
        return (0, 0, 0)


def get_current_per(t, v):
    return (round(((t-v)/t)*100,2))


def write_to_csv(filename,headers, data):
    
    # writing to csv file 
    with open(filename, 'w') as csvfile: 
        # creating a csv writer object 
        csvwriter = csv.writer(csvfile) 
            
        # writing the fields 
        csvwriter.writerow(headers) 
            
        # writing the data rows 
        csvwriter.writerows(data)


def main():
    headers = ["name",
           "Company name", 
           "closePrice", 
           "lastPrice", 
           "52 week high", 
           "52 week low", 
           "All time high",
           "20%52weekHigh",
           "30%52weekHigh",
           "50%52weekHigh",
           "curr%52weekHigh",
           "Recommendations-52W"
            ]
    l = []
    for i in tqdm(names):
        q = nse.get_quote(i)
        per20, per30, per50 = get_percentage_52(q['high52'])
        perCur = get_current_per(q['high52'], q['lastPrice'])

        rec = 0
        if q['lastPrice']<per20:
            rec = 3.5
        if q['lastPrice']<per30:
            rec = 4
        if q['lastPrice']<per50:
            rec = 5
        


        l.append([i, 
                q['companyName'], 
                q['closePrice'],
                q['lastPrice'],  
                q['high52'], 
                q['low52'], 
                "NA",
                per20,
                per30,
                per50,
                perCur,
                rec
                ])


    filename = "./Data/trade_sheets.csv"

    write_to_csv(filename, headers, l)



if __name__=="__main__":
    print("===== STARTED =====")
    main()
    print("----- DONE -----")