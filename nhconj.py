#!/usr/bin/env python3
#
# Conjugates verbs and adjectives in Japanese.
# 
# @author David Foster
# 

import sys
import traceback


# Decorator to mark CLI functions that expect a verb entry rather
# than just a plain string.
def expects_verb_entry(func):
    func.expects_verb_entry = True
    return func


_HIRAGANA_COLS = 'aiueo'
_HIRAGANA_ROWS = (
    ('' , 'あいうえお'),
    ('k', 'かきくけこ'),
    ('s', 'さしすせそ'),
    ('t', 'たちつてと'),
    ('n', 'なにぬねの'),
    ('h', 'はひふへほ'),
    ('m', 'まみむめも'),
    ('r', 'らりるれろ'),
    ('y', 'や　ゆ　よ'),
    ('w', 'わ　　　を'),
    
    ('g', 'がぎぐげご'),
    ('z', 'ざじずぜぞ'),
    ('d', 'だぢづでど'),
    ('b', 'ばびぶべぼ'),
    ('p', 'ぱぴぷぺぽ'),
)

_ROMAJI_FOR_KANA = {};
_ROMAJI_FOR_KANA['ん'] = 'n'
for (prefix, kanas) in _HIRAGANA_ROWS:
    for i in range(len(_HIRAGANA_COLS)):
        romaji = prefix + _HIRAGANA_COLS[i]
        kana = kanas[i]
        _ROMAJI_FOR_KANA[kana] = romaji

_KANA_FOR_ROMAJI = {rj : kana for (kana, rj) in _ROMAJI_FOR_KANA.items()}

def romaji(kana_character):
    romaji = _ROMAJI_FOR_KANA.get(kana_character)
    if romaji is not None:
        return romaji
    else:
        raise ValueError(
            'Expected single kana character: ' + kana_character)

def unromaji(romaji_character_pair):
    kana = _KANA_FOR_ROMAJI.get(romaji_character_pair)
    if kana is not None:
        return kana
    else:
        raise ValueError(
            'Expected romaji character pair: ' + romaji_character_pair)


# Given a verb in dictionary form, returns its possible stem-forms.
# Rules are based on Genki I, 2nd Ed, §3.1.
@expects_verb_entry
def stem(verb_entry):
    dict_verb = verb_entry['dict_verb']
    
    if dict_verb[-2:] in ['する']:
        return dict_verb[:-2] + 'し'
    if dict_verb[-2:] in ['くる']:
        return dict_verb[:-2] + 'き'
    
    if dict_verb[-1] in ['る']:
        if verb_entry['is_ru_verb']:
            return dict_verb[:-1]
        else:
            return dict_verb[:-1] + 'り'
    
    # ~u -> ~i
    return _replace_vowel_suffix(dict_verb, 'u', 'i')

def _replace_vowel_suffix(dict_verb, old_vowel, new_vowel):
    last = romaji(dict_verb[-1])
    if last[-1] != old_vowel:
        raise ValueError(
            'Expected verb to end with vowel "' + old_vowel + '": ' + dict_verb)
    last = last[:-1] + new_vowel
    if old_vowel == 'u' and last in ['a', 'o', 'u']:    # exception: [u] -> [w*]
        last = 'w' + last
    last = unromaji(last)
    return dict_verb[:-1] + last


# Rules are based on Genki I, 2nd Ed, §3.1.
@expects_verb_entry
def long_present_aff(verb_entry):
    return stem(verb_entry) + 'ます'


# Rules are based on Genki I, 2nd Ed, §3.1.
@expects_verb_entry
def long_present_neg(verb_entry):
    return stem(verb_entry) + 'ません'


# Rules are based on Genki I, 2nd Ed, §4.4.
@expects_verb_entry
def long_past_aff(verb_entry):
    return stem(verb_entry) + 'ました'


# Given a verb in dictionary form, returns its possible past-negative forms.
# Rules are based on Genki I, 2nd Ed, §4.4.
@expects_verb_entry
def long_past_neg(verb_entry):
    return stem(verb_entry) + 'ませんでした'


# Rules are based on Genki I, 2nd Ed, §8.1.
@expects_verb_entry
def short_present_aff(verb_entry):
    return verb_entry['dict_verb']


# Rules are based on Genki I, 2nd Ed, §8.1.
@expects_verb_entry
def short_present_neg(verb_entry):
    dict_verb = verb_entry['dict_verb']
    
    if dict_verb[-2:] in ['する']:
        return dict_verb[:-2] + 'しない'
    if dict_verb[-2:] in ['くる']:
        return dict_verb[:-2] + 'こない'
    if dict_verb == 'ある':
        return 'ない'
    
    if dict_verb[-1] in ['る']:
        if verb_entry['is_ru_verb']:
            return dict_verb[:-1] + 'ない'
        else:
            return dict_verb[:-1] + 'らない'
    
    # ~u -> ~anai
    return _replace_vowel_suffix(dict_verb, 'u', 'a') + 'ない'


