# coding=utf-8
from django import forms


class FormaBase(forms.Form):
	
	def as_div(self):
		"Retorna un formulario con un formato que usa el tag HTML DIV"
		return self._html_output(u'<div class="field">%(label)s<div>%(field)s%(help_text)s<span class="field-error">%(errors)s</span></div></div>', u'<div>%s</div>', '<br />', u'<br />%s', False)
	
	def as_table(self):
		"Returns this form rendered as HTML <tr>s -- excluding the <table></table>."
		return self._html_output(u'<tr><th>%(label)s</th><td>%(field)s%(help_text)s%(errors)s</td></tr>', u'<tr><td colspan="2">%s</td></tr>', '</td></tr>', u'<br />%s', False)
	
	
	
	