#ifndef MICROI18N_CPP_H
#define MICROI18N_CPP_H

#include <iostream>
#include <vector>
// #include <array>
// #include <bitset>
#include <string>

#include <cstdint>

extern "C"
{
    #include <microi18n.h>
}

class microi18n
{
public:
    static inline std::string get_lang_key_string(I18N_LANG_KEY key)
    {
        return std::string(i18n_lang_key_name[key]);
    }

    static inline uint16_t get_lang_key_count()
    {
        return i18n_lang_key_len;
    }

    static inline std::string get_trans_key_string(I18N_TRANS_KEY key)
    {
        return std::string(i18n_trans_key_name[key]);
    }

    static inline uint32_t get_trans_key_count()
    {
        return i18n_trans_key_len;
    }

    static inline const i18n_trans_obj* get_translation(I18N_LANG_KEY lang_key, I18N_TRANS_KEY trans_key)
    {
        const i18n_trans_obj* trans_obj = i18n_trans[lang_key][trans_key];

        return trans_obj;
    }
};

#endif // MICROI18N_CPP_H
