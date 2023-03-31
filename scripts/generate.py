#!/bin/env python3

import os
import yaml

# helper functions


def recursive_remove_folder(path: str) -> None:
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))


def check_create_folder(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path)


def write_file(data: str, path: str) -> None:
    file = open(path, mode='w', encoding='utf-8')
    file.write(data)
    file.close()


def get_char_unicode_utf8_str(char: str) -> str:
    encoded_byte = char.encode(encoding='utf-8', errors='ignore')
    return '0x' + ''.join(format(b, '02x') for b in encoded_byte)


def yaml_to_dict(path) -> dict:
    yaml_f = open(path, mode='r', encoding='utf-8')
    yaml_s = yaml_f.read()
    yaml_f.close()
    yaml_dict: dict = yaml.load(yaml_s, Loader=yaml.BaseLoader)
    return yaml_dict


# get_xxx


def get_config() -> dict:
    return yaml_to_dict('config.yaml')


def get_font(font_path) -> dict:
    return yaml_to_dict(font_path)


def get_lang(lang_path) -> dict:
    return yaml_to_dict(lang_path)


# gen_xxx


def gen_i18n_h() -> str:

    config = get_config()

    i18n_h: str = ''

    i18n_h += '#ifndef MICROI18N_H\n'
    i18n_h += '#define MICROI18N_H\n'

    i18n_h += '#include <stdint.h>\n'
    i18n_h += '#include "microi18n_defines.h"\n'
    i18n_h += '#include "font_support.h"\n'

    i18n_h += '// #######################################\n'
    i18n_h += '// generated enums\n\n'

    # language key enum
    i18n_h += '// language key enum\n'
    i18n_h += 'typedef enum I18N_LANG_KEY\n{\n'
    for i in config['langs']:
        i18n_h += f'    lang_{i},\n'
    i18n_h += '} i18n_lang_key;\n'
    # language key enum names
    i18n_h += '// language key enum names\n'
    i18n_h += 'extern const char* i18n_lang_key_name[];\n'
    # language key enum len
    i18n_h += '// language key enum len\n'
    i18n_h += f'extern const uint16_t i18n_lang_key_len;\n'
    i18n_h += '\n'

    # translation key enum
    i18n_h += '// translation key enum\n'
    trans_en = yaml_to_dict('langs/en/en.yml')
    i18n_h += 'typedef enum I18N_TRANS_KEY\n{\n'
    for i in trans_en['en']:
        i18n_h += f'    {i},\n'
    i18n_h += '} i18n_trans_key;\n'
    # translation key enum name
    i18n_h += '// translation key enum name\n'
    i18n_h += 'extern const char* i18n_trans_key_name[];\n'
    # translation key enum len
    i18n_h += '// translation key enum len\n'
    i18n_h += f'extern const uint32_t i18n_trans_key_len;\n'
    i18n_h += '\n'

    i18n_h += '// #######################################\n'
    i18n_h += '// generated objs\n\n'

    # i18n_trans_obj arrays
    i18n_h += '// i18n_trans_obj arrays\n'
    i18n_h += 'extern const i18n_trans_obj** i18n_trans[];\n'
    for i in config['langs']:
        i18n_h += f'extern const i18n_trans_obj* i18n_trans_{i}[];\n'
    i18n_h += '\n'

    i18n_h += '#endif //MICROI18N_H\n'

    return i18n_h


