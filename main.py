import requests
import re
import time
import argparse

def fuzzy_request(card_name="Demonic Tutor", set="STA"):
    # Make request
    response = requests.get("https://api.scryfall.com/cards/named?fuzzy="+card_name+"&set="+set, 
                headers={"User-Agent":"MTGProxyPrinter","Accept":"*/*"})
    
    # Space out requests
    time.sleep(0.05)
    
    return response.json()

def search_request(set="STA", id="90"):
    # Make request
    response = requests.get("https://api.scryfall.com/cards/" + set + "/" + id + "", 
                headers={"User-Agent":"MTGProxyPrinter","Accept":"*/*"})
    
    # Space out requests
    time.sleep(0.05)
    
    return response.json()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--opp", default="csv")
    parser.add_argument("-i", "--iter", default=1, type=int)

    subparsers = parser.add_subparsers()
    set_opts = subparsers.add_parser('set')
    set_opts.add_argument('-s', '--sets', nargs='*', default=['mid'])

    args = parser.parse_args()
    mode = args.opp
    readfrom = 'instance/input.txt'
    readto = 'instance/output'
    iterations = args.iter
    if mode=='set':
        sets = args.sets
    else:
        sets = ['']

    # Decide output file extention
    if mode=='csv':
        readto = readto + '.csv'
    elif mode=='pdf':
        readto = readto + '.html'
    elif mode=='set':
        readto = readto + '.md'
    elif mode=='prox':
        readto = readto + '.txt'
    
    with open(readfrom, "r") as f1:
        with open(readto, "w") as f2:
            if mode == 'csv':
                f2.write('name,set,id,cost\n')
            if mode == 'pdf':
                f2.write('<!DOCTYPE html>\n<html>\n<body>\n')
            for j in sets:
                if mode == 'set':
                    f2.write('##' + j + '\n')
                for i in range (iterations):
                    
                    # Parse card
                    curr_card = next(f1)
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
                            req = search_request(set=card['set'], id=card['card-number'])
                            print(card['name'])
                            f2.write(card['name'] + ',' + card['set'] + ',' + card['card-number'] + ',')
                            if ('E' in card['foils']):
                                f2.write(req['prices']['usd_etched'])
                            elif ('F' in card['foils']):
                                f2.write(req['prices']['usd_foil'])
                            else:
                                f2.write(req['prices']['usd'])
                            f2.write('\n')
                        
                        if (mode=='pdf'):
                            req = search_request(set=card['set'], id=card['card-number'])
                            if req['layout']=='transform':
                                f2.writelines([
                                    '<img src='+ req['card_faces'][0]['image_uris']['normal'] +' width="240" height="336">\n',
                                    '<img src='+ req['card_faces'][1]['image_uris']['normal'] +' width="240" height="336">\n'
                                    ])
                            else:
                                f2.write('<img src='+ req['image_uris']['normal'] +' width="240" height="336">\n')
                            
                        if (mode=='set'):
                            req = fuzzy_request(set=j, card_name=card['name'])
                            if (req['object'] == 'card'):
                                f2.write('1 ' + card['name'] + ' (' + j + ')\n')

                        if mode=='prox':
                            f2.write(str(card['quantity']) + ' ' + card['name'] + '\n')
                if mode=='set':
                    f2.write('\n')
                    f1.seek(0)
            if mode == 'pdf':
                f2.write('</html>')

if __name__=="__main__":
    main()