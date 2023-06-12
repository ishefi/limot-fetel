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
            p: $("#פ").find(":selected").attr("value"),
            a: $("#ע").find(":selected").attr("value"),
            l: $("#ל").find(":selected").attr("value"),
        });
        for (let tw of ["templates", "weights"]) {
            let tws = getTempWeight(tw);
            if (tws.length !== 0) {
                params.set(tw, tws)
            }
        }

        const url = "/api/non-words?" + params.toString();
        const response = await fetch(url);
        let wordList = $("#wordList");
        wordList.empty();
        try {
        var tempNons = await response.json();
            for (let tempNon of tempNons) {
                var node = document.createElement("li");
                var textNode = document.createTextNode(tempNon.template);
                node.appendChild(textNode);
                var nonList = document.createElement("ul");

                for (let non of tempNon.nons) {
                    var nonNode = document.createElement("li");
                    var nonTextNode = document.createTextNode(non);
                    nonNode.appendChild(nonTextNode);
                    nonList.appendChild(nonNode);
                }
                node.appendChild(nonList);
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
