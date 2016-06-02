/*RFPV - Dialog code*/
// WARNING: jQuery serialize() dont serialize hidden or disabled elements
//variables globales para la acción
var currentRecordId=-1; /* Current record Id */
var currentURLAction=''; /* Current URL action */
var currentTableName=''; /* Current URL action */

$(document).ready(function() {
    /*
    $('#windowTitleDialog').bind('show', function () {
        document.getElementById ("xlInput").value = document.title;
    });
    */
});

/* New Dialog begin */
function newDialogShow(url,tablename) {
    /**
     * New dialog show
     */
    $("#newDialog").modal();
    currentRecordId=-1;
    currentURLAction=url;
    currentTableName=tablename;
    var muestreo = $("#muestreo_id").val();
    // Get form by ajax POST and fill newResult div
    $.post(
        url,
        {dataAction:'new', tableName:tablename, muestreo:muestreo},
        function(data) {
            $('#newResult').html(data);
            $("#EnfermedadesEucalyptus_tipo_enfermedad").prop("disabled", true);
            $("#EnfermedadesEucalyptus_opcion_id").prop("disabled", true);
            $.post(
                '/lifn/default/getavailabletreese',
                {muestreo:muestreo},
                function(info) {
                    $('#newResult').append(info);
                }
            );
            $("#EnfermedadesEucalyptus_numArbol").focusout(function()
            {
                var numArbol = $("#EnfermedadesEucalyptus_numArbol").val();
                if(numArbol != "")
                {
                    $("#EnfermedadesEucalyptus_tipo_enfermedad").prop("disabled", false);
                    var request = $.getJSON("/lifn/default/getRemainingDiseasesEucalyptus?numArbol="+numArbol, function(data){
                        $("#EnfermedadesEucalyptus_tipo_enfermedad").html("");
                        var options = {};
                        $.each(data, function(key, val) {
                            if(key == "error")
                            {
                                alert(val);
                                $("#EnfermedadesEucalyptus_opcion_id").prop("disabled", true);
                                $("#EnfermedadesEucalyptus_tipo_enfermedad").prop("disabled", true);
                                $("#EnfermedadesEucalyptus_tipo_enfermedad").html("");
                                $("#EnfermedadesEucalyptus_opcion_id").html("");
                                $("#EnfermedadesEucalyptus_numArbol").val("");
                            }
                            else
                            {
                            $("#EnfermedadesEucalyptus_tipo_enfermedad").append("<option value=" + key + ">" + val + "</option>");
                            }
                        });      
                    });
                }

            })
            $("#EnfermedadesEucalyptus_tipo_enfermedad").change(function() {
                var idPlant = $("#EnfermedadesEucalyptus_tipo_enfermedad").val();
                if (idPlant == ""){
                    $("#EnfermedadesEucalyptus_opcion_id").prop("disabled", true);
                    $("#EnfermedadesEucalyptus_opcion_id").html("");
                } else {
                    $("#EnfermedadesEucalyptus_opcion_id").prop("disabled", false);
                    var request = $.getJSON("/lifn/default/subSelectDataSanidadE?id="+idPlant, function(data){
                        $("#EnfermedadesEucalyptus_opcion_id").html("");
                        var options = {};
                        $.each(data, function(key, val) {
                            $("#EnfermedadesEucalyptus_opcion_id").append("<option value=" + key + ">" + val + "</option>");
                        });      
                    });
                }
            });
        }
    );
    //return false dont process href on a
    return false;
};

function newDialogClose() {
    $('#newDialog').modal('hide');
};

function newDialogSave() {
    /**
     * New dialog show
     */
    // Send (POST) form by ajax and close the modal dialog
    var muestreo = $("#muestreo_id").val();
    $.post(
        currentURLAction,
        $('form#datamanager-new').serialize()+"&muestreo="+muestreo,
        function(data) {
            if (data.result==true) {
                // Data added, reload current page
                location.reload();
            } else {
                alert(data.message);
            }
        },
        'json' //data returned is json
    );
    newDialogClose();
    currentRecordId=-1;
    currentURLAction='';
    currentTableName='';
};
/* New Dialog end */

