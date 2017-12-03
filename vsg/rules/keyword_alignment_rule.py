
from vsg import rule
from vsg import check
from vsg import fix
from vsg import line


class keyword_alignment_rule(rule.rule):
    '''
    Instantiation rule 015 ensures the alignment of the => operator for every generic in the instantiation.
    '''

    def __init__(self):
        rule.rule.__init__(self)
        self.phase = 5
        # The following is filled out by the user
        self.sKeyword = None
        self.sStartGroupTrigger = None
        self.sEndGroupTrigger = None
        self.sLineTrigger = None

    def analyze(self, oFile):
        lGroup = []
        fGroupFound = False
        iStartGroupIndex = None
        for iLineNumber, oLine in enumerate(oFile.lines):
            if oLine.__dict__[self.sStartGroupTrigger] and not fGroupFound:
                fGroupFound = True
                iStartGroupIndex = iLineNumber
            if oLine.__dict__[self.sEndGroupTrigger]:
                lGroup.append(oLine)
                fGroupFound = False
                check.keyword_alignment(self, iStartGroupIndex, self.sKeyword, lGroup)
                lGroup = []
                iStartGroupIndex = None
            if fGroupFound:
                if oLine.__dict__[self.sLineTrigger]:
                    lGroup.append(oLine)
                else:
                    lGroup.append(line.line('Removed line'))

    def _fix_violations(self, oFile):
        fix.keyword_alignment(self, oFile)