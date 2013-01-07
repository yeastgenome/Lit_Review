#!/usr/bin/python

"""

This is a small application that provides a login page for curators to view/edit the
information in Oracle database. This application is using Flask-Login package (created
by Matthew Frazier, MIT) for handling the login sessions and everything. 

"""
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import login_required
from modelOldSchema.model import Model
from queries.associate import LinkPaperException, link_paper, get_ref_summary, \
    FormNotValidException, check_form_validity_and_convert_to_tasks
from queries.misc import get_reftemps
from queries.move_ref import move_reftemp_to_refbad, MoveRefException
from webapp.config import SECRET_KEY, HOST, PORT
from webapp.forms import LoginForm, ManyReferenceForms
from webapp.login_handler import confirm_login_lit_review_user, \
    logout_lit_review_user, login_lit_review_user, setup_app, LoginException, \
    LogoutException

app = Flask(__name__)
model = Model()
setup_app(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/reference")
@login_required
def reference():
    form = ManyReferenceForms(request.form) 
    form.__refill_pmid_to_reference_form__()
    refs = model.execute(get_reftemps())
    
    print form.pmid_to_reference_form.keys() 

    for ref in refs:
        form.add_reference_form(ref.pubmed_id) 
    
    num_of_refs = len(refs) 
    return render_template('literature_review.html',
                           ref_list=refs,
                           ref_count=num_of_refs, 
                           form=form)    

@app.route("/reference/delete/<pmid>", methods=['GET', 'POST'])
@login_required
def discard_ref(pmid):
    if request.method == "POST":
        try:
            moved = model.execute(move_reftemp_to_refbad(pmid), commit=True)
            if not moved:
                raise MoveRefException('An error occurred when deleting the reference for pmid=" + pmid + " from the database.')
            
            #Reference deleted
            flash("Reference for pmid=" + pmid + " has been removed from the database!")
        except MoveRefException as e:
            flash(e.message)
    return redirect(request.args.get("next") or url_for("reference")) 

@app.route("/reference/link/<pmid>", methods=['GET', 'POST'])
@login_required
def link_ref(pmid):
    form = ManyReferenceForms(request.form)
    if request.method == "POST" and form.validate():
        try:
            tasks = check_form_validity_and_convert_to_tasks(request.form)
            paper_linked = model.execute(link_paper(pmid, tasks), commit=True)
            if not paper_linked:
                raise LinkPaperException('Attempt to link paper unsuccessful. Reason unknown')
            
            #Link successful
            summary = model.execute(get_ref_summary(pmid))
            flash("Reference for pmid = " + pmid + " has been added into the database and associated with the following data:<br>" + str(summary))
        except LinkPaperException as e:
            flash(e.message)
        except FormNotValidException as e:
            flash(e.message)
        
    return redirect(request.args.get("next") or url_for("reference", form=form)) 

    #return redirect(request.args.get("next") or url_for("reference"))

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        username = form.username.data
        password = form.password.data
        remember = True
        
        try:
            logged_in = login_lit_review_user(username, password, model, remember)
            if not logged_in:
                raise LoginException('Login unsuccessful. Reason unknown.')
            
            #Login successful.
            flash("Logged in!")
            return redirect(request.args.get("next") or url_for("index"))
        
        except LoginException as e:
            flash(e.message)
    return render_template("login.html", form=form)

@app.route("/reauth", methods=["GET", "POST"])
@login_required
def reauth():
    if request.method == "POST":
        output = confirm_login_lit_review_user()
        flash(output)
        return redirect(url_for("index")) 
    return render_template("reauth.html")

@app.route("/logout")
def logout():
    try:
        logged_out = logout_lit_review_user()
        if not logged_out:
            raise LogoutException('Logout unsuccessful. Reason unknown.')
        
        #Logout successful
        flash('Logged out.')
        
    except LogoutException as e:
        flash(e.message)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.secret_key = SECRET_KEY
    app.run(host=HOST, port=PORT, debug=True) 