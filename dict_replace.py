#!/usr/bin/python
# -*- coding: utf-8 -*-

def dict_replace(dictionary, text, strip_chars=None, replace_func=None):
    """
        Replace word or word phrase in text with keyword in dictionary.

        Arguments:
            dictionary: dict with key:value, key should be in lower case
            text: string to replace
            strip_chars: string contain character to be strip out of each word
            replace_func: function if exist will transform final replacement.
                          Must have 2 params as key and value

        Return:
            string

        Example:
            my_dict = {
                "hello": "hallo",
                "hallo": "hello",    # Only one pass, don't worry
                "smart tv": "http://google.com?q=smart+tv"
            }
            dict_replace(my_dict, "hello google smart tv",
                         replace_func=lambda k,v: '[%s](%s)'%(k,v))
    """

    # First break word phrase in dictionary into single word
    dictionary = dictionary.copy()
    for key in dictionary.keys():
        if ' ' in key:
            key_parts = key.split()
            for part in key_parts:
                # Mark single word with False
                if part not in dictionary:
                    dictionary[part] = False

    # Break text into words and compare one by one
    result = []
    words = text.split()
    words.append('')
    last_match = ''     # Last keyword (lower) match
    original = ''       # Last match in original
    for word in words:
        key_word = word.lower().strip(strip_chars) if \
                   strip_chars is not None else word.lower()
        if key_word in dictionary:
            last_match = last_match + ' ' + key_word if \
                         last_match != '' else key_word
            original = original + ' ' + word if \
                       original != '' else word
        else:
            if last_match != '':
                # If match whole word
                if last_match in dictionary and dictionary[last_match] != False:
                    if replace_func is not None:
                        result.append(replace_func(original, dictionary[last_match]))
                    else:
                        result.append(dictionary[last_match])
                else:
                    # Only match partial of keyword
                    match_parts = last_match.split(' ')
                    match_original = original.split(' ')
                    for i in xrange(0, len(match_parts)):
                        if match_parts[i] in dictionary and \
                           dictionary[match_parts[i]] != False:
                            if replace_func is not None:
                                result.append(replace_func(match_original[i], dictionary[match_parts[i]]))
                            else:
                                result.append(dictionary[match_parts[i]])
            result.append(word)
            last_match = ''
            original = ''

    return ' '.join(result)



# Test
my_dict = {
    "tv": "http://www.samsung.com/us/video/tvs",
    "smart tv": "http://www.samsung.com/us/video/tvs",
    "tv will update itself": "http://www.samsung.com/smart-tv",
    "displayed": "show",
    "show": "displayed"
}
text = '''If you're going to invest in a state-of-the-art TV, it only makes sense to get a model that will keep up with the latest changes. Look for a Smart TV with the intelligence to update when needed. You can connect a hassle-free evolution kit to your current system and the TV will update itself. Even if a broadcast is displayed in standard HD—or even in Standard Definition—a Smart TV with built-in UHD upscaling can give your picture the UHD-level experience. show '''

print dict_replace(my_dict, text, ',.', lambda k,v: '[%s](%s)' % (k,v))
