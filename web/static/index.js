$(document).ready(function () {
    login();
});

function login() {
    
    var $keySendBtn = $('#keySend');
    var $keyInput = $('#keyInput');
    var url = 'http://localhost:8001/wxbot/create/';

    $keySendBtn.click(function () {

        $.ajax({
            url: url + $keyInput.val()
        }).done(function (data) {
            console.log(data);
        });
        return false;
    })
}
