let this_page = 1;
$('.load-more-movies').click(function(page) {

    $.ajax({
        // url: "{{ url_for('load_more_movies')|tojson }}",
        url: "http://127.0.0.1/load_more_movies/",
        type: "post",
        data: {
            page: this_page,
        },
        dataType: 'json',
        success: function(data) {
            console.log(this_page)
            console.log(Object.keys(data).length)
            if (Object.keys(data).length) {

                for (i in data) {
                    // add_dom_to_movies_area('#movies_list_area')
                    str = `
                            <!-- Single Album Area -->
                            <div class="col-12 col-sm-6 col-md-4 col-lg-2">
                                <div class="single-album-area wow fadeInUp" data-wow-delay="100ms"></div>
                                    <div class="album-thumb">
                                        <img src="${data[i].img_url} " alt="${data[i].title}">
                                        <!-- Album Price -->
                                        <div class="album-price">
                                            <p><strong> TOP ${data[i].ranking} </strong></p>
                                        </div>
                                    </div>
                                    <div class="album-info">
                                        <a href="#">
                                            <h5> ${data[i].title} | ${data[i].score}</h5>
                                        </a>
                                        <p>${data[i].stars}</p>
                                    </div>
                                </div>
                            </div>
                            `
                    $('#movies_list_area').append(str);
                }
                this_page += 1

            } else {
                $('.load-more-movies').text("NO MORE")
            }
        },
        error: function(e) {
            alert("error");
        }
    })


})


$('#login-btn').click(function() {

    var form_data = {};
    var t = $('#loginForm').serializeArray();
    $.each(t, function() {
        form_data[this.name] = this.value;
    });

    $.ajax({
        url: "http://127.0.0.1/login/",
        type: "post",
        // data: {
        //     email: $('#exampleInputEmail1').val(),
        //     password: $('#exampleInputPassword1').val(),
        // },
        data: form_data,
        dataType: 'json',
        success: function(data) {
            console.log(data)
            console.log(data.message)
            if (data.status == "success") {
                window.location.href = data.message;
            } else {
                $('.err_message').html(`<i class= "fa fa-warning (alias) mr-2" ></i >` + data.message)
            }



        },
        error: function(e) {
            alert("error");
        }
    })
})

$('#register-btn').click(function() {

    var form_data = {};
    var t = $('#registerForm').serializeArray();
    $.each(t, function() {
        form_data[this.name] = this.value;
    });

    $.ajax({
        url: "http://127.0.0.1/register/",
        type: "post",
        // data: {
        //     username: $('#register-username').val(),
        //     email: $('#register-email').val(),
        //     pssword1: $('#register-password1').val(),
        //     pssword2: $('#register-password2').val(),
        // },
        data: form_data,
        dataType: 'json',
        success: function(data) {
            console.log(daata)

        },
        error: function(e) {
            alert("error");
        }
    })


})