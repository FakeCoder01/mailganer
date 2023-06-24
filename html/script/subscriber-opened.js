const url = new URL(window.location.href);
const id = url.searchParams.get("id");

if(id == undefined || id == null || id == '') {
    window.location.href =  "/mailganer?error=id-no-present";
}

$.ajax({
    type: "GET",
    url: "http://localhost:8000/api/subscriber/"+id+"/",
    success: function(response){
        const opened_emails = document.getElementById("opened_emails");
        opened_emails.innerHTML = '';
        $("#first_name_update").val(response.person.first_name);
        $("#last_name_update").val(response.person.last_name);
        $("#email_update").val(response.person.email);
        $("#birthday_update").val(response.person.birthday);

        response.forEach(email => {
            opened_emails.innerHTML += `
                <tr>
                    <td>${email.email}</td>
                    <td>${email.subject}</td>
                    <td>${email.opened_at}</td>
                    <td class="text-center">
                        <a href="email-opened.html?id=${email.email}" class="btn btn-primary">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="white"
                                class="bi bi-eye" viewBox="0 0 16 16">
                                <path
                                    d="M16 8s-3-5.5-8-5.5S0 8 0 8s3 5.5 8 5.5S16 8 16 8zM1.173 8a13.133 13.133 0 0 1 1.66-2.043C4.12 4.668 5.88 3.5 8 3.5c2.12 0 3.879 1.168 5.168 2.457A13.133 13.133 0 0 1 14.828 8c-.058.087-.122.183-.195.288-.335.48-.83 1.12-1.465 1.755C11.879 11.332 10.119 12.5 8 12.5c-2.12 0-3.879-1.168-5.168-2.457A13.134 13.134 0 0 1 1.172 8z" />
                                <path
                                    d="M8 5.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5zM4.5 8a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0z" />
                            </svg>
                        </a>
                    </td>
                </tr>
            `;
        });

    }
});



$("#update_existing_subscriber_btn").click(function(){
    const first_name = $("#first_name_update").val();
    const last_name = $("#last_name_update").val();
    const email = $("#email_update").val();
    const birthday = $("#birthday_update").val();

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
            type: "PUT",
            url: "http://localhost:8000/api/subscriber/"+id+"/",
            data : {
                'first_name' : first_name,
                'last_name' : last_name,
                'email' : email,
                'birthday' : birthday
            },
            success: function(response){
                alert("Updated..")
            }
        });
    }
});