# import random

# from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Hero 
from .serializers import HeroInfoSerializer
from rest_framework.generics import get_object_or_404
from .forms import HeroForm
from django.shortcuts import redirect, render
# teraz nie wiem jakie importy już są nieistotne
# sprawdźmy to potem, teraz nie mam siły

@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def hero_list(request):
    
    if request.method == 'GET':
        if request.user.is_staff: # widok dla adminów -> mogą zobaczyć wszystkich bohaterów, nawet jeśli nie są ich; gracze tylko swoich
            hero = Hero.objects.all()
            serializer = HeroInfoSerializer(hero, many = True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # jeżeli nie chcemy generic komunikaty, który idzie razem z get_object_or_404 mamy jeszcze taką opcję
        # ale ja rozumiem .first() tak pi*drzwi także potrzebuję żeby ktoś sprawdził:
        # hero = Hero.objects.filter(user=request.user).first()
        # jeżeli dobrze rozumiem .first() zwraca None jak nie ma elementu
        # więęęc możemy potem dać
        # if not hero:
        #   return Response({"ERROR": "Nie masz jeszcze bohatera."}, status=status.HTTP_404_NOT_FOUND)
        # i jest cacy?
        hero = get_object_or_404(Hero, user=request.user)
        serializer = HeroInfoSerializer(hero)
        return Response(serializer.data)

    # elif request.method == 'POST':
    #     serializer = HeroSerializer(data=request.data)
        
    #     if Hero.objects.filter(user=request.user).exists():
    #         raise serializers.ValidationError({"ERROR": "You already have a hero!"}) # jeden gracz -> jeden hero
        
    #     elif serializer.is_valid(): # kuba sprawdź czy elif tu na pewno pasuje bo ja już nie myślę T^T
    #         serializer.save(user=request.user) # tu się przypisuje id
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)

    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([permissions.IsAuthenticated])
def hero_create_django_form(request):
    if Hero.objects.filter(user=request.user).exists():
#        messages.error(request, "ERROR: You already have a hero!")
#        ^^^ (nie działa bo się tak nie komunikują, ale zostawiam żeby nie zapomnieć, że chcę coś takiego)
        return redirect('/api/heros/')

    if request.method == 'POST':
        form = HeroForm(request.POST)
        if form.is_valid():
            hero = form.save(commit=False)
            hero.user = request.user
            hero.save()
            return redirect('/api/heros/')
    else:
        form = HeroForm()

    return render(request, 'game/hero/create.html', {'form': form})

# to-do: usuwanie bohaterów i update??? o ile chcemy dać taką opcję

