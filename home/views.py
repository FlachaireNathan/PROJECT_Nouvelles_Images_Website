from django.contrib.auth.decorators import login_required # Permet de rajouter @login_required ce qui oblige d'être connecté pour visualiser la page
from django.contrib.auth import login as auth_login # Ce qui gère les logins
from django.contrib.auth import logout as auth_logout # Ce qui gère les logout

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger # Ce qui sert à paginer l'index
from django.shortcuts import render_to_response, redirect, render # Ce qui permet de faire appel aux templates html
from django.http import HttpResponse,HttpResponseRedirect,Http404,JsonResponse # Ce qui permet d'envoyer des requêtes url ou réponse json pour l'ajax
from django.template import RequestContext # Permet de donner un context
from django.template.context_processors import csrf # Import les tokens utilisés pour les form POST et requêtes ajax POST
from django.views.generic import TemplateView
from django.contrib.contenttypes.models import ContentType # Permet de get le type des models (si c'est un child post, post, thread)

from .models import * # Importe tous les models de model.py

from home.forms import * # Importe tous les modèles de form de form.py

from datetime import datetime # Permet de get la date actuel pour les messages postés

# Une fois login, revoit sur l'index (page principale)
def login(request):
    context = {
        'template_to_load' : 'index.html'
    }
    return render(request, 'layout.html', context)

# Une fois logout, revoit sur la page  principale qui redirigea automatiquement sur auth.html
def logout(request):
    auth_logout(request)
    return redirect('/')

# Pour aller sur la page qui créer un nouveau thread
@login_required
def gotoNewThread(request):
    
    threadForm = ThreadForm()  # On récupère le modèle de form pour un Thread (titre + texte)

    # Si on clique sur le bouton pour créer le thread
    if (request.method == "POST"):

        form = ThreadForm(request.POST)

        if form.is_valid():

            ThreadToSend = form.save(commit=False)
            ThreadToSend.title = request.POST.get("title", "")
            ThreadToSend.user_op = request.user
            ThreadToSend.creation_date = datetime.now()
            ThreadToSend.save()

            idLatestThread = Thread.objects.latest('id').id


            return HttpResponseRedirect('/index')
        
        else:
            context = {
                'threadIsWrong' : True,
                'threadForm': threadForm,
            'template_to_load': 'new_Thread.html',
            }
            return render(request,'layout.html', context)
    
    # Quand on clique sur "Nouveau Sujet" 

    context = {
        'threadIsWrong' : False,
        'threadForm': threadForm,
        'template_to_load': 'new_Thread.html',
    }

    return render(request,'layout.html', context)

@login_required
def gotoIndexNoSort(request):
    return gotoIndex(request,"mostRecent")

@login_required
def gotoIndex(request,sortBy):

    theThreadsToShow = []
    allThreads = Thread.objects.all()
    allThreadsSize = len(allThreads)

    if (sortBy == "mostRecent"):
        # On les tri par le plus récent en premier
        for i in range(len(allThreads)-1,-1,-1):
            theThreadsToShow.append(allThreads[i])

    elif (sortBy == "mostOlder"):
        theThreadsToShow = allThreads

    elif (sortBy == "alphabetical"):
        theThreadsToShow = Thread.objects.order_by('title')

    if (sortBy == "search"):
        word = request.POST.get('search','')
        theThreadsToShow = Thread.objects.filter(title__contains=word)
    
    else:
        paginator = Paginator(theThreadsToShow,5)

        page = request.GET.get('page')

        try:
            theThreadsToShow = paginator.get_page(page)
        except PageNotAnInteger:
            theThreadsToShow = paginator.page(1)
        except EmptyPage:
            numbers = paginator.page(paginator.num_pages)
            isPost = False

    isPost = True

    context = {
        'isPost' : isPost,
        'theThreadsToShow' : theThreadsToShow,
        'allThreadsSize' : allThreadsSize,
        'template_to_load': 'index.html',
    }

    return render(request,'layout.html',context)


@login_required
def createPost(request):
    if (request.method == "POST"):

        idthread = request.POST.get('thread_id','')


        postToSend = Post()

        postForm = PostForm(request.POST)

        postToSend = postForm.save(commit=False)
        postToSend.thread_id = Thread.objects.get(pk=idthread)
        postToSend.user_op = request.user
        postToSend.creation_date = datetime.now()

        postToSend.save()

    
    return HttpResponseRedirect('/thread-' + str(idthread))



