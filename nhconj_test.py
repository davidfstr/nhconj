#!/usr/bin/env python3

import nhconj
import unittest


class TestNjconj(unittest.TestCase):
    def test_romaji(self):
        self.assertEqual(nhconj.romaji('く'), 'ku')
        self.assertEqual(nhconj.romaji('ん'), 'n')
    
    def test_unromaji(self):
        self.assertEqual(nhconj.unromaji('ku'), 'く')
        self.assertEqual(nhconj.unromaji('n'), 'ん')
    
    def test_stem(self):
        self.assertEqual(nhconj.stem(ve('するー')), 'し')
        self.assertEqual(nhconj.stem(ve('くるー')), 'き')
        self.assertEqual(nhconj.stem(ve('たべる＋')), 'たべ')
        self.assertEqual(nhconj.stem(ve('いく')), 'いき')
    
    def test_long_present_aff(self):
        self.assertEqual(nhconj.long_present_aff(ve('するー')), 'します')
        self.assertEqual(nhconj.long_present_aff(ve('くるー')), 'きます')
        self.assertEqual(nhconj.long_present_aff(ve('たべる＋')), 'たべます')
        self.assertEqual(nhconj.long_present_aff(ve('いく')), 'いきます')
    
    def test_long_present_neg(self):
        self.assertEqual(nhconj.long_present_neg(ve('するー')), 'しません')
        self.assertEqual(nhconj.long_present_neg(ve('くるー')), 'きません')
        self.assertEqual(nhconj.long_present_neg(ve('たべる＋')), 'たべません')
        self.assertEqual(nhconj.long_present_neg(ve('いく')), 'いきません')
    
    def test_long_past_aff(self):
        self.assertEqual(nhconj.long_past_aff(ve('するー')), 'しました')
        self.assertEqual(nhconj.long_past_aff(ve('くるー')), 'きました')
        self.assertEqual(nhconj.long_past_aff(ve('たべる＋')), 'たべました')
        self.assertEqual(nhconj.long_past_aff(ve('いく')), 'いきました')
    
    def test_long_past_neg(self):
        self.assertEqual(nhconj.long_past_neg(ve('するー')), 'しませんでした')
        self.assertEqual(nhconj.long_past_neg(ve('くるー')), 'きませんでした')
        self.assertEqual(nhconj.long_past_neg(ve('たべる＋')), 'たべませんでした')
        self.assertEqual(nhconj.long_past_neg(ve('いく')), 'いきませんでした')
    
    def test_short_present_aff(self):
        self.assertEqual(nhconj.short_present_aff(ve('するー')), 'する')
        self.assertEqual(nhconj.short_present_aff(ve('くるー')), 'くる')
        self.assertEqual(nhconj.short_present_aff(ve('たべる＋')), 'たべる')
        self.assertEqual(nhconj.short_present_aff(ve('いく')), 'いく')
    
    def test_short_present_neg(self):
        self.assertEqual(nhconj.short_present_neg(ve('するー')), 'しない')
        self.assertEqual(nhconj.short_present_neg(ve('くるー')), 'こない')
        self.assertEqual(nhconj.short_present_neg(ve('たべる＋')), 'たべない')
        self.assertEqual(nhconj.short_present_neg(ve('いく')), 'いかない')
        # Exception
        self.assertEqual(nhconj.short_present_neg(ve('あるー')), 'ない')
    
    def test_short_past_aff(self):
        self.assertEqual(nhconj.short_past_aff(ve('するー')), 'した')
        self.assertEqual(nhconj.short_past_aff(ve('くるー')), 'きた')
        self.assertEqual(nhconj.short_past_aff(ve('たべる＋')), 'たべた')
        self.assertEqual(nhconj.short_past_aff(ve('あう')), 'あった')
        self.assertEqual(nhconj.short_past_aff(ve('まつ')), 'まった')
        self.assertEqual(nhconj.short_past_aff(ve('とるー')), 'とった')
        self.assertEqual(nhconj.short_past_aff(ve('よむ')), 'よんだ')
        self.assertEqual(nhconj.short_past_aff(ve('あそぶ')), 'あそんだ')
        self.assertEqual(nhconj.short_past_aff(ve('しぬ')), 'しんだ')
        self.assertEqual(nhconj.short_past_aff(ve('かく')), 'かいた')
        self.assertEqual(nhconj.short_past_aff(ve('いく')), 'いった') # exception
        self.assertEqual(nhconj.short_past_aff(ve('行く')), '行った') # exception
        self.assertEqual(nhconj.short_past_aff(ve('およぐ')), 'およいだ')
        self.assertEqual(nhconj.short_past_aff(ve('はなす')), 'はなした')
    
    def test_short_past_neg(self):
        self.assertEqual(nhconj.short_past_neg(ve('するー')), 'しなかった')
        self.assertEqual(nhconj.short_past_neg(ve('くるー')), 'こなかった')
        self.assertEqual(nhconj.short_past_neg(ve('たべる＋')), 'たべなかった')
        self.assertEqual(nhconj.short_past_neg(ve('いく')), 'いかなかった')
        # Exception
        self.assertEqual(nhconj.short_past_neg(ve('あるー')), 'なかった')
    
    def test_tai(self):
        self.assertEqual(nhconj.tai(ve('するー')), 'したい')
        self.assertEqual(nhconj.tai(ve('くるー')), 'きたい')
        self.assertEqual(nhconj.tai(ve('たべる＋')), 'たべたい')
        self.assertEqual(nhconj.tai(ve('いく')), 'いきたい')
    
    def test_tari(self):
        self.assertEqual(nhconj.tari(ve('するー')), 'したり')
        self.assertEqual(nhconj.tari(ve('くるー')), 'きたり')
        self.assertEqual(nhconj.tari(ve('たべる＋')), 'たべたり')
        self.assertEqual(nhconj.tari(ve('あう')), 'あったり')
        self.assertEqual(nhconj.tari(ve('まつ')), 'まったり')
        self.assertEqual(nhconj.tari(ve('とるー')), 'とったり')
        self.assertEqual(nhconj.tari(ve('よむ')), 'よんだり')
        self.assertEqual(nhconj.tari(ve('あそぶ')), 'あそんだり')
        self.assertEqual(nhconj.tari(ve('しぬ')), 'しんだり')
        self.assertEqual(nhconj.tari(ve('かく')), 'かいたり')
        self.assertEqual(nhconj.tari(ve('いく')), 'いったり') # exception
        self.assertEqual(nhconj.tari(ve('行く')), '行ったり') # exception
        self.assertEqual(nhconj.tari(ve('およぐ')), 'およいだり')
        self.assertEqual(nhconj.tari(ve('はなす')), 'はなしたり')
    
    def test_te(self):
        self.assertEqual(nhconj.te(ve('するー')), 'して')
        self.assertEqual(nhconj.te(ve('くるー')), 'きて')
        self.assertEqual(nhconj.te(ve('たべる＋')), 'たべて')
        self.assertEqual(nhconj.te(ve('あう')), 'あって')
        self.assertEqual(nhconj.te(ve('まつ')), 'まって')
        self.assertEqual(nhconj.te(ve('とるー')), 'とって')
        self.assertEqual(nhconj.te(ve('よむ')), 'よんで')
        self.assertEqual(nhconj.te(ve('あそぶ')), 'あそんで')
        self.assertEqual(nhconj.te(ve('しぬ')), 'しんで')
        self.assertEqual(nhconj.te(ve('かく')), 'かいて')
        self.assertEqual(nhconj.te(ve('いく')), 'いって') # exception
        self.assertEqual(nhconj.te(ve('行く')), '行って') # exception
        self.assertEqual(nhconj.te(ve('およぐ')), 'およいで')
        self.assertEqual(nhconj.te(ve('はなす')), 'はなして')

def ve(dict_verb_descriptor):
    if dict_verb_descriptor[-1] in '+＋':
        is_ru_verb = True
        dict_verb = dict_verb_descriptor[:-1]
    elif dict_verb_descriptor[-1] in '-ー':
        is_ru_verb = False
        dict_verb = dict_verb_descriptor[:-1]
    elif dict_verb_descriptor[-1] in 'る':
        raise ValueError(
            'Must specify whether verb ending in る is る- or う-verb')
    else:
        is_ru_verb = False
        dict_verb = dict_verb_descriptor
    
    return { 'dict_verb': dict_verb, 'is_ru_verb': is_ru_verb }


if __name__ == '__main__':
    unittest.main()