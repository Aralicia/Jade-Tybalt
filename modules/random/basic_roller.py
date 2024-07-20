from heapq import nlargest, nsmallest
from random import randint
from collections import namedtuple
import re
import regex

#dice_regex = re.compile(r"^(\d*)d(\d*)([hmle+t-]|\.[+-])?(\d*)?\ ?((adv)|(disadv))?$")


#dice_regex = re.compile(r"^(\d+)d(\d+)( *([+-]) *(\d+))?")
dice_regex = regex.compile("^([+-])?(?:(\d+)|(\d+)d(\d+))$")
formula_dice_subregex = "(?:\d+|\d+d\d+)";
formula_regex = regex.compile("^(\s*[+-]?\s*{d})(\s*[+-]\s*{d})*(?:\s+(.*))?$".format(d=formula_dice_subregex))


#            'h',  # Highest Roll
#            'l',  # Lowest Roll
#            '+',  # Add to total
#            '-',  # Remove from total
#            '.+', # Add to every individual
#            '.-', # Remove from every individual
#            'e',  # Exploding dice
#            't',  # Total

class Dice:

    def __init__(self, sign, count, faces=1, flags={}):
        self.sign = sign
        self.count = int(count)
        self.faces = int(faces)
        self.flags = flags

        self.result = 0
        self.resultList = []

    def __str__(self):
        return self.normalized()
    
    def normalized(self, is_first=False):
        sign = '' if self.sign == '+' and is_first else self.sign
        if self.faces == 1:
            return "{}{}".format(sign, str(self.count))
        return "{}{}d{}".format(sign, str(self.count), str(self.faces))

    def roll(self):
        if self.faces > 1:
            self.result = 0
            for i in range(1, self.count+1):
                value = randint(1, self.faces)
                self.result += value
                self.resultList.append(value)
        elif self.faces == 1:
            self.result = self.count
            self.resultList = [self.count]
        if self.sign == '-':
            self.result = -self.result

    def expandedResult(self, is_first=False):
        if self.faces == 1:
            if self.result < 0 or is_first:
                return str(self.result)
            else:
                return '+'+str(self.result)
        res = '[{}]'.format(','.join(map(str, self.resultList)))

        if self.sign == '+' and is_first:
            return res
        return '{}{}'.format(self.sign, res)


def roll(user_input: str = None):
    parsed = parse_roll(user_input)
    print(parsed)
    if parsed is None:
        return None

    summary = ""
    expanded = ""
    result = 0

    for i, dice in enumerate(parsed.dices):
        dice.roll()
        summary += dice.normalized(i==0)
        expanded += dice.expandedResult(i==0)
        result += dice.result

    return namedtuple('Roll', 'summary expanded result comment')(summary, expanded, result, parsed.comment)


def parse_roll(roll:str):
    formula_parse = formula_regex.match(roll)
    print(formula_parse)
    if formula_parse is None:
        return None

    captures = formula_parse.allcaptures();
    raw_dices = captures[2]
    raw_dices.insert(0, captures[1][0])
    comment = captures[3][0] if len(captures[3]) > 0 else None
    dices = []

    for raw_dice in raw_dices:
        dice_parse = dice_regex.match(raw_dice)
        captures = dice_parse.allcaptures()
        sign = captures[1][0] if len(captures[1]) > 0 else '+'
        if len(captures[2]) == 0:
            dice = Dice(sign, captures[3][0], captures[4][0])
        else:
            dice = Dice(sign, captures[2][0])
        dices.append(dice)

    return namedtuple('Formula', 'dices comment')(dices, comment)

