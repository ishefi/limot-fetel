let limotFetel = (function() {
    'use strict';

    function getTempWeight(tempWeight) {
        if ($("#" + tempWeight + "All").is(":checked")) {
            return [];
        } else {
            let tws = [];
            $("#" + tempWeight).find(":selected").each(function() {
                tws.push(this.value);
            });

            return tws;
        }
    }

    async function getWords() {
        const params = new URLSearchParams({
            weights: getTempWeight("weights"),
            templates: getTempWeight("templates"),
            p: $("#פ").find(":selected").attr("value"),
            a: $("#ע").find(":selected").attr("value"),
            l: $("#ל").find(":selected").attr("value"),
        });

        const url = "/api/non-words?" + params.toString();
        const response = await fetch(url);
        let wordList = $("#wordList");
        wordList.empty();
        try {
        var words = await response.json();
            for (let word of words) {
                var node = document.createElement("li");
                var textNode = document.createTextNode(word);
                node.appendChild(textNode);
                wordList.append(node);
            }
        } catch(e) {
            return null;
        }
    }

    for (let tw of ["weights", "templates"]) {
        $("#" + tw + "All").change(function () {
            let tws = $("#" + tw);
            if (this.checked === true) { tws.attr("disabled", "disabled") }
            else { tws.removeAttr("disabled")}
        })
    }


    $('#getWords').on("click",getWords);

    return {
    // API
    }
}
);

limotFetel();
$(document).ready(limotFetel);
