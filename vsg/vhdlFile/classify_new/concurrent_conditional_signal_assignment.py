
from vsg import parser

from vsg.token import concurrent_conditional_signal_assignment as token
from vsg.token import conditional_waveforms

from vsg.vhdlFile.classify_new import delay_mechanism
from vsg.vhdlFile.classify_new import conditional_waveforms
from vsg.vhdlFile import utils


def detect(iCurrent, lObjects):
    '''

    [ label : ] [ postponed ] concurrent_conditional_signal_assignment

    concurrent_conditional_signal_assignment ::=
        target <= [ guarded ] [ delay_mechanism ] conditional_waveforms ;

    conditional_waveforms ::=
        waveform when condition
        { else waveform when condition }
        [ else waveform ]

    The key to detecting this is looking for an assignment <= followed by the keyword **when** before a semicolon.
    '''

    iToken = iCurrent
    bAssignmentFound = False

    while lObjects[iToken].get_value() != ';':
        if utils.is_item(lObjects, iToken):
            if bAssignmentFound:
                if utils.object_value_is(lObjects, iToken, 'when'):
                    return True
            else:
                if utils.object_value_is(lObjects, iToken, 'when'):
                    return False
                if utils.object_value_is(lObjects, iToken, 'with'):
                    return False
    
            if utils.object_value_is(lObjects, iToken, '<=') and not bAssignmentFound:
                bAssignmentFound = True
        iToken += 1
    else:
        return False


def classify(iToken, lObjects):
    '''
    concurrent_conditional_signal_assignment ::=
        target <= [ guarded ] [ delay_mechanism ] conditional_waveforms ;
    '''
    iCurrent = utils.assign_tokens_until('<=', token.target, iToken, lObjects)
    iCurrent = utils.assign_next_token_required('<=', token.assignment, iCurrent, lObjects)
    iCurrent = utils.assign_next_token_if('guarded', token.guarded_keyword, iCurrent, lObjects)
    iCurrent = delay_mechanism.detect(iCurrent, lObjects)
    iCurrent = conditional_waveforms.classify(iCurrent, lObjects)
    iCurrent = utils.assign_next_token_required(';', token.semicolon, iCurrent, lObjects)
    return iCurrent