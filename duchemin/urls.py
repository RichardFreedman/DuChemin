from django.conf.urls import patterns, include, url
from django.conf import settings
from duchemin.views.analysis import AnalysisList, AnalysisDetail
from duchemin.views.person import PersonList, PersonDetail
from duchemin.views.phrase import PhraseList, PhraseDetail
from duchemin.views.comment import CommentList, CommentDetail
from duchemin.views.note import NoteList, NoteDetail
from duchemin.views.user import UserList, UserDetail
from duchemin.views.auth import SessionAuth, SessionStatus, SessionClose

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from rest_framework.authtoken.views import obtain_auth_token
admin.autodiscover()

urlpatterns = []

if 'django.contrib.admin' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^admin/', include(admin.site.urls))
    )

    urlpatterns += patterns('duchemin.views.main',
        url(r'^$', 'home', name='home'),
        url(r'^auth/token/$', obtain_auth_token),
        url(r'^auth/session/$', SessionAuth.as_view()),
        url(r'^auth/status/$', SessionStatus.as_view()),
        url(r'^auth/logout/$', SessionClose.as_view()),
        url(r'^piece/(?P<piece_id>[0-9a-zA-Z]+)/add-observation/$', 'add_observation'),
        url(r'^piece/(?P<piece_id>[0-9a-zA-Z]+)/discussion/$', 'discussion'),
        url(r'^piece/(?P<pk>[0-9a-zA-Z]+)/$', 'piece', name="dcpiece-detail"),
        url(r'^pieces/$', 'pieces', name="dcpiece-list"),

        url(r'^book/(?P<pk>[0-9]+)/$', 'book', name="dcbook-detail"),
        url(r'^books/$', 'books', name="dcbook-list"),

        url(r'^profile/', 'profile'),

        url(r'^reconstructions/$', 'reconstructions'),
        url(r'^reconstruction/(?P<reconstruction_id>[0-9]+)/$', 'reconstruction'),

        url(r'^people/$', PersonList.as_view(), name="dcperson-list"),
        url(r'^person/(?P<pk>[a-zA-Z0-9]+)/$', PersonDetail.as_view(), name="dcperson-detail"),

        url(r'^analyses/$', AnalysisList.as_view(), name="dcanalysis-list"),
        url(r'^analysis/(?P<pk>[0-9]+)/$', AnalysisDetail.as_view(), name="dcanalysis-detail"),

        url(r'^phrases/$', PhraseList.as_view(), name="dcphrase-list"),
        url(r'^phrase/(?P<pk>[0-9]+)/$', PhraseDetail.as_view(), name="dcphrase-detail"),

        url(r'^users/$', UserList.as_view(), name="user-list"),
        url(r'^user/(?P<pk>[0-9]+)/$', UserDetail.as_view(), name="user-detail"),

        url(r'^comments/$', CommentList.as_view(), name="dccomment-list"),
        url(r'^comment/(?P<pk>[0-9]+)/$', CommentDetail.as_view(), name='dccomment-detail'),

        url(r'^notes/$', NoteList.as_view(), name="dcnote-list"),
        url(r'^note/(?P<pk>[a-zA-Z0-9]+)/$', NoteDetail.as_view(), name='dcnote-detail'),

        url(r'^password_change/$', 'my_password_change'),
    )

    urlpatterns += patterns('duchemin.views.search',
        url(r'^search/$', 'search', name="search")
    )

    urlpatterns += patterns('duchemin.views.data',
        url(r'^data/analysis/(?P<anid>[0-9]+)/$', 'analysis'),
        url(r'^data/phrase/(?P<piece_id>[a-zA-Z0-9_]+)/(?P<phrase_id>[0-9]+)/$', 'phrase'),
    )

    urlpatterns += patterns('duchemin.views.callbacks',
        url(r'^search/results/(?P<restype>[0-9a-zA-Z]+)/$', 'result_callback'),
        url(r'^favourite/(?P<ftype>[a-zA-Z]+)/(?P<fid>[a-zA-Z0-9]+)/$', 'favourite_callback'),
    )

    urlpatterns += patterns('',
        url(r'^login/$', 'django.contrib.auth.views.login', {'extra_context': {'next': '/profile'}}),
        url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    )

    urlpatterns += patterns('django.contrib.flatpages.views',
        url(r'^about/$', 'flatpage', {'url': '/about/'}, name="about")
    )

# urlpatterns = patterns('',
#     # Examples:
#     url(r'^$', 'duchemin.views.home', name='home'),
#     # url(r'^duchemin/', include('duchemin.foo.urls')),

#     # Uncomment the admin/doc line below to enable admin documentation:
#     # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

#     # Uncomment the next line to enable the admin:
#     url(r'^admin/', include(admin.site.urls)),
# )
