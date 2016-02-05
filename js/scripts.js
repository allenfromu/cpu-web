function initMap() {
    var mapDiv = document.getElementById('map');
    var myLatlng = new google.maps.LatLng(40.7693659, -111.84626020000002);
    var map = new google.maps.Map(mapDiv, {
        center: myLatlng,
        zoom: 12
    });
    var marker = new google.maps.Marker({
        position: myLatlng,
        title:"50 Central Campus Dr, Salt Lake City, UT 84112, USA"
    });
    marker.setMap(map);
}

function removeEmptyLinks(){

    $("a").each(function() {
        var href = $(this).attr("href");
        if(!href || href === '') { // or anything else you want to remove...
            $(this).remove();
        }
    });
}


$(document).ready(function() {
    initMap();
  $('[data-toggle=offcanvas]').click(function() {
    $('.row-offcanvas').toggleClass('active');
  });

});

$(window).scroll(function(){
    topHeight = $('.top').height();
    scrollT = $(document).scrollTop();
    if (scrollT < topHeight)
        $('.navbar').removeClass('navbar-fixed-top');
    else
        $('.navbar').addClass('navbar-fixed-top');
    console.log(scrollT - topHeight);
    
});

$(window).bind('load', function () {

    resizeElements();

    function resizeElements() {
        topHeight = $('.top').height();

        headerHeight = $('.navbar').height();
        footerHeight = $('.footerbar').height();
        console.log(topHeight);
        if (($(document.body).height() + footerHeight) < $(window).height()) {
            $('.footerbar').addClass('navbar-fixed-bottom');
        } else {
            $('.footerbar').removeClass('navbar-fixed-bottom');
        }
    }
     

    $(window).resize(resizeElements);

});


$(window).resize( function(){
    if($(this).width() > 768){
        $(".navbar-collapse").removeClass("in");
    }
});