def gen_i18n_c() -> str:

    config = get_config()

    i18n_c: str = ''

    i18n_c += '#include "microi18n.h"\n'
    i18n_c += '\n'

    i18n_c += '// #######################################\n'
    i18n_c += '// generated enums\n\n'

    # language key enum name
    i18n_c += '// language key enum names\n'
    i18n_c += 'const char* i18n_lang_key_name[] = \n{\n'
    for i in config['langs']:
        i18n_c += f'    "lang_{i}",\n'
    i18n_c += '};\n'
    # language key enum len
    i18n_c += '// language key enum len\n'
    i18n_c += f'const uint16_t i18n_lang_key_len = {len(config["langs"].keys())};\n'
    i18n_c += '\n'

    # translation key enum name
    i18n_c += '// translation key enum name\n'
    trans_en = yaml_to_dict('langs/en/en.yml')
    i18n_c += 'const char* i18n_trans_key_name[] = \n{\n'
    for i in trans_en['en']:
        i18n_c += f'    "{i}",\n'
    i18n_c += '};\n'
    # translation key enum len
    i18n_c += '// translation key enum len\n'
    trans_en = yaml_to_dict('langs/en/en.yml')
    i18n_c += f'const uint32_t i18n_trans_key_len = {len(trans_en["en"].keys())};\n'
    i18n_c += '\n'

    i18n_c += '// #######################################\n'
    i18n_c += '// generated objs\n\n'

    # i18n_trans_obj arrays
    i18n_c += '// i18n_trans_obj arrays\n'
    i18n_c += 'const i18n_trans_obj** i18n_trans[] = \n{\n'
    for i in config['langs']:
        i18n_c += f'    i18n_trans_{i},\n'
    i18n_c += '};\n'
    i18n_c += '\n'

    # # i18n_lang_obj arrays
    # i18n_c += '// i18n_lang_obj arrays\n'
    # i18n_c += 'const i18n_lang_obj i18n_trans[] = \n{\n'
    # for i in config['langs']:
    #     i18n_c += f'    i18n_trans_{i},\n'
    # i18n_c += '};\n'
    # i18n_c += '\n'

    return i18n_c


def gen_microi18n_defines_h() -> str:

    microi18n_defines_h: str = '''
#ifndef MICROI18N_DEFINES_H
#define MICROI18N_DEFINES_H
#include <stdint.h>

// #######################################
// macros
#define _get_trans_obj(lang_key, trans_key)  i18n_trans[lang_key][trans_key]

// #######################################
// typedefs

typedef struct
{
    const uint8_t w;
    const uint8_t h;
    const uint8_t* bitmap;
} i18n_bitmap_obj;

typedef struct
{
    const uint16_t bitmap_count;
    const i18n_bitmap_obj** bitmap_obj;
} i18n_trans_obj;

// #######################################
// generated enums

#endif //MICROI18N_DEFINES_H
'''
    return microi18n_defines_h


# def gen_makefile() -> str:
#     makefile: str = ''
#     return makefile


def gen_cmakelists_txt() -> str:
    cmakelists_txt: str = ''

    cmakelists_txt += '''
cmake_minimum_required(VERSION 3.5)

set(PROJ_NAME "microi18n")

project(${PROJ_NAME} VERSION 0.1 LANGUAGES C)

set(CMAKE_C_STANDARD 17)
set(CMAKE_C_STANDARD_REQUIRED ON)

set(I18N_GENERATE_ROOT "${CMAKE_CURRENT_LIST_DIR}/..")

include_directories(${I18N_GENERATE_ROOT})

file(GLOB I18N_SRC ${I18N_GENERATE_ROOT}/*.c)
file(GLOB I18N_SRC_FONTS ${I18N_GENERATE_ROOT}/fonts/*.c)
file(GLOB I18N_SRC_LANGS ${I18N_GENERATE_ROOT}/langs/*.c)

set(I18N_FILES
    ${I18N_SRC}
    ${I18N_SRC_FONTS}
    ${I18N_SRC_LANGS}
)

message("Gathered following generated files:")
foreach(I18N_GENERATED_FILES IN ITEMS ${I18N_FILES})
    message(${I18N_GENERATED_FILES})
endforeach()

set(PROJECT_SOURCES
    ${I18N_FILES}
)

add_library(${PROJ_NAME} STATIC ${PROJECT_SOURCES})

# add_compile_definitions(FONT_FULL)
'''

    return cmakelists_txt


