import usaddress

def getQuery(state, keyword, county, doc_types, years):
    query = '(state:"' + state + '") AND (doc_full_text:' + keyword + \
        ') AND (county:"' + county + '") '

    ##query += ' AND '

    for doc in doc_types:
    #    query += ' AND (doc_type_search:'  + ' AND doc_type_search:'.join(doc.split())+ ') '
        is_parsed = 0 

    if len(years)>0:
        query += ' AND '
        
    for yr in years:
        query += ' (year:' + str(yr) + ') OR '

    query =  query[:-3].strip()
    return query


def getRightSideData(x):
    try:
        DOCUMENT_TYPE_RIGHT = x[0].text.title()
    except:
        DOCUMENT_TYPE_RIGHT = 'NA'
    try:
        RECORDING_DATE = x[2].text
    except:
        RECORDING_DATE = 'NA'
    try:
        APN = x[3].text
    except:
        APN = 'NA'
    try:
        ADDRESS = x[4].text.title()
        parse_address = usaddress.parse(ADDRESS)
        parse_address_dict = {}
        for i in parse_address:
            if i[1] not in parse_address_dict.keys():
                    parse_address_dict[i[1]] = i[0]
            else:
                    parse_address_dict[i[1]] += ' '+ i[0]


        try:
            address_number_right = str(parse_address_dict['AddressNumber']).title()
        except:
            address_number_right = 'NA'
        try:
            streetName_right = str(parse_address_dict['StreetName']).title()
        except:
            streetName_right = 'NA'
        try:
            PlaceName_right = str(parse_address_dict['PlaceName']).title()
        except:
            PlaceName_right = 'NA'
        try:
            StateName_right = str(parse_address_dict['StateName']).upper()
        except:
            StateName_right = 'NA'
        try:
            ZipCode_right = parse_address_dict['ZipCode']
        except:
            ZipCode_right = 'NA'                
    except:
        ADDRESS = 'NA'
        address_number_right = streetName_right = PlaceName_right = StateName_right = ZipCode_right = 'NA'
    try:
        OWNER_BORROWER = ' '.join(x[5].text.title().split()[::-1])
        OWNER_BORROWER = OWNER_BORROWER.split()
        OWNER_BORROWER = ' '.join([i for i in OWNER_BORROWER if len(i)>1])
    except:
        OWNER_BORROWER = 'NA'
    try:
        SELLER_LENDER = ' '.join(x[6].text.title().split()[::-1])
        SELLER_LENDER = SELLER_LENDER.split()
        SELLER_LENDER = ' '.join([i for i in SELLER_LENDER if len(i)>1])
    except:
        SELLER_LENDER = 'NA'

    return DOCUMENT_TYPE_RIGHT, RECORDING_DATE, APN,ADDRESS, address_number_right,streetName_right,\
                    PlaceName_right,  StateName_right, ZipCode_right, OWNER_BORROWER,\
                    SELLER_LENDER
