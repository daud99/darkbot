var checker=0;

$(document).ready(function(){
    if ($('#search-dropdown').val()=="3" && $('#type-dropdown').val()=="2")
    {
        addOption();
    }
    
    if ($('#search-dropdown').val()=="3")
    {
        $("#bankOptions").removeClass("d-none");   
    }
    if ($('#search-dropdown').val()=="2")
    {
        $("#emailOptions").removeClass("d-none");
        if($('#email-search-type').val()=="1")
        {
            add_email_options();
        }
        else if ($('#email-search-type').val()=="2")
        {
            add_password_options();
        } 
        else if ($('#email-search-type').val()=="3")
        {
                add_uname_options();
        }   
    }

    $('#email-search-type').on('change',function(e)
    {
        if($('#email-search-type').val()=="1")
        {
            add_email_options();
        }
        else if ($('#email-search-type').val()=="2")
        {
            add_password_options();
        }   
        else if ($('#email-search-type').val()=="3")
        {
                add_uname_options();
        }  
    });

    $('#type-dropdown').on('change',function(e)
    {
        if ($('#type-dropdown').val()=="2")
            { 
                    addOption()
            }
        else
        {
                removeOption()
        }
    });
    $('#search-dropdown').on('change',function(e){
        
         e.preventDefault();
        var parca_turu = $(this).val();
        if (parca_turu =="3")
        {
            $("#bankOptions").removeClass("d-none");
            if ($('#type-dropdown').val()=="2")
            { 
                    addOption()
            }
            else
            {
                    removeOption()
            }
        }
        
        else
        $("#bankOptions").addClass("d-none");
        if (parca_turu =="2")
        {
        $("#emailOptions").removeClass("d-none");
            if($('#email-search-type').val()=="1")
            {
                add_email_options();
            }
            else if ($('#email-search-type').val()=="2")
            {
                    add_password_options();
            }   
            else if ($('#email-search-type').val()=="3")
            {
                    add_uname_options();
            }  
        }
        else
        $("#emailOptions").addClass("d-none");
        console.log("Secilen: "+parca_turu);
        $.ajax({
            url:"",
            method:'POST',
          // send selected data to the parca_kayit method which is in views.py
            data : {'category' : $(this).val()}, // 'parcaAdi' will be used in request.GET.get('parcaAdi') which is in views.py, $(this).val() is selected item,
            success:function(gelen_parca_turu){
                //console.log(gelen_parca_turu);
            }
        });
        $("#userpopup").css("display","none");
        $("#userpopup2").css("display","none");
        $("#search-field").removeClass("is-invalid");
        checker=0;
    });
    console.log("checker outside is: "+checker);

    /*$('#seach-field').on('click',function(e){
         if(checker==1)
    {
        console.log("this is checker value : "+checker);
        $("#search-field").focusin(function(){
            console.log("hello");
            $("#userpopup").css("display","none");
            $("#search-field").removeClass("is-invalid");
            });
        }
    });
    $('#seach-field').on('click',function(e){
         if(checker==1)
    {
        console.log("this is checker value : "+checker);
        $("#search-field").focusin(function(){
            console.log("hello");
            $("#userpopup").css("display","none");
            $("#search-field").removeClass("is-invalid");
            });


            $("#search-field").focusout(function(){
            console.log("hello");
            $("#userpopup").css("display","block");
            $("#search-field").addClass("is-invalid");
            });
    }
    });*/


});

function loading(){
            var a=$("#search-field").val();
            var selectedOption = $( "#search-dropdown").val();
            console.log("this is a: "+a);
            /*$("#search-dropdown").change(function(){
                selectedOption = $(this).children("option:selected").val();
            });*/
            console.log(selectedOption);
            if(a==""||a==null)
            {
                return false;
            }
            else if (a!=""&&a!=null&&selectedOption=="2")
            {
                if($('#email-search-type').val()==1)
                {
                    if( !validateEmail(a))
                    {
                        $("#userpopup").css("display", "block");
                        $("#search-field").addClass("is-invalid");
                        checker=1;
                        return false;
                    }
                    else
                    {
                    console.log("hello");
                    $("#userpopup").css("display","none");
                    $("#search-field").removeClass("is-invalid");
                    $("#loading").show();
                    $(".wrapper").hide();
                    checker=0;
                    return true;

                    }
                }
                else if ($('#email-search-type').val()==3)
                {
                    if( validateEmail(a))
                    {
                        $("#userpopup2").css("display", "block");
                        $("#search-field").addClass("is-invalid");
                        checker=1;
                        return false;
                    }
                    else
                    {
                    console.log("hello");
                    $("#userpopup2").css("display","none");
                    $("#search-field").removeClass("is-invalid");
                    $("#loading").show();
                    $(".wrapper").hide();
                    checker=0;
                    return true;
    
                    }
                }
            }
            
                $("#loading").show();
                $(".wrapper").hide();
                checker=0;


        }