/* Edit Dialog begin */
function editDialogShow (url,tablename,recordId) {
    $("#editDialog").modal();
    currentRecordId=recordId;
    currentURLAction=url;
    currentTableName=tablename;
    // POST via ajax
    $.post(
        url,
        {dataAction:'edit', tableName:tablename, dataId:recordId},
        function(data) {
            $('#editResult').html(data);
            var idPlant = $("#EnfermedadesEucalyptus_tipo_enfermedad").val();
            if (idPlant == ""){
                $("#EnfermedadesEucalyptus_opcion_id").prop("disabled", true);
                $("#EnfermedadesEucalyptus_opcion_id").html("");
            } else {
                $("#EnfermedadesEucalyptus_opcion_id").prop("disabled", false);
                var request = $.getJSON("/lifn/default/subSelectDataSanidadE?id="+idPlant, function(data){
                    $("#EnfermedadesEucalyptus_opcion_id").html("");
                    var options = {};
                    $.each(data, function(key, val) {
                        $("#EnfermedadesEucalyptus_opcion_id").append("<option value=" + key + ">" + val + "</option>");
                    });      
                });
            }
            $("#EnfermedadesEucalyptus_tipo_enfermedad").change(function() {
                var idPlant = $("#EnfermedadesEucalyptus_tipo_enfermedad").val();
                if (idPlant == ""){
                    $("#EnfermedadesEucalyptus_opcion_id").prop("disabled", true);
                    $("#EnfermedadesEucalyptus_opcion_id").html("");
                } else {
                    $("#EnfermedadesEucalyptus_opcion_id").prop("disabled", false);
                    var request = $.getJSON("/lifn/default/subSelectDataSanidadE?id="+idPlant, function(data){
                        $("#EnfermedadesEucalyptus_opcion_id").html("");
                        var options = {};
                        $.each(data, function(key, val) {
                            $("#EnfermedadesEucalyptus_opcion_id").append("<option value=" + key + ">" + val + "</option>");
                        });      
                    });
                }
            });
        }
    );
    //return false dont process href on a
    return false;
};

function editDialogClose() {
    $('#editDialog').modal('hide');
};

function editDialogSave() {
    // POST form via ajax
    $.post(
        currentURLAction,
        $('form#datamanager-edit').serialize(),
        function(data) {
            if (data.result==true) {
                // Data added, reload current page
                location.reload();
            } else {
                alert(data.message);
            }
        },
        'json' //data returned is json
    );
    editDialogClose();
    currentRecordId=-1;
    currentURLAction='';
    currentTableName='';
};
/* Edit Dialog end */

/* Delete Dialog begin */
function deleteDialogShow(url,tablename,recordId) {
    $("#deleteDialog").modal();
    currentRecordId=recordId;
    currentURLAction=url;
    currentTableName=tablename;
    //Write HTML table of record to modal dialog data area
    var title=tableGetHeaders();
    var data=tableGetRowById(currentRecordId);
    tableWrite(title, data, "deleteResult");
    //return false dont process href on a
    return false;
};

function deleteDialogClose() {
    $('#deleteDialog').modal('hide');
};

function deleteDialogDelete() {
    $.post(
        currentURLAction,
        {dataAction:'delete', tableName:currentTableName, dataId:currentRecordId},
        function(data) {
            //Parse string as JSON
            // var jsonData = jQuery.parseJSON(data);
            if (data.result==true) {
                // Reload current page
                location.reload();
            } else {
                alert(data.message);
            }
        },
        'json' //data returned is json
    );
    deleteDialogClose();
    currentRecordId=-1;
    currentURLAction='';
    currentTableName='';
};
/* Delete end */

/* Details dialog begin */
function detailsEDialogShow (url, recordId) {
    $("#detailsEDialog").modal();
    currentRecordId=recordId;
    currentURLAction=url;
    currentTableName='';
    // POST via ajax
    $.post(
        url,
        {dataId:recordId},
        function(data) {
            $('#detailsEResult').html(data);
        }
    );
    //return false dont process href on a
    return false;
};

function detailsEDialogClose() {
    $('#detailsEDialog #save').attr('disabled',true);
    $('#detailsEDialog').modal('hide');
    rid=[];
    rcint=[];
    rdest=[];
    rfdest=[];
};

