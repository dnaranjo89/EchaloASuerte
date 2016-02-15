Raffle = {};
Raffle.url_register = null;
Raffle.url_raffle = null;

/**
 * Show FB registration button and bind the registration event to it
 */
Raffle.fb_enable_registration = function(){
    var $fb_register = $('#register-raffle-fb');
    $fb_register.toggleClass('hidden', false);
    $fb_register.click(Raffle.fb_share_to_participate);
};

Raffle.register_in_server = function(participant_id, participant_name){
    var participant_details = {
        participant_id : participant_id,
        participant_name: participant_name
    };
    $.ajax({
        method : "POST",
        contentType : 'application/json',
        url : Raffle.url_register,
        data: JSON.stringify(participant_details),
        statusCode: {
            200: function(){
                $('#id_participants').tokenfield('createToken', participant_name);
                $('#already-registered').removeClass('hidden');
                $('#register-button').addClass('hidden');
            },
            304: function(){
                $('#already-registered').removeClass('hidden');
                $('#register-button').addClass('hidden');
            }
        }
    }).fail(function (e) {
        alert("There was an issue when registering in the draw :(");
    }).always(function(){
    });
};

Raffle.fb_login_to_participate = function(){
    FB.login(function(response) {
        if (response.authResponse) {
            console.log('Welcome!  Fetching your information.... ');
            FB.api('/me', function(response) {
                Raffle.register_in_server(response.id, response.name);
            });
        } else {
            console.log('User cancelled login or did not fully authorize.');
        }
    });
};

Raffle.fb_share_to_participate = function(){
    FB.login(function(response) {
        if (response.authResponse) {
            FB.api('/me', function(response) {
                Raffle.fb_user_id = response.id;
                Raffle.fb_user_name = response.name;
                FB.ui({
                    method: 'share',
                    href: Raffle.url_raffle
                }, function(response){
                    if (response != undefined && response.post_id != undefined){
                        Raffle.register_in_server(Raffle.fb_user_id, Raffle.fb_user_name);
                    }else{
                        console.log('User cancelled share.');
                    }
                });
            });
        } else {
         console.log('User cancelled login or did not fully authorize.');
        }
    }, {
        scope: 'publish_actions'
    });
};

Raffle.setup_creation = function(is_shared){
    $('#id_registration_type').on('change', function(){
        var option_selected = $(this).find(":selected").text();
        $('#div_id_participants').toggleClass('hidden', option_selected != 'Restricted');
        // Disable Facebook registration type in normal draws
        var allowed_registration_type = is_shared || option_selected != 'Facebook';
        $('#shared-draw-required').toggleClass('hidden', allowed_registration_type);
        $('#create-and-toss').toggleClass('disabled', !allowed_registration_type);
        $('#info-facebook-registration').toggleClass('hidden', !allowed_registration_type);
        // Disable 'Try' button when creating a shared draw
        $('#try').toggleClass('hidden', option_selected == 'Facebook');
    });
};

Raffle.setup_display = function(registration_type){
    $('#div_id_registration_type').addClass('hidden');
    if (registration_type == 'facebook'){
        // Make the 'participants' field read-only
        var $participants = $('#id_participants');
        $participants.tokenfield('readonly');
        $participants.parent('.tokenfield').attr('readonly', "true");
    }
};