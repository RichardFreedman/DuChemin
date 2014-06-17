# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DCPerson'
        db.create_table(u'duchemin_dcperson', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person_id', self.gf('django.db.models.fields.CharField')(max_length=16, unique=True, null=True, db_index=True)),
            ('surname', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=64, null=True, blank=True)),
            ('given_name', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('birth_date', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('death_date', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('active_date', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('alt_spelling', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('remarks', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('duchemin', ['DCPerson'])

        # Adding model 'DCBook'
        db.create_table(u'duchemin_dcbook', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('book_id', self.gf('django.db.models.fields.IntegerField')(unique=True, db_index=True)),
            ('title', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=128, null=True, blank=True)),
            ('complete_title', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('publisher', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('place_publication', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('volumes', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('part_st_id', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('part_sb_id', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('num_compositions', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('num_pages', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('rism', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('cesr', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('remarks', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
        ))
        db.send_create_signal('duchemin', ['DCBook'])

        # Adding model 'DCFile'
        db.create_table(u'duchemin_dcfile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('attachment', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('duchemin', ['DCFile'])

        # Adding model 'DCPiece'
        db.create_table(u'duchemin_dcpiece', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('piece_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=16, db_index=True)),
            ('book_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['duchemin.DCBook'], to_field='book_id')),
            ('book_position', self.gf('django.db.models.fields.IntegerField')(max_length=16, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('composer_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['duchemin.DCPerson'], to_field='person_id')),
            ('composer_src', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('forces', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('print_concordances', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('ms_concordances', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('pdf_link', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('mei_link', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('audio_link', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('duchemin', ['DCPiece'])

        # Adding M2M table for field attachments on 'DCPiece'
        db.create_table(u'duchemin_dcpiece_attachments', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('dcpiece', models.ForeignKey(orm['duchemin.dcpiece'], null=False)),
            ('dcfile', models.ForeignKey(orm['duchemin.dcfile'], null=False))
        ))
        db.create_unique(u'duchemin_dcpiece_attachments', ['dcpiece_id', 'dcfile_id'])

        # Adding model 'DCPhrase'
        db.create_table(u'duchemin_dcphrase', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('phrase_id', self.gf('django.db.models.fields.IntegerField')(unique=True, db_index=True)),
            ('piece_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['duchemin.DCPiece'], to_field='piece_id')),
            ('phrase_num', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('phrase_start', self.gf('django.db.models.fields.CharField')(max_length=4, null=True, blank=True)),
            ('phrase_stop', self.gf('django.db.models.fields.CharField')(max_length=4, null=True, blank=True)),
            ('phrase_text', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('rhyme', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
        ))
        db.send_create_signal('duchemin', ['DCPhrase'])

        # Adding model 'DCAnalysis'
        db.create_table(u'duchemin_dcanalysis', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('analyst', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['duchemin.DCPerson'], to_field='person_id')),
            ('composition_number', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['duchemin.DCPiece'], to_field='piece_id')),
            ('phrase_number', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['duchemin.DCPhrase'], to_field='phrase_id')),
            ('start_measure', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('stop_measure', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('cadence', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('cadence_kind', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('cadence_alter', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('cadence_role_cantz', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('cadence_role_tenz', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('cadence_final_tone', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('voices_p6_up', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('voices_p6_lo', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('voices_p3_up', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('voices_p3_lo', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('voices_53_up', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('voices_53_lo', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('other_formulas', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('other_pres_type', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('voice_role_up1_nim', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('voice_role_lo1_nim', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('voice_role_up2_nim', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('voice_role_lo2_nim', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('voice_role_dux1', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('voice_role_com1', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('voice_role_dux2', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('voice_role_com2', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('voice_role_un_oct', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('voice_role_fifth', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('voice_role_fourth', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('voice_role_above', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('voice_role_below', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('other_contrapuntal', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('text_treatment', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('repeat_kind', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('earlier_phrase', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('repeat_exact_varied', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('needs_review', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('duchemin', ['DCAnalysis'])

        # Adding model 'DCReconstruction'
        db.create_table(u'duchemin_dcreconstruction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('piece', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['duchemin.DCPiece'], to_field='piece_id')),
            ('reconstructor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['duchemin.DCPerson'], to_field='person_id')),
        ))
        db.send_create_signal('duchemin', ['DCReconstruction'])

        # Adding M2M table for field attachments on 'DCReconstruction'
        db.create_table(u'duchemin_dcreconstruction_attachments', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('dcreconstruction', models.ForeignKey(orm['duchemin.dcreconstruction'], null=False)),
            ('dcfile', models.ForeignKey(orm['duchemin.dcfile'], null=False))
        ))
        db.create_unique(u'duchemin_dcreconstruction_attachments', ['dcreconstruction_id', 'dcfile_id'])

        # Adding model 'DCUserProfile'
        db.create_table(u'duchemin_dcuserprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['duchemin.DCPerson'], null=True, blank=True)),
        ))
        db.send_create_signal('duchemin', ['DCUserProfile'])

        # Adding M2M table for field favourited_piece on 'DCUserProfile'
        db.create_table(u'duchemin_dcuserprofile_favourited_piece', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('dcuserprofile', models.ForeignKey(orm['duchemin.dcuserprofile'], null=False)),
            ('dcpiece', models.ForeignKey(orm['duchemin.dcpiece'], null=False))
        ))
        db.create_unique(u'duchemin_dcuserprofile_favourited_piece', ['dcuserprofile_id', 'dcpiece_id'])

        # Adding M2M table for field favourited_analysis on 'DCUserProfile'
        db.create_table(u'duchemin_dcuserprofile_favourited_analysis', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('dcuserprofile', models.ForeignKey(orm['duchemin.dcuserprofile'], null=False)),
            ('dcanalysis', models.ForeignKey(orm['duchemin.dcanalysis'], null=False))
        ))
        db.create_unique(u'duchemin_dcuserprofile_favourited_analysis', ['dcuserprofile_id', 'dcanalysis_id'])

        # Adding M2M table for field favourited_reconstruction on 'DCUserProfile'
        db.create_table(u'duchemin_dcuserprofile_favourited_reconstruction', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('dcuserprofile', models.ForeignKey(orm['duchemin.dcuserprofile'], null=False)),
            ('dcreconstruction', models.ForeignKey(orm['duchemin.dcreconstruction'], null=False))
        ))
        db.create_unique(u'duchemin_dcuserprofile_favourited_reconstruction', ['dcuserprofile_id', 'dcreconstruction_id'])

        # Adding model 'DCContentBlock'
        db.create_table(u'duchemin_dccontentblock', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('content_type', self.gf('django.db.models.fields.CharField')(default='block', max_length=32)),
            ('position', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal('duchemin', ['DCContentBlock'])


    def backwards(self, orm):
        # Deleting model 'DCPerson'
        db.delete_table(u'duchemin_dcperson')

        # Deleting model 'DCBook'
        db.delete_table(u'duchemin_dcbook')

        # Deleting model 'DCFile'
        db.delete_table(u'duchemin_dcfile')

        # Deleting model 'DCPiece'
        db.delete_table(u'duchemin_dcpiece')

        # Removing M2M table for field attachments on 'DCPiece'
        db.delete_table('duchemin_dcpiece_attachments')

        # Deleting model 'DCPhrase'
        db.delete_table(u'duchemin_dcphrase')

        # Deleting model 'DCAnalysis'
        db.delete_table(u'duchemin_dcanalysis')

        # Deleting model 'DCReconstruction'
        db.delete_table(u'duchemin_dcreconstruction')

        # Removing M2M table for field attachments on 'DCReconstruction'
        db.delete_table('duchemin_dcreconstruction_attachments')

        # Deleting model 'DCUserProfile'
        db.delete_table(u'duchemin_dcuserprofile')

        # Removing M2M table for field favourited_piece on 'DCUserProfile'
        db.delete_table('duchemin_dcuserprofile_favourited_piece')

        # Removing M2M table for field favourited_analysis on 'DCUserProfile'
        db.delete_table('duchemin_dcuserprofile_favourited_analysis')

        # Removing M2M table for field favourited_reconstruction on 'DCUserProfile'
        db.delete_table('duchemin_dcuserprofile_favourited_reconstruction')

        # Deleting model 'DCContentBlock'
        db.delete_table(u'duchemin_dccontentblock')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'duchemin.dcanalysis': {
            'Meta': {'object_name': 'DCAnalysis'},
            'analyst': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['duchemin.DCPerson']", 'to_field': "'person_id'"}),
            'cadence': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'cadence_alter': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'cadence_final_tone': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'cadence_kind': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'cadence_role_cantz': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'cadence_role_tenz': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'composition_number': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['duchemin.DCPiece']", 'to_field': "'piece_id'"}),
            'earlier_phrase': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'needs_review': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'other_contrapuntal': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'other_formulas': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'other_pres_type': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'phrase_number': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['duchemin.DCPhrase']", 'to_field': "'phrase_id'"}),
            'repeat_exact_varied': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'repeat_kind': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'start_measure': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'stop_measure': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'text_treatment': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'voice_role_above': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'voice_role_below': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'voice_role_com1': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'voice_role_com2': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'voice_role_dux1': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'voice_role_dux2': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'voice_role_fifth': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'voice_role_fourth': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'voice_role_lo1_nim': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'voice_role_lo2_nim': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'voice_role_un_oct': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'voice_role_up1_nim': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'voice_role_up2_nim': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'voices_53_lo': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'voices_53_up': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'voices_p3_lo': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'voices_p3_up': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'voices_p6_lo': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'voices_p6_up': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'})
        },
        'duchemin.dcbook': {
            'Meta': {'object_name': 'DCBook'},
            'book_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'db_index': 'True'}),
            'cesr': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'complete_title': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'num_compositions': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'num_pages': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'part_sb_id': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'part_st_id': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'place_publication': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'publisher': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'remarks': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'rism': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'volumes': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'})
        },
        'duchemin.dccontentblock': {
            'Meta': {'object_name': 'DCContentBlock'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'content_type': ('django.db.models.fields.CharField', [], {'default': "'block'", 'max_length': '32'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'duchemin.dcfile': {
            'Meta': {'object_name': 'DCFile'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'duchemin.dcperson': {
            'Meta': {'object_name': 'DCPerson'},
            'active_date': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'alt_spelling': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'birth_date': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'death_date': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'given_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person_id': ('django.db.models.fields.CharField', [], {'max_length': '16', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'surname': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '64', 'null': 'True', 'blank': 'True'})
        },
        'duchemin.dcphrase': {
            'Meta': {'ordering': "['piece_id', 'phrase_num']", 'object_name': 'DCPhrase'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phrase_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'db_index': 'True'}),
            'phrase_num': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'phrase_start': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'phrase_stop': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'phrase_text': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'piece_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['duchemin.DCPiece']", 'to_field': "'piece_id'"}),
            'rhyme': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'})
        },
        'duchemin.dcpiece': {
            'Meta': {'object_name': 'DCPiece'},
            'attachments': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['duchemin.DCFile']", 'null': 'True', 'blank': 'True'}),
            'book_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['duchemin.DCBook']", 'to_field': "'book_id'"}),
            'book_position': ('django.db.models.fields.IntegerField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'composer_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['duchemin.DCPerson']", 'to_field': "'person_id'"}),
            'composer_src': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'forces': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ms_concordances': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'pdf_link': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'mei_link': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'audio_link': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'piece_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '16', 'db_index': 'True'}),
            'print_concordances': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'})
        },
        'duchemin.dcreconstruction': {
            'Meta': {'object_name': 'DCReconstruction'},
            'attachments': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['duchemin.DCFile']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'piece': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['duchemin.DCPiece']", 'to_field': "'piece_id'"}),
            'reconstructor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['duchemin.DCPerson']", 'to_field': "'person_id'"})
        },
        'duchemin.dcuserprofile': {
            'Meta': {'object_name': 'DCUserProfile'},
            'favourited_analysis': ('django.db.models.fields.related.ManyToManyField', [], {'db_index': 'True', 'to': "orm['duchemin.DCAnalysis']", 'symmetrical': 'False', 'blank': 'True'}),
            'favourited_piece': ('django.db.models.fields.related.ManyToManyField', [], {'db_index': 'True', 'to': "orm['duchemin.DCPiece']", 'symmetrical': 'False', 'blank': 'True'}),
            'favourited_reconstruction': ('django.db.models.fields.related.ManyToManyField', [], {'db_index': 'True', 'to': "orm['duchemin.DCReconstruction']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['duchemin.DCPerson']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['duchemin']