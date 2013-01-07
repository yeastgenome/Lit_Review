'''
Created on Dec 19, 2012

@author: kpaskov
'''

from wtforms import Form, TextField, validators
from wtforms.fields.core import BooleanField, FieldList, FormField
from wtforms.fields.simple import PasswordField, TextAreaField, SubmitField
from wtforms.validators import ValidationError

class LoginForm(Form):
    username = TextField('Username:', [validators.Required(message='Please log in.')])
    password = PasswordField('Password:') 
    login = SubmitField('Login')

def validate_go_genes(form, field):
    if form.go.data and form.go_genes.data == "":
        raise ValidationError("Please enter gene names for " + form.go.label.text)
    
class ReferenceForm(Form):
    pubmed_id = TextField()
    
    high_priority = BooleanField('High Priority')
    high_priority_comment = TextAreaField('Comment:')
    delay = BooleanField('Delay')
    delay_comment = TextAreaField('Comment:')
    htp = BooleanField("HTP phenotype data (adds the 'Omics' topic")
    htp_comment = TextAreaField('Comment:')
    other = BooleanField("Other HTP data (adds the 'Omics' topic")
    other_comment = TextAreaField('Comment:')
    go = BooleanField('GO information')
    go_genes = TextAreaField('Link to these genes and add paper to Primary Literature:', [validators.Required(message='Must have something'), validate_go_genes])
    go_comment = TextAreaField('Comment:')
    phenotype = BooleanField('Classical phenotype information')
    phenotype_genes = TextAreaField('Link to these genes and add paper to Primary Literature:')
    phenotype_comment = TextAreaField('Comment:')
    headline = BooleanField('Headline Information')
    headline_genes = TextAreaField('Link to these genes and add paper to Primary Literature:')
    headline_comment = TextAreaField('Comment:')
    review = BooleanField('Review')
    review_genes = TextAreaField('Optionally link to these genes:')
    review_comment = TextAreaField('Comment:')
    add_to_db = BooleanField('Add to database')
    add_to_db_genes = TextAreaField('Optionally link to these genes and add paper to Additional Literature:')
    add_to_db_comment = TextAreaField('Comment:')
    link = SubmitField('Link checked tags/topics/genes to this paper')
    
class ManyReferenceForms(Form):
    reference_forms = FieldList(FormField(ReferenceForm))
    
    pmid_to_reference_form = None
    
    def __refill_pmid_to_reference_form__(self):
        self.pmid_to_reference_form = {}
        for sub_form in self.reference_forms:
            pubmed_id = sub_form.pubmed_id
            self.pmid_to_reference_form[pubmed_id] = sub_form
    
    def add_reference_form(self, pmid):
        if self.pmid_to_reference_form is None:
            self.__refill_pmid_to_reference_form__()
            
        if pmid not in self.pmid_to_reference_form:
            self.reference_forms.append_entry({'pubmed_id', pmid})
            self.pmid_to_reference_form[pmid] = self.reference_forms[-1]
    
    def get_reference_form(self, pmid):
        if self.pmid_to_reference_form is None:
            self.__refill_pmid_to_reference_form__()
            
        return self.pmid_to_reference_form[pmid]

