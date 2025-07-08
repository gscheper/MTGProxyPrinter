import requests
import re
import sys
import time
import argparse

def make_scryfall_request(card_name="Demonic Tutor", set="STA", id="90"):
    # Make request
    response = requests.get("https://api.scryfall.com/cards/" + set + "/" + id + "", 
                headers={"User-Agent":"MTGProxyPrinter","Accept":"*/*"})
    
    # Space out requests
    time.sleep(0.05)
    
    return response.json()

def main():
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--opp", default="list")
    args = parser.parse_args()
    #print(args.operation)
    '''

    mode = 'csv'
    readfrom = 'input.txt'
    readto = 'output.csv'
    iterations = 10
    sets = ["mic", "inr", "mid", "vow", "soi", "emn", "isd", "dka", "avr", "voc"]

    with open(readfrom, "r") as f1:
        with open(readto, "w") as f2:
            if mode == 'csv':
                f2.write('name,set,id,cost\n')
            for i in range (iterations):
                # Parse card
                curr_card = next(f1)
                edhrec = re.match(r"(^[1-9]+) (([A-Z]|[a-z]| |/|,|-|')+)\n", curr_card + "\n")
                mox = re.match(r"(^[1-9]+) (([A-Z]|[a-z]| |/|,|-|')+) \((.+)\) (([0-9]|-|[A-Z])*.?)( \*[A-Z]+\*)*( #[A-z]*)*\n", curr_card + "\n")
                mox_foils = re.findall(r"\*([A-Z]+)\**", curr_card + "\n")
                mox_tags = re.findall(r"#([A-z]+)*", curr_card + "\n")
                if (mox != None):
                    card = {
                        "quantity": int(mox.group(1)),
                        "name": mox.group(2),
                        "set": mox.group(4),
                        "card-number": mox.group(5),
                        "tags": mox_tags,
                        "foils": mox_foils
                    }
                    
                    if (mode=='csv'):
                        req = make_scryfall_request(set=card['set'], id=card['card-number'])
                        f2.write(card['name'] + ',' + card['set'] + ',' + card['card-number'] + ',')
                        if ('E' in card['foils']):
                            f2.write(req['prices']['usd_etched'])
                        elif ('F' in card['foils']):
                            f2.write(req['prices']['usd_foil'])
                        else:
                            f2.write(req['prices']['usd'])
                        f2.write('\n')

if __name__=="__main__":
    main()