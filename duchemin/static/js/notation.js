function log(msg) {
    setTimeout(function() {
        throw new Error(msg);
    }, 0);
}

function attachPhraseClickEvents() {
    $('.view-phrase').on({
        'click': function(event) {
            $("#analysis-modal").remove();
            var modal = $("<div />", {
                "id": "analysis-modal"
            }).appendTo("body");

            $("#analysis-modal").dialog({
                'height': 600,
                'width': 980,
                'modal': true,
                'title': $(this).data('pieceid') + ', phrase ' + $(this).data('phrasenum')
            });
            $("<div />", {
                "class": "analysis-modal-body"
            }).appendTo(modal);
            ajaxRenderAnalysis($(this).attr('phid'), $(this).data('pieceid'),
                $(this).data('start'), $(this).data('stop'), true);
            return false;
        }
    });
}

function attachAnalysisClickEvents() {
    $('.view-analysis').on({
        'click': function(event) {
            $("#analysis-modal").remove();
            var modal = $("<div />", {
                "id": "analysis-modal"
            }).appendTo("body");

            $("#analysis-modal").dialog({
                'height': 600,
                'width': 980,
                'modal': true,
                'title': ($(this).data('pieceid') + ', measures ' +
                    $(this).data('start') + '–' + $(this).data('stop'))
            });
            $("<div />", {
                "class": "analysis-modal-body"
            }).appendTo(modal);
            ajaxRenderAnalysis($(this).attr('anid'), $(this).data('pieceid'),
                $(this).data('start'), $(this).data('stop'), false);
            return false;
        }
    });
}

function ajaxRenderAnalysis(id, piece_id, start, end, phrase) {
    $.ajax({
        url: (phrase ? '/data/phrase/' : '/data/analysis/')  + id,
        dataType: 'json',
        success: function(data, status, xhr) {
            var loadedXML = meiView.Util.loadXMLDoc('/static/xml/' + piece_id + '.xml');
            var filteredXml = meiView.filterMei(loadedXML, { noSysBreak:true });
            var meiDoc = new MeiLib.MeiDoc(filteredXml);

            var pagination = new meiView.Pages();

            /* If you want scrolling: */
            pagination.AddPage(start, end);

            /* If you want pagination rather than scrolling:

            // Throughout, -1 appears because measures are not counted "logically"
            var max_m = start;

            while (max_m < end) {
                if (end - (max_m - 1) < 8) {
                    // Less than 8 measures left: fit it all in
                    pagination.AddPage(max_m, end);
                    max_m = end;
                }
                else if (end - (max_m - 1) < 12) {
                    // To avoid uneven cramming at the end, consider pages of 5
                    pagination.AddPage(max_m, max_m + 4);
                    max_m += 5;
                }
                else {
                    pagination.AddPage(max_m, max_m + 3);
                    max_m += 4;
                }
            }
            */

            var modal_viewer = new meiView.CompactViewer({
                maindiv: $('.analysis-modal-body'),
                MEI: meiDoc,
                pages: pagination,
                title: "",
                displayFirstPage: true,
                scale: 0.85,
                pxpMeasure: 200,
            });

            var modal = $("#analysis-modal");
        }
    });
}
