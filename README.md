# nhconj

Conjugates Japanese verbs and adjectives.

I use this program to read and write Japanese essays more quickly.

For example:

```
$ ./nhconj.py
Commands:
  unte <te_form> - Convert て-form verb or adjective -> dict-form.
  te <dict_verb> - Convert dict-form verb -> て-form.

Metacommands:
  repeat <command> - Run <command> multiple times.
  quit - Quit the program.

> te はなす
['はなして']

> unte はなして
['はなす']

> te わかる
['わかて (if る-verb)', 'わかって (if う-verb)']

> unte わかって
['わかう', 'わかつ', 'わかる']

> unte あつくなって
['あつい + negative']

> quit
```