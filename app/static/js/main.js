// user_profile.html

// 
// SOME CODE HERE
// 


//user_registration.html

setInterval( function() {
    var cursor = document.getElementById('cursor');

    if (cursor.style.visibility === 'visible') {
        cursor.style.visibility = 'hidden';
    } else {
        cursor.style.visibility = 'visible';
    }
}, 750)

// changeCursorState();