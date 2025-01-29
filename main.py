import requests
import re
import sys
import json


def main():
    readfrom = sys.argv[1]
    readto = sys.argv[2]
    iterations = int(sys.argv[3])

    with open(readfrom, "r") as f1:
        with open(readto, "w") as f2:
            f2.write("<!DOCTYPE html>\n\t<html>\n\t<body>\n")
            for i in range (iterations):
                curr_card = next(f1)
                searchfor = " ".join(re.split(" ", curr_card)[1:-2])
                if (curr_card[-3] == 'F'): searchfor = " ".join(re.split(" ", curr_card)[1:-3])
                print(searchfor)
                response = requests.get("https://api.scryfall.com/cards/named?fuzzy="+searchfor, 
                                headers={"User-Agent":"MTGProxyPrinter","Accept":"*/*"})
                f2.write("\t\t<img src=" + str(response.json()["image_uris"]["normal"]) + " width=\"240\" height=\"336\">\n")
                
                with open( "datafile.json" , "w" ) as write:
                    json.dump( response.json() , write )
            f2.write("\t</html>")


if __name__=="__main__":
    main()