# Rules are based on Genki I, 2nd Ed, §9.1.
@expects_verb_entry
def short_past_aff(verb_entry):
    return _replace_vowel_suffix(te(verb_entry), 'e', 'a')


# Rules are based on Genki I, 2nd Ed, §9.1.
@expects_verb_entry
def short_past_neg(verb_entry):
    return short_present_neg(verb_entry)[:-1] + 'かった'


# Rules are based on Genki I, 2nd Ed, §11.1.
@expects_verb_entry
def tai(verb_entry):
    return stem(verb_entry) + 'たい'


# Rules are based on Genki I, 2nd Ed, §11.2.
@expects_verb_entry
def tari(verb_entry):
    return short_past_aff(verb_entry) + 'り'


# Rules are based on Genki I, 2nd Ed, §13.1.
# Can..., Has the ability to...
@expects_verb_entry
def potential(verb_entry):
    dict_verb = verb_entry['dict_verb']
    
    if dict_verb[-2:] in ['する']:
        return dict_verb[:-2] + 'できる'
    if dict_verb[-2:] in ['くる']:
        return dict_verb[:-2] + 'こられる'
    
    if dict_verb[-1] in ['る']:
        if verb_entry['is_ru_verb']:
            return dict_verb[:-1] + 'られる'
        else:
            return dict_verb[:-1] + 'れる'
    
    # ~u -> ~eru
    return _replace_vowel_suffix(dict_verb, 'u', 'e') + 'る'


# Rules are based on Genki I, 2nd Ed, §15.1.
# Lets... [casual]
@expects_verb_entry
def volitional(verb_entry):
    dict_verb = verb_entry['dict_verb']
    
    if dict_verb[-2:] in ['する']:
        return dict_verb[:-2] + 'しよう'
    if dict_verb[-2:] in ['くる']:
        return dict_verb[:-2] + 'こよう'
    
    if dict_verb[-1] in ['る']:
        if verb_entry['is_ru_verb']:
            return dict_verb[:-1] + 'よう'
        else:
            return dict_verb[:-1] + 'ろう'
    
    # ~u -> ~ou
    return _replace_vowel_suffix(dict_verb, 'u', 'o') + 'う'


# Rules are based on Genki I, 2nd Ed, §21.1.
# NOTE: Passive forms of verbs themselves conjugate as regular る-verbs.
@expects_verb_entry
def passive(verb_entry):
    dict_verb = verb_entry['dict_verb']
    
    if dict_verb[-2:] in ['する']:
        return dict_verb[:-2] + 'される'
    if dict_verb[-2:] in ['くる']:
        return dict_verb[:-2] + 'こられる'
    
    if dict_verb[-1] in ['る']:
        if verb_entry['is_ru_verb']:
            return dict_verb[:-1] + 'られる'
        else:
            return dict_verb[:-1] + 'られる'
    
    # ~u -> ~areru
    return _replace_vowel_suffix(dict_verb, 'u', 'a') + 'れる'


# Shortened form of 〜てしまう, observed in wild, and explained on:
# http://everything2.com/title/Japanese+verb+inflection+summary
# Expresses regret...
def chau(verb_entry):
    return te(verb_entry)[:-1] + 'ちゃ'


# NOTE: Disabled until I see this in the wild.
## Shortened form of 〜てしまう, and explained on:
## http://everything2.com/title/Japanese+verb+inflection+summary
## Expresses regret...
#def chimau(verb_entry):
#    return te(verb_entry)[:-1] + 'ちまう'


