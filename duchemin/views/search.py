from django.shortcuts import render
from duchemin.helpers.solrsearch import DCSolrSearch

VOICE_NAMES = ["S", "Ct", "T", "B", "None"]


def search(request):
    if 'q' not in request.GET:
        return _empty_search(request)
    else:
        return render(request, 'search/results.html')


def _empty_search(request):
    s = DCSolrSearch(request)
    ret = s.facets(fq=['duchemin_analysis'], rows=0)

    facets = ret.facet_counts['facet_fields']
    cadence_alter = sorted(facets['cadence_alter'])
    book_title = sorted(facets['book_id_title'])
    cadence_final_tone = sorted(facets['cadence_final_tone'])
    cadence_kind = sorted(facets['cadence_kind'])
    composer = sorted(facets['composer'])
    contributor = sorted(facets['contributor'])
    is_cadence = sorted(facets['is_cadence'])
    repeat_kind = sorted(facets['repeat_kind'])
    text_treatment = sorted(facets['text_treatment'])
    other_pres_type = sorted(facets['other_pres_type'])
    repeat_exact_varied = sorted(facets['repeat_exact_varied'])

    book_info = sorted([tuple(book.split("_")) for book in book_title])

    cad_voice_cantz = [__construct_voice_facet(v, 'cadence_role_cantz', hidden=False) for v in VOICE_NAMES]
    cad_voice_tenz = [__construct_voice_facet(v, 'cadence_role_tenz') for v in VOICE_NAMES]

    intpatt_up6_voice = [__construct_voice_facet(v, 'intpatt_p6_up', hidden=False) for v in VOICE_NAMES]
    intpatt_lo6_voice = [__construct_voice_facet(v, 'intpatt_p6_lo') for v in VOICE_NAMES]

    intpatt_up3_voice = [__construct_voice_facet(v, 'intpatt_p3_up', hidden=False) for v in VOICE_NAMES]
    intpatt_lo3_voice = [__construct_voice_facet(v, 'intpatt_p3_lo') for v in VOICE_NAMES]

    intpatt_up53_voice = [__construct_voice_facet(v, 'intpatt_53_up', hidden=False) for v in VOICE_NAMES]
    intpatt_lo53_voice = [__construct_voice_facet(v, 'intpatt_53_lo') for v in VOICE_NAMES]

    prestype_nonim_up1 = [__construct_voice_facet(v, 'prestype_nim_up1', hidden=False) for v in VOICE_NAMES]
    prestype_nonim_lo1 = [__construct_voice_facet(v, 'prestype_nim_lo1') for v in VOICE_NAMES]
    prestype_nonim_up2 = [__construct_voice_facet(v, 'prestype_nim_up2') for v in VOICE_NAMES]
    prestype_nonim_lo2 = [__construct_voice_facet(v, 'prestype_nim_lo2') for v in VOICE_NAMES]

    prestype_free_dux = [__construct_voice_facet(v, 'prestype_free_dux', hidden=False) for v in VOICE_NAMES]
    prestype_free_comes = [__construct_voice_facet(v, 'prestype_free_comes') for v in VOICE_NAMES]

    prestype_imduet_dux1 = [__construct_voice_facet(v, 'prestype_imduet_dux1', hidden=False) for v in VOICE_NAMES]
    prestype_imduet_comes1 = [__construct_voice_facet(v, 'prestype_imduet_comes1') for v in VOICE_NAMES]
    prestype_imduet_dux2 = [__construct_voice_facet(v, 'prestype_imduet_dux2') for v in VOICE_NAMES]
    prestype_imduet_comes2 = [__construct_voice_facet(v, 'prestype_imduet_comes2') for v in VOICE_NAMES]

    prestype_entry_dux1 = [__construct_voice_facet(v, 'prestype_entry_p_dux1', hidden=False) for v in VOICE_NAMES]
    prestype_entry_comes1 = [__construct_voice_facet(v, 'prestype_entry_p_comes1') for v in VOICE_NAMES]
    prestype_entry_dux2 = [__construct_voice_facet(v, 'prestype_entry_p_dux2') for v in VOICE_NAMES]
    prestype_entry_comes2 = [__construct_voice_facet(v, 'prestype_entry_p_comes2') for v in VOICE_NAMES]

    prestype_entry_t_dux1 = [__construct_voice_facet(v, 'prestype_entry_t_dux1', hidden=False) for v in VOICE_NAMES]
    prestype_entry_t_comes1 = [__construct_voice_facet(v, 'prestype_entry_t_comes1') for v in VOICE_NAMES]
    prestype_entry_t_dux2 = [__construct_voice_facet(v, 'prestype_entry_t_dux2') for v in VOICE_NAMES]
    prestype_entry_t_comes2 = [__construct_voice_facet(v, 'prestype_entry_t_comes2') for v in VOICE_NAMES]

    prestype_entry_s_dux1 = [__construct_voice_facet(v, 'prestype_entry_s_dux1', hidden=False) for v in VOICE_NAMES]
    prestype_entry_s_comes1 = [__construct_voice_facet(v, 'prestype_entry_s_comes1') for v in VOICE_NAMES]
    prestype_entry_s_dux2 = [__construct_voice_facet(v, 'prestype_entry_s_dux2') for v in VOICE_NAMES]
    prestype_entry_s_comes2 = [__construct_voice_facet(v, 'prestype_entry_s_comes2') for v in VOICE_NAMES]

    data = {
        'book_info': book_info,
        'cadence_alters': cadence_alter,
        'cadence_final_tones': cadence_final_tone,
        'cadence_kinds': cadence_kind,
        'composers': composer,
        'contributors': contributor,
        'is_cadences': is_cadence,
        'repeat_kinds': repeat_kind,
        'text_treatments': text_treatment,
        'other_pres_type': other_pres_type,
        'repeat_exact_varied': repeat_exact_varied,
        'cad_voice_cantz': cad_voice_cantz,
        'cad_voice_tenz': cad_voice_tenz,
        'intpatt_up6_voice': intpatt_up6_voice,
        'intpatt_lo6_voice': intpatt_lo6_voice,
        'intpatt_up3_voice': intpatt_up3_voice,
        'intpatt_lo3_voice': intpatt_lo3_voice,
        'intpatt_up53_voice': intpatt_up53_voice,
        'intpatt_lo53_voice': intpatt_lo53_voice,
        'prestype_nonim_up1': prestype_nonim_up1,
        'prestype_nonim_lo1': prestype_nonim_lo1,
        'prestype_nonim_up2': prestype_nonim_up2,
        'prestype_nonim_lo2': prestype_nonim_lo2,
        'prestype_free_dux': prestype_free_dux,
        'prestype_free_comes': prestype_free_comes,
        'prestype_imduet_dux1': prestype_imduet_dux1,
        'prestype_imduet_comes1': prestype_imduet_comes1,
        'prestype_imduet_dux2': prestype_imduet_dux2,
        'prestype_imduet_comes2': prestype_imduet_comes2,
        'prestype_entry_dux1': prestype_entry_dux1,
        'prestype_entry_comes1': prestype_entry_comes1,
        'prestype_entry_dux2': prestype_entry_dux2,
        'prestype_entry_comes2': prestype_entry_comes2,
        'prestype_entry_t_dux1': prestype_entry_t_dux1,
        'prestype_entry_t_comes1': prestype_entry_t_comes1,
        'prestype_entry_t_dux2': prestype_entry_t_dux2,
        'prestype_entry_t_comes2': prestype_entry_t_comes2,
        'prestype_entry_s_dux1': prestype_entry_s_dux1,
        'prestype_entry_s_comes1': prestype_entry_s_comes1,
        'prestype_entry_s_dux2': prestype_entry_s_dux2,
        'prestype_entry_s_comes2': prestype_entry_s_comes2,
    }
    return render(request, 'search/search.html', data)


def __construct_voice_facet(voice, group, hidden=True):
    d = {
        'id': "{0}_{1}".format(voice.lower(), group),
        'voice': voice,
        'group': group,
        'hidden': hidden,
        'checked': False
    }
    if voice == "None":
        d['checked'] = True

    return VoiceFacet(**d)


class VoiceFacet(object):
    def __init__(self, **entries):
        self.__dict__.update(entries)
