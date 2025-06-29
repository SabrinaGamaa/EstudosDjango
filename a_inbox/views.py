from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.db.models import Q
from a_users.models import Profile
from .models import *
from .forms import InboxNewMessageForm

@login_required
def inbox_view(request, conversation_id=None):
    # SE o usuário estiver logado:
    my_conversations = Conversation.objects.filter(participants=request.user)
    
    # SE foi passado um ID de conversa na URL:
    if conversation_id:
        # Buscar todas as conversas em que o usuário atual participa
        conversation = get_object_or_404(my_conversations, id=conversation_id)
        # Buscar essa conversa específica entre as que o usuário participa
        # (ou retornar erro 404 se não existir)
        
    # SENÃO:
    else:
        # Nenhuma conversa específica foi selecionada
        conversation = None
        
    context = {
        'conversation' : conversation,
        'my_conversations' : my_conversations
    }
    return render(request, 'a_inbox/inbox.html', context)
    # Enviar para o template:
    # - A conversa selecionada (se houver)
    # - A lista de todas as conversas do usuário


# Pegar o que o usuário digitou no campo de busca ("search-user")
def search_users(request):
    letters = request.GET.get('search-user')
    
    # SE a requisição veio via HTMX (requisição dinâmica):
    if request.htmx:
        if len(letters) > 0:
            # Buscar perfis onde o nome real contenha as letras digitadas | Excluir o perfil do próprio usuário
            profiles = Profile.objects.filter(realname__icontains=letters).exclude(realname=request.user.profile.realname)
            
            # A partir desses perfis, pegar os IDs dos usuários
            users_id = profiles.values_list('user', flat=True)
            
            # Procurar usuários com:
            #     - username parecido com a busca
            #     - OU com ID presente nos perfis encontrados
            # Excluir o próprio usuário dos resultados
            users = User.objects.filter(
                Q(username__icontains=letters) | Q(id__in=users_id)
            ).exclude(username=request.user.username)
            
            # Renderizar a lista de usuários encontrados usando o template parcial
            return render(request, 'a_inbox/list_searchuser.html', {'users' : users})
        else:
            # Retornar uma resposta vazia
            return HttpResponse('')
    else:
        raise Http404()
    
    
    
@login_required    
def new_message(request, recipient_id):
    recipient = get_object_or_404(User, id=recipient_id)
    # Criar um formulário vazio de nova mensagem
    new_message_form = InboxNewMessageForm()
    
    if request.method == 'POST':
        # Preencher o formulário com os dados enviados
        form = InboxNewMessageForm(request.POST)
        
        if form.is_valid():
            # Criar a mensagem mas ainda não salvar no banco
            message = form.save(commit=False)
            # Definir o remetente como o usuário logado
            message.sender = request.user
            
            # Buscar todas as conversas do usuário atual
            my_conversations = request.user.conversations.all()
            
            for c in my_conversations:
                # SE o destinatário estiver nessa conversa:
                if recipient in c.participants.all():
                    # Atribuir a conversa à mensagem
                    message.conversation = c
                    # Salvar a mensagem
                    message.save()
                    
                    # Atualizar a data do último envio na conversa
                    c.lastmessage_created = timezone.now()
                    # Salvar a conversa
                    c.save()
                    # Redirecionar para a conversa existente
                    return redirect('inbox', c.id)
                
            # (Se nenhuma conversa encontrada entre os dois)
            # Criar uma nova conversa
            new_conversation = Conversation.objects.create()
            # Adicionar o remetente e o destinatário nela
            new_conversation.participants.add(request.user, recipient)
            # Salvar a nova conversa
            new_conversation.save()
            # Atribuir essa nova conversa à mensagem
            message.conversation = new_conversation
            # Salvar a mensagem
            message.save()
            # Redirecionar para essa nova conversa
            return redirect('inbox', new_conversation.id)
    
    context = {
        'recipient' : recipient,
        'new_message_form' : new_message_form
    }
    return render(request, 'a_inbox/form_newmessage.html', context)


@login_required
def new_reply(request, conversation_id):
    # Criar um formulário vazio para nova mensagem (sem dados preenchidos ainda)
    new_message_form = InboxNewMessageForm()
    # Buscar todas as conversas do usuário atual
    my_conversations = request.user.conversations.all()
    # Procurar a conversa com o ID passado na URL dentro daquelas que ele participa | Se não encontrar, retornar erro 404
    conversation = get_object_or_404(my_conversations, id=conversation_id)
    
    if request.method == 'POST':
        form = InboxNewMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.conversation = conversation
            message.save()
            conversation.lastmessage_created = timezone.now()
            conversation.save()
            return redirect('inbox', conversation.id)
    
    
    # Preparar os dados para enviar ao template:
    # - O formulário de nova mensagem (vazio)
    # - A conversa em que a resposta será enviada
    context = {
        'new_message_form' : new_message_form,
        'conversation' : conversation
    }
    
    return render(request, 'a_inbox/form_newreply.html', context)