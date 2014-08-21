import datetime
from django.shortcuts import render
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import password_change
from django.http import HttpResponseRedirect
from django.template import RequestContext

from duchemin.forms.analysis_form import AnalysisForm
from duchemin.models.piece import DCPiece
from duchemin.models.phrase import DCPhrase
from duchemin.models.analysis import DCAnalysis
from duchemin.models.book import DCBook
from duchemin.models.comment import DCComment
from duchemin.models.reconstruction import DCReconstruction
from duchemin.models.content_block import DCContentBlock
from duchemin.templatetags.notetext import notetext


def home(request):
    front_page_blocks = DCContentBlock.objects.filter(published=True, content_type="block").order_by('position')
    front_page_blocks = front_page_blocks[0:3]
    news_blocks = DCContentBlock.objects.filter(published=True, content_type="news").order_by('position')
    is_logged_in = False
    if request.user.is_authenticated():
        is_logged_in = True
    data = {
        'user': request.user,
        'front_page_blocks': front_page_blocks,
        'news_blocks': news_blocks,
        'is_logged_in': is_logged_in
    }
    return render(request, 'main/home.html', data)


def book(request, pk):
    try:
        book = DCBook.objects.get(book_id=pk)
        pieces = DCPiece.objects.filter(book_id=pk).order_by('book_position')
    except DCBook.DoesNotExist:
        raise Http404
    return render(request, 'main/book.html', {'book': book, 'pieces': pieces})


def books(request):
    books = DCBook.objects.all().order_by('id')
    paginator = Paginator(books, 25)

    page = request.GET.get('page')
    try:
        all_books = paginator.page(page)
    except PageNotAnInteger:
        all_books = paginator.page(1)
    except EmptyPage:
        all_books = paginator.page(paginator.num_pages)

    return render(request, 'main/books.html', {'books': all_books})


def pieces(request):
    pieces = DCPiece.objects.all().order_by('book_id__id', 'book_position')
    paginator = Paginator(pieces, 25)

    is_logged_in = False
    if request.user.is_authenticated():
        is_logged_in = True
        profile = request.user.profile
        favourite_pieces = profile.favourited_piece.all()
        for piece in pieces:
            if piece in favourite_pieces:
                piece.is_favourite = True
            else:
                piece.is_favourite = False

    page = request.GET.get('page')
    try:
        all_pieces = paginator.page(page)
    except PageNotAnInteger:
        all_pieces = paginator.page(1)
    except EmptyPage:
        all_pieces = paginator.page(paginator.num_pages)

    return render(request, 'main/pieces.html', {'pieces': all_pieces, 'is_logged_in': is_logged_in})


def piece(request, pk):
    # note: this is not the *actual* pk, it's the piece_id. This field name just makes REST Framework happy.
    # Redirect to url with uppercase piece ID
    if pk != pk.upper():
        return HttpResponseRedirect("/piece/{0}/".format(pk.upper()))
    try:
        piece = DCPiece.objects.get(piece_id=pk)
    except DCPiece.DoesNotExist:
        raise Http404

    is_favourite = False
    is_logged_in = False
    is_staff = False
    if request.user.is_authenticated():
        is_logged_in = True
        is_staff = request.user.is_staff
        profile = request.user.profile
        if profile.favourited_piece.filter(id=piece.id):
            is_favourite = True

    phrases = DCPhrase.objects.filter(piece_id=pk).order_by('phrase_num')

    # Typographically correct apostrophes in title and phrases
    piece.title = unicode(piece.title).replace(u"'", u"\u2019")
    for phrase in phrases:
        phrase.phrase_text = unicode(phrase.phrase_text).replace(u"'", u"\u2019")

    analyses = DCAnalysis.objects.filter(composition_number=pk).order_by('phrase_number__phrase_num', 'start_measure')
    reconstructions = DCReconstruction.objects.filter(piece=pk).order_by('piece')
    comments = DCComment.objects.filter(piece=piece).order_by('created')

    data = {
        'piece': piece,
        'piece_id' : pk,
        'phrases': phrases,
        'analyses': analyses,
        'reconstructions': reconstructions,
        'comments': comments,
        'is_favourite': is_favourite,
        'is_logged_in': is_logged_in,
        'is_staff': is_staff
    }
    return render(request, 'main/piece.html', data, context_instance=RequestContext(request))


def discussion(request, piece_id):
    # Redirect to url with uppercase piece ID
    if piece_id != piece_id.upper():
        return HttpResponseRedirect("/piece/{0}/discussion/".format(piece_id.upper()))
    try:
        piece = DCPiece.objects.get(piece_id=piece_id)
    except DCPiece.DoesNotExist:
        raise Http404

    is_favourite = False
    is_logged_in = False
    is_staff = False
    if request.user.is_authenticated():
        is_logged_in = True
        is_staff = request.user.is_staff
        profile = request.user.profile
        if profile.favourited_piece.filter(id=piece.id):
            is_favourite = True

    comments = DCComment.objects.filter(piece=piece).order_by('created')

    # Typographically correct apostrophes in title
    piece.title = unicode(piece.title).replace(u"'", u"\u2019")

    data = {
        'user': request.user,
        'piece': piece,
        'piece_id' : piece_id,
        'is_favourite': is_favourite,
        'is_logged_in': is_logged_in,
        'is_staff': is_staff,
        'comments': comments,
    }
    return render(request, 'main/discussion.html', data, context_instance=RequestContext(request))


def reconstructions(request):
    reconstructions = DCReconstruction.objects.all().order_by('piece__piece_id', 'reconstructor__surname')
    paginator = Paginator(reconstructions, 25)
    page = request.GET.get('page')
    try:
        all_r = paginator.page(page)
    except PageNotAnInteger:
        all_r = paginator.page(1)
    except EmptyPage:
        all_r = paginator.page(paginator.num_pages)

    return render(request, 'main/reconstructions.html', {'reconstructions': all_r})


