$(document).ready(function () {
    $('.toast').not("#report-toast").toast('show');
})
$("#project-report-btn").click(function(){
    $.ajax({
        url: '/project/report/',
        method: 'GET',
        data:{
            body: $("#report-message").val(),
            project: $("#project_id").val()
        },
        success: function(data){
            if (data.return){
                $('#report-toast').toast('show')
                $("#report-message").val('')
                $("#exampleModal").modal("hide")
            }else{
                alert("error reporting")
            }
        }
    })

})

$('#commentReportModal').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Button that triggered the modal
  var comment = button.data('comment') // Extract info from data-* attributes
  var modal = $(this)
  modal.find('.created-by').text('created by '+ button.data('created-by'))

  $("#commentReportBtn").click(function(){
    $.ajax({
            url: `/comment_report/${comment}`,
            method: 'GET',
            data:{
                body: $("#commentReportMessage").val()
            },
            success: function(data){
            console.log(data)
                if (data.return){
                    $('#report-toast').toast('show')
                    $("#commentReportMessage").val('')
                    $("#commentReportModal").modal("hide")
                }else{
                    alert("error reporting")
                }
            }
        })
    })
})