function validateEmail($email) {
  var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
  return emailReg.test( $email );
}

function fcus(){
    if(checker==1)
    {

            console.log("hello");
            $("#userpopup").css("display","none");
            $("#search-field").removeClass("is-invalid");
    }

}

function blu(){
    if(checker==1)
    {
        console.log("this is checker value : "+checker);
  $("#userpopup").css("display","block");
            $("#search-field").addClass("is-invalid");

    }
}

function scrollToServices() {

    window.scrollTo(0, 1780);

    // if(window.location == "http://127.0.0.1:8000") {
    //
    // }
}
function scrollToTeam() {
  window.scrollTo(0, 2430);
}

function addOption() { 
    optionText = 'Owner Name'; 
    optionValue = '5'; 
    opt_class = 'removableOption'
    $('#option-dropdown').append(`<option class="${opt_class}" value="${optionValue}"> 
                               ${optionText} 
                          </option>`); 
    optionText = 'City'; 
    optionValue = '6'; 

    $('#option-dropdown').append(`<option class="${opt_class}" value="${optionValue}"> 
                                ${optionText} 
                        </option>`); 
    optionText = 'Zip No'; 
    optionValue = '7'; 

    $('#option-dropdown').append(`<option class="${opt_class}" value="${optionValue}"> 
                                ${optionText} 
                        </option>`); 
} 

function removeOption()
{
    $("option[class='removableOption']").remove();
}
function add_email_options()
{

    optionText = 'DarkNet Int'; 
    optionValue = '1'; 
    opt_class = 'removableOption'
    $('#email-search-what').empty().append(`<option class="${opt_class}" value="${optionValue}"> 
                               ${optionText} 
                          </option>`); 
    optionText = 'Clean Passwords'; 
    optionValue = '2'; 

    $('#email-search-what').append(`<option class="${opt_class}" value="${optionValue}"> 
                                ${optionText} 
                        </option>`); 
    optionText = 'Trace in Breaches'; 
    optionValue = '3'; 

    $('#email-search-what').append(`<option class="${opt_class}" value="${optionValue}"> 
                                ${optionText} 
                        </option>`); 
    optionText = 'Trace Pastes'; 
    optionValue = '4'; 

    $('#email-search-what').append(`<option class="${opt_class}" value="${optionValue}"> 
                                ${optionText} 
                        </option>`); 
}
function add_password_options()
{

    optionText = 'Clean Passwords'; 
    optionValue = '1'; 
    opt_class = 'removableOption'
    $('#email-search-what').empty().append(`<option class="${opt_class}" value="${optionValue}"> 
                               ${optionText} 
                          </option>`); 
    optionText = 'SHA-1 Passwords'; 
    optionValue = '2'; 

    $('#email-search-what').append(`<option class="${opt_class}" value="${optionValue}"> 
                                ${optionText} 
                        </option>`); 
    
}


function add_uname_options()
{

    optionText = 'Clean Password'; 
    optionValue = '1'; 
    opt_class = 'removableOption'
    $('#email-search-what').empty().append(`<option class="${opt_class}" value="${optionValue}"> 
                               ${optionText} 
                          </option>`); 
    optionText = 'DarkNet Int'; 
    optionValue = '2'; 
    opt_class = 'removableOption'
    $('#email-search-what').append(`<option class="${opt_class}" value="${optionValue}"> 
                                ${optionText} 
                        </option>`); 
}
$('.dumps_table_row').click(function(){
    var check = false;
    if ($(this).next('tr').hasClass('d-none'))
        check = true;
    // $('.hiddenRow').hide();
    //$('.p').hide();
    $('.p').addClass("d-none");
    if (check)
    {
    $(this).next('tr').removeClass("d-none");
    //$(this).next('tr').show();
    // $(this).next('tr').find('.hiddenRow').show();
    }
     
});

