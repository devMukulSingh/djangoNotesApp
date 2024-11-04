from django.urls import path
from .views import SignUpUser,SignInUser,PostNote,GetNotes,EditNote,DeleteNote

urlpatterns = [
    path('sign-up/',SignUpUser.as_view()),
    path('sign-in/',SignInUser.as_view()),
    path('notes/post-note',PostNote.as_view()),   
    path('notes/get-notes',GetNotes.as_view()),
    path('notes/edit-note',EditNote.as_view()),  
    path('notes/delete-note',DeleteNote.as_view()),  
]
 