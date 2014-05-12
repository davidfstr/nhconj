#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys

# Given a verb in て-form, returns its possible dictionary forms.
# 
# Also, given an adjective in て-form, makes a best-effort attempt to return
# its single possible dictionary form.
# (ex: 'あつくなって' -> ['あつい + negative'])
# 
# NOTE: Does not recognize all *adjectives* in て-form,
#       since I don't know all the rules.
# NOTE: Does not recognize all *negative* て-forms,
#       since I don't know all the rules.
def unte(te_form):
    # Reverse い-adjectives in て-form
    if te_form.endswith('くて'):  # based on Wikipedia rules
        prefix = te_form[:-2]
        return [prefix + 'い']
    if te_form.endswith('くなって'):  # based on empirical observation
        prefix = te_form[:-4]
        return [prefix + 'い + negative']
    
    # Reverse な-adjectives in て-form
    if te_form.endswith('で'):  # based on Wikipedia rules
        prefix = te_form[:-1]
        return [prefix]
    # TODO: What about the negative て-form for な-adjectives?
    
    # Reverse verbs in て-form,
    # based on rules from Genki I, chapter 7
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
    
    raise ValueError(
        'Expected て-form to end with て or で: ' + te_form)

def unte_cli():
    print 'て-form:', 
    te_form = raw_input().decode(sys.stdin.encoding)
    
    possible_dict_forms = unte(te_form)
    print
    print 'Possible dict forms:'
    for x in possible_dict_forms:
        print '  ' + x

# Given a verb in dictionary form, returns its possible て-forms.
# Rules are based on Genki I, chapter 6.
def te(dict_verb):
    if dict_verb in ['する']:
        return ['して']
    if dict_verb in ['くる']:
        return ['きて']
    
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

def te_cli():
    print 'Dict-verb:', 
    dict_verb = raw_input().decode(sys.stdin.encoding)
    
    possible_te_forms = te(dict_verb)
    print
    print 'Possible て-forms:'
    for x in possible_te_forms:
        print '  ' + x
