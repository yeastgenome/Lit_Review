'''
Created on Dec 19, 2012

@author: kpaskov
'''
from wtforms.fields.core import BooleanField, FieldList, FormField
from wtforms.fields.simple import TextField, PasswordField, SubmitField, \
    HiddenField, TextAreaField
from wtforms.form import Form
from wtforms.validators import ValidationError, Required


class LoginForm(Form):
    username = TextField('Username:', [Required(message='Please log in.')])
    password = PasswordField('Password:') 
    login = SubmitField('Login')

def validate_go_genes(form, field):
    if form.go_genes.data == "":
        raise ValidationError("Please enter gene names for " + form.go.label.text)
    
class ReferenceForm(Form):
    pubmed_id = HiddenField() 
    
    high_priority = BooleanField('High Priority')
    high_priority_comment = TextAreaField('Comment:')
    delay = BooleanField('Delay')
    delay_comment = TextAreaField('Comment:')
    htp = BooleanField("HTP phenotype data (adds the 'Omics' topic")
    htp_comment = TextAreaField('Comment:')
    other = BooleanField("Other HTP data (adds the 'Omics' topic")
    other_comment = TextAreaField('Comment:')
    go = BooleanField('GO information')
    go_genes = TextAreaField('Link to these genes and add paper to Primary Literature:', [Required(message='Must enter something.')])
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
    pmids = {}
    
    def fill_pmids_list(self):
        pmids = {}
        for sub_form in self.reference_forms.entries:
            pmids[sub_form.data["pubmed_id"]] = sub_form
    
    def create_reference_form(self, pmid):
        if not len(self.pmids) == len(self.reference_forms.entries):
            self.fill_pmids_list()
            
        if pmid not in self.pmids:
            self.reference_forms.append_entry()
            sub_form = self.reference_forms.entries[-1]
            sub_form.pubmed_id.data = pmid 
            self.pmids[pmid] = sub_form
    
    def get_reference_form(self, pmid):
        if not len(self.pmids) == len(self.reference_forms.entries):
            self.fill_pmids_list()
            
        return self.pmids[pmid] 

