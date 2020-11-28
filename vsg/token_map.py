
import bisect
import pprint
from vsg import token

class New():

    def __init__(self, dMap):
        self.dMap = dMap

    def get_token_indexes(self, oToken):
        lReturn = []
        sBase, sSub = extract_unique_id(oToken)
        try:
            return self.dMap[sBase][sSub]
        except KeyError:
            return {}

    def get_line_number_of_index(self, iIndex):
        iLine = bisect.bisect_left(self.dMap['parser']['carriage_return'], iIndex) + 1
        return iLine

    def pretty_print(self):
        pp=pprint.PrettyPrinter(indent=4)
        pp.pprint(self.dMap)



def extract_unique_id(oToken):
    sBase = None
    sSub = None
    lDoc = oToken.__doc__.split()
    for iDoc, sDoc in enumerate(lDoc):
        if sDoc == 'unique_id':
            return lDoc[iDoc + 2], lDoc[iDoc + 4]
    return None, None


def process_tokens(lTokens):
    iLibIndex = 0
    dMap = build_default_map()
    for iToken, oToken in enumerate(lTokens):
        sBase, sSub = oToken.get_unique_id()
        if sBase is not None:
           try:
               dMap[sBase][sSub].append(iToken)
           except KeyError:
               try:
                   dMap[sBase][sSub] = []
                   dMap[sBase][sSub].append(iToken)
               except KeyError:
                   dMap[sBase] = {}
                   dMap[sBase][sSub] = []
                   dMap[sBase][sSub].append(iToken)

    return New(dMap)


def build_default_map():
    dMap = {}
    return dMap