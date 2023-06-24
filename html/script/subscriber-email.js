$("#sent_a_new_newsletter_btn").click(function(){
    const subject = $("#subject").val();
    const body = tinymce.get("editor").getContent();
    let delay = $("#delay").val();
    if(delay == null || delay == ''){
        delay = 0;
    }
    if(subject == null || body == null){
        alert("Fill all fields");
        return;
    }
    else if(subject == '' || body == ''){
        alert("Fill all fields");
        return;
    }
    else{
        $.ajax({
            type: "POST",
            url: "http://localhost:8000/api/newsletter/",
            data : {
                'subject' : subject,
                'body' : body.toString(),
                'delay' : delay
            },
            success: function(response){
                alert("Sending..")
            }
        });
    }
});

$("#add_a_new_subscriber_btn").click(function(){
    const first_name = $("#first_name").val();
    const last_name = $("#last_name").val();
    const email = $("#email").val();
    const birthday = $("#birthday").val();

    if(first_name == null || last_name == null || email == null || birthday == null){
        alert("Fill all fields");
        return;
    }
    else if(first_name == '' || last_name == '' || email == '' || birthday == ''){
        alert("Fill all fields");
        return;
    }
    else{
        $.ajax({
            type: "POST",
            url: "http://localhost:8000/api/subscriber/",
            data : {
                'first_name' : first_name,
                'last_name' : last_name,
                'email' : email,
                'birthday' : birthday
            },
            success: function(response){
                alert("Added..")
            }
        });
    }
});