def gen_font_config_h() -> str:

    config = get_config()

    font_config_h: str = ''

    font_config_h += f'#ifndef FONT_CONFIG_H\n'
    font_config_h += f'#define FONT_CONFIG_H\n'
    font_config_h += '\n'

    # used unicode list
    font_config_h += '//#define FONT_FULL // switch to build with full font\n'
    font_config_h += '\n'

    font_config_h += f'#ifndef FONT_FULL\n'
    unicode_list: list = []

    for lang_name in config['langs']:
        lang = get_lang(config['langs'][lang_name]['path'])
        for trans_key in lang[lang_name]:
            for char in lang[lang_name][trans_key].replace('\\n','\n'): # yaml loader '\n' becomes ['\\','n'], we need to convert back
                unicode_list.append(get_char_unicode_utf8_str(char))

    unicode_list = list(dict.fromkeys(unicode_list))
    unicode_list.sort()

    for unicode_char in unicode_list:
        font_config_h += f'#define UNICODE_{unicode_char}\n'

    font_config_h += f'#endif // FONT_FULL\n'
    font_config_h += '\n'

    font_config_h += f'#endif // FONT_CONFIG_H\n'

    return font_config_h


def gen_font_c(font: str) -> str:

    font_c: str = ''

    font_c += f'// Name: {font["name"]}\n'
    font_c += f'// Encoding: {font["encoding"]}\n'
    font_c += f'// Conversion type: {font["conversion-type"]}\n'
    font_c += f'// Main scan direction: {font["main-scan-direction"]}\n'
    font_c += f'// Line scan direction: {font["line-scan-direction"]}\n'
    font_c += f'// Inverse: {font["inverse"]}\n'
    font_c += '\n'

    font_c += f'#include "{font["name"]}.h"\n'
    font_c += '\n'

    for bitmap in font['bitmaps']:
        font_c += f'#if defined(UNICODE_0x{bitmap}) || defined(FONT_FULL)\n'
        font_c += f'const uint8_t unicode_bitmap_0x{bitmap}[] = {{ {font["bitmaps"][bitmap]["data"]} }};\n'
        font_c += f'const i18n_bitmap_obj unicode_0x{bitmap} = {{ .w = {font["bitmaps"][bitmap]["w"]}, .h = {font["bitmaps"][bitmap]["h"]}, .bitmap = unicode_bitmap_0x{bitmap} }};\n'
        font_c += '#endif\n'

    return font_c


def gen_font_h(font: str) -> str:

    config = get_config()

    font_h: str = ''

    font_h += f'// Name: {font["name"]}\n'
    font_h += f'// Encoding: {font["encoding"]}\n'
    font_h += f'// Conversion type: {font["conversion-type"]}\n'
    font_h += f'// Main scan direction: {font["main-scan-direction"]}\n'
    font_h += f'// Line scan direction: {font["line-scan-direction"]}\n'
    font_h += f'// Inverse: {font["inverse"]}\n'
    font_h += '\n'

    font_h += f'#ifndef FONT_{font["name"]}_H\n'
    font_h += f'#define FONT_{font["name"]}_H\n'

    font_h += '#include "microi18n_defines.h"\n'
    font_h += '#include "font_config.h"\n'
    font_h += '\n'

    for bitmap in font['bitmaps']:
        font_h += f'#if defined(UNICODE_0x{bitmap}) || defined(FONT_FULL)\n'
        font_h += f'extern const i18n_bitmap_obj unicode_0x{bitmap};\n'
        font_h += '#endif\n'

    font_h += f'#endif // FONT_{font["name"]}_H\n'

    return font_h


def gen_font_support_c() -> str:

    config = get_config()

    font_support_c: str = ''

    font_support_c += '#include "font_support.h"\n'
    font_support_c += '\n'

    font_support_c += '#ifdef FONT_FULL\n'

#     font_support_c += '''
# #include <stdio.h>
# #include <stdlib.h>
# #define printf_flush(format, vars...) \\
#     printf(format, vars); \\
#     fflush(stdout);

# void debug_code_parse(const uint64_t char_code)
# {
#     printf_flush("char_code = %#lx\\n", char_code);

