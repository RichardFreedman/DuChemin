from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from duchemin.admin.actions import export_as_csv_action

from duchemin.models.analysis import DCAnalysis
from duchemin.models.book import DCBook
from duchemin.models.person import DCPerson
from duchemin.models.phrase import DCPhrase
from duchemin.models.piece import DCPiece
from duchemin.models.reconstruction import DCReconstruction
from duchemin.models.userprofile import DCUserProfile
from duchemin.models.file import DCFile
from duchemin.models.content_block import DCContentBlock
from duchemin.models.comment import DCComment
from duchemin.models.note import DCNote


class DCAnalysisAdmin(admin.ModelAdmin):
    MODEL_FIELDS = (
            "timestamp",
            "analyst",
            "composition_number",
            "phrase_number",
            "start_measure",
            "stop_measure",
            "cadence",
            "cadence_kind",
            "cadence_alter",
            "cadence_role_cantz",
            "cadence_role_tenz",
            "cadence_final_tone",
            "voices_p6_up",
            "voices_p6_lo",
            "voices_p3_up",
            "voices_p3_lo",
            "voices_53_up",
            "voices_53_lo",
            "other_formulas",
            "other_pres_type",
            "voice_role_up1_nim",
            "voice_role_lo1_nim",
            "voice_role_up2_nim",
            "voice_role_lo2_nim",
            "voice_role_dux1",
            "voice_role_com1",
            "voice_role_dux2",
            "voice_role_com2",
            "voice_role_un_oct",
            "voice_role_fifth",
            "voice_role_fourth",
            "voice_role_above",
            "voice_role_below",
            "other_contrapuntal",
            "text_treatment",
            "repeat_kind",
            "earlier_phrase",
            "comment",
            "repeat_exact_varied"
        )
    list_display = ["id", 'analyst', 'phrase_number', 'start_measure', 'stop_measure']
    search_fields = ["id", 'analyst__surname', 'composition_number__title']
    list_filter = ('needs_review',)
    actions = [export_as_csv_action("Export as CSV", fields=MODEL_FIELDS)]


class DCPersonAdmin(admin.ModelAdmin):
    MODEL_FIELDS = (
            "person_id",
            "surname",
            "given_name",
            "birth_date",
            "death_date",
            "active_date",
            "alt_spelling",
            "remarks"
        )
    list_display = ['full_name', 'birth_date', 'death_date', 'active_date', 'alt_spelling']
    search_fields = ['surname', 'given_name', 'alt_spelling']
    actions = [export_as_csv_action("Export as CSV", fields=MODEL_FIELDS)]


class DCBookAdmin(admin.ModelAdmin):
    MODEL_FIELDS = (
            "book_id",
            "title",
            "complete_title",
            "publisher",
            "place_publication",
            "date",
            "volumes",
            "part_st_id",
            "part_sb_id",
            "num_compositions",
            "num_pages",
            "location",
            "rism",
            "cesr",
            "remarks"
        )
    list_display = ['title', 'publisher', 'place_publication', 'date', 'volumes', 'num_compositions', 'num_pages', 'location']
    search_fields = ['title']
    actions = [export_as_csv_action("Export as CSV", fields=MODEL_FIELDS)]

# # Include only if "attachments" instead of "mei_file"
# 
# class DCFilePieceInline(admin.TabularInline):
#     model = DCPiece.attachments.through
#     can_delete = True
#     verbose_name = "File"
#     verbose_name_plural = "Files"


class DCPieceAdmin(admin.ModelAdmin):
    MODEL_FIELDS = (
            "piece_id",
            "book_id",
            "book_position",
            "title",
            "composer_id",
            "composer_src",
            "forces",
            "print_concordances",
            "ms_concordances"
        )
#     inlines = (
#         DCFilePieceInline,
#     )
    search_fields = ('piece_id', 'book_id__title', 'title', 'print_concordances', 'ms_concordances')
    list_display = ('piece_id', 'title', 'composer_id', 'composer_src', 'forces', 'print_concordances', 'ms_concordances')
    # Add 'book_id', 'book_position', above if these become necessary -- but for now piece_id is fine
    ordering = ('piece_id',)
    actions = [export_as_csv_action]

class DCFileReconstructionInline(admin.TabularInline):
    model = DCReconstruction.attachments.through
    can_delete = True
    verbose_name = "File"
    verbose_name_plural = "Files"


class DCReconstructionAdmin(admin.ModelAdmin):
    list_display = ['piece', 'reconstructor',]
    ordering = ['piece', 'reconstructor',]
    actions = [export_as_csv_action]


class DCPhraseAdmin(admin.ModelAdmin):
    # If we want to show only piece ID, not title of piece
    def get_piece_id(self, obj):
        return obj.piece_id.piece_id
    get_piece_id.short_description = 'Piece'

    list_display = ['phrase_id', 'get_piece_id', 'phrase_num', 'phrase_start', 'phrase_stop', 'phrase_text']
    list_editable = ['phrase_start', 'phrase_stop']
    ordering = ('piece_id','phrase_num',)
    change_list_template = "admin/change_list_pagination_top.html"
    actions = [export_as_csv_action("Export as CSV", fields=['phrase_id', 'piece_id', 'phrase_num', 'phrase_start', 'phrase_stop', 'phrase_text'])]


class DCCommentAdmin(admin.ModelAdmin):
    list_display = ['piece', 'author', 'created', 'text',]
    ordering = ['piece', 'created',]
    actions = [export_as_csv_action]


class DCNoteAdmin(admin.ModelAdmin):
    list_display = ['piece', 'author', 'time', 'text',]
    ordering = ['piece', 'time',]
    actions = [export_as_csv_action]


class UserProfileInline(admin.StackedInline):
    model = DCUserProfile
    can_delete = False
    verbose_name_plural = 'profile'


class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(DCUserProfile)
admin.site.register(DCAnalysis, DCAnalysisAdmin)
admin.site.register(DCBook, DCBookAdmin)
admin.site.register(DCPerson, DCPersonAdmin)
admin.site.register(DCPhrase, DCPhraseAdmin)
admin.site.register(DCPiece, DCPieceAdmin)
admin.site.register(DCReconstruction, DCReconstructionAdmin)
admin.site.register(DCFile)
admin.site.register(DCContentBlock)
admin.site.register(DCComment, DCCommentAdmin)
admin.site.register(DCNote, DCNoteAdmin)
