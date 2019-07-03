window.onload = function(){
    var ref1 = firebase.database().ref('Aum');
    ref1.orderByValue().limitToLast(1).on("value", function(snap){
        snap.forEach(function(data){
            $('#Aum').html(data.val())
        })
    })
    var ref1 = firebase.database().ref('June');
    ref1.orderByValue().limitToLast(1).on("value", function(snap){
        snap.forEach(function(data){
            $('#June').html(data.val())
        })
    })
    var ref1 = firebase.database().ref('Pe');
    ref1.orderByValue().limitToLast(1).on("value", function(snap){
        snap.forEach(function(data){
            $('#Pe').html(data.val())
        })
    })
    var ref1 = firebase.database().ref('Jame');
    ref1.orderByValue().limitToLast(1).on("value", function(snap){
        snap.forEach(function(data){
            $('#Jame').html(data.val())
        })
    })
    var ref1 = firebase.database().ref('Pichet');
    ref1.orderByValue().limitToLast(1).on("value", function(snap){
        snap.forEach(function(data){
            $('#Pichet').html(data.val())
        })
    })
    var ref1 = firebase.database().ref('Phon');
    ref1.orderByValue().limitToLast(1).on("value", function(snap){
        snap.forEach(function(data){
            $('#Phon').html(data.val())
        })
    })
    var ref1 = firebase.database().ref('Att');
    ref1.orderByValue().limitToLast(1).on("value", function(snap){
        snap.forEach(function(data){
            $('#Att').html(data.val())
        })
    })
    var ref1 = firebase.database().ref('Neung');
    ref1.orderByValue().limitToLast(1).on("value", function(snap){
        snap.forEach(function(data){
            $('#Neung').html(data.val())
        })
    })
    var ref1 = firebase.database().ref('unknown');
    ref1.orderByValue().limitToLast(1).on("value", function(snap){
        snap.forEach(function(data){
            $('#unknown').html(data.val())
        })
    })
}