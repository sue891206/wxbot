$(document).ready(function () {
    login();
    logout();
});

function login() {

    var $keySendBtn = $('#keySend');
    var $keyInput = $('#keyInput');
    var url = 'http://localhost:8001/wxbot/create/';

    var $imgLoading = $('#loading-img');
    var $imgQrcode = $('#qrcode-img');

    var $yesLoginBtn = $('#yesLogin');
    var $loginModal = $('#loginModal');

    $keySendBtn.click(function () {
        $imgLoading.show();
        $.ajax({
            url: url + $keyInput.val()
        }).done(function (data) {
            data = JSON.parse(data);
            if (data.code == 0) {
                $imgLoading.attr('src', data.png);
            }

        });
        return false;
    });

    $yesLoginBtn.click(function () {
        $loginModal.modal('hide');
        window.location.reload();
    });
}

function logout() {
    var $logoutBtn = $('.logoutBtn');
    var $logoutModal = $('#logoutModal');
    var $usrname = $('#modalUsername');
    var $yesBtn = $('#yesLogout');

    var url = 'http://localhost:8001/wxbot/logouthash/';

    $logoutBtn.click(function () {
        var $tr = $(this).parents('tr');
        var username = $tr.data('username');
        var md5 = $tr.data('md5');

        $usrname.text(username);
        $logoutModal.data('md5', md5);
    });

    $yesBtn.click(function () {
        var md5 = $logoutModal.data('md5');
        $.ajax({
            url: url + md5
        }).done(function (data) {
            data = JSON.parse(data);
            if (data.code == 0) {
                console.log('done!');
                $logoutModal.modal('hide');
                window.location.reload();
            }

        });
        return false;
    });


}