@login_required
def gotoThread(request, thread_id_gotten):

    isPinnedAnswer = False # Variable booléenne pour savoir s'il y a une une réponse principal au thread
    isPinnedAnswerChild = False # Variable booléenne pour savoir si la réponse des commentaires enfants
    pinnedAnswer = None # Variable contenant l'objet ThreadAnswer du thread en question
    thePinnedAnswerChilds = None # Liste contenant toud les commentaires enfants au thread enfant
    
    selectedThread = Thread.objects.get(pk=int(thread_id_gotten)) # Get le thread selectionné dans la database 

    isPosts = False # Variable booléenne pour savoir s'il y a des commentaires
    thePosts = Post.objects.filter(thread_id=int(thread_id_gotten)) # Liste contenant tous les commentaires
    thePostsSize = len(thePosts) # Le nombre de commentaires
    theChildPosts = [] # Liste contenant toutes les listes de commentaires enfant pour chaque commentaire

    # Trouve le commentaire épinglé
    for i in thePosts:
        if (i.is_pin == True):
            pinnedAnswer = i

    # S'il y a une réponse, récupère les childs posts de la réponse
    if (pinnedAnswer):
        isPinnedAnswer = True
        thePinnedAnswerChilds = ChildPost.objects.filter(post_id=pinnedAnswer.id)
        if (len(thePinnedAnswerChilds) > 0):
            isPinnedAnswerChild = True

    # Vérifie s'il y a des childposts dans la base de donnée
    is_childPost = False
    if (len(ChildPost.objects.all()) > 0) :
        is_childPost = True

    # S'il y a des childposts, on peut en chercher dans la base de données celle qui correspondrait à nos posts.
    if (is_childPost == True):
        for i in thePosts:
            childsOfPost = ChildPost.objects.filter(post_id=i.id)
            theChildPosts.append(childsOfPost)


    allPosts = [] # Liste contenant tous les commentaires et commentaires enfant dans l'ordre
                  # Car le template django ne peut pas exectuer des for dans des for.

    # Pour tous les commentaires, on ajoute un commentaire à allPosts puis tous ses commentaires enfants 
    for i in range(0,thePostsSize):
        allPosts.append(thePosts[i])
        if (is_childPost == True):
                for j in range(0,len(theChildPosts[i]),1):
                        allPosts.append(theChildPosts[i][j])


    for i in range (0,len(allPosts),1):
        
        if (ContentType.objects.get_for_model(allPosts[i]) == ContentType.objects.get_for_model(Post.objects.latest('id'))):
            if (i+1 < len(allPosts)):
                if (is_childPost == True):
                    if (ContentType.objects.get_for_model(allPosts[i+1]) == ContentType.objects.get_for_model(ChildPost.objects.latest('id'))):
                        allPosts[i].have_child = True

        
        if (is_childPost == True):
            if (ContentType.objects.get_for_model(allPosts[i]) == ContentType.objects.get_for_model(ChildPost.objects.latest('id'))):
                if (i+1 < len(allPosts)):
                    if (ContentType.objects.get_for_model(allPosts[i+1]) == ContentType.objects.get_for_model(Post.objects.latest('id'))):
                        allPosts[i].is_last = True
                else:
                    allPosts[i].is_last = True
        
            #if (allPosts[i+1]):
                #if (isinstance(allPosts[i+1]) == ):

    allPostsSize = len(allPosts) # Nombre total de commentaires (compte les commentaires enfants)

    postForm = PostForm()
    

    # Contient toutes les informations que l'on souhaite envoyer à la partie html
    context = {
        'postForm':postForm,

        'isPinnedAnswer': isPinnedAnswer,
        'isPinnedAnswerChild': isPinnedAnswerChild,
        'isPosts': isPosts,
        'selectedThread': selectedThread,
        'pinnedAnswer': pinnedAnswer,
        'thePinnedAnswerChilds': thePinnedAnswerChilds,
        'allPosts': allPosts,
        'allPostsSize' : allPostsSize,
        'template_to_load': 'Thread.html',
    }

    return render(request,'layout.html',context)
    
    
@login_required
def gotoProfil(request,nameOfUser):

    isPost = False

    userToSee = User.objects.get(username=nameOfUser)

    theThreadsToShow = []
    allThreads = Thread.objects.all()
    allThreadsSize = len(allThreads)

        # On les tri par le plus récent en premier
    for i in range(len(allThreads)-1,-1,-1):
        isPost = True
        theThreadsToShow.append(allThreads[i])

    
    context = {
        'isPost' : isPost,
        'theThreadsToShow' : theThreadsToShow,
        'userToSee' : userToSee,
        'template_to_load': 'profil.html'
    }

    return render(request,'layout.html', context)


def gotoAuth(request):
    """
    if (request.user == None):
        context = {
        'template_to_load': 'index.html',
        }
        return render(request,'layout.html',context)
    """

    return render(request,'auth.html')


def gotoLogged(request):
    context = {
        'template_to_load': 'index.html',
    }
    return render(request,'layout.html', context)

@login_required
def addChildPost(request):


    if (request.method == "POST"):

        if (request.POST.get("bodychildPost", "") == "") :
            return redirect('/')

        parentPost = Post.objects.get(pk=request.POST.get("idPost", ""))

        childPostToSend = ChildPost()

        childPostToSend.body = request.POST.get("bodychildPost", "")
        childPostToSend.user_op = request.user
        childPostToSend.post_id = parentPost
        childPostToSend.creation_date = datetime.now()

        childPostToSend.save()
        
        context = {}

        return JsonResponse(context)

    return redirect('/')