#     printf_flush("================ %s ================\\n", "1 Byte")
#     printf_flush("(0x00 <= char_code && char_code <= 0xff) = %s\\n",(0x00 <= char_code && char_code <= 0xff) ? "yes":"no");
#     printf_flush("(((char_code >> 0) >> 7) == 0b00000000) = %s\\n",(((char_code >> 0) >> 7) == 0b00000000) ? "yes":"no");
#     printf_flush("(((char_code >> 0) >> 7) = %lx\\n",(((char_code >> 0) >> 7)));

#     printf_flush("================ %s ================\\n", "2 Byte")
#     printf_flush("(0xff <= char_code && char_code <= 0xffff) = %s\\n",(0xff <= char_code && char_code <= 0xffff) ? "yes":"no");
#     printf_flush("(((char_code >> 8) >> 5) == 0b00000110) = %s\\n",(((char_code >> 8) >> 5) == 0b00000110) ? "yes":"no");
#     printf_flush("(((char_code >> 8) >> 5) = %lx\\n",(((char_code >> 8) >> 5)));

#     printf_flush("================ %s ================\\n", "3 Byte")
#     printf_flush("(0xffff <= char_code && char_code <= 0xffffff) = %s\\n",(0xffff <= char_code && char_code <= 0xffffff) ? "yes":"no");
#     printf_flush("(((char_code >> 16) >> 4) == 0b00001110) = %s\\n",(((char_code >> 16) >> 4) == 0b00001110) ? "yes":"no");
#     printf_flush("(((char_code >> 16) >> 4) = %lx\\n",(((char_code >> 16) >> 4)));
# }
# '''

    font_support_c += '''
// if (returned_item.unicode_len_byte == 0) { //nothing found!! }
const unicode_item get_unicode_item(const uint64_t char_code)
{
    // debug_code_parse(char_code);

    unicode_item item = {0};
    item.unicode_len_byte = 0;

    // if((char_code_header>>6) == 0b00000010)
    // {
    //     // 0b01000000 is mid bytes mask, not header
    //     // invalid or unsupported UTF-8 header byte
    //     // do nothing
    // }

    if ( (0x00 <= char_code && char_code <= 0xff) && (((char_code >> 0) >> 7) == 0b00000000) )
    {
        uint64_t low = 0, mid = 0, high = unicode_list_1Btye_count - 1;

        while ( low <= high )
        {
            mid = (low + high) / 2;
            if ( char_code < unicode_list_1Btye[mid].code )
                high = mid - 1;
            else if ( char_code > unicode_list_1Btye[mid].code )
                low = mid + 1;
            else if ( char_code == unicode_list_1Btye[mid].code )
            {
                item.unicode_len_byte = 1;
                item.unicode_item_xbyte._1b.code = char_code;
                item.unicode_item_xbyte._1b.bitmap_obj = unicode_list_1Btye[mid].bitmap_obj;
                break;
            }
        }
    }
    if ( (0xff <= char_code && char_code <= 0xffff) && (((char_code >> 8) >> 5) == 0b00000110) )
    {
        uint64_t low = 0, mid = 0, high = unicode_list_2Btye_count - 1;

        while ( low <= high )
        {
            mid = (low + high) / 2;
            if ( char_code < unicode_list_2Btye[mid].code )
                high = mid - 1;
            else if ( char_code > unicode_list_2Btye[mid].code )
                low = mid + 1;
            else if ( char_code == unicode_list_2Btye[mid].code )
            {
                item.unicode_len_byte = 2;
                item.unicode_item_xbyte._2b.code = char_code;
                item.unicode_item_xbyte._2b.bitmap_obj = unicode_list_2Btye[mid].bitmap_obj;
                break;
            }
        }
    }
    if ( (0xffff <= char_code && char_code <= 0xffffff) && (((char_code >> 16) >> 4) == 0b00001110) )
    {
        uint64_t low = 0, mid = 0, high = unicode_list_3Btye_count - 1;

        while ( low <= high )
        {
            mid = (low + high) / 2;
            if ( char_code < unicode_list_3Btye[mid].code )
                high = mid - 1;
            else if ( char_code > unicode_list_3Btye[mid].code )
                low = mid + 1;
            else if ( char_code == unicode_list_3Btye[mid].code )
            {
                item.unicode_len_byte = 3;
                item.unicode_item_xbyte._3b.code = char_code;
                item.unicode_item_xbyte._3b.bitmap_obj = unicode_list_3Btye[mid].bitmap_obj;
                break;
            }
        }
    }

    return item;
}

'''

    unicode_1b_list: list = []
    unicode_2b_list: list = []
    unicode_3b_list: list = []

    for font_item in config['fonts']:
        font = get_font(config['fonts'][font_item]['path'])
        for char_code in font['bitmaps']:

            if int(char_code[0:2], 16) >> 6 == 0b00000010:
                print(
                    f'Error: invalid or unsupported UTF-8 header byte -> 0x{char_code}')

            if int(char_code[0:2], 16) >> 7 == 0b00000000:
                unicode_1b_list.append(char_code)

            if int(char_code[0:2], 16) >> 5 == 0b00000110:
                unicode_2b_list.append(char_code)

            if int(char_code[0:2], 16) >> 4 == 0b00001110:
                unicode_3b_list.append(char_code)

    unicode_1b_list = list(dict.fromkeys(unicode_1b_list))
    unicode_1b_list.sort()
    unicode_2b_list = list(dict.fromkeys(unicode_2b_list))
    unicode_2b_list.sort()
    unicode_3b_list = list(dict.fromkeys(unicode_3b_list))
    unicode_3b_list.sort()

    font_support_c += f'const uint64_t unicode_list_1Btye_count = {len(unicode_1b_list)};\n'
    font_support_c += 'const unicode_item_1Byte unicode_list_1Btye[] = \n{\n'
    for char in unicode_1b_list:
        font_support_c += f'    {{ .code = 0x{char}, .bitmap_obj = &unicode_0x{char}, }},\n'
    font_support_c += '};\n'
    font_support_c += '\n'

    font_support_c += f'const uint64_t unicode_list_2Btye_count = {len(unicode_2b_list)};\n'
    font_support_c += 'const unicode_item_2Byte unicode_list_2Btye[] = \n{\n'
    for char in unicode_2b_list:
        font_support_c += f'    {{ .code = 0x{char}, .bitmap_obj = &unicode_0x{char}, }},\n'
    font_support_c += '};\n'
    font_support_c += '\n'

    font_support_c += f'const uint64_t unicode_list_3Btye_count = {len(unicode_3b_list)};\n'
    font_support_c += 'const unicode_item_3Byte unicode_list_3Btye[] = \n{\n'
    for char in unicode_3b_list:
        font_support_c += f'    {{ .code = 0x{char}, .bitmap_obj = &unicode_0x{char}, }},\n'
    font_support_c += '};\n'
    font_support_c += '\n'

    font_support_c += '#endif // FONT_FULL\n'
    font_support_c += '\n'

    return font_support_c


