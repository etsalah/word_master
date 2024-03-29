
var addBtnCtrls = document.getElementsByClassName("add-button"),
    buildWordContainer = document.getElementById("WordContainer"),
    choosenWordsCtrl = document.getElementById("choosen_words"),
    clearChoosenWordBtn = document.getElementById("clear_choosen_words");

var getSelectedWords = function() {
    return localStorage.getItem("selectedWords");
};


var addNewSelectedWords = function(previousSelectedWords, newWord) {
    if (previousSelectedWords === null || previousSelectedWords === undefined) {
        localStorage.setItem("selectedWords", newWord);
        return true;
    } else if (previousSelectedWords.indexOf(newWord) > -1) {
        return false;
    } else {
        previousSelectedWords += ("," + newWord);
        localStorage.setItem("selectedWords", previousSelectedWords);
        return true;
    }
};


var createWordCardHtml = function(word, indexOfCard) {
    var wordSegments = word.split("$$"),
        cls = (indexOfCard % 2 == 0 ? "bg-secondary" : "bg-primary"),
        word = wordSegments[2],
        wordCardHtml = (
            "<span class='badge " + cls + " m-1'>" + word + "</span>");
    return wordCardHtml;
};


var addWordCards = function(wordContainerCtrl, selectedWords) {
    var splitWords = selectedWords.split(","),
        html = "";
    for(var i = 0, len = splitWords.length; i < len; i++) {
        html += createWordCardHtml(splitWords[i], i);
    }
    wordContainerCtrl.innerHTML = html;
};


var setChoosenWords = function(choosenWordsCtrlRef, selectedWords) {
    if (choosenWordsCtrlRef === null || choosenWordsCtrlRef === undefined) {
        console.log("Choosen Word control reference is invalid");
    }
    choosenWordsCtrlRef.value = selectedWords;
};

localStorage.removeItem("selectedWords");


for(var i = 0, len = addBtnCtrls.length; i < len; i++) {

    addBtnCtrls[i].addEventListener('click', function(event) {
        event.preventDefault();
        var dataContainer = this.parentElement.getAttribute('data-container'),
            selectedWords = getSelectedWords();

        var result = addNewSelectedWords(selectedWords, dataContainer);
        
        if (result) {
            addWordCards(buildWordContainer, getSelectedWords());
            setChoosenWords(choosenWordsCtrl, getSelectedWords());
        }

    });

};

clearChoosenWordBtn.addEventListener('click', function(event) {
    event.preventDefault();
    localStorage.removeItem("selectedWords");
    choosenWordsCtrl.value = "";
    buildWordContainer.innerHTML = "";
});