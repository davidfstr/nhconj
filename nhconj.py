#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Conjugates verbs and adjectives in Japanese.
# 
# @author David Foster
# 

import sys
import traceback

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
                    try:
                        result = globals()[cmd](*args[1:])
                    except Exception as e:
                        traceback.print_exc()
                    else:
                        if result is not None:
                            print(result)
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


HIRAGANA_COLS = 'aiueo'
HIRAGANA_ROWS = (
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
)

ROMAJI_FOR_KANA = {};
ROMAJI_FOR_KANA['ん'] = 'n'
for (prefix, kanas) in HIRAGANA_ROWS:
    for i in range(len(HIRAGANA_COLS)):
        romaji = prefix + HIRAGANA_COLS[i]
        kana = kanas[i]
        ROMAJI_FOR_KANA[kana] = romaji

KANA_FOR_ROMAJI = {rj : kana for (kana, rj) in ROMAJI_FOR_KANA.items()}

def romaji(kana_character):
    romaji = ROMAJI_FOR_KANA.get(kana_character)
    if romaji is not None:
        return romaji
    else:
        raise ValueError(
            'Expected single kana character: ' + kana_character)

def unromaji(romaji_character_pair):
    kana = KANA_FOR_ROMAJI.get(romaji_character_pair)
    if kana is not None:
        return kana
    else:
        raise ValueError(
            'Expected romaji character pair: ' + romaji_character_pair)


# Given a verb in dictionary form, returns its possible stem-forms.
# Rules are based on Genki I, 2nd Ed, §3.1.
def stem(dict_verb):
    if dict_verb[-2:] in ['する']:
        return [dict_verb[:-2] + 'し']
    if dict_verb[-2:] in ['くる']:
        return [dict_verb[:-2] + 'き']
    
    if dict_verb[-1] in ['る']:
        return [
            '(if る-verb) ' + dict_verb[:-1],
            '(if う-verb) ' + dict_verb[:-1] + 'り'
        ]
    
    # ~u -> ~i
    return [_replace_vowel_suffix(dict_verb, 'u', 'i')]

def _replace_vowel_suffix(dict_verb, old_vowel, new_vowel):
    last = romaji(dict_verb[-1])
    if last[-1] != old_vowel:
        raise ValueError(
            'Expected verb in dictionary form: ' + dict_verb)
    last = last[:-1] + new_vowel
    last = unromaji(last)
    return dict_verb[:-1] + last


# Rules are based on Genki I, 2nd Ed, §3.1.
def long_present_aff(dict_verb):
    return [s + 'ます' for s in stem(dict_verb)]


# Rules are based on Genki I, 2nd Ed, §3.1.
def long_present_neg(dict_verb):
    return [s + 'ません' for s in stem(dict_verb)]


# Rules are based on Genki I, 2nd Ed, §4.4.
def long_past_aff(dict_verb):
    return [s + 'ました' for s in stem(dict_verb)]


# Given a verb in dictionary form, returns its possible past-negative forms.
# Rules are based on Genki I, 2nd Ed, §4.4.
def long_past_neg(dict_verb):
    return [s + 'ませんでした' for s in stem(dict_verb)]


# Rules are based on Genki I, 2nd Ed, §8.1.
def short_present_aff(dict_verb):
    return [dict_verb]


# Rules are based on Genki I, 2nd Ed, §8.1.
def short_present_neg(dict_verb):
    if dict_verb[-2:] in ['する']:
        return [dict_verb[:-2] + 'しない']
    if dict_verb[-2:] in ['くる']:
        return [dict_verb[:-2] + 'こない']
    if dict_verb == 'ある':
        return ['ない']
    
    if dict_verb[-1] in ['る']:
        return [
            '(if る-verb) ' + dict_verb[:-1] + 'ない',
            '(if う-verb) ' + dict_verb[:-1] + 'らない'
        ]
    
    # ~u -> ~anai
    return [_replace_vowel_suffix(dict_verb, 'u', 'a') + 'ない']


# Rules are based on Genki I, 2nd Ed, §9.1.
def short_past_aff(dict_verb):
    return [_replace_vowel_suffix(v_te, 'e', 'a') for v_te in te(dict_verb)]


# Rules are based on Genki I, 2nd Ed, §9.1.
def short_past_neg(dict_verb):
    return [spn[:-1] + 'かった' for spn in short_present_neg(dict_verb)]


# Rules are based on Genki I, 2nd Ed, §11.1.
def tai(dict_verb):
    return [s + 'たい' for s in stem(dict_verb)]


# Rules are based on Genki I, 2nd Ed, §11.2.
def tari(dict_verb):
    return [spa + 'り' for spa in short_present_aff(dict_verb)]


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
def te(dict_verb):
    if dict_verb[-2:] in ['する']:
        return [dict_verb[:-2] + 'して']
    if dict_verb[-2:] in ['くる']:
        return [dict_verb[:-2] + 'きて']
    
    if dict_verb in ['いく', '行く']:
        return [dict_verb[:-1] + 'って']
    
    if dict_verb[-1] in ['る']:
        return [
            '(if る-verb) ' + dict_verb[:-1] + 'て',
            '(if う-verb) ' + dict_verb[:-1] + 'って'
        ]
    
    if dict_verb[-1] in ['う', 'つ', 'る']:
        return [dict_verb[:-1] + 'って']
    if dict_verb[-1] in ['む', 'ぶ', 'ぬ']:
        return [dict_verb[:-1] + 'んで']
    if dict_verb[-1] in ['く']:
        return [dict_verb[:-1] + 'いて']
    if dict_verb[-1] in ['ぐ']:
        return [dict_verb[:-1] + 'いで']
    if dict_verb[-1] in ['す']:
        return [dict_verb[:-1] + 'して']
    
    raise ValueError(
        'Expected verb in dictionary form: ' + dict_verb)
    

def repeat(cmd):
    if cmd not in globals():
        print('*** Unknown command: ' + cmd)
        return
    
    while True:
        args = input('>> ').split(' ')
        if args == ['']:
            break
        else:
            try:
                result = globals()[cmd](*args)
            except Exception as e:
                traceback.print_exc()
            else:
                if result is not None:
                    print(result)


def quit():
    raise KeyboardInterrupt


if __name__ == '__main__':
    main()
