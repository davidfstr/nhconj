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
            dict_verb[:-1] + 'て (if る-verb)',
            dict_verb[:-1] + 'って (if う-verb)'
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
