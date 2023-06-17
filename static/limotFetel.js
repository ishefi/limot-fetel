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
        try {
            var tempNons = await response.json();
            const roots = tempNons.roots;

            $.each(["template", "weight"], function(i, twName) {
                 let tableId = "#" + twName + "Nons";
                 let thead = $(tableId + " thead");
                 if (thead.length === 0) {
                     thead = $("<thead>");
                     $(tableId).append(thead);
                 } else {
                     thead.empty();
                 }
                 let headTr = $("<tr>");
                 headTr.append($("<th>").html("Template"));
                 $.each(roots, function(i, root) {
                     headTr.append($("<th>").html(root));
                 });
                 thead.append(headTr);

                 let tbody = $(tableId + " tbody");
                 if (tbody.length === 0) {
                     tbody = $("<tbody>");
                     $("#" + twName).append(tbody);
                 } else {
                     tbody.empty();
                 }
                 $.each(tempNons[twName + "s"], function(i, tw) {
                     let trid = tw;
                     let tr = $('<tr>').attr("id", trid);
                     tr.append($('<td>').append($("<b>").html(tw)));
                     $.each(roots, function(i, root) {
                         let tdid = trid + '-' + root.replace(/\s/g, '');
                         $('<td>').attr("id", tdid).appendTo(tr);
                     });
                     tbody.append(tr);
                 });
            });
            $.each(tempNons.data, function(i, tempNon) {
                var trid = tempNon.template;
                var tdid = tempNon.root.replace(/\s/g, '');
                $("td#" + trid + '-' + tdid).html(tempNon.populated);
            });
        } catch(e) {
            console.log(e);
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