def reconstruction(request, recon_id):
    try:
        recon = DCReconstruction.objects.get(pk=recon_id)
    except DCReconstruction.DoesNotExist:
        raise Http404

    data = {
        'reconstruction': recon
    }
    return render(request, 'main/reconstruction.html', data)


@login_required(login_url="/login/")
def my_password_change(request):
    return password_change(request, template_name='registration/password_change_form.html',
        post_change_redirect="/profile/",)


@login_required(login_url="/login/")
def profile(request):
    profile = request.user.profile

    analyses = None
    reconstructions = None
    discussed_pieces = []

    if profile.person:
        analyses = DCAnalysis.objects.filter(analyst=profile.person.person_id).order_by('composition_number')
        reconstructions = DCReconstruction.objects.filter(reconstructor=profile.person.person_id).order_by('piece')

    comments_by_piece_id = DCComment.objects.filter(author=request.user).order_by('piece')
    for comment in comments_by_piece_id:
        if comment.piece not in discussed_pieces:
            discussed_pieces.append(comment.piece)

    pieces_with_notes = []
    for piece in DCPiece.objects.all().order_by('piece_id'):
    	if notetext(request.user, piece):
    		pieces_with_notes.append(piece)

    data = {
        'user': request.user,
        'profile': profile,
        'favourited_pieces': profile.favourited_piece.order_by('piece_id'),
        'favourited_analyses': profile.favourited_analysis.order_by('piece_id'),
        'favourited_reconstructions': profile.favourited_reconstruction.order_by('piece'),
        'my_analyses': analyses,
        'my_reconstructions': reconstructions,
        'my_comments': DCComment.objects.filter(author=request.user).order_by('-created'),
        'discussed_pieces': discussed_pieces,
        'pieces_with_notes': pieces_with_notes,
    }
    return render(request, 'main/profile.html', data, context_instance=RequestContext(request))


def login(request):
    return render(request, 'main/login.html')


@login_required(login_url="/login/")
def add_observation(request, piece_id):
    # Redirect to url with uppercase piece ID
    if piece_id != piece_id.upper():
        return HttpResponseRedirect("/piece/{0}/add-observation/".format(piece_id.upper()))
    # return render(request, 'main/add_analysis.html', {})
    try:
        piece = DCPiece.objects.get(piece_id=piece_id)
    except DCPiece.DoesNotExist:
        raise Http404
    if request.method == "POST":
        form_data = AnalysisForm(request.POST)
        if not form_data.is_valid():
            return render(request, 'main/add_observation.html', {'form': form_data, 'piece': piece})

        #process data in form.cleaned_data()
        earlier_phrase = form_data.cleaned_data.get('earlier_phrase', None)
        if earlier_phrase:
            form_data.cleaned_data['earlier_phrase'] = earlier_phrase.phrase_num

        cadence_alter = form_data.cleaned_data.get('cadence_alter', None)
        if cadence_alter:
            if "Other" in cadence_alter:
                cadence_alter = [c for c in cadence_alter if c != "Other"]
                cadence_alter.append(form_data.cleaned_data.get('cadence_alter_other', None))
            form_data.cleaned_data['cadence_alter'] = ", ".join(cadence_alter)
        else:
            form_data.cleaned_data['cadence_alter'] = ""
        del form_data.cleaned_data['cadence_alter_other']

        other_contrapuntal = form_data.cleaned_data.get('other_contrapuntal', None)
        print "Other: ", other_contrapuntal
        if other_contrapuntal:
            if "Other" in other_contrapuntal:
                other_contrapuntal = [c for c in other_contrapuntal if c != "Other"]
                other_contrapuntal.append(form_data.cleaned_data.get('other_contrapuntal_other', None))
            form_data.cleaned_data['other_contrapuntal'] = ", ".join(other_contrapuntal)
        else:
            form_data.cleaned_data['other_contrapuntal'] = ""

        del form_data.cleaned_data['other_contrapuntal_other']

        other_formulas = form_data.cleaned_data.get('other_formulas', None)
        if other_formulas:
            form_data.cleaned_data['other_formulas'] = "".join(other_formulas)  # right now this is only one item, Romanesca.
        else:
            form_data.cleaned_data['other_formulas'] = ""

        text_treatment = form_data.cleaned_data.get('text_treatment', None)
        if text_treatment == "Other":
            other_description = form_data.cleaned_data.get("text_treatment_other", None)
            if not other_description:
                # raise a form validation error
                pass
            text_treatment = other_description
        del form_data.cleaned_data['text_treatment_other']

        form_data.cleaned_data['composition_number'] = piece
        form_data.cleaned_data['analyst'] = request.user.profile.person
        form_data.cleaned_data['needs_review'] = True
        tstamp = datetime.datetime.now()
        form_data.cleaned_data['timestamp'] = tstamp.strftime("%d/%m/%Y %H:%M:%S")

        # more form cleaning here.
        analysis = DCAnalysis(**form_data.cleaned_data)
        analysis.save()

        return HttpResponseRedirect('/piece/' + piece_id)
    else:
        form_data = AnalysisForm()
        phrases_for_piece = DCPhrase.objects.filter(piece_id=piece_id).order_by('phrase_num')
        form_data.fields['phrase_number'].queryset = phrases_for_piece
        form_data.fields['earlier_phrase'].queryset = phrases_for_piece
        # phrases = DCPhrase.objects.filter(piece_id=piece_id).order_by('phrase_num')
    return render(request, 'main/add_observation.html', {'form': form_data, 'piece': piece})