# Given a verb in て-form, returns its possible dictionary forms.
# 
# Also, given an adjective in て-form, returns its single possible
# dictionary form. (ex: 'あつくなって' -> ['あつい + negative'])
def unte(te_form):
    # Reverse irr-adjectives in て-form
    # based on rules from Genki I, 2nd Ed, §7.3
    if te_form == 'よくて':
        return ['いい']
    
    # Reverse い-adjectives in て-form
    # based on rules from Genki I, 2nd Ed, §7.3
    # 
    # NOTE: Must be before the 〜て rule below
    if te_form.endswith('くて'):
        prefix = te_form[:-2]
        return [prefix + 'い']
    if te_form.endswith('くなって'):  # based on empirical observation
        prefix = te_form[:-4]
        return [prefix + 'い + negative']
    
    # Reverse verbs in て-form,
    # based on rules from Genki I, 2nd Ed, §6.1
    if te_form == 'いって':
        return ['いく']
    if te_form.endswith('って'):
        prefix = te_form[:-2]
        return [
            prefix + 'う',
            prefix + 'つ',
            prefix + 'る',
        ]
    if te_form.endswith('んで'):
        prefix = te_form[:-2]
        return [
            prefix + 'む',
            prefix + 'ぶ',
            prefix + 'ぬ',
        ]
    if te_form.endswith('いて'):
        prefix = te_form[:-2]
        return [prefix + 'く']
    if te_form.endswith('いで'):
        prefix = te_form[:-2]
        return [prefix + 'ぐ']
    if te_form.endswith('して'):
        prefix = te_form[:-2]
        return [prefix + 'す']
    if te_form.endswith('て'):
        prefix = te_form[:-1]
        return [prefix + 'る']
    
    # Reverse な-adjectives in て-form
    # based on rules from Genki I, 2nd Ed, §7.3
    # 
    # NOTE: Must be after the 〜んで rule above
    if te_form.endswith('で'):
        prefix = te_form[:-1]
        return [prefix]
    # TODO: What about the negative て-form for な-adjectives?
    
    raise ValueError(
        'Expected て-form to end with て or で: ' + te_form)


# Given a verb in dictionary form, returns its possible て-forms.
# Rules are based on Genki I, 2nd Ed, §6.1.
@expects_verb_entry
def te(verb_entry):
    dict_verb = verb_entry['dict_verb']
    
    if dict_verb[-2:] in ['する']:
        return dict_verb[:-2] + 'して'
    if dict_verb[-2:] in ['くる']:
        return dict_verb[:-2] + 'きて'
    
    if dict_verb in ['いく', '行く']:
        return dict_verb[:-1] + 'って'
    
    if dict_verb[-1] in ['る']:
        if verb_entry['is_ru_verb']:
            return dict_verb[:-1] + 'て'
        else:
            return dict_verb[:-1] + 'って'
    
    if dict_verb[-1] in ['う', 'つ', 'る']:
        return dict_verb[:-1] + 'って'
    if dict_verb[-1] in ['む', 'ぶ', 'ぬ']:
        return dict_verb[:-1] + 'んで'
    if dict_verb[-1] in ['く']:
        return dict_verb[:-1] + 'いて'
    if dict_verb[-1] in ['ぐ']:
        return dict_verb[:-1] + 'いで'
    if dict_verb[-1] in ['す']:
        return dict_verb[:-1] + 'して'
    
    raise ValueError(
        'Expected verb in dictionary form: ' + dict_verb)


# Observed in wild, and explained on:
# http://www.guidetojapanese.org/learn/grammar/compound
@expects_verb_entry
def te_neg(verb_entry):
    return short_present_neg(verb_entry)[:-1] + 'くて'

# ------------------------------------------------------------------------------
# CLI

def main():
    print('Commands:')
    print('  unte <te_form> - Convert て-form verb or adjective -> dict-form.')
    print('  te <dict_verb> - Convert dict-form verb -> て-form.')
    print()
    print('Metacommands:')
    print('  repeat <command> - Run <command> multiple times.')
    print('  quit - Quit the program.')
    print()
    
    try:
        while True:
            args = input('> ').split(' ')
            
            if args == ['']:
                break
            else:
                cmd = args[0]
                if cmd in globals():
                    _run_command(globals()[cmd], args[1:])
                else:
                    print('*** Unknown command: ' + cmd)
    except KeyboardInterrupt as e:
        # User typed Control-C
        print()
        pass
    except EOFError as e:
        # User typed Control-D
        print()
        pass

def _run_command(func, args):
    try:
        if hasattr(func, 'expects_verb_entry'):
            if args[0].endswith('る'):
                result1 = func({ 'dict_verb': args[0], 'is_ru_verb': True })
                result2 = func({ 'dict_verb': args[0], 'is_ru_verb': False })
                if result1 != result2:
                    result = [
                        '(if る-verb) ' + result1,
                        '(if う-verb) ' + result2
                    ]
                else:
                    result = [result1]
            else:
                result = [func({ 'dict_verb': args[0], 'is_ru_verb': False })]
        else:
            result = func(*args)
    except Exception as e:
        traceback.print_exc()
    else:
        if result is not None:
            print(result)


def repeat(cmd):
    if cmd not in globals():
        print('*** Unknown command: ' + cmd)
        return
    
    while True:
        args = input('>> ').split(' ')
        if args == ['']:
            break
        else:
            _run_command(globals()[cmd], args)


def quit():
    raise KeyboardInterrupt


if __name__ == '__main__':
    main()
