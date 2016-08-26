import usaddress, re

text_box_left = 'proprty settlement agreement or decree of dissolution of a of l marriage egal separation. or . . . ...i . ..... ! A creation, transfer, or termination, solely between spouses, of any co -owners interest. The distribution of a legal entitys property to a spouse or frIrmer spouse in exchange for the'
text_box_left = 'Marc C.Tonnesen 2:29 PM AR64 Recorded in Official Records; Solano County 6/20/2016 WHEN RECORDED MAIL TO: Assessor/Recorder 06 Name LORENZO NOVOA P Lorenzo Novoa StrW. . Doc#: 201600051838 Titles: 1 Pages: 3 . MARIBEL NOVOA Address 324 PINTAIL DRIVE 11111'
keyword = '"name", "dissolution"'
data_from_left = text_box_left.lower().split(keyword.replace('"',''))[-1]
name_address = re.findall(r'\s([a-z][a-z]+.*?)$', data_from_left)[0]
try:
    name_address = re.findall(r'(\w\w.*?\s\w\w\.?\s*\d\d\d\d\d)', name_address)[0]
except:
    name_address = ''
    
name_address_split = name_address.split()
b = 0
for i in name_address_split:
    b+=1
    try:
        i = int(i)
        isinstance(i, int)
        break
    except Exception,e:
        pass

name = ' '.join(name_address_split[:b-1]).title()
name = name.split()
name = ' '.join([i for i in name if len(i)>1])
address = ' '.join(name_address_split[b-1:]).title()
parse_address = usaddress.parse(address)
parse_address_dict = {}
for i in parse_address:
    if i[1] not in parse_address_dict.keys():
        parse_address_dict[i[1]] = i[0]
    else:
        parse_address_dict[i[1]] += ' '+ i[0]
try:
    address_number = str(parse_address_dict['AddressNumber']).title()
except:
    address_number = 'NA'
try:
    streetName = str(parse_address_dict['StreetName']).title()
except:
    streetName = 'NA'
try:
    StreetNamePostType = str(parse_address_dict['StreetNamePostType']).title()
except:
    StreetNamePostType = 'NA'
try:
    PlaceName = str(parse_address_dict['PlaceName']).title()
except:
    PlaceName = 'NA'
try:
    StateName = str(parse_address_dict['StateName']).upper()
except:
    StateName = 'NA'
try:
    ZipCode = parse_address_dict['ZipCode']
except:
    ZipCode = 'NA'
try:
    StreetNamePostType = str(parse_address_dict['StreetNamePostType']).title()
except:
    StreetNamePostType = 'NA'
try:
    StreetNamePreDirectional = str(parse_address_dict['StreetNamePreDirectional']).title()
except:
    StreetNamePreDirectional = 'NA'
is_parsed = 1
leftSideParseGood = 1