@login_required
def modifyThread(request):

    if (request.method == "POST"):
        
        threadForm = ThreadForm(request.POST)


        threadToModify = Thread()
        threadToModify.title = request.POST.get('title','')
        threadToModify.body = request.POST.get('body','')
        threadToModify.id = request.POST.get('id','')

        request.session['idThreadToModify'] = request.POST.get('id','')


        context = {
            'threadToModify': threadToModify,
            'template_to_load': 'modify_thread.html',
        }

        return render(request,'layout.html', context)


@login_required
def modifyPost(request):

    if (request.method == "POST"):
        
        postForm = PostForm(request.POST)

        postToModify = Post()
        postToModify = postForm.save(commit=False)

        request.session['idPostToModify'] = request.POST.get('id','')

        context = {
            'postToModify': postToModify,
            'template_to_load': 'modify_post.html',
        }


        return render(request,'layout.html', context)


@login_required
def modifyChildPost(request):

    if (request.method == "POST"):

        childPostForm = ChildPostForm(request.POST)

        childPostToModify = ChildPost()
        childPostToModify = childPostForm.save(commit=False)

        request.session['idChildPostToModify'] = request.POST.get('id','')

        context = {
            'idThread': request.POST.get('thread_id',''),
            'childPostToModify': childPostToModify,
            'template_to_load': 'modify_childPost.html',
        }

        return render(request,'layout.html', context)


@login_required
def threadModified(request):

    if (request.method == "POST"):



        idThreadToModify = request.session['idThreadToModify']

        threadToModify = Thread.objects.get(pk=idThreadToModify)

        threadToModify.title = request.POST.get('title','')
        threadToModify.body = request.POST.get('body','')
        threadToModify.user_modo = request.user
        threadToModify.modification_date = datetime.now()
        threadToModify.modification = True

        threadToModify.save()

        
        

        context = {
            'idThreadToModify': request.POST.get('id',''),
            'threadToModify': threadToModify,
            'template_to_load': 'modify_thread.html',
    }


    return gotoThread(request,threadToModify.id)


@login_required
def postModified(request):

    if (request.method == "POST"):
        

        idPostToModify = request.session['idPostToModify']

        postToModify = Post.objects.get(pk=idPostToModify)

        postToModify.body = request.POST.get('body','')
        postToModify.user_modo = request.user
        postToModify.modification_date = datetime.now()
        postToModify.modification = True

        postToModify.save()

        return gotoThread(request,postToModify.thread_id.id)


@login_required
def childPostModified(request):

    if (request.method == "POST"):

        idChildPostToModify = request.session['idChildPostToModify']

        childPostToModify = ChildPost.objects.get(pk=idChildPostToModify)

        childPostToModify.body = request.POST.get('body','')
        childPostToModify.user_modo = request.user
        childPostToModify.modification_date = datetime.now()
        childPostToModify.modification = True

        childPostToModify.save()



        return gotoThread(request,childPostToModify.post_id.thread_id.id)

@login_required
def deleteThread(request):

    if (request.method == "POST"):

        idThreadToDelete = request.POST.get('idThreadToDelete','')
        ThreadToDelete = Thread.objects.get(pk=idThreadToDelete)
        ThreadToDelete.delete()

        context = {}

        return JsonResponse(context) 

@login_required
def deletePost(request):

    if (request.method == "POST"):

        idPostToDelete = request.POST.get('idPostToDelete','')
        PostToDelete = Post.objects.get(pk=idPostToDelete)
        PostToDelete.delete()

        context = {}

        return JsonResponse(context) 

@login_required
def deleteChildPost(request):

    if (request.method == "POST"):
        
        idChildPostToDelete = request.POST.get('idChildPostToDelete','')
        ChildPostToDelete = ChildPost.objects.get(pk=idChildPostToDelete)
        ChildPostToDelete.delete()

        context = {}

        return JsonResponse(context) 



@login_required
def pinPost(request):
    
    if (request.method == "POST"):


        idPostToPin = request.POST.get("idPost","")
        postToPin = Post.objects.get(pk=idPostToPin)
        # Recupère tous les post du même thread et passe leurs variable pin à False
        allPost = Post.objects.filter(thread_id=postToPin.thread_id)
        for i  in allPost:
            i.is_pin = False
            i.save()
        
        postToPin.is_pin = True
        postToPin.save()

        context = {}

        return JsonResponse(context)


@login_required
def lockThread(request,lock):

    if (request.method == "POST"):
        threadToModify = Thread.objects.get(pk=request.POST.get("idChildThreadToLock",""))
        if (lock == 'True'):
            threadToModify.resolved=True
        elif (lock == 'False'):
            threadToModify.resolved=False
        threadToModify.save()

    context = {}

    return JsonResponse(context)