function detailsEDialogSave() {
    // POST form via ajax
    formCustomPost();
    detailsEDialogClose();
    currentRecordId=-1;
    currentURLAction='';
    currentTableName='';
};
/* Details dialog end */


/* Deleteall Dialog begin */
function deleteAllDialogShow(url,tablename) {
    /**
     * Show the deleteAll Dialog
     */
    $("#deleteAllDialog").modal();
    currentRecordId=-1;
    currentURLAction=url;
    currentTableName=tablename;
    //return false dont process href on a
    return false;
};

function deleteAllDialogClose() {
    /**
     * Close the deleteAll Dialog
     */
    $('#deleteAllDialog').modal('hide');
};

function deleteAllDialogDelete() {
    $.post(
        currentURLAction,
        {dataAction:'deleteAll', tableName:currentTableName},
        function(data) {
            //Parse string as JSON
            // var jsonData = jQuery.parseJSON(data);
            if (data.result==true) {
                // Reload current page
                location.reload();
            } else {
                alert(data.message);
            }
        },
        'json' //data returned is json
    );
    deleteDialogClose();
    currentRecordId=-1;
    currentURLAction='';
    currentTableName='';
};
/* Deleteall Dialog end */

/* Utils begin */
function tableWrite(tit, dat, target) {
    /** Write html table with tit, dat in this target
    */
    var html = '<table class="show-data">\n';
    len = dat.length;
    for (var i = 0; i < len; i++)
    {
        html += '<tr><td class="cell-title">' + tit[i] + '</td><td class="cell-data">' + dat[i] + '</td></tr>';
    }
    html += '</table>\n';
    $('#' + target).html(html);
}

function tableGetRowById(rowId, initCol, endCol) {
    /**
     * Get row (total o partoally) by his id (<tr id=1>) and return
     * an array
    */
    cellArr = new Array();
    // Get text of each cell in this table row
    $('table tr#' + rowId + ' td').each(function(){
        cellArr.push($(this).text());
    });

    if (typeof(initCol)==='undefined') {
        initCol=0;
    }

    // Dont get last col
    if (typeof(endCol)==='undefined') {
        if (cellArr.length==1) {
            endCol=0;
        } else {
          endCol=cellArr.length-1;
        }
    }

    return cellArr.slice( initCol, endCol);
};

function tableGetHeaders(initCol, endCol) {
    /**
     * Get heders (total o partially) of a table
    */
    cellArr = new Array();
    // Get text of each cell in this table row
    $('table tr th').each(function(){
        cellArr.push($(this).text());
    });

    if (typeof(initCol)==='undefined') {
        initCol=0;
    } else {
        if ( (initCol<0) || (initCol>(cellArr.length-1)) ) {
            initCol=0;
        }
    }

    // Dont get last col
    if (typeof(endCol)==='undefined') {
        endCol=cellArr.length-1;
    } else {
        if ( (endCol<0) || (endCol>(cellArr.length-1)) ) {
            endCol=initCol+1;
        }
    }

    return cellArr.slice(initCol, endCol);
};

function tableDeleteRowById(rowId) {
    /**
     * Delete a row in a table by his id
    */
    $('table tr#' + rowId).remove();
};

function selectAllRows(val) {
    /**
     * Selecciona todos los registros en la tabla
     */
    $('div.web2py_htmltable input[type=checkbox]').attr('checked', val);
    checkControlOthers();
};

function checkControlOthers() {
    /**
     * Utilidades y cambios en el menu util segun la accion
     */
    var tcb=$('div.web2py_htmltable input[type=checkbox]').length;
    var ccb=$('div.web2py_htmltable input:checked').length;
    if (ccb>0) {
        $('a#unselectRows').show();
        $('a#cloneSelectedRows').show();
        if (ccb==tcb) {
            $('a#selectAllRows').hide();
        } else {
            $('a#selectAllRows').show();
        }
    } else {
        $('a#selectAllRows').show();
        $('a#unselectRows').hide();
        $('a#cloneSelectedRows').hide();
    }
};

/* Utils end */