def gen_font_support_h() -> str:

    font_support_h: str = ''

    font_support_h += '#ifndef FONT_SUPPORT_H\n'
    font_support_h += '#define FONT_SUPPORT_H\n'

    font_support_h += '#include <stdint.h>\n'
    font_support_h += '\n'

    # fonts headers
    for font in config['fonts']:
        font_support_h += f'#include "fonts/{font}.h"\n'
    font_support_h += '\n'

    font_support_h += '#include "microi18n_defines.h"\n'
    font_support_h += '\n'

    # full font supports
    font_support_h += '''
#ifdef FONT_FULL

typedef struct
{
    uint32_t code : 8;
    const i18n_bitmap_obj* bitmap_obj;
} unicode_item_1Byte;

typedef struct
{
    uint32_t code : 16;
    const i18n_bitmap_obj* bitmap_obj;
} unicode_item_2Byte;

typedef struct
{
    uint32_t code : 24;
    const i18n_bitmap_obj* bitmap_obj;
} unicode_item_3Byte;

typedef union
{
    unicode_item_1Byte _1b;
    unicode_item_2Byte _2b;
    unicode_item_3Byte _3b;
} unicode_item_xByte;

typedef struct
{
    uint8_t unicode_len_byte : 4; // 4 bit, dont need range larger than number 8
    unicode_item_xByte unicode_item_xbyte;
} unicode_item;

const unicode_item get_unicode_item(const uint64_t char_code);

extern const uint64_t unicode_list_1Btye_count;
extern const unicode_item_1Byte unicode_list_1Btye[];
extern const uint64_t unicode_list_2Btye_count;
extern const unicode_item_2Byte unicode_list_2Btye[];
extern const uint64_t unicode_list_3Btye_count;
extern const unicode_item_3Byte unicode_list_3Btye[];

#endif // FONT_FULL
'''
    font_support_h += '\n'

    font_support_h += '#endif //FONT_SUPPORT_H\n'

    return font_support_h


