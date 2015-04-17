from django.contrib import admin
from django import forms
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext

from santaclara_emoticons.models import EmoticonsCollection,Emoticon,EmoticonsSet

class EmoticonAdmin(admin.ModelAdmin):
    list_display=[ 'id','set','get_image','enabled','label' ]
    list_display_links=['id']
    list_editable=[ 'label','enabled','set' ]
    list_filter=['set','enabled']
    actions=['change_emoticonsset']

    class EmoticonsSetChoiceForm(forms.Form):
        _selected_action=forms.CharField(widget=forms.MultipleHiddenInput)
        emoticonsset = forms.ModelChoiceField(EmoticonsSet.objects)

    def change_emoticonsset(self,request,queryset):
        form=None
        if "cancel" in request.POST:
            self.message_user(request,"Action canceled")
            return
        if "apply" in request.POST:
            form=self.EmoticonsSetChoiceForm(request.POST)
            if form.is_valid():
                emoticonsset=form.cleaned_data["emoticonsset"]
                rows_updated=queryset.update(set=emoticonsset)
                if rows_updated==1:
                    msg="1 emoticon was"
                else:
                    msg="%s emoticons were" % rows_updated
            self.message_user(request,"%s successfully moved to %s" % (msg,emoticonsset.name))
            return HttpResponseRedirect(request.get_full_path())
        if not form:
            form = self.EmoticonsSetChoiceForm(initial={'_selected_action':
                                                        request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})
        return render_to_response('admin/change_emoticonsset.html',
                                  context={'emoticons': queryset, 'form': form})

    change_emoticonsset.short_description="Change emoticons set"

admin.site.register(Emoticon,EmoticonAdmin)
admin.site.register(EmoticonsCollection)

class EmoticonsSetAdmin(admin.ModelAdmin):
    list_display=[ 'id','name','numerosity','colspan' ]
    list_display_links=['id']
    list_editable=[ 'name','colspan' ]

admin.site.register(EmoticonsSet,EmoticonsSetAdmin)
