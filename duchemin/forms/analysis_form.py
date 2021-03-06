from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, Button, MultiField, HTML
from crispy_forms.bootstrap import FormActions, InlineCheckboxes, InlineRadios

from duchemin.models.phrase import DCPhrase

CADENCE_KIND_CHOICES = [("", ""),
                        ("Authentic", "Authentic"),
                        ("Plagal", "Plagal"),
                        ("Phrygian", "Phrygian"),
                        ("CadInCad", "CadInCad"),
                        ("CAD NDLT", "CAD NDLT"),
                        ("NoCadence", "NoCadence")]

CADENCE_ALTER_CHOICES = [("Displaced", "Displaced"),
                         ("Inverted", "Inverted"),
                         ("Incomplete", "Incomplete"),
                         ("Evaded", "Evaded"),
                         ("Other", "Other")]

FOUR_VOICES = [("S", "S"),
               ("Ct", "Ct"),
               ("T", "T"),
               ("B", "B"),
               ("", "")]

FINAL_TONE_CHOICES = [("", ""),
                      ("A", "A"),
                      ("B-flat", "B-flat"),
                      ("C", "C"),
                      ("D", "D"),
                      ("E", "E"),
                      ("F", "F"),
                      ("G", "G")]

FORMULA_CHOICES = [("Romanesca", "Romanesca"), ]

CONTRAPUNTAL_CHOICES = [("Invertible Counterpoint", "Invertible Counterpoint"),
                        ("Stretto Fuga", "Stretto Fuga"),
                        ("Other", "Other")]

TEXT_TREATMENT_CHOICES = [("", ""),
                          ("Text Representation", "Text Representation"),
                          ("Text Declamation", "Text Declamation"),
                          ("Text Overlap", "Text Overlap"),
                          ("Text Pause", "Text Pause"),
                          ("Text Enjambment", "Text Enjambment"),
                          ("Other", "Other")]

REPEAT_CHOICES = [("", ""),
                  ("Direct Repeat", "Direct Repeat"),
                  ("Refrain", "Refrain"),
                  ("Da Capo", "Da Capo"),
                  ("Final Repeat", "Final Repeat"),
                  ("Other", "Other")]

PRESENTATION_TYPE_CHOICES = [("", ""),
                             ("FI", "FI"),
                             ("ID", "ID"),
                             ("PEn", "PEn"),
                             ("PEn Tonal", "PEn Tonal"),
                             ("PEn Stacked", "PEn Stacked"),
                             ("NIM", "NIM"),
                             ("HR Dactyll", "HR Dactyll"),
                             ("HR Simple", "HR Simple"),
                             ("HR Stagger", "HR Stagger"),
                             ("HR Dance", "HR Dance"),
                             ("HR Fauxbourdon", "HR Fauxbourdon")]


class AnalysisForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(AnalysisForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'DuChemin Observation Form',
                'phrase_number',
                'start_measure',
                'stop_measure'
            ),
            Fieldset(
                'Cadence',
                HTML("<p>If not a cadence, skip to next section!</p>"),
                'cadence',
                'cadence_kind',
                'cadence_alter',
                'cadence_alter_other',
                MultiField("Cadence Voice Roles",
                    InlineRadios('cadence_role_cantz'),
                    InlineRadios('cadence_role_tenz')
                ),
                'cadence_final_tone'),
            Fieldset(
                'Interval Formula',
                MultiField("Voice Roles",
                    InlineRadios('voices_p6_up'),
                    InlineRadios('voices_p6_lo'),
                    InlineRadios('voices_p3_up'),
                    InlineRadios('voices_p3_lo'),
                    InlineRadios('voices_53_up'),
                    InlineRadios('voices_53_lo')
                ),
                'other_formulas'),
            Fieldset(
                'Presentation Type or Texture',
                'other_pres_type',
                MultiField("Voice Roles",
                    HTML("<p>Use only those rows that apply to the chosen type. @ intervals and direction are relative to previous entry.</p>"),
                    InlineRadios('voice_role_up1_nim'),
                    InlineRadios('voice_role_lo1_nim'),
                    InlineRadios('voice_role_up2_nim'),
                    InlineRadios('voice_role_lo2_nim'),
                    InlineRadios('voice_role_dux1'),
                    InlineRadios('voice_role_com1'),
                    InlineRadios('voice_role_dux2'),
                    InlineRadios('voice_role_com2'),
                    InlineRadios('voice_role_un_oct'),
                    InlineRadios('voice_role_fifth'),
                    InlineRadios('voice_role_fourth'),
                ),
                'other_contrapuntal',
                'other_contrapuntal_other'),
            Fieldset(
                'Text Treatment',
                HTML("<p>Use COMMENT to Elaborate if needed. ENJAMBEMENT tag goes with LEADING phrase. OVERLAP tag goes with FOLLOWING phrase.</p>"),
                'text_treatment',
                'text_treatment_other'),
            Fieldset(
                'Musical Form',
                HTML("<p>Any pattern of large-scale repetition or return? In case of PHRASE repetition, the START/STOP measures refer to the entire phrase. Use COMMENT to explain VARIED.</p>"),
                'repeat_kind',
                'earlier_phrase',
                'repeat_exact_varied'),
            Fieldset(
                'Comment Space',
                'comment'),
            FormActions(
                Submit('save', 'Save changes'),
                Button('cancel', 'Cancel')
            )
        )
        self.helper.form_method = 'post'

    phrase_number = forms.ModelChoiceField(queryset=DCPhrase.objects.all())
    start_measure = forms.IntegerField()
    stop_measure = forms.IntegerField()
    cadence = forms.BooleanField(required=False)
    cadence_kind = forms.TypedChoiceField(choices=CADENCE_KIND_CHOICES, required=False, help_text="See INSTRUCTIONS for treatment of Phrygian, Plagal, CadInCad and NOCadence types", empty_value=None)
    cadence_alter = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=CADENCE_ALTER_CHOICES, required=False)
    cadence_alter_other = forms.CharField(required=False, label="If Other, Please Specify:")
    cadence_role_cantz = forms.TypedChoiceField(required=False, choices=FOUR_VOICES, widget=forms.RadioSelect, label="Cantizans", empty_value=None)
    cadence_role_tenz = forms.TypedChoiceField(required=False, choices=FOUR_VOICES, widget=forms.RadioSelect, label="Tenorizans", empty_value=None)
    cadence_final_tone = forms.TypedChoiceField(required=False, choices=FINAL_TONE_CHOICES, empty_value=None)
    voices_p6_up = forms.TypedChoiceField(required=False, choices=FOUR_VOICES, widget=forms.RadioSelect, label="Parallel 6th Upper", empty_value=None)
    voices_p6_lo = forms.TypedChoiceField(required=False, choices=FOUR_VOICES, widget=forms.RadioSelect, label="Parallel 6th Lower", empty_value=None)
    voices_p3_up = forms.TypedChoiceField(required=False, choices=FOUR_VOICES, widget=forms.RadioSelect, label="Parallel 3rd Upper", empty_value=None)
    voices_p3_lo = forms.TypedChoiceField(required=False, choices=FOUR_VOICES, widget=forms.RadioSelect, label="Parallel 3rd Lower", empty_value=None)
    voices_53_up = forms.TypedChoiceField(required=False, choices=FOUR_VOICES, widget=forms.RadioSelect, label="5/3 Upper", empty_value=None)
    voices_53_lo = forms.TypedChoiceField(required=False, choices=FOUR_VOICES, widget=forms.RadioSelect, label="5/3 Lower", empty_value=None)
    other_formulas = forms.MultipleChoiceField(required=False, choices=FORMULA_CHOICES, widget=forms.CheckboxSelectMultiple, help_text="Use as many combinations as apply, indicating which voices.")
    other_pres_type = forms.TypedChoiceField(required=False, choices=PRESENTATION_TYPE_CHOICES, label="Does this seem to be a conventional texture or presentation type?", help_text="If no type, leave blank and skip to next section.", empty_value=None)
    voice_role_up1_nim = forms.TypedChoiceField(required=False, choices=FOUR_VOICES, widget=forms.RadioSelect, label="Upper Voice 1 (NIM)", empty_value=None)
    voice_role_lo1_nim = forms.TypedChoiceField(required=False, choices=FOUR_VOICES, widget=forms.RadioSelect, label="Lower Voice 1 (NIM)", empty_value=None)
    voice_role_up2_nim = forms.TypedChoiceField(required=False, choices=FOUR_VOICES, widget=forms.RadioSelect, label="Upper Voice 2 (NIM)", empty_value=None)
    voice_role_lo2_nim = forms.TypedChoiceField(required=False, choices=FOUR_VOICES, widget=forms.RadioSelect, label="Lower Voice 2 (NIM)", empty_value=None)
    voice_role_dux1 = forms.TypedChoiceField(required=False, choices=FOUR_VOICES, widget=forms.RadioSelect, label="Dux 1 (FI ID or PEn)", empty_value=None)
    voice_role_com1 = forms.TypedChoiceField(required=False, choices=FOUR_VOICES, widget=forms.RadioSelect, label="Comes 1 (FI ID or PEn)", empty_value=None)
    voice_role_dux2 = forms.TypedChoiceField(required=False, choices=FOUR_VOICES, widget=forms.RadioSelect, label="Dux 2 (ID or PEn)", empty_value=None)
    voice_role_com2 = forms.TypedChoiceField(required=False, choices=FOUR_VOICES, widget=forms.RadioSelect, label="Comes 2 (ID or PEn)", empty_value=None)
    voice_role_un_oct = forms.TypedChoiceField(required=False, choices=FOUR_VOICES, widget=forms.RadioSelect, label="@1 or 8", empty_value=None)
    voice_role_fifth = forms.TypedChoiceField(required=False, choices=FOUR_VOICES, widget=forms.RadioSelect, label="@5", empty_value=None)
    voice_role_fourth = forms.TypedChoiceField(required=False, choices=FOUR_VOICES, widget=forms.RadioSelect, label="@4", empty_value=None)
    other_contrapuntal = forms.MultipleChoiceField(required=False, choices=CONTRAPUNTAL_CHOICES, widget=forms.CheckboxSelectMultiple, label="Other Features?")
    other_contrapuntal_other = forms.CharField(required=False, label="If Other, Please Specify:")
    text_treatment = forms.TypedChoiceField(required=False, choices=TEXT_TREATMENT_CHOICES, empty_value=None)
    text_treatment_other = forms.CharField(required=False, label="If Other, Please Specify:")
    repeat_kind = forms.TypedChoiceField(required=False, choices=REPEAT_CHOICES, empty_value=None)
    earlier_phrase = forms.ModelChoiceField(required=False, queryset=DCPhrase.objects.all(), label="To which earlier phrase does the CURRENT phrase correspond?")
    comment = forms.CharField(widget=forms.Textarea, required=False)
    repeat_exact_varied = forms.TypedChoiceField(required=False, choices=[("", ""), ("Exact", "Exact"), ("Varied", "Varied")], label="Exact or Varied?", empty_value=None)
