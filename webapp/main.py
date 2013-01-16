#!/usr/bin/python

"""

This is a small application that provides a login page for curators to view/edit the
information in Oracle database. This application is using Flask-Login package (created
by Matthew Frazier, MIT) for handling the login sessions and everything. 

"""
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import login_required
from model_old_schema.model import Model
from queries.associate import link_paper, get_ref_summary, \
    check_form_validity_and_convert_to_tasks
from queries.misc import get_reftemps, get_recent_history
from queries.move_ref import move_reftemp_to_refbad, MoveRefException
from webapp.config import SECRET_KEY, HOST, PORT
from webapp.forms import LoginForm, ManyReferenceForms
from webapp.login_handler import confirm_login_lit_review_user, \
    logout_lit_review_user, login_lit_review_user, setup_app, LoginException, \
    LogoutException

app = Flask(__name__)
model = Model()
setup_app(app)
app.debug = True

@app.route("/")
def index():
    labels = []
    data = []
    if model.is_connected():
        recent_history = model.execute(get_recent_history())
        sorted_history = recent_history.items()
        sorted_history.sort() 
        
        for k, v in sorted_history:
            labels.append(k.strftime("%m/%d"))
            data.append([v.refbad_count, v.ref_count])
        
    return render_template("index.html", history_labels=labels, history_data=data)

@app.route("/reference", methods=['GET', 'POST'])
@login_required
def reference():
    form = ManyReferenceForms(request.form)
    
    refs = model.execute(get_reftemps()) 
    for ref in refs:
        form.create_reference_form(ref.pubmed_id)  
        
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
            flash("Reference for pmid=" + pmid + " has been removed from the database.", 'success')
        except MoveRefException as e:
            flash(e.message, 'error')
    return redirect(request.args.get("next") or url_for("reference")) 

@app.route("/reference/link/<pmid>", methods=['GET', 'POST'])
@login_required 
def link_ref(pmid):  
    if request.method == "POST":
        try:
            tasks = check_form_validity_and_convert_to_tasks(request.form)
            model.execute(link_paper(pmid, tasks), commit=True)
            
            #Link successful
            summary = model.execute(get_ref_summary(pmid))
            flash("Reference for pmid = " + pmid + " has been added into the database and associated with the following data:<br>" + str(summary), 'success')
        except Exception as e:
            flash(e.message, 'error')

    return redirect(request.args.get("next") or url_for("reference"))

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        username = form.username.data
        password = form.password.data
        remember = False
        
        try:
            logged_in = login_lit_review_user(username, password, model, remember)
            if not logged_in:
                raise LoginException('Login unsuccessful. Reason unknown.')
            
            #Login successful.
            flash("Logged in!", 'login')
            return redirect(request.args.get("next") or url_for("index"))
        
        except LoginException as e:
            flash(e.message, 'login')
    return render_template("login.html", form=form)

@app.route("/reauth", methods=["GET", "POST"])
@login_required
def reauth():
    if request.method == "POST":
        output = confirm_login_lit_review_user()
        flash(output, 'login')
        return redirect(url_for("index")) 
    return render_template("reauth.html")

@app.route("/logout")
def logout():
    try:
        logged_out = logout_lit_review_user()
        if not logged_out:
            raise LogoutException('Logout unsuccessful. Reason unknown.')
        
        #Logout successful
        flash('Logged out.', 'login')
        
    except LogoutException as e:
        flash(e.message, 'login')
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.secret_key = SECRET_KEY
    app.run(host=HOST, port=PORT, debug=True) 