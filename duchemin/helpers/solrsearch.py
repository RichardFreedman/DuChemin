from django.conf import settings
from duchemin.helpers.solrpaginate import SolrPaginator, SolrGroupedPaginator
import solr


class DCSolrSearch(object):
    def __init__(self, request):
        self.server = solr.Solr(settings.SOLR_SERVER)
        self.request = request
        self.parsed_request = {}
        self.prepared_query = u""
        self.solr_params = {}
        self._parse_request()
        self._prep_q()

    def search(self, q=None, **kwargs):
        if q:
            self.solr_params['q'] = q
        self.solr_params.update(kwargs)
        res = self._do_query()
        return SolrPaginator(res)
        
        
    def facets(self, facet_fields=settings.SOLR_FACET_FIELDS, **kwargs):
        facet_params = {
            'facet': 'true',
            'facet_field': facet_fields,
        }
        self.solr_params.update(facet_params)
        self.solr_params.update(kwargs)

        res = self._do_query()
        return res

    def group_search(self, group_fields, **kwargs):
        group_params = {
            'group': 'true',
            'group_ngroups': 'true',
            'group_field': group_fields
        }
        self.solr_params.update(group_params)
        self.solr_params.update(kwargs)

        res = self._do_query()
        return SolrGroupedPaginator(res)

    def _do_query(self):
        return self.server.select(self.prepared_query, **self.solr_params)

    def _parse_prestypes(self):
        prestype = []
        qdict = self.request.GET
        for k, v in qdict.lists():
            if 'prestype_nim' in k and 'NIM' not in prestype:
                prestype.append('NIM')
            elif 'prestype_free' in k and 'FI' not in prestype:
                prestype.append('FI')
            elif 'prestype_imduet' in k and 'ID' not in prestype:
                prestype.append('ID')
            elif 'prestype_entry_p' in k and 'PEn' not in prestype:
                prestype.append('PEn')
            elif 'prestype_entry_t' in k and 'PEn Tonal' not in prestype:
                prestype.append('PEn Tonal')
            elif 'prestype_entry_s' in k and 'PEn Stacked' not in prestype:
                prestype.append('PEn Stacked')
        self.parsed_request['other_pres_type'] = prestype

    def _parse_voice_filter(self):
        """ Parses the voice filter grid to construct an appropriate query.
            The format of this is *very* picky -- it's tied to the entry form
            that was used to generate the data, which is somewhat counter-intuitive
            for parsing.

            "The '@' and 'direction' are relative to the previous entry". This means
            that an entry for:
            Dux1:Ct, Comes1:B, Dux2:T, Comes2:S, @1 or 8:S, @5:B, Above:S, Below:B

            Translates to "Comes 1 (Bass) enters at a fifth below (the CounterTenor),
            and Comes 2 (Soprano) enters at an octave/unison above (the Tenor)."

            Here's an ASCII version of the entry form. At the intersection of each row/column
            there is a radio button for selection.

                                        S       Ct      T       B
            Upper Voice 1 (NIM)     |
            Lower Voice 1 (NIM)     |
            Upper Voice 2 (NIM)     |
            Lower Voice 2 (NIM)     |
            Dux 1 (FI ID or PEn)    |
            Comes 1 (FI ID or PEn)  |
            Dux 2 (FI ID or PEn)    |
            Comes 2 (FI ID or PEn)  |
                        @1 or 8     |
                            @5      |
                            @4      |
                            Above   |
                            Below   |

        """
        qdict = self.request.GET
        self.parsed_request['voice_role_un_oct'] = []
        self.parsed_request['voice_role_fifth'] = []
        self.parsed_request['voice_role_fourth'] = []
        self.parsed_request['voice_role_above'] = []
        self.parsed_request['voice_role_below'] = []

        def __get_voice_value(voice):
            ret = None
            for k, v in qdict.lists():
                if voice == k.split("_")[-1]:
                    ret = v[0]
                    break
            if ret in ("S", "T", "Ct", "B"):
                return ret
            else:
                return None

        def __parse_entry(entry, values):
            checked = [v for v in values if v is not None]

            if len(checked) > 1:
                q = [checked[0], checked[1]]
            elif len(checked) == 1:
                q = [checked[0]]
            else:
                return

            if entry == 'un_oct':
                # d1 = __get_voice_value('dux1')
                self.parsed_request['voice_role_un_oct'].extend(q)
            elif entry == 'fifth':
                self.parsed_request['voice_role_fifth'].extend(q)
            elif entry == 'fourth':
                self.parsed_request['voice_role_fourth'].extend(q)
            else:
                # wildcard for this field
                pass

        def __parse_position(entry, values):
            checked = [v for v in values if v is not None]

            if len(checked) > 1:
                q = [checked[0], checked[1]]
            elif len(checked) == 1:
                q = [checked[0]]
            else:
                return

            if entry == 'above':
                self.parsed_request['voice_role_above'].extend(q)
            elif entry == 'below':
                self.parsed_request['voice_role_below'].extend(q)
            else:
                # wildcard
                pass

        for k, v in qdict.lists():
            if '_comes1_entry' in k:
                c1 = __get_voice_value('comes1')
                c2 = __get_voice_value('comes2')
                __parse_entry(v[0], [c1, c2])

            if '_dux2_entry' in k:
                d2 = __get_voice_value('dux2')
                __parse_entry(v[0], [d2])

            if '_comes1_position' in k:
                c1 = __get_voice_value('comes1')
                c2 = __get_voice_value('comes2')
                __parse_position(v[0], [c1, c2])

            if '_dux2_position' in k:
                d2 = __get_voice_value('dux2')
                __parse_position(v[0], [d2])

            if "_stretto" in k:
                if 'other_contrapuntal' in self.parsed_request.keys():
                    self.parsed_request['other_contrapuntal'].append('Stretto Fuga')
                else:
                    self.parsed_request['other_contrapuntal'] = []
                    self.parsed_request['other_contrapuntal'].append('Stretto Fuga')

            if "_invertible" in k:
                if 'other_contrapuntal' in self.parsed_request.keys():
                    self.parsed_request['other_contrapuntal'].append('Invertible Counterpoint')
                else:
                    self.parsed_request['other_contrapuntal'] = []
                    self.parsed_request['other_contrapuntal'].append('Invertible Counterpoint')

    def _parse_request(self):
        self._parse_voice_filter()
        self._parse_prestypes()

        qdict = self.request.GET
        for k, v in qdict.lists():
            if k not in settings.SEARCH_PARAM_MAP.keys():
                continue
            self.parsed_request[settings.SEARCH_PARAM_MAP[k]] = v

    def _prep_q(self):
        if self.parsed_request:
            arr = []
            for k, v in self.parsed_request.items():
                if not v:
                    continue
                if k == 'q':
                    if v[0] != u'':
                        arr.insert(0, u"{0}".format(v[0]))
                else:
                    arr.append(u"{0}:({1})".format(k, " OR ".join(["\"{0}\"".format(s) for s in v if v is not None])))
            self.prepared_query = u" AND ".join(arr)
        else:
            self.prepared_query = u"*:*"