def gen_lang_c(lang: str) -> str:

    # as we don't want make changes on yaml from Lokalise and do not want pass more parameters
    lang_name = ''
    for i in lang:
        # there should only be one, so this is ok
        lang_name = i

    lang_c: str = ''

    lang_c += f'// Name: {lang_name}\n'

    lang_c += '#include "microi18n.h"\n'
    lang_c += '\n'

    # each translations
    for trans in lang[lang_name]:
        array_s: str = ''
        lang_c += f'// {trans}\n'
        for char in lang[lang_name][trans].replace('\\n','\n'): # yaml loader '\n' becomes ['\\','n'], we need to convert back
            array_s += f'&unicode_{get_char_unicode_utf8_str(char)}, '
        array_s = array_s[:-2]  # remove the last ', '

        lang_c += f'const i18n_bitmap_obj* i18n_trans_bitmap_{lang_name}_{trans}[] = {{ {array_s} }};\n'
        lang_c += f'const i18n_trans_obj i18n_trans_{lang_name}_{trans} = {{ .bitmap_count =  {len(lang[lang_name][trans])}, .bitmap_obj = i18n_trans_bitmap_{lang_name}_{trans}}};\n'
    lang_c += '\n'

    # object array
    lang_c += f'const i18n_trans_obj* i18n_trans_{lang_name}[] = \n'
    lang_c += '{\n'
    for trans in lang[lang_name]:
        lang_c += f'    &i18n_trans_{lang_name}_{trans},\n'
    lang_c += '};\n'
    lang_c += '\n'

    return lang_c


################################################
# folders
print('Recreating folders...')
recursive_remove_folder('gen')
check_create_folder('gen')
check_create_folder('gen/fonts')
check_create_folder('gen/langs')
check_create_folder('gen/library')

################################################
# main
print('Reading config...')
config = get_config()

################################################
# gen/microi18n*.*
print('Generating microi18n...')
write_file(gen_microi18n_defines_h(), 'gen/microi18n_defines.h')
write_file(gen_i18n_h(), 'gen/microi18n.h')
write_file(gen_i18n_c(), 'gen/microi18n.c')

################################################
# gen/font_config.h
print('Generating font_config...')
write_file(gen_font_config_h(), 'gen/font_config.h')

################################################
# gen/font_support.*
print('Generating font_support...')
write_file(gen_font_support_h(), 'gen/font_support.h')
write_file(gen_font_support_c(), 'gen/font_support.c')

################################################
# gen/fonts/*.*
for font_item in config['fonts']:
    print(f'Generating fonts -> [{font_item}]...')
    font = get_font(config['fonts'][font_item]['path'])
    write_file(gen_font_c(font), f'gen/fonts/{font["name"]}.c')
    write_file(gen_font_h(font), f'gen/fonts/{font["name"]}.h')
    pass

################################################
# gen/langs/*.*
for lang_item in config['langs']:
    print(f'Generating languages -> [{lang_item}]...')
    lang = get_lang(config['langs'][lang_item]['path'])
    write_file(gen_lang_c(lang), f'gen/langs/{lang_item}.c')
    pass

################################################
# makefile

################################################
# cmakelists_txt
print('Generating cmakelists...')
write_file(gen_cmakelists_txt(), 'gen/library/CMakeLists.txt')
