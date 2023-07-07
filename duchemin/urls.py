from django.urls import include, path, re_path
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.contrib.flatpages.views import flatpage
from duchemin.views.analysis import AnalysisList, AnalysisDetail
from duchemin.views.person import PersonList, PersonDetail
from duchemin.views.phrase import PhraseList, PhraseDetail
from duchemin.views.comment import CommentList, CommentDetail
from duchemin.views.note import NoteList, NoteDetail
from duchemin.views.user import UserList, UserDetail
from duchemin.views.auth import SessionAuth, SessionStatus, SessionClose
from duchemin.views.main import *
from django.conf.urls.static import static
from duchemin.views.data import *
from duchemin.views.callbacks import *
from duchemin.views.search import *
from django.urls import path


# Uncomment the next two lines to enable the admin:
from django.contrib import admin

from rest_framework.authtoken.views import obtain_auth_token
admin.autodiscover()

urlpatterns = []

if 'django.contrib.admin' in settings.INSTALLED_APPS:
    urlpatterns += [
        path('admin/', admin.site.urls)
    ]

    urlpatterns += [
        path('', home, name='home'),
        path('auth/token/', obtain_auth_token),
        path('auth/session/', SessionAuth.as_view()),
        path('auth/status/', SessionStatus.as_view()),
        path('auth/logout/', SessionClose.as_view()),
        path('piece/<str:piece_id>/add-observation/', add_observation, name = "add_observation"),
        path('piece/<str:piece_id>/discussion/', discussion),
        path('piece/<str:pk>/', piece, name="dcpiece-detail"),
        path('pieces/', pieces, name="dcpiece-list"),

        path('book/<int:pk>/', book, name="dcbook-detail"),
        path('books/', books, name="dcbook-list"),

        path('profile/', profile),

        path('reconstructions/', reconstructions),
        path('reconstruction/<int:reconstruction_id>/', reconstruction),

        path('people/', PersonList.as_view(), name="dcperson-list"),
        re_path(r'^person/(?P<pk>\d+)/$', PersonDetail.as_view(), name="dcperson-detail"),

        path('analyses/', AnalysisList.as_view(), name="dcanalysis-list"),
        path('analysis/<int:pk>/', AnalysisDetail.as_view(), name="dcanalysis-detail"),

        path('phrases/', PhraseList.as_view(), name="dcphrase-list"),
        path('phrase/<int:pk>/', PhraseDetail.as_view(), name="dcphrase-detail"),

        path('users/', UserList.as_view(), name="user-list"),
        path('user/<int:pk>/', UserDetail.as_view(), name="user-detail"),

        path('comments/', CommentList.as_view(), name="dccomment-list"),
        path('comment/<int:pk>/', CommentDetail.as_view(), name='dccomment-detail'),

        path('notes/', NoteList.as_view(), name="dcnote-list"),
        path('note/<str:pk>/', NoteDetail.as_view(), name='dcnote-detail'),

        path('password_change/', my_password_change),
    ]

    urlpatterns += [
        path('search/', search, name="search"),
    ]

    urlpatterns += [
        path('data/analysis/<int:anid>/', analysis),
        path('data/phrase/<str:piece_id>/<int:phrase_id>/', phrase)
    ]

    urlpatterns += [
        path('search/results/<str:restype>/', result_callback),
        path('favourite/<str:ftype>/<str:fid>/', favourite_callback)
        ]

    urlpatterns += [
        path('login/', auth_views.LoginView.as_view(extra_context={'next': '/profile'}), name='login'),
        path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout')]

    urlpatterns += [
        path('about/', flatpage, {'url':'/about/'},name="about")
]



    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



# urlpatterns = patterns('',
#     # Examples:
#     url(r'^$', 'duchemin.views.home', name='home'),
#     # url(r'^duchemin/', include('duchemin.foo.urls')),

#     # Uncomment the admin/doc line below to enable admin documentation:
#     # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

#     # Uncomment the next line to enable the admin:
#     url(r'^admin/', include(admin.site.urls)),
# )
