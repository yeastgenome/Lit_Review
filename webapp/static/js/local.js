/* this function will call the delete url to discard the paper from the database 
 * and replace the section with the message returned from the server.
 */ 

function show_hide_comment(id, show) {
	checkbox = document.getElementById(id)
	block = document.getElementById(id + '_block')
	comment_text = document.getElementById(id + '_comment')
	gene_text = document.getElementById(id + '_genes')
	if (!checkbox.checked) {
		block.style.display = 'none';
		comment_text.value = "";
		gene_text.value = "";
	}
	else {
		block.style.display = 'block';
	}
}


/* this is used for creating the collapsible section for abstracts */
function activateCollapsible(id) {
	if (window.addEventListener) {
		window.addEventListener("load", function(){makeCollapsible(document.getElementById(id), 1);}, false);
	}
	else if (window.attachEvent) {
		window.attachEvent("onload", function(){makeCollapsible(document.getElementById(id), 1);});
	}
	else {
		window.onload = function(){makeCollapsible(document.getElementById(id), 1);};
	}
}

/* used to bold the author names in the citation */
function bold_citation(count) {
	for (var i = 1; i <= count; i++) {
		citation = document.getElementById('citation' + i);
		citation.innerHTML = citation.innerHTML.replace(/([^0-9]+\([0-9]{4}\))/g, "<strong>$1</strong>");
	}
	return true;
}


/* following methods are used for highlighting the keywords */


/*
 * This is the function that actually highlights a text string by
 * adding HTML tags before and after all occurrences of the search
 * term. You can pass your own tags if you'd like, or if the
 * highlightStartTag or highlightEndTag parameters are omitted or
 * are empty strings then the default <font> tags will be used.
 */
function doHighlight(bodyText, searchTerm, highlightStartTag, highlightEndTag) {
  // the highlightStartTag and highlightEndTag parameters are optional
  if ((!highlightStartTag) || (!highlightEndTag)) {
    highlightStartTag = "<font style='color:blue; background-color:yellow;'>";
    highlightEndTag = "</font>";
  }
  
  // find all occurences of the search term in the given text,
  // and add some "highlight" tags to them (we're not using a
  // regular expression search, because we want to filter out
  // matches that occur within HTML tags and script blocks, so
  // we have to do a little extra validation)
  var newText = "";
  var i = -1;
  var lcSearchTerm = searchTerm.toLowerCase();
  var lcBodyText = bodyText.toLowerCase();
    
  while (bodyText.length > 0) {
    i = lcBodyText.indexOf(lcSearchTerm, i+1);
    if (i < 0) {
      newText += bodyText;
      bodyText = "";
    } else {
      // skip anything inside an HTML tag
      if (bodyText.lastIndexOf(">", i) >= bodyText.lastIndexOf("<", i)) {
        // skip anything inside a <script> block
        if (lcBodyText.lastIndexOf("/script>", i) >= lcBodyText.lastIndexOf("<script", i)) {
          newText += bodyText.substring(0, i) + highlightStartTag + bodyText.substr(i, searchTerm.length) + highlightEndTag;
          bodyText = bodyText.substr(i + searchTerm.length);
          lcBodyText = bodyText.toLowerCase();
          i = -1;
        }
      }
    }
  }
  
  return newText;
}


/*
 * This is sort of a wrapper function to the doHighlight function.
 * It takes the searchText that you pass, optionally splits it into
 * separate words, and transforms the text on the current web page.
 * Only the "searchText" parameter is required; all other parameters
 * are optional and can be omitted.
 */
function highlightSearchTerms(searchText, treatAsPhrase, warnOnFailure, highlightStartTag, highlightEndTag) {
  // if the treatAsPhrase parameter is true, then we should search for 
  // the entire phrase that was entered; otherwise, we will split the
  // search string so that each word is searched for and highlighted
  // individually
  if (treatAsPhrase) {
    searchArray = [searchText];
  } else {
    searchArray = searchText.split(" ");
  }
  
  if (!document.body || typeof(document.body.innerHTML) == "undefined") {
    if (warnOnFailure) {
      alert("Sorry, for some reason the text of this page is unavailable. Searching will not work.");
    }
    return false;
  }
  
  var bodyText = document.body.innerHTML;
  for (var i = 0; i < searchArray.length; i++) {
    bodyText = doHighlight(bodyText, searchArray[i], highlightStartTag, highlightEndTag);
  }
  
  document.body.innerHTML = bodyText;

  return true;
}


function show_hide (buttonId, buttonNm, contentId) {
	if ($('#' + buttonId).val().match('Show')) {
	    $('#' + buttonId).val('Hide ' + buttonNm);
	    $('#' + contentId).show();
	}
	else {
	    $('#' + buttonId).val('Show ' + buttonNm);
            $('#' + contentId).hide();
	}

}


//Downloaded from http://www.acmeous.com/tutorials/demo/acmeousCollapsibleLists/acmeousCollapsibleLists.js

//CONFIGURATION
// collapsedImage='http://www.yeastgenome.org/images/plus.gif';
// expandedImage='http://www.yeastgenome.org/images/minus.gif';
collapsedImage='../static/img/plus.gif';
expandedImage='../static/img/minus.gif';

defaultState=1;	//1 = show, 0 = hide
/* makeCollapsible - makes a list have collapsible sublists
 * 
 * listElement - the element representing the list to make collapsible
 */
function makeCollapsible(listElement,listState) {
  if(listState!=null) defaultState=listState;

  // removed list item bullets and the sapce they occupy
  listElement.style.listStyle='none';
  listElement.style.marginLeft='0';
  listElement.style.paddingLeft='0';

  // loop over all child elements of the list
  var child=listElement.firstChild;
  while (child!=null){

    // only process li elements (and not text elements)
    if (child.nodeType==1){

      // build a list of child ol and ul elements and show/hide them
      var list=new Array();
      var grandchild=child.firstChild;
      while (grandchild!=null){
        if (grandchild.tagName=='OL' || grandchild.tagName=='UL'){
          if(defaultState==1) grandchild.style.display='block';
		  else grandchild.style.display='none';
          list.push(grandchild);
        }
        grandchild=grandchild.nextSibling;
      }

      // add toggle buttons
	  if(defaultState==1) {
		  var node=document.createElement('img');
		  node.setAttribute('src',expandedImage);
		  node.setAttribute('class','collapsibleOpen');
		  node.style.marginRight="5px";
		  node.style.display = "inline";
		  node.onclick=createToggleFunction(node,list);
		  child.insertBefore(node,child.firstChild);
	  } else {
		  var node=document.createElement('img');
		  node.setAttribute('src',collapsedImage);
		  node.setAttribute('class','collapsibleClosed');
		  node.style.marginRight="5px";
		  node.style.display = "inline";
		  node.onclick=createToggleFunction(node,list);
		  child.insertBefore(node,child.firstChild);
	  }
    }

    child=child.nextSibling;
  }

}

/* createToggleFunction - returns a function that toggles the sublist display
 * 
 * toggleElement  - the element representing the toggle gadget
 * sublistElement - an array of elements representing the sublists that should
 *                  be opened or closed when the toggle gadget is clicked
 */
function createToggleFunction(toggleElement,sublistElements) {

  return function() {

    // toggle status of toggle gadget
    if (toggleElement.getAttribute('class')=='collapsibleClosed'){
      toggleElement.setAttribute('class','collapsibleOpen');
      toggleElement.setAttribute('src',expandedImage);
    }else{
      toggleElement.setAttribute('class','collapsibleClosed');
      toggleElement.setAttribute('src',collapsedImage);
    }

    // toggle display of sublists
    for (var i=0;i<sublistElements.length;i++){
      sublistElements[i].style.display=
          (sublistElements[i].style.display=='block')?'none':'block';
    }

  }

}



